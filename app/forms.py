from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=128)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    password = forms.CharField(label='Password', min_length=6, max_length=128, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm Password', max_length=128, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("Passwords should match")
        
        
        