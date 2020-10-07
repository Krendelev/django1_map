from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Photo, Place


class PhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Photo
    fields = ("photo", "thumbnail")
    readonly_fields = ("thumbnail",)

    def thumbnail(self, obj):
        return mark_safe("<img src='{url}' height='200' />".format(url=obj.photo.url))


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    search_fields = ("title",)
