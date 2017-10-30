from django.conf.urls import url
from plants import views

app_name = 'plants'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^newplant/$', views.create_new_plant, name='newplant'),
    url(r'^editplant/$', views.PlantInfoView.as_view(), name='editplant'),
]
