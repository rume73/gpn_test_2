from datetime import datetime
from rest_framework.generics import get_object_or_404

from .models import Batch, Shift, Sale
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
        return ShiftSerializer

    def perform_create(self, serializer):
        if len(Shift.objects.all()) != 0:
            last_object = Shift.objects.latest('date_of_beginning')
            last_object.end_date = datetime.now()
            current_volume = last_object.current_volume
            last_object.save()
        else:
            current_volume = 0.0
        serializer.save(
            begin_vol_of_prod=current_volume,
            current_volume=current_volume,
            )
        if len(Batch.objects.all()) != 0:
            batch = get_object_or_404(Batch, id=self.request.data.get('batch'))
            batch.shift_accepted = self.request.data.get('id')
            batch.save()
            serializer.save()


class SaleViewSet(ListCreateRetrieveDestroyViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return SaleCreateSerializer
        return SaleSerializer
