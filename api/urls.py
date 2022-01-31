from django.conf.urls import include
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(router.urls),),
]
