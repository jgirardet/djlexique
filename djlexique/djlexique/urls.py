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
from django.contrib import admin
from django.urls import path
from lexique.views import (
    lexique_home,
    lexique_add_view,
    lexique_list_view,
    lexon_edit_view,
    lexique_add_confirmation_view,
)

urlpatterns = [
    path("lexique/<slug:slug>/", lexique_home, name="lexique-home"),
    path("lexique/<slug:slug>/list/", lexique_list_view, name="lexique-list"),
    path("lexique/<slug:slug>/add/", lexique_add_view, name="lexique-add"),
    path("lexique/<slug:slug>/add/confirmation/", lexique_add_confirmation_view, name="lexique-add-confirmation"),
    path("lexon/<int:id>/edit/", lexon_edit_view, name="lexon-edit"),
    # path('form/', form_view, name="list"),
    path("admin/", admin.site.urls),
]
