from django.shortcuts import render
from django.views.decorators.http import require_POST

from djlexique.utils import get_object_if_owner
from lexique.models import Lexique

from .forms import QuizzForm
from .quizz import Quizz


def main_view(request, slug: str):
    lexique = get_object_if_owner(request, Lexique, slug=slug)
    query_filter = request.POST.get("query_filter", "all")
    source = int(request.POST.get("source", 0))

    quizz = Quizz(lexique=lexique, query_filter=query_filter, source=source)
    quizz.load_new_question()
    context = {"quizz": quizz, "lexique": lexique}
    return render(request, "quizz/main.html", context)


@require_POST
def guess_view(request, slug: str):
    """guess view

    Args:
        request (Request): django request
        slug (str): lexique slug
    """
    lexique = get_object_if_owner(request, Lexique, slug=slug)
    form = QuizzForm(request.POST or None)

    assert form.is_valid(), f"{form.er}.join('\n')"
    guess = form.cleaned_data.pop("guess", "")
    go_next = form.cleaned_data.pop("go_next", None)
    quizz = Quizz(**form.cleaned_data, lexique=lexique)
    if go_next:
        quizz.next_pick()
    elif quizz.check(guess):
        quizz.next_pick(success=True)
    context = {"quizz": quizz, "lexique": lexique}
    return render(request, "quizz/quizzbox.html", context)
