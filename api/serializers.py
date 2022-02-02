from django.db import transaction
from rest_framework import serializers

from .models import Shift, Sale, Batch, Employee, Reservoir, Product, Provider


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        exclude = ('id',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ('id',)


class ReservoirSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservoir
        exclude = ('id',)


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'third_name', 'experience')


class BatchSerializer(serializers.ModelSerializer):
    batch_id = serializers.ReadOnlyField(source='id',)
    reservoir = ReservoirSerializer(read_only=True,)
    product = ProductSerializer(read_only=True,)
    provider = ProviderSerializer(read_only=True,)

    class Meta:
        model = Batch
        fields = ('batch_id', 'product', 'number', 'date_of_delivery',
                  'tonnage', 'provider', 'volume', 'reservoir', 'density',
                  'shift_accepted')


class ShiftSerializer(serializers.ModelSerializer):
    batch = BatchSerializer(read_only=True,)
    employees = serializers.SerializerMethodField()
    is_current_shift  = serializers.SerializerMethodField()

    class Meta:
        model = Shift
        fields = ('id', 'batch', 'employees', 'date_of_beginning', 'end_date',
                  'begin_vol_of_prod', 'end_delta_vol_of_prod',
                  'is_current_shift',)

    def get_employees(self, obj):
        qs = obj.employees.all()
        return EmployeeSerializer(qs, many=True).data

    def get_is_current_shift(self, obj):
        if obj.end_date is None:
            return True
        else:
            return False


class ShiftCreateSerializer(serializers.ModelSerializer):
    end_date = serializers.ReadOnlyField()

    class Meta:
        model = Shift
        fields = ('id', 'batch', 'employees', 'date_of_beginning', 'end_date',
                  'begin_vol_of_prod', 'end_delta_vol_of_prod',)


class ShowShiftInSale(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()
    shift_id = serializers.ReadOnlyField(source='id',)

    class Meta:
        model = Shift
        fields = ('shift_id', 'employees', 'date_of_beginning')
    
    def get_employees(self, obj):
        qs = obj.employees.all()
        return EmployeeSerializer(qs, many=True).data


class SaleSerializer(serializers.ModelSerializer):
    shift = ShowShiftInSale()

    class Meta:
        model = Sale
        fields = '__all__'


class SaleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'

    def to_representation(self, instance):
        return SaleSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
