from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from auth.auth import log_required
from client.gets import get_all_pots, get_user
from client.puts import update_pot_owner, update_pot_name
from client.posts import new_pot
from pots.forms import EditPotForm


def create_new_pot(request):
    new_pot()
    return redirect("pots:index")


class IndexView(TemplateView):

    template_name = 'pots/pots_index.html'

    @log_required
    def get(self, request, *args, **kwargs):
        pots_list = []
        form = EditPotForm()
        for pot in get_all_pots()[1]:
            owner = 'Nadie'
            if 'owner' in pot:
                owner = pot['owner']
            pots_list.append({
                'id': pot['_id'],
                'name': pot['name'],
                'owner': owner,
                'requests': len(pot['requests']),
                'watchers': len(pot['watchers']),
            })
        return render(request, self.template_name, {'pots': pots_list, 'form': form, })

    @log_required
    def post(self, request, *args, **kwargs):
        form = EditPotForm(request.POST)
        if form.is_valid():
            pot_id = form.cleaned_data['id']
            update_pot_name(pot_id, form.cleaned_data['name'])
            owner = form.cleaned_data['owner']
            status, _ = get_user(owner)
            if status == 200:
                update_pot_owner(pot_id, owner)

        return redirect('pots:index')
