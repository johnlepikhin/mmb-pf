import datetime
import logging
import mimetypes
import os
import random
import time

import magic
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator
from django.db import models

from addrbook.models import CustomSignes, Streets, StreetSignes, Teams
from mmb_pf.common_services import get_constant_models

# This is shared storage - it CAN BE ACCESSED by nginx without authorization. So files should have unpredictable names
image_storage_shared = FileSystemStorage(location=f"{settings.BASE_DIR}/media")

constant_models = get_constant_models()


class SystemSettingsMananger(models.Manager):
    def get_option(self, **kwargs):
        """
        TAKE:
            name=option_name,
            default=123, # [Optional], desired value if no such option created
        """
        if "name" not in kwargs:
            raise ValueError("Имя настройки не передано")

        option_val = ""
        option_obj = None
        try:
            option_obj = self.get(name=kwargs["name"])
        except Exception:
            if "default" not in kwargs:
                raise ValueError(  # pylint: disable = raise-missing-from
                    f"Настройки с именем '{kwargs['name']}' не существует, и не передано значение по умолчанию"
                )
            else:
                option_val = kwargs["default"]
        if option_obj:
            system_settings = SystemSettings()
            type_names = system_settings.OPTION_TYPES["names"]
            option_val = getattr(option_obj, type_names[option_obj.option_type])

        return option_val

    def set_option(self, **kwargs):
        """
        TAKE:
            name=option_name,
            value=123, # option value
        """
        if "name" not in kwargs:
            raise ValueError("Имя настройки не передано")
        if "value" not in kwargs:
            raise ValueError("Значение настройки не передано")

        option_obj = None
        try:
            option_obj = self.get(name=kwargs["name"])
        except Exception:
            raise ValueError(  # pylint: disable = raise-missing-from
                f"Настройки с именем '{kwargs['name']}' не существует"
            )

        if option_obj:
            system_settings = SystemSettings()
            type_names = system_settings.OPTION_TYPES["names"]
            setattr(option_obj, type_names[option_obj.option_type], kwargs["value"])
            option_obj.save()

        return getattr(option_obj, type_names[option_obj.option_type])


class SystemSettings(models.Model):
    OPTION_TYPES = {
        "names": {  # used for filtering
            "BooleanField": "BooleanField",
            "PositiveIntegerField": "PositiveIntegerField",
            "IntegerField": "IntegerField",
            "CharField": "CharField",
            "TextField": "TextField",
            "JsonField": "JsonField",
            "DateField": "DateField",
            "DateTimeField": "DateTimeField",
        },
        "choices": [
            ("BooleanField", "Булево значение"),
            ("PositiveIntegerField", "Положительное целое число"),
            ("IntegerField", "Целое число"),
            ("CharField", "Строка"),
            ("TextField", "Текст"),
            ("JsonField", "Json"),
            ("DateField", "Дата"),
            ("DateTimeField", "Дата и время"),
        ],
        "default": "BooleanField",
    }

    name = models.CharField(
        default="",
        blank=False,
        null=False,
        unique=True,
        max_length=128,
        help_text="Имя настройки",
    )
    option_type = models.CharField(
        max_length=128,
        choices=OPTION_TYPES["choices"],
        default=OPTION_TYPES["default"],
        help_text="Тип опции",
    )
    desc = models.TextField(
        default="",
        blank=True,
        max_length=2048,
        help_text="Описание настройки",
    )
    BooleanField = models.BooleanField(
        blank=True,
        help_text="Булево значение",
    )
    PositiveIntegerField = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Положительное целое число",
    )
    IntegerField = models.IntegerField(
        blank=True,
        null=True,
        help_text="Целое число",
    )
    CharField = models.CharField(
        blank=True,
        help_text="Строка",
        max_length=1024,
    )
    TextField = models.TextField(
        blank=True,
        help_text="Текст",
    )
    JsonField = models.JSONField(
        blank=True,
        null=True,
        help_text="Json",
    )
    DateField = models.DateField(
        blank=True,
        null=True,
        help_text="Дата",
    )
    DateTimeField = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Дата и время",
    )

    objects = SystemSettingsMananger()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Настройки системы"


class MainMenu(models.Model):
    """
    This is main menu of the MMB PF
    """

    MAIN_MENU_TYPES = [
        ("dropdown", "dropdown"),
        ("fixed", "fixed"),
    ]
    order = models.PositiveSmallIntegerField(
        default=1,
        blank=False,
        null=False,
        help_text="Порядок отображения",
    )
    disabled = models.BooleanField(blank=True, default=False, help_text="Не отображать в меню")

    permission = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=128,
        help_text="Право отвечающее за доступ в элемент меню. Если не задано, меню будет отображаться всегда",
    )
    name = models.CharField(
        default="",
        unique=True,
        blank=False,
        max_length=512,
        help_text="Отображаемое имя",
    )
    menu_type = models.CharField(
        max_length=128,
        choices=MAIN_MENU_TYPES,
        default="dropdown",
        help_text="Тип меню",
    )
    tid = models.CharField(
        default="",
        unique=True,
        blank=False,
        max_length=512,
        help_text="Уникальный идентификатор, латиница. Используется для поиска элемента на странице",
    )
    icon = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=128,
        help_text="Отображаемая иконка, из https://fontawesome.com/icons?d=gallery&m=free Например: fas fa-user-shield",
    )
    items = models.JSONField(
        default=list,
        blank=True,
        help_text="Подкатегории",
    )

    def __str__(self):
        return str(self.tid)

    class Meta:
        verbose_name_plural = "Главное меню"


