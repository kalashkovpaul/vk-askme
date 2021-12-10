from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField

from app.models import Profile

class UsernameField(CharField):
    def validate(self, value):
        super().validate(value)
        if value == '123':
            raise ValidationError("No 123!")
        return value


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
            

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-area'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-area'}))

class SingUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-area'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-area'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-area'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-area'}))
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            self.add_error(None, "Password do not match!")
        profiles = Profile.objects.all()
        for profile in profiles:
            user = profile.user
            if user.username == cleaned_data['username']:
                self.add_error(None, "This username is already taken")
            elif user.email == cleaned_data['email']:
                self.add_error(None, "This email is already taken")
    
    # TODO: upload image