# loans/admin.py
from django.contrib import admin
from .models import Loan, Device, Functionteam, Cocodri, Pegadri, Station, Log

from import_export.admin import ImportExportMixin, ExportActionModelAdmin
from import_export import resources, widgets, fields
from import_export.widgets import ForeignKeyWidget

class StationResource(resources.ModelResource):
    #config = fields.Field(column_name='config', attribute='config', 
    #        widget=ForeignKeyWidget(Config, 'name'))
    class Meta:
        model = Station
        fields = ('id','name')
        #widgets = {
        #          'received_at': {'format': '%m/%d/%Y %I:%M:%S %p'},
        #          'approved_at': {'format': '%m/%d/%Y %I:%M:%S %p'},
        #        }
        #fields = ('id', 'config', 'request', 'unit_no', 'isn',)

class DeviceInline(admin.TabularInline):
    model = Device
    extra = 1

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'function_team', 'purpose', 'disassemble',
        'cocodri', 'pegadri', 'created_at',
    )
    inlines = (DeviceInline,)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'isn', 'config', 'unit_no',
        'station', 'failure_symptoms',
    )

@admin.register(Cocodri)
class CocodriAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'owner')

@admin.register(Pegadri)
class PegadriAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'owner')

@admin.register(Functionteam)
class FunctionteamAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Station)
class StationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    resource_class = StationResource 

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'function', 'info',
        'created_at',
    )
    list_filter = ['name', 'function']
