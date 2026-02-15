from django.contrib import admin
from .models import SiteVisit

@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'ip_address', 'timestamp', 'user_agent')
    list_filter = ('timestamp', 'path')
    search_fields = ('path', 'ip_address')
