from django.conf.urls import url
from posts import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^social/$', views.SocialView.as_view(), name='social'),
    url(r'^sales/$', views.SalesView.as_view(), name='sales'),
    url(r'^comments/$', views.CommentsView.as_view(), name='comments'),
    url(r'^new_comment/$', views.NewCommentsView.as_view(), name='new_comment'),
    url(r'^remove_comment/$', views.remove_comment, name='remove_comment'),
    url(r'^remove_post/$', views.remove_post, name='remove_post'),
    url(r'^remove_sale/$', views.remove_sale, name='remove_sale'),
    url(r'^new_social/$', views.NewSocialView.as_view(), name='new_social'),
    url(r'^new_sales/$', views.NewSalesView.as_view(), name='new_sales'),

]
