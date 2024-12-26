from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

''' 
register function (/users/register/)
    - handles both GET and POST methods
    - uses default django register form
'''
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

''' 
sign in function (/users/login/)
    - handles both GET and POST methods
    - check if user exists
    - uses default django login form
'''
def login(request):
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None:
            form = auth_login(request, user)

            return redirect('index')
        else:
            messages.info(request, f'invalid credentials')

    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form})

# logs user out
def logout(request):
    auth_logout(request)

    return redirect('login')