from django import forms
from .models import Expenditure


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['title', 'description', 'price']        
