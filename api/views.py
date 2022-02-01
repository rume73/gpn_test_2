from datetime import datetime

from .models import Batch, Employee, Provider, Product, Reservoir, Shift, Sale
from .serializers import (
    ShiftSerializer,
    SaleSerializer,
    ShiftCreateSerializer,
    SaleCreateSerializer,
)
from .viewsets import (
    ListCreateRetrieveViewSet,
    ListCreateRetrieveDestroyViewSet,
)


class ShiftViewSet(ListCreateRetrieveViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return ShiftCreateSerializer
        return  ShiftSerializer
    
    def perform_create(self, serializer):
        if len(Shift.objects.all()) != 0:
            last_object = Shift.objects.latest('date_of_beginning')
            last_object.end_date = datetime.now()
            last_object.save()
        serializer.save()


class SaleViewSet(ListCreateRetrieveDestroyViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return SaleCreateSerializer
        return  SaleSerializer
