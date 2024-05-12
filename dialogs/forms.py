from django import forms
from .models import Dialog, Query


class DialogCreateForm(forms.ModelForm):
    class Meta:
        model = Dialog
        fields = "__all__"


class QueryCreateForm(forms.ModelForm):
    dialog = forms.ModelChoiceField(
        queryset=Dialog.objects.all(), widget=forms.HiddenInput()
    )

    class Meta:
        model = Query
        fields = (
            "req",
            "dialog",
        )
