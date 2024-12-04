from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('users.login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None:
            form = login(request, user)

            return redirect('categories.index')
        else:
            messages.info(request, f'invalid credentials')

    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form})