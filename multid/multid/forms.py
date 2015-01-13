from django import forms
from django.core.exceptions import ValidationError
from multid.models import ConceptEn
class ImportConcept(forms.Form):
    #url=#celex_id
    url=forms.URLField(required = True)	
    #kind#article2,  article1, article3
    kind = forms.ChoiceField(widget = forms.Select(), 
                     choices = ([('article1','article1'), ('article2','article2'),('article3','article3'), ]), initial='2', required = True,)
    #bullet #letters, numbers"letters" 
    bullet = forms.ChoiceField(widget = forms.Select(),
                     choices = ([('letters','letters'), ('numbers','numbers')]), initial='1', required = True,)
    

class ConceptSearchFormEN(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

class ConceptSearchFormES(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

class ConceptSearchFormFR(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

class ConceptSearchFormGE(forms.Form):
    concept_search = forms.CharField(label='Search', max_length=100)

