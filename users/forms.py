from django import forms


class EditUserForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(required=False)
    name = forms.CharField()
    nickname = forms.CharField()
    avatar = forms.FileField(required=False)


class SearchForm(forms.Form):
    text = forms.CharField()
