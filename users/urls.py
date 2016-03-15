from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.user_register, name='user-register'),
    url(r'^activate/(?P<code>\w+)/(?P<user_id>\d+)/$', views.users_activate, name='user-activate'),
    url(r'^notification/$', views.user_notification, name='user-notification'),
    url(r'^change/pass/$', views.user_changepassword, name='user-changepassword'),
    url(r'^change/username/$', views.user_changeusername, name='user-changeusername'),
    url(r'^reset/pass/$', views.user_sendcoderesetpass, name='user-sendresedpass'),
    url(r'^recover/pass/(?P<code>\w+)/(?P<user_id>\d+)/$', views.user_recoverpass, name='user-recoverpass'),

    url(r'^my/information/$', views.my_information, name='user-myinformation'),
    url(r'^modify/information/$', views.modify_information, name='user-modifyinformation'),
]
