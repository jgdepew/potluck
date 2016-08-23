from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^dashboard$', views.index, name='index'),
    url(r'^user/(?P<id>\d+)$', views.show_user, name='show_user'),
]
