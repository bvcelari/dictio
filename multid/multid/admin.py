from django.contrib import admin

from .models import Concept, ConceptEs,ConceptEn,ConceptFr,ConceptGe

from .models import  Category, SourceDocument


admin.site.register(ConceptEs)
admin.site.register(ConceptEn)
admin.site.register(ConceptFr)
admin.site.register(ConceptGe)
admin.site.register(Concept)
admin.site.register(Category)
admin.site.register(SourceDocument)
