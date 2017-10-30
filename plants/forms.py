from django import forms
from client.gets import get_plant


class EditPlantForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField()

    minHumeTie = forms.IntegerField()
    maxHumeTie = forms.IntegerField()

    minHumeAmb = forms.IntegerField()
    maxHumeAmb = forms.IntegerField()

    minTempTie = forms.IntegerField()
    maxTempTie = forms.IntegerField()

    minTempAmb = forms.IntegerField()
    maxTempAmb = forms.IntegerField()


class InfoPlantForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.plant_id = None
        if 'plant_id' in kwargs:
            self.plant_id = kwargs.pop('plant_id')
        super(InfoPlantForm, self).__init__(*args, **kwargs)
        if self.plant_id is not None:
            status, plant = get_plant(self.plant_id)
            if status == 200:
                self.fields['plant'] = forms.CharField(label='Planta', disabled=True, initial=plant['name'])
                self.fields['id'] = forms.CharField(widget=forms.HiddenInput(), initial=plant['_id'])
                for tip in plant['tips']:
                    self.fields[tip['type']] = forms.CharField(widget=forms.Textarea(), initial=tip['description'])

    plant = forms.CharField()
    description = forms.CharField(label="Descripción", widget=forms.Textarea(), required=False)
    new_tip_type = forms.CharField(label='Titulo nuevo consejo', required=False)
    new_tip_description = forms.CharField(widget=forms.Textarea(), label='Descripción nuevo consejo', required=False)

    def clean(self):
        cleaned_data = super(InfoPlantForm, self).clean()
        key_list = list(cleaned_data.keys())
        new_type = cleaned_data.get("new_tip_type")
        if new_type in key_list:
            self.add_error('new_tip_type', "No puedes usar "+new_type+" como nuevo nombre de categoría")
