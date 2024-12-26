from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.contrib.auth.models import User
from categories.models import Category

''' 
Register function (/users/register/)
- Handles both GET and POST methods for user registration.
- Uses a custom user registration form (`UserRegisterForm`).
- Includes logic to migrate data from an incognito session if needed.
'''
def register(request):
    if request.method == "POST":  # If the form is submitted
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            # Save the new user instance
            user = form.save()

            # Check if the user wants to migrate data from an incognito session
            migrate_from_incognito = form.cleaned_data['migrate_from_incognito']
            responce = redirect('login')  # Redirect to login page after registration
            
            # Retrieve the incognito token from cookies
            incognito_token = request.COOKIES.get('incognito_token')
            if migrate_from_incognito and incognito_token:
                # Move incognito data to the registered user
                move_user_data(user, incognito_token)
            
            # Clear the incognito token cookie after migration
            responce.delete_cookie('incognito_token')
            return responce
    else:  # If the form is not submitted, display an empty registration form
        form = UserRegisterForm()

    # Render the registration page with the form
    return render(request, 'users/register.html', {'form': form})

''' 
Login function (/users/login/)
- Handles both GET and POST methods for user authentication.
- Validates user credentials and logs in the user if valid.
- Supports migrating data from an incognito session.
'''
def login(request: HttpRequest):
    if request.method == 'POST':  # If the form is submitted
        # Retrieve username, password, and migration preference from the form
        username = request.POST['username']
        password = request.POST['password']
        migrate_from_incognito = request.POST.get('migrate_from_incognito', False)        
        
        # Authenticate the user against the database
        user = authenticate(request, username=username, password=password)

        if user is not None:  # If authentication is successful
            # Log the user in
            auth_login(request, user)
            responce = redirect('index')  # Redirect to the index page
            
            # Check for incognito data migration
            incognito_token = request.COOKIES.get('incognito_token')
            if migrate_from_incognito and incognito_token:
                # Migrate incognito data to the logged-in user
                move_user_data(user, incognito_token)
            
            # Clear the incognito token cookie after migration
            responce.delete_cookie('incognito_token')
            return responce
        else:  # If authentication fails, display an error message
            messages.info(request, 'Invalid credentials')

    # For GET requests or failed POST requests, render the login form
    form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

'''
Move user data from an incognito session to a registered user account.
- Reassigns all categories created during the incognito session to the registered user.
- Clears the `incognito_user_token` field for migrated categories.
'''
def move_user_data(user: User, incognito_token: str):
    # Fetch categories linked to the incognito session
    categories = Category.objects.filter(incognito_user_token=incognito_token).all()
    
    # Reassign each category to the registered user
    for cat in categories:
        cat.author = user  # Assign the category to the registered user
        cat.incognito_user_token = None  # Clear the incognito token
        
        # Save the updated category object to the database
        cat.save()

'''
Logout function (/users/logout/)
- Logs out the currently authenticated user.
- Redirects the user to the login page after logout.
'''
def logout(request):
    # Perform Django's logout operation to clear the user's session
    auth_logout(request)

    # Redirect to the login page after logout
    return redirect('login')