"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views as v

app_name = 'auth_extension'
urlpatterns = [
    url(r'^$',
        v.LoginRedirectView.as_view(),
        name='login_redirect'),

    url(r'^list/$',
        v.ProfileListView.as_view(),
        name='profile_list'),

    url(r'^(?P<pk>\d+)/$',
        v.ProfileRedirectView.as_view(),
        name='profile'),

    url(r'^(?P<pk>\d+)/view/$',
        v.ProfileView.as_view(),
        name='profile_view'),

    url(r'^(?P<pk>\d+)/edit/$',
        v.ProfileEditView.as_view(),
        name='profile_edit'),

    url(r'^login-required/$',
        v.Unauthorized.as_view(),
        name='unauthorized'),

    url(r'^permission-denied/$',
        v.PermissionDenied.as_view(),
        name='permission_denied'),

    url(r'^suggest/',
        v.suggest_profiles,
        name='profile_search'),

    url(r'^settings/$',
        v.settings,
        name='settings'),

    url(r'^settings/password/$',
        v.password,
        name='password'),
]
