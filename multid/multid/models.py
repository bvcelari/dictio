from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)
    name_ge = models.CharField(max_length=200)
    name_es = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    others = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True)
    def __unicode__(self):
      return self.name

class SourceDocument(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)
    name_ge = models.CharField(max_length=200)
    name_es = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    others = models.IntegerField(default=0)
    def __unicode__(self):
      return self.name

class ConceptEn(models.Model):
    name_en = models.CharField(max_length=150,blank=True)
    description_en = models.TextField(blank=True)
    cheked = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    sourcedocument = models.ForeignKey(SourceDocument)
    added = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name_en


class ConceptGe(models.Model):
    name_ge = models.CharField(max_length=150,blank=True)
    description_ge = models.TextField(blank=True)
    cheked = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    sourcedocument = models.ForeignKey(SourceDocument)
    added = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name_ge

class ConceptFr(models.Model):
    name_fr = models.CharField(max_length=150,blank=True)
    description_fr = models.TextField(blank=True)
    cheked = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    sourcedocument = models.ForeignKey(SourceDocument)
    added = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name_fr

class ConceptEs(models.Model):
    name_es = models.CharField(max_length=150,blank=True)
    description_es = models.TextField(blank=True)
    cheked = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    sourcedocument = models.ForeignKey(SourceDocument)
    added = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name_es


class Concept(models.Model):
    name = models.CharField(max_length=150,blank=True)
    concept_en = models.ForeignKey(ConceptEn,blank=True, null=True)
    concept_es = models.ForeignKey(ConceptEs,blank=True, null=True)
    concept_fr = models.ForeignKey(ConceptFr,blank=True, null=True)
    concept_ge = models.ForeignKey(ConceptGe,blank=True, null=True)
    def __unicode__(self):
        return self.name

