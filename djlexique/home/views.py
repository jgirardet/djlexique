from django.shortcuts import render
from django.views.decorators.http import require_POST

from lexique.forms import LexiqueForm
from lexique.models import Lexique


def lexiques_index_view(request):
    context = {"lexiques": Lexique.objects.filter(user=request.user)}
    return render(request, "home/lexiques-index.html", context)


@require_POST
def lexiques_add_view(request):
    form = LexiqueForm(request.POST or None)
    if form.is_valid():
        Lexique.objects.create(**form.cleaned_data, user=request.user)
    context = {"lexiques": Lexique.objects.filter(user=request.user)}
    return render(request, "home/lexiques-list.html", context)
