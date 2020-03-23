from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('', include(router.urls)),
]