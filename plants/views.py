from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from auth.auth import log_required
from client.posts import new_plant, new_plant_tip
from client.gets import get_all_plants
from client.deletes import delete_plant_tip
from client.puts import update_plant, update_plant_description, update_plant_category
from plants.forms import EditPlantForm, InfoPlantForm


def create_new_plant(request):
    new_plant()
    return redirect("plants:index")


class IndexView(TemplateView):

    template_name = 'plants/plants_index.html'

    @log_required
    def get(self, request, *args, **kwargs):
        plant_list = []
        form = EditPlantForm()
        for plant in get_all_plants()[1]:
            name = 'Sin nombre'
            if 'name' in plant:
                name = plant['name']
            plant_list.append({
                'id': plant['_id'],
                'name': name,
                'min_hume_tierra': plant['minMoist'],
                'max_hume_tierra': plant['maxMoist'],
                'min_temp_tierra': plant['minTemp'],
                'max_temp_tierra': plant['maxTemp'],
                'min_hume_amb': plant['minHum'],
                'max_hume_amb': plant['maxHum'],
                'min_temp_amb': plant['minRoomTemp'],
                'max_temp_amb': plant['maxRoomTemp'],
            })
        return render(request, self.template_name, {'plants': plant_list, 'form': form, })

    @log_required
    def post(self, request, *args, **kwargs):
        form = EditPlantForm(request.POST)
        if form.is_valid():
            plant_id = form.cleaned_data['id']
            plant_name = form.cleaned_data['name']
            hume_tie = (form.cleaned_data['minHumeTie'], form.cleaned_data['maxHumeTie'])
            hume_amb = (form.cleaned_data['minHumeAmb'], form.cleaned_data['maxHumeAmb'])
            temp_tie = (form.cleaned_data['minTempTie'], form.cleaned_data['maxTempTie'])
            temp_amb = (form.cleaned_data['minTempAmb'], form.cleaned_data['maxTempAmb'])
            update_plant(plant_id, plant_name, hume_tie, hume_amb, temp_tie, temp_amb)

        return redirect('plants:index')


class PlantInfoView(TemplateView):

    template_name = 'plants/plants_edit_info.html'

    @log_required
    def get(self, request, *args, **kwargs):
        plant_id = request.GET.get("id")
        if plant_id is not None:
            form = InfoPlantForm(plant_id=plant_id)
            excluding_head_form = ['plant', 'description']
            excluding_foot_form = ['new_tip_type', 'new_tip_description']
            return render(request, self.template_name, {'form': form,
                                                        'excluding_foot_form': excluding_foot_form,
                                                        'excluding_head_form': excluding_head_form, })
        return redirect('plants:index')

    @log_required
    def post(self, request, *args, **kwargs):
        form = InfoPlantForm(request.POST, plant_id=request.POST['id'])
        if form.is_valid():
            plant_id = form.cleaned_data['id']
            description = form.cleaned_data['description']
            update_plant_description(plant_id, description)

            new_tip_type = form.cleaned_data['new_tip_type']
            new_tip_description = form.cleaned_data['new_tip_description']
            if len(new_tip_type) > 0:
                new_plant_tip(plant_id, new_tip_type, new_tip_description)

            all_entries = form.cleaned_data.copy()
            del all_entries['plant']
            del all_entries['id']
            del all_entries['description']
            del all_entries['new_tip_type']
            del all_entries['new_tip_description']

            for key in all_entries:
                key_split = key.split(':')
                if key_split[1] == 'type':
                    if len(all_entries[key]) > 0:
                        update_plant_category(plant_id,
                                              key_split[0],
                                              all_entries[key_split[0]+':type'],
                                              all_entries[key_split[0]+':description'])
                    else:
                        delete_plant_tip(plant_id, key_split[0])

            next_page = request.POST.get('next', '/')
            return HttpResponseRedirect(next_page)

        return render(request, self.template_name, {'form': form, })
