from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^(?P<username>\w+)$', views.view_profile, name='get-user-info'),
    # url(r'^(?P<username>\w+)/social$', views.view_social, name='get-user-social'),
    # url(r'^(?P<username>\w+)/personal$', views.view_personal, name='get-user-personal'),
    # url(r'^$', views.index,name= 'index'),
    url(r'^demo$', views.demo,name= 'demo'),
    url(r'^location/enter$', views.location,name= 'location'),

    url(r'^(?P<username>\w+)/permanent_address/edit$', views.update_permanent_address, name='edit-permanent-address'),
    url(r'^(?P<username>\w+)/current_address/edit$', views.update_current_address, name='edit-current-address'),


    url(r'^(?P<username>\w+)/basic/edit$', views.update_basic, name='edit-user-basic'),
    url(r'^(?P<username>\w+)/social/edit$', views.update_social, name='edit-user-social'),
    url(r'^(?P<username>\w+)/personal/edit$', views.update_personal, name='edit-user-personal'),

    url(r'^(?P<username>\w+)/work_experience/add$', views.add_work_experience, name='add-work-experience'),
    url(r'^(?P<username>\w+)/work_experience/delete/(?P<pk>\w+)', views.delete_work_experience, name='delete-work-experience'),

    url(r'^(?P<username>\w+)/qualification/add$', views.add_qualification, name='add-user-qualification'),
    url(r'^(?P<username>\w+)/qualification/delete/(?P<pk>\w+)', views.delete_qualification, name='delete-qualification'),

    url(r'^address/update/(?P<pk>\w+)$', views.update_address),
    # url(r'^(?P<username>\w+)/work_experience/edit', views.update_work_experience, name='edit-user-work-experience'),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)[0],
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)[0],
]