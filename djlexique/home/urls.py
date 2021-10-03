from django.urls import path
from .apps import HomeConfig
from .views import lexiques_index_view

app_name = HomeConfig.name
urlpatterns = [
    path("", lexiques_index_view, name="lexiques-add"),
]
