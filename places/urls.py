from django.urls import path

from .views import PlaceDetails, PlacesList

urlpatterns = [
    path("", PlacesList.as_view(), name="places"),
    path("places/<int:pk>", PlaceDetails.as_view(), name="place-details"),
]
