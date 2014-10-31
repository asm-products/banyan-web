from django.contrib import admin
from content_feedback.models import FlaggedObject, HiddenObject

class FlaggedObjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(FlaggedObject, FlaggedObjectAdmin)

class HiddenObjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(HiddenObject, HiddenObjectAdmin)