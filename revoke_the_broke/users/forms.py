from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    migrate_from_incognito = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# form extend default django AuthenticationForm to add new field so user can 
# determine whatever what to copy everything from the time when he used incognito mode or not
class LoginForm(AuthenticationForm):
    migrate_from_incognito = forms.BooleanField(required=False)
    