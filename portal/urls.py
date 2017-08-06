from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<username>\w+)/basic$', views.view_basic, name='get-user-basic'),
    url(r'^(?P<username>\w+)/social$', views.view_social, name='get-user-social'),
    url(r'^(?P<username>\w+)/misc$', views.view_misc, name='get-user-misc'),
    url(r'^(?P<username>\w+)/work_experience$', views.view_work_experience, name='get-work-experience'),

    url(r'^$', views.index,name= 'index_page'),
    url(r'^demo', views.demo,name= 'demo_page'),

    url(r'^(?P<username>\w+)/permanent_address/edit$', views.update_permanent_address, name='edit-permanent-address'),
    url(r'^(?P<username>\w+)/current_address/edit$', views.update_current_address, name='edit-current-address'),

    url(r'^(?P<username>\w+)/work_experiences$', views.view_work_experience, name='view-work-experience'),

    url(r'^(?P<username>\w+)/basic/edit$', views.update_basic, name='edit-user-basic'),
    url(r'^(?P<username>\w+)/social/edit$', views.update_social, name='edit-user-social'),
    url(r'^(?P<username>\w+)/misc/edit$', views.update_misc, name='edit-user-misc'),

    url(r'^(?P<username>\w+)/work_experience/add$', views.add_work_experience, name='add-user-work-experience'),

    url(r'^address/update/(?P<pk>\w+)$', views.update_address)
    # url(r'^(?P<username>\w+)/work_experience/edit', views.update_work_experience, name='edit-user-work-experience'),
]
