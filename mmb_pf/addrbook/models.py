from django.db import models


class CustomSignes(models.Model):
    """
    Custom signes placed by participants
    """

    name = models.CharField(
        default="",
        unique=True,
        blank=False,
        max_length=512,
        help_text="Название знака",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Индивидуальные указатели"


class StreetSignes(models.Model):
    """
    Signes places at the streets
    """

    name = models.CharField(
        default="",
        unique=True,
        blank=False,
        max_length=512,
        help_text="Название знака",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Уличные указатели"


class Streets(models.Model):
    """
    Streets at the "city"
    """

    name = models.CharField(
        default="",
        unique=True,
        blank=False,
        max_length=512,
        help_text="Название улицы",
    )

    signes = models.ManyToManyField(StreetSignes, blank=True, related_name="street_signes")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Улицы"


class Teams(models.Model):
    """
    Teams for competition
    """

    team_id = models.PositiveIntegerField(
        unique=True,
        blank=False,
        help_text="Номер команды",
    )

    name = models.CharField(
        default="",
        unique=True,
        blank=False,
        max_length=512,
        help_text="Название Команды",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Команды"
