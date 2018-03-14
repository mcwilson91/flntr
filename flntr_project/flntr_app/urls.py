from django.conf.urls import url
from flntr_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^search/$', views.search, name='search'),
	url(r'^results/$', views.results, name='results'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^property/$', views.property, name='property'),
    url(r'^property/(?P<flat_id_slug>[\w\-]+)/$',
        views.show_property, name='show_property'),
    url(r'^property/(?P<flat_id_slug>[\w\-]+)/(?P<student_profile_slug>[\w\-]+)/profile$',
        views.show_property_user_profile, name='show_property_user_profile'),
    # url(r'^user/(?P<user_id_slug>[\w\-]+)/$',
    #     views.show_user, name='show_user'),
    url(r'^user/(?P<landlord_id_slug>[\w\-]+)/requests/$',
        views.show_user_requests, name='show_user_requests'),
    url(r'^user/(?P<landlord_id_slug>[\w\-]+)/requests/(?P<student_profile_slug>[\w\-]+)/$',
        views.show_user_requests_profile, name='show_user_requests_profile'),
    url(r'^user/my-account/$',
        views.show_user_account, name='show_user_account'),
    url(r'^user/(?P<student_profile_slug>[\w\-]+)/profile/$',
        views.show_user_profile, name='show_user_profile'),
    url(r'^edit-profile/$',
        views.edit_profile, name='edit_profile'),
    url(r'^delete-profile/$',
        views.delete_profile, name='delete_profile'),
    url(r'^user/(?P<user_id_slug>[\w\-]+)/invitations/$',
        views.show_user_invitations, name='show_user_invitations'),
    url(r'^user/(?P<landlord_id_slug>[\w\-]+)/property/$',
        views.show_user_properties, name='show_user_properties'),
    url(r'^user/(?P<landlord_id_slug>[\w\-]+)/property/(?P<flat_id_slug>[\w\-]+)/$',
        views.show_user_properties_aProperty, name='show_user_properties_aProperty'),
    url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^add_flat/$', views.add_flat, name='add_flat'),
	url(r'^property/(?P<flat_id_slug>[\w\-]+)/send_request/(?P<room_number>[\w\-]+)$',
        views.send_request, name='send_request'),
    url(r'^edit_flat/(?P<flat_id_slug>[\w\-]+)/$', views.edit_flat, name='edit_flat'),
    url(r'^delete_flat/(?P<flat_id_slug>[\w\-]+)/$', views.delete_flat, name='delete_flat'),
]
