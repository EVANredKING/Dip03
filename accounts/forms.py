from django import forms
from .models import Nomenclature, LSI

class NomenclatureForm(forms.ModelForm):
    class Meta:
        model = Nomenclature
        fields = '__all__'

class LSIForm(forms.ModelForm):
    class Meta:
        model = LSI
        fields = '__all__'
