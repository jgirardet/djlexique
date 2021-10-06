from django.shortcuts import get_object_or_404, render
from .quizz import Quizz
from lexique.models import Lexique
from django.views.decorators.http import require_POST

# Create your views here.
from .forms import QuizzForm


def main_view(request, slug: str):
    lexique = get_object_or_404(Lexique, slug=slug)
    query_filter = request.POST.get("query_filter", "all")
    quizz = Quizz(lexique=lexique, query_filter=query_filter)
    quizz.load_new_question()
    context = {"quizz": quizz, "lexique": lexique}
    return render(request, "quizz/main.html", context)


@require_POST
def guess_view(request, slug: str):
    lexique = get_object_or_404(Lexique, slug=slug)
    form = QuizzForm(request.POST or None)
    form.full_clean()
    guess = form.cleaned_data.pop("guess", "")
    go_next = form.cleaned_data.pop("go_next", None)
    quizz = Quizz(**form.cleaned_data, lexique=lexique)
    if go_next:
        quizz.next_pick()
    elif quizz.check(guess):
        quizz.next_pick(success=True)
    context = {"quizz": quizz, "lexique": lexique}
    print(quizz)
    return render(request, "quizz/quizzbox.html", context)
