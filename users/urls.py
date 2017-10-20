from django.conf.urls import url
from users import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.NewUserView.as_view(), name='new_user'),
]
