from __future__ import annotations
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from .apps import LexiqueConfig

User = get_user_model()


class Lexique(models.Model):

    langue1 = models.CharField(max_length=20)
    langue2 = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"lexique {self.langue1} - {self.langue2}"

    def get_absolute_url(self):
        return reverse(f"{LexiqueConfig.name}:home", kwargs={"slug": self.slug})

    def get_add_url(self):
        return reverse(f"{LexiqueConfig.name}:add-lexon", kwargs={"slug": self.slug})

    def get_add_lexon_url(self):
        return reverse(f"{LexiqueConfig.name}:add-lexon", kwargs={"slug": self.slug})

    def get_add_lexon_confirmation_url(self):
        return reverse(
            f"{LexiqueConfig.name}:add-lexon-confirmation", kwargs={"slug": self.slug}
        )

    def get_list_lexon_url(self):
        return reverse(f"{LexiqueConfig.name}:list-lexon", kwargs={"slug": self.slug})

    def get_lexons_by(self, order_by: str = "mot1") -> QuerySet[Lexon]:
        try:
            return self.lexon_set.order_by(order_by)
        except FieldError:
            return self.lexon_set.order_by("mot1")

    def get_lexons(self, mot1: str, mot2: str):
        lookups = Q(mot1__iexact=mot1) | Q(mot2__iexact=mot2)
        return self.lexon_set.filter(lookups)

    def search_lexons(self, mot: str):
        lookups = (
            Q(mot1__contains=mot)
            | Q(mot2__icontains=mot)
            | Q(mot1__contains=mot)
            | Q(mot2__icontains=mot)
        )
        return self.lexon_set.filter(lookups)


def article_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.langue1}-{instance.langue2}")


pre_save.connect(article_pre_save, sender=Lexique)


class Lexon(models.Model):
    """DEfault lexon class"""

    mot1 = models.CharField(max_length=40)
    mot2 = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    lexique = models.ForeignKey(Lexique, on_delete=models.CASCADE)
    time_asked = models.PositiveIntegerField(default=0, blank=False)
    streak = models.SmallIntegerField(default=0, blank=False)

    def __str__(self) -> str:
        return f"{self.mot1}   -   {self.mot2}"

    def __repr__(self) -> str:
        return f"{self.mot1} {self.mot2}: [{self.time_asked}/{self.streak}]"

    def get_edit_url(self) -> str:
        return reverse(f"{LexiqueConfig.name}:edit-lexon", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse(f"{LexiqueConfig.name}:delete-lexon", kwargs={"id": self.id})

    def udpate_asked(self, success: bool):
        """on ajoute 1 à la série en cours si juste sinon on repart à zero"""
        self.time_asked += 1
        if success:
            self.streak = min(self.streak + 1, 3)
        else:
            self.streak = 0
        self.save()

    @staticmethod
    def choose_lexon(qs: QuerySet) -> Lexon:
        """tire au hasard un lexo en ponderant selon la streak"""
        res = []
        for streak, weight in zip(range(4), (7, 4, 2, 1)):
            try:
                res += list(set(random.choices(qs.filter(streak=streak), k=weight)))
            except IndexError:
                res += list(set(qs.filter(streak=streak)))
        print(res)
        return random.choice(res)
