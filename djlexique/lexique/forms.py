from django import forms
from .models import Lexon, Lexique


class LexonForm(forms.ModelForm):
    class Meta:
        model = Lexon
        fields = ["mot1", "mot2"]


class LexiqueForm(forms.ModelForm):
    class Meta:
        model = Lexique
        fields = ["langue1", "langue2"]
