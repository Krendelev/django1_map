import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from pathlib import Path

from places.models import Photo, Place


class Command(BaseCommand):
    help = "Добавляект объект в базу данных"

    def add_arguments(self, parser):
        parser.add_argument("url", nargs="+")

    def handle(self, *args, **options):
        try:
            response = requests.get(*options["url"], timeout=5)
            response.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError) as err:
            self.stderr.write(self.style.ERROR(err))
            exit()

        place = response.json()
        obj, _ = Place.objects.get_or_create(
            title=place["title"],
            description_short=place["description_short"],
            description_long=place["description_long"],
            longitude=place["coordinates"]["lng"],
            latitude=place["coordinates"]["lat"],
        )
        obj.save()

        missed_images = []
        for idx, url in enumerate(place["imgs"], start=1):
            image, _ = Photo.objects.get_or_create(place=obj, position=idx)
            image_name = Path(url).name
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
            except (requests.HTTPError, requests.ConnectionError) as err:
                missed_images.append(image_name)

            image.photo.save(image_name, ContentFile(response.content), save=True)

        if missed_images:
            self.stderr.write(
                self.style.WARNING(f"Не удалось загрузить: {missed_images}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Объект {place['title']} успешно добавлен в базу")
        )
