# loans/admin.py
from django.contrib import admin
from .models import Loan, Device, Functionteam, Cocodri, Pegadri, Station

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
class FunctionteamAdmin(admin.ModelAdmin):
    list_display = ('name',)