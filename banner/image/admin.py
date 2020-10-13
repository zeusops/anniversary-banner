from django.contrib import admin

from .models import Side, Team

class TeamInline(admin.TabularInline):
    model = Team
    extra = 3


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'side', 'points', 'is_active')

    def is_active(self, obj):
        return obj.side.active
    # is_active.admin_order_field = 'is_active'
    is_active.boolean = True
    is_active.short_description = "Team's side is active"


@admin.register(Side)
class SideAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'active', 'has_logo')
    inlines = [TeamInline]

    def has_logo(self, obj):
        return obj.logo != ''
    # has_logo.admin_order_field = 'has_logo'
    has_logo.boolean = True
    has_logo.short_description = 'Has logo'

