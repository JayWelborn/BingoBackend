from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^contact/$', views.contact_list),
    url(r'contact/(?P<pk>[0-9]+)/$', views.contact_detail)
]
