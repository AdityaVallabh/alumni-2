from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<username>\w+)/basic', views.view_basic, name='get-user-basic'),
    url(r'^(?P<username>\w+)/social', views.view_social, name='get-user-social'),
    url(r'^(?P<username>\w+)/misc', views.view_misc, name='get-user-misc'),

    url(r'^basic/edit', views.update_basic, name='edit-user-basic'),
    url(r'^social/edit', views.update_social, name='edit-user-social'),
    url(r'^misc/edit', views.update_misc, name='edit-user-misc'),
    # url(r'^(?P<username>\w+)/permanent_address/edit', views.PostInfo.permanent_address, name='edit-permanent-address'),
    # url(r'^(?P<username>\w+)/current_address/edit', views.PostInfo.current_address, name='edit-current-address'),
]
