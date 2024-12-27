from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotFound
from categories.helper import get_categories
from .models import Expenditure
from .forms import ExpenditureForm
from categories.decorators import with_category
from categories.models import Category


# View to display expenditures for a specific category
@with_category
def category_spendings(request, category: Category, *args, **kwargs):
    expenditures = Expenditure.objects.filter(category=category)

    # Prepare data for Chart.js
    chart_data = {
        "titles": [exp.title for exp in expenditures],
        "prices": [exp.price for exp in expenditures],
        "total_price": sum(exp.price for exp in expenditures),
    }

    return render(request, 'spendings/category_spendings.html', {
        'expenditures': expenditures,
        'chart_data': chart_data,
        'category': category
    })

# View to add a new expenditure for a specific category
@with_category
def add_expenditure(request: HttpRequest, category: Category, *args, **kwargs):
    if request.method == 'POST':  # Handle form submission
        form = ExpenditureForm(request.POST)  # Bind the form to POST data
        if form.is_valid():  # Check if the form is valid
            new_expenditure = form.save(commit=False)  # Save the form data without committing to the database
            new_expenditure.category = category  # Assign the current category to the new expenditure
            new_expenditure.save()  # Save the expenditure to the database
            
            return redirect('category_spendings', id=category.id)
        else:
            # If the form is invalid, render the form with an error message
            return render(
                request,
                'spendings/expediture_form.html',
                {'form': form, 'category': category, 'error_message': 'Invalid data provided'}
            )
    else:  # If the request is not POST, render a blank form
        form = ExpenditureForm()
        # Render the form for adding a new expenditure
        return render(request, 'spendings/expediture_form.html', {'form': form, 'category': category})
    
@with_category
def update_expenditure(request: HttpRequest, category: Category, exp_id: int, *args, **kwargs):
    exp = Expenditure.objects.filter(pk = exp_id).first()
    if not exp:
        return HttpResponseNotFound("Expenditure not found")
    
    if request.method == 'POST':  # Handle form submission
        form = ExpenditureForm(request.POST, instance=exp)  # Bind the form to POST data
        if form.is_valid():  # Check if the form is valid
            new_expenditure = form.save()  # Save the form data without committing to the database
            new_expenditure.save()  # Save the expenditure to the database
            
            return redirect('category_spendings', id=category.id)
        else:
            # If the form is invalid, render the form with an error message
            return render(
                request,
                'spendings/expediture_form.html',
                {'form': form, 'category': category, 'error_message': 'Invalid data provided'}
            )
    else:  # If the request is not POST, render a form
        form = ExpenditureForm(instance=exp)
        # Render the form for adding a new expenditure
        return render(request, 'spendings/expediture_form.html', {'form': form, 'category': category})

@with_category
def delete_expenditure(request: HttpRequest, category: Category, exp_id: int, *args, **kwargs):
    exp = Expenditure.objects.filter(pk = exp_id).first()
    if not exp:
        return HttpResponseNotFound("Expenditure not found")
    
    exp.delete()
    
    return redirect('category_spendings', id=category.id)