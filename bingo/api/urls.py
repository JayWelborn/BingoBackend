from django.conf.urls import url, include

from .routers import Router

from . import viewsets, views


# Wire up the router
router = Router()
router.register(r'users', viewsets.UserViewset)
router.register(r'profiles', viewsets.UserProfileViewset)
router.register(r'cards', viewsets.BingoCardViewset)
router.register(r'squares', viewsets.BingoCardSquareViewset)
router.register(r'contact', viewsets.ContactViewSet)

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^contact', views.EmailFormView.as_view()),
    url(r'^', include(router.urls)),
]