def image_path(instance, filename):
    unix_time = int(time.time())
    now_date = datetime.datetime.now()
    current_up_dir = f"{now_date.year}-{now_date.month:02d}"

    _, file_extension = os.path.splitext(filename)
    if not file_extension:
        image_data = bytes(instance.file.read())
        detected_type = magic.from_buffer(image_data, mime=True)
        if detected_type:
            file_extension = mimetypes.guess_extension(detected_type)
    if not file_extension or file_extension == ".jpe":
        file_extension = ".jpg"
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return f"upload/{current_up_dir}/img_{randomstr}_{unix_time}{file_extension}"


class ImageStorage(models.Model):

    file = models.ImageField(storage=image_storage_shared, upload_to=image_path)
    app_name = models.CharField(
        max_length=128,
        blank=False,
        help_text="Идентификатор приложения, которое загрузило файл",
    )
    desc = models.CharField(
        default="",
        max_length=2048,
        blank=True,
        help_text="Описание",
    )

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            try:
                os.remove(self.file.path)
            except Exception:
                logging.error(f"Can't remove file: '{self.file.path}'")

        super(ImageStorage, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if hasattr(self, "id"):
            try:
                this = ImageStorage.objects.get(id=self.id)
                if this.file != self.file:
                    this.file.delete()
            except Exception:
                logging.error(f"Can't remove file: '{self.file.path}'")

        super(ImageStorage, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Хранилище изображений"


class MMBPFUsers(AbstractUser):
    """
    This is users of the MMB PF system
    """

    user_type = models.PositiveSmallIntegerField(
        choices=constant_models["USER_TYPE"]["choices"],
        default=constant_models["USER_TYPE"]["default"],
        help_text="Тип пользователя",
    )

    modification_date = models.DateTimeField(
        auto_now=True,
        unique=False,
        blank=False,
        null=False,
        help_text="Время последней модификации основных данных",
    )
    first_name = models.CharField(
        default="",
        unique=False,
        blank=False,
        max_length=512,
        help_text="Имя",
    )
    last_name = models.CharField(
        default="",
        unique=False,
        blank=False,
        max_length=512,
        help_text="Фамилия",
    )
    patronymic = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=512,
        help_text="Отчество",
    )
    gender = models.PositiveSmallIntegerField(
        choices=constant_models["GENDER"]["choices"],
        default=constant_models["GENDER"]["default"],
        blank=True,
    )
    phone = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=128,
        help_text="Телефон",
    )
    email = models.EmailField(
        default="",
        unique=False,
        blank=True,
        help_text="Почта",
    )
    birth = models.DateField(
        blank=True,
        null=True,
        help_text="Дата рождения",
    )
    tourist_club = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=1024,
        help_text="Название туристического клуба если есть",
    )

    team = models.ForeignKey(Teams, blank=False, null=True, on_delete=models.SET_NULL, help_text="Команда")
    street = models.ForeignKey(Streets, blank=True, null=True, on_delete=models.SET_NULL, help_text="Улица")
    sign = models.ForeignKey(
        StreetSignes, blank=True, null=True, on_delete=models.SET_NULL, help_text="Уличный указатель"
    )
    custom_sign = models.ForeignKey(
        CustomSignes, blank=True, null=True, on_delete=models.SET_NULL, help_text="Индивидуальный указатель"
    )
    images = models.ManyToManyField(ImageStorage, blank=True, related_name="user_images")

    user_desc = models.TextField(
        default="",
        blank=True,
        max_length=32768,
        help_text="Заметки о пользователе",
    )

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name_plural = "Пользователи"


class MMBPFGroups(Group):
    desc = models.TextField(
        default="",
        blank=True,
        max_length=2000,
        help_text="Описание группы",
    )

    class Meta:
        verbose_name_plural = "Группы"


class JournalsManager(models.Manager):
    def add_to_journal(self, **kwargs):
        new_entry = None
        max_entries = SystemSettings.objects.get_option(name="max_journal_entries", default=10000)

        if "username" not in kwargs or "user_id" not in kwargs:
            if "serializer" in kwargs:
                request = kwargs["serializer"].context.get("request")
                if request and hasattr(request, "user"):
                    user = request.user
                    kwargs["username"] = user.username or "Неавторизованный пользователь"
                    kwargs["user_id"] = user.id

                kwargs["user_agent"] = request.META["HTTP_USER_AGENT"]
                kwargs["ip"] = request.META.get("REMOTE_HOST", None) or request.META.get("REMOTE_ADDR", "")
                del kwargs["serializer"]
            else:
                kwargs["username"] = "Неавторизованный пользователь"
                kwargs["user_id"] = None

        if "desc" in kwargs:
            kwargs["desc"] = kwargs["desc"][:4095]

        try:
            new_entry = self.create(**kwargs)
        except Exception:
            pass

        if self.get_queryset().count() >= max_entries:
            for instance_id in self.get_queryset().values_list("id", flat=True):
                self.get_queryset().get(id=instance_id).delete()
                if self.get_queryset().count() <= max_entries:
                    break

        return new_entry


class ParticipantCardActionsJournal(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True,
        unique=False,
        blank=False,
        null=False,
        help_text="Дата и время создания события",
    )

    ip = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=48,
        help_text="ip адрес с которого пришёл запрос",
    )

    user_agent = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=1024,
        help_text="User agent котрый прислал браузер пользователя",
    )

    username = models.CharField(
        default="",
        unique=False,
        blank=False,
        max_length=256,
        help_text="username пользователя вошедшего в систему",
    )

    user_id = models.IntegerField(
        null=True,
        default=None,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="id пользователя",
    )

    participant_id = models.IntegerField(
        default=None,
        blank=False,
        validators=[MinValueValidator(1)],
        help_text="id карточки участника",
    )

    desc = models.CharField(
        default="",
        blank=True,
        max_length=4096,
        help_text="Описание действия",
    )

    objects = JournalsManager()
