from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # contact list
    url(r'^contact/$', views.ContactList.as_view(), name='contact-list'),

    # contact detail
    url(r'^contact/(?P<pk>[0-9]+)/$',
        views.ContactDetail.as_view(),
        name='contact-detail'),

    # user list
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),

    # user detail
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),

    # profile list
    url(r'profiles/$',
        views.UserProfileList.as_view(),
        name='profile-list'),

    # profile detail
    url(r'profiles/(?P<pk>[0-9]+)/$',
        views.UserProfileDetail.as_view(),
        name='profile-detail'),

    # bingo card list
    url(r'^cards/$',
        views.BingoCardList.as_view(),
        name='card-list'),

    # bingo card detail
    url(r'^cards/(?P<pk>[0-9]+)/$',
        views.BingoCardDetail.as_view(),
        name='card-detail'),

    # bingo card square list
    url(r'^squares/$',
        views.BingoCardSquareList.as_view(),
        name='square-list'),

    # bingo card square detail
    url(r'^squares/(?P<pk>[0-9]+)/$',
        views.BingoCardSquareDetail.as_view(),
        name='square-detail'),

    # api root
    url(r'^$',
        views.api_root,
        name='api-root')
]

urlpatterns = format_suffix_patterns(urlpatterns)
