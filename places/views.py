from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .models import Place


class PlacesList(ListView):
    model = Place
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["places"] = {"type": "FeatureCollection", "features": []}
        for place in self.object_list:
            context["places"]["features"].append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [place.longitude, place.latitude],
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": place.id,
                        "detailsUrl": reverse("place-details", args=[place.id]),
                    },
                }
            )
        return context


class PlaceDetails(DetailView):
    model = Place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place = self.get_object()
        context["place"] = {"title": place.title}
        context["place"]["imgs"] = [obj.photo.url for obj in place.photos.all()]
        context["place"]["description_short"] = place.short_description
        context["place"]["description_long"] = place.long_description
        context["place"]["coordinates"] = {
            "lat": place.latitude,
            "lng": place.longitude,
        }
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return JsonResponse(context["place"], json_dumps_params={"ensure_ascii": False})
