"""djlexique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from lexique.views import (
    lexique_home,
    lexique_add_lexon_view,
    lexique_list_view,
    lexon_edit_view,
    lexique_add_confirmation_view,
    lexon_delete_view,
    lexiques_index_view,
    lexiques_add_view
)
from .apps import LexiqueConfig

app_name = LexiqueConfig.name
urlpatterns = [
    path("", lexiques_index_view, name="lexiques"),
    path("add/", lexiques_add_view, name="lexiques-add"),
    path("<slug:slug>/", lexique_home, name="home"),
    path("<slug:slug>/lexons/list/", lexique_list_view, name="list-lexon"),
    path("<slug:slug>/lexons/add/", lexique_add_lexon_view, name="add-lexon"),
    path(
        "<slug:slug>/lexons/add_confirmation/",
        lexique_add_confirmation_view,
        name="add-lexon-confirmation",
    ),
    path("lexons/<int:id>/edit/", lexon_edit_view, name="edit-lexon"),
    path("lexons/<int:id>/delete/", lexon_delete_view, name="delete-lexon"),
]
