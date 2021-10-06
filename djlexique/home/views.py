from django.shortcuts import render
from lexique.forms import LexiqueForm
from lexique.models import Lexique
from django.views.decorators.http import require_POST

def lexiques_index_view(request):
    context = {"lexiques": Lexique.objects.filter()}
    return render(request, "home/lexiques-index.html", context)

@require_POST
def lexiques_add_view(request):
    form = LexiqueForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {"lexiques": Lexique.objects.all()}
    return render(request, "home/lexiques-list.html", context)
