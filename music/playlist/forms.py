from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Donate

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'bio', 'avatar']

    
class UpdateUserPasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']


class DonationForm(ModelForm):
    class Meta:
        model = Donate
        fields = ['name', 'phone', 'email', 'amount']