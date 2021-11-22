from typing import Tuple

from django.contrib import admin

from .models import Streets, StreetSignes, Teams


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


class StreetsAdmin(admin.ModelAdmin):
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
    fieldsets: Tuple = (
        (
            "Общее",
            {
                "fields": [
                    ("name",),
                ]
            },
        ),
        ("Знаки на этой улице", {"fields": (("signes"),)}),
    )

    model = Streets


class TeamsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "team_id",
        "name",
    ]
    list_display_links = [
        "team_id",
        "name",
    ]
    search_fields = [
        "team_id",
        "name",
    ]
    list_per_page = 35
    ordering = (
        "team_id",
        "name",
    )
    fieldsets: Tuple = (
        (
            "Общее",
            {
                "fields": [
                    (
                        "team_id",
                        "name",
                    ),
                ]
            },
        ),
    )

    model = Teams


admin.site.register(StreetSignes, StreetSignesAdmin)
admin.site.register(Streets, StreetsAdmin)
admin.site.register(Teams, TeamsAdmin)
