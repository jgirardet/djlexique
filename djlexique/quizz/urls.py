from django.urls import path
from .apps import QuizzConfig
from .views import main_view


app_name = QuizzConfig.name
urlpatterns = [
    # path("", lexiques_index_view, name="lexiques"),
    # path("add/", lexiques_add_view, name="lexiques-add"),
    # path("/check/", pick_view, name="check"),
    path("<slug:slug>/", main_view, name="main"),
    # path("<slug:slug>/pick/", pick_view, name="pick"),
]
