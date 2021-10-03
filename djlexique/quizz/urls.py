from django.urls import path
from .apps import QuizzConfig
from .views import main_view


app_name = QuizzConfig.name
urlpatterns = [
    path("<slug:slug>/", main_view, name="main"),
]
