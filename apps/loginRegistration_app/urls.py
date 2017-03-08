from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    # url(r'^dashboard$', views.index, name='index'),
    # url(r'^user/(?P<id>\d+)$', views.show_user, name='show_user'),
    # url(r'^recipe/(?P<recipe_id>\d+)$', views.show_recipe, name='show_recipe'),
    # url(r'^add_recipe$', views.add_recipe, name='add_recipe'),
    # url(r'^delete_recipe/(?P<recipe_id>\d+)$', views.delete_recipe, name='delete_recipe'),
    # url(r'^edit_recipe/(?P<recipe_id>\d+)$', views.edit_recipe, name='edit_recipe'),
    # url(r'^add_step$', views.add_step, name='add_step'),
    # url(r'^add_rating(?P<recipe_id>\d+)$', views.add_rating, name='add_rating'),
    # url(r'^save_recipe(?P<recipe_id>\d+)$', views.save_recipe, name='save_recipe'),
    # url(r'^update_step/(?P<step_id>\d+)$', views.update_step, name='update_step'),
    # url(r'^delete_step/(?P<step_id>\d+)$', views.delete_step, name='delete_step'),
    # url(r'^search$', views.search, name='search'),
]
