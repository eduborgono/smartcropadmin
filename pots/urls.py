from django.conf.urls import url
from pots import views

app_name = 'pots'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^newpot/$', views.create_new_pot, name='newpot'),
]
