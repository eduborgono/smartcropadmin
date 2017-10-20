from django import forms


class EditUserForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(required=False)
    name = forms.CharField()
    nickname = forms.CharField()
    avatar = forms.FileField(required=False)


class NewUserForm(forms.Form):
    name = forms.CharField()
    nickname = forms.CharField()
    mail = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            self.add_error('password1', "Las contraseñas no coinciden")


class SearchForm(forms.Form):
    text = forms.CharField()
