from django.contrib import admin
from accounts.models import BanyanUser, BanyanUserDevices, BanyanUserNotifications

class BanyanUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(BanyanUser, BanyanUserAdmin)

class BanyanUserDevicesAdmin(admin.ModelAdmin):
    pass
admin.site.register(BanyanUserDevices, BanyanUserAdmin)

class BanyanUserNotificationsAdmin(admin.ModelAdmin):
    pass
admin.site.register(BanyanUserNotifications, BanyanUserAdmin)
