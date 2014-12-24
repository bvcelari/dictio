from django import forms
from django.core.exceptions import ValidationError
from multid.models import ConceptEn

class ConceptSearchFormEN(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

class ConceptSearchFormES(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

class ConceptSearchFormFR(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

class ConceptSearchFormGE(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

