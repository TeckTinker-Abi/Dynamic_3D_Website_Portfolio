from django.contrib import admin
from .dashboard_models import GlobalSetting, ImpactMetric, CapabilitySignal, CurrentFocus, IdentityCore, LiveSystem

@admin.register(GlobalSetting)
class GlobalSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description', 'is_public')
    search_fields = ('key', 'description')

@admin.register(IdentityCore)
class IdentityCoreAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'current_status', 'organization_name', 'updated_at')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(LiveSystem)
class LiveSystemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'highlight_tag')
    list_editable = ('is_active',)

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(ImpactMetric)
class ImpactMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(CapabilitySignal)
class CapabilitySignalAdmin(admin.ModelAdmin):
    list_display = ('title', 'strength_level', 'display_order', 'is_active')
    list_editable = ('strength_level', 'display_order', 'is_active')

@admin.register(CurrentFocus)
class CurrentFocusAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
