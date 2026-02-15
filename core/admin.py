from django.contrib import admin
from django.utils.html import format_html
from .models import Profile
from .models import Profile
from .system_models import SystemNode, SystemConnection
from . import admin_dashboard # Import separate admin config

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title')
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(SystemNode)
class SystemNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_core_badge', 'order_index', 'is_active', 'color_preview')
    list_filter = ('is_active', 'is_core', 'category')
    search_fields = ('title', 'slug', 'description')
    ordering = ('-is_core', 'order_index')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order_index', 'is_active')

    fieldsets = (
        ('Identity', {
            'fields': ('title', 'slug', 'description', 'category', 'is_active')
        }),
        ('Visuals', {
            'fields': ('color', 'icon', 'importance_weight', 'pulse_enabled')
        }),
        ('Architecture', {
            'fields': ('is_core', 'order_index')
        }),
    )

    def is_core_badge(self, obj):
        if obj.is_core:
            return format_html('<span style="color: #7B61FF; font-weight: bold;">★ CORE</span>')
        return "Node"
    is_core_badge.short_description = "Type"

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_preview.short_description = "Color"

@admin.register(SystemConnection)
class SystemConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_node', 'to_node', 'flow_type_badge', 'strength_bar', 'is_bidirectional')
    list_filter = ('flow_type', 'is_bidirectional')
    search_fields = ('from_node__title', 'to_node__title')
    autocomplete_fields = ['from_node', 'to_node']

    def flow_type_badge(self, obj):
        colors = {
            'data': '#00F5FF',
            'inference': '#7B61FF',
            'feedback': '#10B981'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.flow_type, '#fff'),
            obj.get_flow_type_display().upper()
        )
    flow_type_badge.short_description = "Flow Type"

    def strength_bar(self, obj):
        return format_html(
            '<div style="width: {}px; height: 6px; background-color: #ccc; border-radius: 3px;">'
            '<div style="width: {}%; height: 100%; background-color: #00F5FF; border-radius: 3px;"></div>'
            '</div>',
            50, (obj.strength / 5) * 100
        )
    strength_bar.short_description = "Signal Strength"
