from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField

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
    username = forms.CharField
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_repeat']:
            self.add_error(None, "Password do not match!")
        