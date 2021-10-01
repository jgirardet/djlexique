from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Lexique(models.Model):

    langue1 = models.CharField(max_length=20)
    langue2 = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"lexique {self.langue1} - {self.langue2}"

    def get_absolute_url(self):
        return reverse("lexique-home", kwargs={"slug": self.slug})

    def get_add_url(self):
        return reverse("lexique-add", kwargs={"slug": self.slug})

    def get_list_url(self):
        return reverse("lexique-list", kwargs={"slug": self.slug})

    def langue1_alpha_list(self) -> QuerySet:
        return self.lexon_set.order_by("mot1")

    def langue2_alpha_list(self) -> QuerySet:
        return self.lexon_set.order_by("mot2")

    def get_lexons(self, mot1:str, mot2:str):
        lookups = Q(mot1__iexact=mot1) | Q(mot2__iexact=mot2)
        return self.lexon_set.filter(lookups)


def article_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.langue1}-{instance.langue2}")


pre_save.connect(article_pre_save, sender=Lexique)


class Lexon(models.Model):
    mot1 = models.CharField(max_length=40)
    mot2 = models.CharField(max_length=40)
    created = models.DateField(auto_now_add=True)
    lexique = models.ForeignKey(Lexique, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.mot1}   -   {self.mot2}"

    def get_edit_url(self) -> str:
        return reverse("lexon-edit", kwargs={"id": self.id})
