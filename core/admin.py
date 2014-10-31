from django.contrib import admin
from core.models import Activity, Story, Piece

class StoryObjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Story, StoryObjectAdmin)

class PieceObjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Piece, PieceObjectAdmin)

class ActivityObjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Activity, ActivityObjectAdmin)
