from rest_framework import serializers

from .models import Shift, Sale


class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'
