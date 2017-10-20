from django.conf.urls import url
from home import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.HomePageView.as_view(), name="log_home"),
    url(r'^logout/$', views.logout, name="logout"),
]
