from django import forms


class QuizzForm(forms.Form):
    score = forms.IntegerField()
    total = forms.IntegerField()
    reponse = forms.CharField()
    question = forms.CharField()
    guess = forms.CharField()
    langue_q = forms.CharField()
    langue_r = forms.CharField()
    try_index = forms.IntegerField()
    go_next = forms.BooleanField()
