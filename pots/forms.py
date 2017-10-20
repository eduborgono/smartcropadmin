from django import forms


class EditPotForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField()
    owner = forms.CharField()
