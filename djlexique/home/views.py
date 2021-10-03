from django.shortcuts import render
from lexique.models import Lexique


def lexiques_index_view(request):
    context = {"lexiques": Lexique.objects.all()}
    return render(request, "home/lexiques-index.html", context)
