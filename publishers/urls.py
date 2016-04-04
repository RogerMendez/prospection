from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='publisher-index'),
    url(r'^new/$', views.new_publisher, name='publisher-new'),
    url(r'^(?P<publisher_id>\d+)/dates/$', views.dates_publisher, name='publisher-dates'),
    url(r'^(?P<publisher_id>\d+)/dates/ends/$', views.ends_dates_publisher, name='publisher-ends-dates'),
]
