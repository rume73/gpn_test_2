from django.contrib import admin

from .models import Batch, Employee, Provider, Product, Reservoir, Shift, Sale


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__',)
    readonly_fields = ('density', 'shift_accepted')
    search_fields = ('provider', 'shift_accepted',)
    empty_value_display = '-пусто-'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'third_name',)
    readonly_fields = ('experience',)
    search_fields = ('last_name', 'first_name', 'third_name', 'gender')
    empty_value_display = '-пусто-'


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Reservoir)
class ReservoirAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__')
    search_fields = ('name',)
    readonly_fields = ('end_date', 'begin_vol_of_prod',
                       'end_delta_vol_of_prod',)
    empty_value_display = '-пусто-'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'volume')
    empty_value_display = '-пусто-'
