from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'nickname' in request.session:
            return redirect("home:log_home")
        form = UserForm()
        return render(request, 'home/index.html', {'form': form, })

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            match = User.objects.filter(nickname=form.cleaned_data['nickname'])
            if len(match) == 1:
                if match[0].password == form.cleaned_data['password']:
                    request.session['nickname'] = form.cleaned_data['nickname']
                    return redirect("home:log_home")
        form = UserForm()
        return render(request, 'home/index.html', {'form': form, })


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        if 'nickname' in request.session:
            return render(request, 'home/home.html')
        else:
            return redirect("home:index")


def logout(request):
    try:
        del request.session['nickname']
    except:
        pass

    return redirect("home:index")
