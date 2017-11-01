from django import forms
from client.gets import get_user
import re


class EditPostForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    photo = forms.FileField(label="Imagen", required=False)
    text = forms.CharField(label="Información extra", widget=forms.Textarea, required=True)


class NewPostForm(forms.Form):
    author = forms.CharField(label="ID del autor")
    image = forms.FileField(label="Imagen", required=False)
    text = forms.CharField(label="Información extra", widget=forms.Textarea, required=True)

    def clean_author(self):
        user_id = self.cleaned_data['author']
        status, _ = get_user(user_id)
        if status != 200:
            raise forms.ValidationError("No existe ese usuario")

        return user_id


class EditSaleForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    price = forms.IntegerField(label="Precio")
    image = forms.FileField(label="Imagen", required=False)
    text = forms.CharField(label="Información extra", widget=forms.Textarea)
    tags = forms.CharField(label="Etiquetas")

    def clean_price(self):
        price_positive = self.cleaned_data['price']
        if price_positive < 0:
            raise forms.ValidationError('El precio debe ser mayor a cero.')
        return price_positive

    def clean_tags(self):
        tags_format = self.cleaned_data['tags']
        regex = r"^\w(?:\w|\,\w)*$"
        matches = re.match(regex, tags_format.replace(" ", ""))
        if matches is None:
            raise forms.ValidationError('Las etiquetas deben estar de la forma "Etiqueta1, Etiqueta2, ..., EtiquetaN".')

        return tags_format


class NewSaleForm(forms.Form):
    author = forms.CharField(label="ID del autor")
    price = forms.IntegerField(label="Precio")
    image = forms.FileField(label="Imagen", required=False)
    text = forms.CharField(label="Información extra", widget=forms.Textarea)
    tags = forms.CharField(label="Etiquetas")

    def clean_author(self):
        user_id = self.cleaned_data['author']
        status, _ = get_user(user_id)
        if status != 200:
            raise forms.ValidationError("No existe ese usuario.")

        return user_id

    def clean_price(self):
        price_positive = self.cleaned_data['price']
        if price_positive < 0:
            raise forms.ValidationError('El precio debe ser mayor a cero.')
        return price_positive

    def clean_tags(self):
        tags_format = self.cleaned_data['tags']
        regex = r"^\w(?:\w|\,\w)*$"
        matches = re.match(regex, tags_format.replace(" ", ""))
        if matches is None:
            raise forms.ValidationError('Las etiquetas deben estar de la forma "Etiqueta1, Etiqueta2, ..., EtiquetaN".')

        return tags_format


class EditCommentForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    text = forms.CharField(label="Comentario", widget=forms.Textarea, required=True)


class NewCommentForm(forms.Form):
    author = forms.CharField(label="ID del autor")
    text = forms.CharField(label="Comentario", widget=forms.Textarea)

    def clean_author(self):
        user_id = self.cleaned_data['author']
        status, _ = get_user(user_id)
        if status != 200:
            raise forms.ValidationError("No existe ese usuario")

        return user_id
