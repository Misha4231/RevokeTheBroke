from django import forms
from .models import Category
from django.forms.widgets import TextInput
from .helper import set_cookie
from django.http import HttpRequest, HttpResponse
import uuid

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description', 'color']
        
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
        
    '''
        save method is overloaded to 
        - assign right user
        - avoid repetitive code
        - make views shorter
    '''
    def save(self, commit=True, request: HttpRequest = None, responce: HttpResponse = None): 
        category: Category = super().save(commit)
        
        if not request or not responce:
            raise Exception("Empty parameters are passed to save method")
        
        if request.user.is_authenticated:
            category.author = request.user
            
        else:
            incognito_token = request.COOKIES.get('incognito_token') # gets token (can be None)
            if incognito_token:
                category.incognito_user_token = incognito_token
            else:
                incognito_token = str(uuid.uuid4())  # generate and assign token in case if user adds his first category
                
                set_cookie(responce, 'incognito_token', incognito_token)
                category.incognito_user_token = incognito_token
            
        if commit:
            category.save()
        return category