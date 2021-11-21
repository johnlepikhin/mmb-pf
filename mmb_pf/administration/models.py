from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from mmb_pf.common_services import get_constant_models

constant_models = get_constant_models()


class MMBPFUsers(AbstractUser):
    """
    This is users of the MMB PF system
    """

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
    fact_address = models.CharField(
        default="",
        unique=False,
        blank=True,
        max_length=1024,
        help_text="Фактический адрес",
    )

    # photos = models.ManyToManyField(ImageStorage, blank=True, related_name="user_images")
    # files = models.ManyToManyField(FilePrivateStorage, blank=True, related_name="user_files")

    user_desc = models.TextField(
        default="",
        blank=True,
        max_length=32768,
        help_text="Заметки о пользователе",
    )

    def __str__(self):
        return self.username

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


class SystemSettingsMananger(models.Manager):
    def get_option(self, **kwargs):
        """
        TAKE:
            name=option_name,
            default=123, # [Optional], desired value if no such option created
        """
        if not "name" in kwargs:
            raise ValueError(f"Имя настройки не передано")

        option_val = ""
        option_obj = None
        try:
            option_obj = self.get(name=kwargs["name"])
        except:
            if not "default" in kwargs:
                raise ValueError(
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
        if not "name" in kwargs:
            raise ValueError(f"Имя настройки не передано")
        if not "value" in kwargs:
            raise ValueError(f"Значение настройки не передано")

        option_obj = None
        try:
            option_obj = self.get(name=kwargs["name"])
        except:
            raise ValueError(f"Настройки с именем '{kwargs['name']}' не существует")

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
        return self.name

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
        return self.tid

    class Meta:
        verbose_name_plural = "Главное меню"
