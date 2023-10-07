from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    mfa_code = forms.CharField(max_length=6, required=True)
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].help_text = None
        self.fields['mfa_code'].help_text="Type you MFA code"

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    # Add any additional fields you need for your registration form

class MFATokenForm(forms.Form):
    MFA_CODE = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    mfa_code = forms.CharField(max_length=6, required=True)



