from django.conf.urls import url
from flntr_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^search/$', views.search, name='search'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^property/$', views.property, name='property'),
    url(r'^property/(?P<property_id_slug>[\w\-]+)/$',
        views.show_property, name='show_property'),
    url(r'^user/$', views.user, name='user'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)/$',
        views.show_user, name='show_user'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)/requests/$',
        views.show_user_requests, name='show_user_requests'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)/my-account/$',
        views.show_user_account, name='show_user_account'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)/profile/$',
        views.show_user_profile, name='show_user_profile'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)/invitations/$',
        views.show_user_invitations, name='show_user_invitations'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)/property/$',
        views.show_user_properties, name='show_user_properties'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)//property/(?P<property_id_slug>[\w\-]+)/$',
        views.show_user_properties_aProperty, name='show_user_properties_aProperty'),
    url(r'^logout/$', views.user_logout, name='logout'),
]