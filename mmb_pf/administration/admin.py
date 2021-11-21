from ckeditor.widgets import CKEditorWidget
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import ContentType, Group, Permission
from django.db import models
from django.utils.html import mark_safe
from jsoneditor.forms import JSONEditor

from .forms import (
    MMBPFUsersAdminPasswordChangeForm,
    MMBPFUsersCreationForm,
    MMBPFUsersForm,
    SystemSettingsCreationForm,
    SystemSettingsForm,
)
from .models import MainMenu, MMBPFGroups, MMBPFUsers, SystemSettings


class MainMenuAdmin(admin.ModelAdmin):
    list_display = ["order", "tid", "name", "disabled"]
    list_display_links = [
        "order",
        "tid",
    ]
    search_fields = [
        "tid",
        "name",
        "items",
    ]
    list_per_page = 35
    ordering = ("id",)
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditor},
    }
    fieldsets = (
        ("Пункт меню", {"fields": (("order", "disabled"), ("name",), ("permission",))}),
        ("Настройки", {"fields": ("tid", "menu_type", "icon", "items")}),
    )
    model = MainMenu


class MMBPFGroupsAdmin(admin.ModelAdmin):
    model = MMBPFGroups
    list_display = ["id", "name"]
    list_display_links = [
        "id",
        "name",
    ]


class MMBPFUsersAdmin(UserAdmin):
    add_form = MMBPFUsersCreationForm
    form = MMBPFUsersForm
    change_password_form = MMBPFUsersAdminPasswordChangeForm
    model = MMBPFUsers
    list_display = [
        "id",
        "username",
        "last_name",
        "first_name",
        "patronymic",
        "is_active",
    ]
    list_display_links = [
        "id",
        "username",
    ]
    search_fields = ["id", "username", "last_name", "first_name", "patronymic"]
    readonly_fields = [
        "date_joined",
        "last_login",
    ]
    list_per_page = 35
    # raw_id_fields = ("photos", "files")
    ordering = ("id",)

    readonly_added = False
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget(config_name="basic_extended")},
    }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )
    fieldsets = (
        (
            "Общее",
            {
                "fields": [
                    # ("user_type",),
                    (
                        "is_active",
                        "is_staff",
                    ),
                    ("date_joined"),
                ]
            },
        ),
        ("Авторизация", {"fields": (("username", "password"),)}),
        (
            "Персональная информация",
            {
                "fields": (
                    ("last_name", "first_name", "patronymic"),
                    (
                        "gender",
                        "birth",
                    ),
                    "fact_address",
                )
            },
        ),
        (
            "Контакты",
            {
                "fields": (
                    (
                        "phone",
                        "email",
                    ),
                )
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": (
                    # (
                    #     "photos",
                    #     "files",
                    # ),
                    ("user_desc",),
                )
            },
        ),
        ("Права", {"fields": ("groups",)}),
        ("Информация о активности", {"fields": ("last_login",)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        # if request.user.is_superuser:
        #     if "is_superuser" not in self.fieldsets[0][1]["fields"]:
        #         self.fieldsets[0][1]["fields"].append("is_superuser")
        # else:
        #     if "is_superuser" in self.fieldsets[0][1]["fields"]:
        #         self.fieldsets[0][1]["fields"].remove("is_superuser")

        return self.fieldsets

    def get_queryset(self, request):
        """
        hide superusers from not superusers
        """
        qs = super(UserAdmin, self).get_queryset(request)
        # if not request.user.is_superuser:
        #     qs = qs.filter(is_superuser=False)
        #     is_admin = False
        #     for group_obj in request.user.groups.all():
        #         if group_obj.name == "Администраторы":
        #             is_admin = True
        #     if not is_admin:
        #         qs = qs.filter(user_type=constant_models["USER_TYPE"]["names"]["PERSONNEL"])
        return qs

    def get_form(self, request, obj=None, **kwargs):
        """
        Change fileds of user admin
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)

        return super().get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        super(MMBPFUsersAdmin, self).save_model(request, obj, form, change)


class SystemSettingsAdmin(admin.ModelAdmin):
    add_form = SystemSettingsCreationForm
    form = SystemSettingsForm
    list_display = [
        "id",
        "name",
        "option_type",
        "desc",
    ]
    list_display_links = [
        "id",
        "name",
    ]
    search_fields = [
        "id",
        "name",
    ]
    list_per_page = 35
    ordering = ("id",)
    # readonly_fields = []
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditor},
    }
    fieldsets = (  # typing: ignore
        (
            "Общие",
            {
                "fields": (
                    (
                        "name",
                        "option_type",
                    ),
                    ("desc",),
                ),
            },
        ),
        (
            "Поля",
            {
                "fields": [],
            },
        ),
    )
    change_list_template = "admin/administration/systemsettings_list.html"

    def get_queryset(self, request):
        """
        hide critical options from non superusers
        """
        hidden = ["personnel_default_group_id"]
        qs = super(SystemSettingsAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(name__in=hidden)
        return qs

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            self.readonly_fields = []
            self.fieldsets[1][1]["fields"] = [
                "BooleanField",
                "PositiveIntegerField",
                "IntegerField",
                "CharField",
                "TextField",
                "JsonField",
                "DateField",
                "DateTimeField",
            ]
        else:
            self.readonly_fields = ["name", "option_type", "desc"]
            self.fieldsets[1][1]["fields"] = [obj.option_type]

        return self.fieldsets

    def get_form(self, request, obj=None, **kwargs):
        """
        Change fileds
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)

        return super().get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        # check filled right field depends from type
        # This is not good place for validation (should be performed at form model, but form model doesn't get readonly fields!)
        can_be_saved = True
        if not request.user.is_superuser:
            if form.changed_data[0] != obj.option_type:
                messages.error(
                    request,
                    f"ОШИБКА СОХРАНЕНИЯ: В опции с типом '{obj.option_type}' нельзя изменять другие поля кроме '{obj.option_type}', проверьте правильность заполнения формы",
                )
                can_be_saved = False

        if can_be_saved:
            super(SystemSettingsAdmin, self).save_model(request, obj, form, change)


admin.site.register(MMBPFUsers, MMBPFUsersAdmin)
admin.site.register(MMBPFGroups, MMBPFGroupsAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(MainMenu, MainMenuAdmin)
admin.site.register(SystemSettings, SystemSettingsAdmin)
