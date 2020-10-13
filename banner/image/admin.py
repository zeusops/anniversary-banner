from django.contrib import admin
from django.db.models import Count

from .models import Side, Team, BannerConfig, BannerConfigEntry

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
    list_display = ('name', 'points', 'active', 'teams', 'has_logo')
    inlines = [TeamInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(teams=Count('team'))

    def teams(self, obj):
        return obj.teams
    teams.admin_order_field = 'teams'

    def has_logo(self, obj):
        return obj.logo != ''
    # has_logo.admin_order_field = 'has_logo'
    has_logo.boolean = True
    has_logo.short_description = 'Has logo'


class BannerConfigEntryInline(admin.TabularInline):
    model = BannerConfigEntry


@admin.register(BannerConfig)
class BannerConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        permission = super().has_add_permission(request)
        if permission and BannerConfig.objects.exists():
            permission = False
        return permission
    inlines = [BannerConfigEntryInline]

# admin.site.register(BannerConfigEntry)
