from django.shortcuts import render, redirect
from django.conf import settings
from .models import Category
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .forms import CategoryForm
from .helper import set_cookie, get_categories

# Home page displaying a list of categories and a link to the form for adding a new category
def index(request: HttpRequest):
    # Fetch categories, potentially from a cookie or session (helper function handles logic)
    categories = get_categories(request)
    
    # Render the index page with the list of categories
    return render(request, 'categories/index.html', {'categories': categories})

# Page containing the form to add a category; uses a Django ModelForm
def add_category(request: HttpRequest):
    if request.method == 'GET':  # Handle GET request to display an empty form
        form = CategoryForm()
        return render(request, 'categories/category_form.html', {'form': form})
    elif request.method == 'POST':  # Handle POST request to submit form data
        form = CategoryForm(request.POST)
        if form.is_valid(): 
            # Redirect to the index page on successful form submission
            responce = redirect('index')
            # Save the category using a custom save method, which may handle cookies
            form.save(True, request, responce) 
            return responce
        else:  # If form validation fails, reload the form with an error message
            error_message = 'Invalid data provided'
            return render(request, 'categories/category_form.html', {'form': form, 'error_message': error_message})

# View to update an existing category
def update_category(request: HttpRequest, id: int):
    # Fetch the category by ID using a helper function; return 404 if not found
    category = get_categories(request, id)
    if not category:
        return HttpResponseNotFound("404 not found")
    
    if request.method == 'POST':  # Handle POST request to submit updated category data
        form = CategoryForm(request.POST, instance=category)  # Bind form to existing instance
        if form.is_valid():
            # Redirect to the index page after successful update
            responce = redirect('index')
            # Save the updated category using a custom save method
            form.save(True, request, responce)
            return responce
        else:  # If form validation fails, reload the form with an error message
            error_message = 'Invalid data provided'
            form = CategoryForm(instance=category)  # Reinitialize the form with existing data
            return render(request, 'categories/category_form.html', {'form': form, 'update': True, 'error_message': error_message})
    else:  # Handle GET request to display the form pre-filled with the category's current data
        form = CategoryForm(instance=category)
        return render(request, 'categories/category_form.html', {'form': form, 'update': True})

# View to delete an existing category
def remove_category(request: HttpRequest, id: int):
    # Fetch the category by ID using a helper function; return 404 if not found
    category = get_categories(request, id)
    if not category:
        return HttpResponseNotFound("404 not found")
    
    # Delete the category object from the database
    category.delete()
    # Redirect to the index page after successful deletion
    return redirect('index')
