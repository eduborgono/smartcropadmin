from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from client.gets import search_user
from client.puts import update_user_nick, update_user_name, update_user_pass, update_profile
from client.posts import new_user_acc
from users.forms import EditUserForm, NewUserForm
from django.http import HttpResponseRedirect
from django.core.signing import Signer, BadSignature
from auth.auth import log_required
import os
import time


class IndexView(TemplateView):
    @log_required
    def get(self, request, *args, **kwargs):
        signer = Signer()
        users = []
        list_users = []
        user_search = request.GET.get("search-param")
        if user_search is not None:
            _, users = search_user(user_search)

        for user in users:
            data = {
                'id': signer.sign(user['_id']),
                'ID': user['_id'],
                'mail': user['email'],
                'name': user['name'],
                'nickname': user['nickname'],
                'avatar': user['avatar'],
            }

            list_users.append(data)
        form = EditUserForm()
        return render(request, "users/index.html", {'users': list_users, 'form': form})

    @log_required
    def post(self, request, *args, **kwargs):
        form = EditUserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                signer = Signer()
                user_id = signer.unsign(form.cleaned_data['id'])
                update_user_nick(user_id, form.cleaned_data['nickname'])
                update_user_name(user_id, form.cleaned_data['name'])
                update_user_pass(user_id, form.cleaned_data['password'])
                if len(request.FILES) > 0:
                    _, extension = os.path.splitext(request.FILES['avatar'].name)
                    path_file = 'media/'+str(int(time.time()))+extension
                    with open(path_file, 'wb+') as destination:
                        for chunk in request.FILES['avatar'].chunks():
                            destination.write(chunk)
                        update_profile(user_id, path_file)

                next_page = request.POST.get('next', '/')
                return HttpResponseRedirect(next_page)

            except BadSignature:
                pass

        return redirect("users:index")


class NewUserView(TemplateView):
    @log_required
    def get(self, request, *args, **kwargs):
        form = NewUserForm()
        return render(request, "users/userform.html", {'form': form})

    @log_required
    def post(self, request, *args, **kwargs):
        error = ""
        form = NewUserForm(request.POST)
        if form.is_valid():
            status = new_user_acc(form.cleaned_data['mail'],
                         form.cleaned_data['name'],
                         form.cleaned_data['password1'],
                         form.cleaned_data['nickname'])
            if status == 201:
                return redirect("users:index")
            else:
                error = 'Intentalo nuevamente'

        return render(request, "users/userform.html", {'form': form, 'error': error, })
