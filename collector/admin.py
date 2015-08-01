from django.contrib import admin
from collector.models import HumidTemp


class HumidTempAdmin(admin.ModelAdmin):
    fields = ('temperature', 'humidity', 'collect_datetime')
    list_display = ('temperature', 'humidity', 'collect_datetime')

admin.site.register(HumidTemp, HumidTempAdmin)

