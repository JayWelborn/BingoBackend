"""bingo URL Configuration

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

app_name = 'cards'
urlpatterns = [

    url(r'^(?P<pk>\d+)/$',
        v.CardDetailView.as_view(),
        name='card_detail'),

    url(r'^create/$',
        v.CardCreateView.as_view(),
        name='card_create'),

    url(r'^update/(?P<pk>\d+)/$',
        v.CardUpdateView.as_view(),
        name='card_update'),

    url(r'^my-cards/$',
        v.MyCardListView.as_view(),
        name='my_cards'),

    url(r'^search/$',
        v.CardSearchView.as_view(),
        name='card_search'),

    url(r'^suggest/',
        v.suggest_cards,
        name='suggest_cards'),

    url(r'^',
        v.CardListView.as_view(),
        name='card_list'),
]
