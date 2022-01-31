from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import ShiftViewSet, SaleViewSet


router = routers.DefaultRouter()
router.register(r'shifts', ShiftViewSet, base_name='shifts')
router.register(r'sales', SaleViewSet, base_name='sales')


urlpatterns = [
    path('v1/', include(router.urls),),
]
