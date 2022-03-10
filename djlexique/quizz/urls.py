from django.urls import path

from .apps import QuizzConfig
from .views import guess_view, main_view

app_name = QuizzConfig.name
urlpatterns = [
    path("<slug:slug>/guess/", guess_view, name="guess"),
    path("<slug:slug>/", main_view, name="main"),
]
