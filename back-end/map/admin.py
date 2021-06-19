from django.contrib import admin

from map.models import Marker, MarkerImage


class MarkerImageAdminInline(admin.TabularInline):
    extra = 1
    model = MarkerImage


@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    inlines = [MarkerImageAdminInline, ]
