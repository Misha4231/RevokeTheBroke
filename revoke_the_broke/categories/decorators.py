from django.http import HttpRequest, HttpResponseNotFound
from .models import Category
from functools import wraps
from .helper import get_categories

# Decorator to handle category retrieval and pass it to the view
def with_category(view_func):
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs): # Fetch the category by ID using a helper function; return 404 if not found
        category_id = kwargs.get('id') or kwargs.get('category_id')  # Supports multiple parameter names
        category = get_categories(request, id=category_id)
        
        if not category:  # If category is not found, return a 404 response
            return HttpResponseNotFound('404 category not found')
        
        return view_func(request, category=category, *args, **kwargs) # Call the original view function, passing the category as an argument

    return wrapper