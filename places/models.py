from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description_short = models.CharField(max_length=255, verbose_name="Синопсис")
    description_long = HTMLField(verbose_name="Описание")
    longitude = models.FloatField(verbose_name="Долгота")
    latitude = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


class Photo(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="place_photos",
        verbose_name="Место",
    )
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Позиция")

    def photo_upload_path(self, filename):
        return f"{self.place.id}/{filename}"

    photo = models.ImageField(upload_to=photo_upload_path, verbose_name="Фото")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"
        ordering = ("position",)

    def __str__(self):
        return f"{self.position} {self.place.title}"
