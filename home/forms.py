from django import forms


class UserForm(forms.Form):
    nickname = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())

