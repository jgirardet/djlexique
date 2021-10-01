from django import forms
from .models import Lexon


class LexonForm(forms.ModelForm):
    class Meta:
        model = Lexon
        fields = ["mot1", "mot2"]
