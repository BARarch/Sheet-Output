from django.contrib import admin
from sheetoutput.models import CredetialsModel
from sheetoutput.models import FlowModel
from sheetoutput.models import SheetModel

# Register your models here.

class CredetialsModelAdmin(admin.ModelAdmin):
	pass
admin.site.register(CredetialsModel, CredetialsModelAdmin)

class FlowModelAdmin(admin.ModelAdmin):
	pass
admin.site.register(FlowModel, FlowModelAdmin)

class SheetModelAdmin(admin.ModelAdmin):
	pass
admin.site.register(SheetModel, SheetModelAdmin)

