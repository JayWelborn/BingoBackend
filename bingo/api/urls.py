from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views


# Wire up the router
router = DefaultRouter()
router.register(r'cards', views.BingoCardViewset)
router.register(r'users', views.UserViewset)
router.register(r'profiles', views.UserProfileViewset)
router.register(r'contact', views.ContactViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
