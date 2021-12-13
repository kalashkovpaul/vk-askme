from io import TextIOWrapper
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.contrib.auth.forms import User
from django.urls.base import set_urlconf

from app.models import Profile, Tag

class UsernameField(CharField):
    def validate(self, value):
        super().validate(value)
        if value == '123':
            raise ValidationError("No 123!")
        return value
            

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
    
class SettingsForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-area'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-area'}))
    avatar = forms.ImageField()
    profile = Profile()

    class Meta:
        model = User
        fields = ['username', 'avatar']
    
    def clean(self):
        cleaned_data = super().clean()
        profiles = Profile.objects.all()
        for profile in profiles:
            user = profile.user
            if user.username == cleaned_data['username'] and user.username != profile.user.username:
                self.add_error(None, "This username is already taken")
            elif user.email == cleaned_data['email'] and user.username != profile.user.username:
                self.add_error(None, "This email is already taken")
    
    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user
    # TODO: upload image

class QuestionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    def clean(self):
        cleaned_data = super().clean()
        tag_names = cleaned_data['tags'].split()
        if len(tag_names) > 3:
            self.add_error(None, "There must be 3 tags or less")
        
class AnswerForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    question_id = 0


    