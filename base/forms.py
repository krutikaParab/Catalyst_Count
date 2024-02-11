from django.contrib.auth.forms import UserCreationForm
from .models import User, Upload, Company
from django.forms import ModelForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'