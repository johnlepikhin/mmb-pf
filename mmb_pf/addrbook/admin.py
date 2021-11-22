from django.contrib import admin

from .models import StreetSignes


class StreetSignesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    list_display_links = [
        "name",
    ]
    search_fields = [
        "id",
        "name",
    ]
    list_per_page = 35
    ordering = ("name",)

    model = StreetSignes


admin.site.register(StreetSignes, StreetSignesAdmin)
