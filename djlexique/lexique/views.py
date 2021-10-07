from typing import NamedTuple
from django.db.models.query import QuerySet

from django.http.response import HttpResponse, HttpResponseBadRequest
from .models import Lexon, Lexique
from django.shortcuts import get_object_or_404, render
from .forms import LexonForm, LexiqueForm
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.core.paginator import InvalidPage, Paginator
from djlexique.utils import get_object_if_owner

#######################################################################
# Lexique Détail et Lexon
#######################################################################
LEXON_LIST_LIMIT = 100


def lexique_home(request, slug: str):
    lexique = get_object_if_owner(request, Lexique, slug=slug)
    qs = lexique.get_lexons_by()[:LEXON_LIST_LIMIT]
    form = LexonForm()
    form.instance.lexique = lexique
    context = {"objects": qs, "form": form, "lexique": lexique, "errors": ""}
    return render(request, "lexique/lexique.html", context)


@require_POST
def lexique_add_lexon_view(request, slug: str):
    lexique, context, form = get_lexique(request, slug)
    if form.is_valid():
        lexons = lexique.get_lexons(**form.cleaned_data)
        if lexons.exists():
            context.update(form.cleaned_data)
            context["objects"] = lexons
            return render(request, "lexique/lexon/form-already-exists.html", context)
        else:
            form.instance.lexique = lexique
            obj = form.save()
            context["message"] = {"type": "success", "content": f"{str(obj)} ajouté"}
    else:
        context["message"] = {"type": "error", "content": form.errors}

    return _get_add_response_succes(request, context)


@require_POST
def lexique_add_confirmation_view(request, slug=str):
    if confirm := request.POST.get("confirm"):
        lexique, context, form = get_lexique(request, slug)
        if (
            form.is_valid() and confirm == "oui"
        ):  # si pas valid, on n'accepte pas le oui
            form.instance.lexique = lexique
            obj = form.save()
            context["message"] = {"type": "success", "content": f"{str(obj)} ajouté"}
            return _get_add_response_succes(request, context)
        else:
            context.update(form.cleaned_data)  # is_valid doit bien êtr appelé avant
            return _get_add_response_succes(request, context)
    else:
        return HttpResponseBadRequest("'confirm' flag not provided")


def lexique_list_view(request, slug: str):
    search = request.GET.get("search")
    order_by = request.GET.get("order_by")
    lexique = get_object_if_owner(request, Lexique, slug=slug)
    qs: QuerySet[Lexon]
    if search:
        qs = lexique.search_lexons(search)
    else:
        qs = lexique.get_lexons_by(order_by)
    pages = Paginator(qs, LEXON_LIST_LIMIT)
    num_page = int(request.GET.get("page", 1))
    if request.GET.get("next_page"):
        num_page += 1
    try:
        objects = pages.page(num_page).object_list
    except InvalidPage:
        return HttpResponse("")
    context = {"lexique": lexique, "objects": objects, "errors": [], "page": num_page}
    return render(request, "lexique/lexon-list.html", context)


@require_http_methods(["GET", "POST"])
def lexon_edit_view(request, id: int):
    lexon = get_object_if_owner(request, Lexon, id=id, field="lexique.user")
    if request.method == "GET":
        return render(request, "lexique/lexon/edit-form.html", {"object": lexon})
    if request.method == "POST":
        lexon = get_object_or_404(Lexon, id=id)
        form = LexonForm(request.POST, instance=lexon)
        if form.is_valid():
            form.save()
        return render(request, "lexique/lexon/as_row.html", {"object": lexon})


@require_GET
def lexon_delete_view(request, id: int):
    lexon = get_object_if_owner(request, Lexon, id=id, field="lexique.user")
    lexon.delete()
    return HttpResponse("")


#############################################################
# privates
#############################################################


def get_lexique(request, slug: str):
    lexique = get_object_if_owner(request, Lexique, slug=slug)
    context = {
        "message": None,
        "lexique": lexique,
    }
    form = LexonForm(request.POST or None)
    return lexique, context, form


def _get_add_response_succes(request, context):
    response = render(request, "lexique/lexon/add-form.html", context)
    response["HX-Trigger"] = "newLexiqueEntry"
    return response
