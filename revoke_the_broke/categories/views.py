from django.shortcuts import render, redirect
from django.conf import settings
from .models import Category
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .forms import CategoryForm
from .helper import set_cookie, get_categories

# Home page displaying list of categories and link to form adding category
def index(request: HttpRequest):
    categories = get_categories(request)
    
    return render(request, 'categories/index.html', {'categories': categories})

# Page contain form to add category, uses ModelForm
def add_category(request: HttpRequest):
    if request.method == 'GET': # GET -> return page with empty form
        form = CategoryForm()
        
        return render(request, 'categories/category_form.html', {'form': form})
    elif request.method == 'POST': # POST -> validate provided data, save it or return back page with error message
        form = CategoryForm(request.POST)
        if form.is_valid(): 
            responce = redirect('index')
            form.save(True, request, responce) # request and responce provided to handle incognito mode case
            
            return responce
        else:
            form = CategoryForm()
            error_message = 'Invalid data provided'
            
            return render(request, 'categories/category_form.html', {'form': form, 'error_message': error_message})


def update_category(request: HttpRequest, id: int):
    category = get_categories(request, id)
    if not category:
        return HttpResponseNotFound("404 not found")
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            responce = redirect('index')
            form.save(True, request, responce)
            
            return responce
        else:
            error_message = 'Invalid data provided'
            form = CategoryForm(instance=category)
            return render(request, 'categories/category_form.html', {'form': form, 'update': True})
    else:
        form = CategoryForm(instance=category)
        
        return render(request, 'categories/category_form.html', {'form': form, 'update': True})
    
def remove_category(request: HttpRequest, id: int):
    category = get_categories(request, id)
    if not category:
        return HttpResponseNotFound("404 not found")
    
    category.delete()
    return redirect('index')