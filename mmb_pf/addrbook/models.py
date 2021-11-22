from django.db import models


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
