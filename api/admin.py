from django.contrib import admin

from .models import Batch, Employee, Provider, Product, Reservoir, Shift, Sale


class BatchAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__',)
    readonly_fields = ('density',)
    search_fields = ('provider', 'shift_accepted',)
    empty_value_display = '-пусто-'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'third_name',)
    readonly_fields = ('experience',)
    search_fields = ('last_name', 'first_name', 'third_name', 'gender')
    empty_value_display = '-пусто-'


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReservoirAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_of_delivery')
    empty_value_display = '-пусто-'


class SaleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'volume')
    empty_value_display = '-пусто-'


admin.site.register(Batch, BatchAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Reservoir, ReservoirAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Sale, SaleAdmin)
