from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from client.gets import search_user
from client.puts import update_user_nick, update_user_name, update_user_pass, update_profile
from users.forms import EditUserForm
from django.http import HttpResponseRedirect
from django.core.signing import Signer, BadSignature
import os
import time


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        if 'nickname' not in request.session:
            return redirect("home:index")
        else:
            signer = Signer()
            users = []
            list_users = []
            user_search = request.GET.get("search-param")
            if user_search is not None:
                _, users = search_user(user_search)

            for user in users:
                data = {
                    'id': signer.sign(user['_id']),
                    'mail': user['email'],
                    'name': user['name'],
                    'nickname': user['nickname'],
                    'avatar': user['avatar'],
                }

                list_users.append(data)
            form = EditUserForm()
            return render(request, "users/index.html", {'users': list_users, 'form': form})

    def post(self, request, *args, **kwargs):
        if 'nickname' not in request.session:
            return redirect("home:index")
        else:
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

