from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import Http404
from multid.models import ConceptEs,ConceptEn,ConceptFr,ConceptGe
from multid.models import Concept

from multid.models import Category,SourceDocument
from multid.forms import ConceptSearchFormEN
from multid.forms import ConceptSearchFormES
from multid.forms import ConceptSearchFormFR
from multid.forms import ConceptSearchFormGE
from multid.forms import ImportConcept

import subprocess
import ast


query_limit = 5
#TODO: refactor search adding the language in the parameter and use it to call the right template...



@login_required(login_url='/login/')
def import_concepts(request):
    form = ImportConcept()
    values_es = {} 
    values_en = {} 
    values_fr = {} 
    values_de = {} 
    dict_tree = {} 
    output_values=[]
    new_values = {}
    if request.POST:
      form = ImportConcept(request.POST)
      if form.is_valid():
        print "we have a valid "
        url = request.POST['url']
        kind = request.POST['kind']
        bullet = request.POST['bullet']
        document_id = url.split('CELEX:')[1]
        dict_tree = {}
        p = subprocess.Popen(["/home/adminuser/Fran2/dictio/wsdl_consumer/article2_parser.py -c "+document_id+" -s "+kind +" --bullet=\""+bullet+"\"" ],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        #print out
        dict_tree = eval(out)
        #print dict_tree['ES']
        values_es = dict_tree['ES'].copy()
        values_en = dict_tree['EN'].copy()
        values_fr = dict_tree['FR'].copy()
        values_de = dict_tree['DE'].copy()
        #for key in output_values_es:
        #  print key, 'corresponds to', output_values_es[key]
        #  print key, 'corresponds to', output_values_en[key]
	listed_bullets=sorted(values_es)
	#from 1 to 4 ES EN FR DE
        output_values=[[]]
	new_values = {}
        for key in listed_bullets:
          new_values[key]={}
          new_values[key]=[values_es[key],values_en[key],values_fr[key],values_de[key]]
          #output_values[1].append(values_es[key])
          #output_values[2].append(values_en[key])
          #output_values[3].append(values_fr[key])
          #output_values[4].append(values_de[key])
        for i in new_values:
	  print i 
	  print new_values[i]
    return render(request, 'import.html', {'form':form,'values_es':values_es,'values_en':values_en,'dict_tree':dict_tree,'output_values':output_values,'new_values':new_values})

def searchen(request):
    search_param = ""
    parent = ""
    definition = ""
    full_result = []
    if request.POST:
      form = ConceptSearchFormEN(request.POST)
      if form.is_valid():
        #do your search here
        search_param = request.POST['concept_search']
	#TODO:refactor to remove spaces
	definition = ConceptEn.objects.filter(name_en__icontains=search_param)[:query_limit]

	if definition:
  	  #print "EN: id "+  str(definition[0].id)
	  #print "EN: name "+ str(definition[0].name_en)
	  #print "EN: description "+ str(definition[0].description_en)
          for i in definition:
	    #look for this concept in the parent Concepts
            #could be a concept that has no parent...
	    parent = Concept.objects.get(concept_en__id=i.id)
	    if parent:
	      full_result.append(parent)
	    #print "who is your daddy " +str (parent.id)
	    #print "who is your daddy EN " +str (parent.concept_en.id)
    else:
        form = ConceptSearchFormEN()

    concepts = zip(full_result,definition)
    return render(request, 'search_en.html', {'form': form,'definition':definition,'search_param':search_param,'parent':parent,'concepts':concepts})

def searchge(request):
    search_param = ""
    parent = ""
    definition = ""
    full_result = []
    if request.POST:
      form = ConceptSearchFormGE(request.POST)
      if form.is_valid():
        #do your search here
        search_param = request.POST['concept_search']
        definition = ConceptGe.objects.filter(name_ge__icontains=search_param)[:query_limit]
        if definition:
          for i in definition:
            #look for this concept in the parent Concepts
            parent = Concept.objects.get(concept_ge__id=i.id)
            full_result.append(parent)
    else:
        form = ConceptSearchFormGE()

    concepts = zip(full_result,definition)
    return render(request, 'search_ge.html', {'form': form,'definition':definition,'search_param':search_param,'parent':parent,'concepts':concepts})

def searchfr(request):
    search_param = ""
    parent = ""
    definition = ""
    full_result = []
    if request.POST:
      form = ConceptSearchFormFR(request.POST)
      if form.is_valid():
        #do your search here
        search_param = request.POST['concept_search']
        definition = ConceptFr.objects.filter(name_fr__icontains=search_param)[:query_limit]
        if definition:
          for i in definition:
            #look for this concept in the parent Concept
	    try:
              parent = Concept.objects.get(concept_fr__id=i.id)
              full_result.append(parent)
	    except:
	      parent = ""
	      full_result.append(parent)
    else:
        form = ConceptSearchFormFR()

    concepts = zip(full_result,definition)
    return render(request, 'search_fr.html', {'form': form,'definition':definition,'search_param':search_param,'parent':parent,'concepts':concepts})

def searches(request):
    search_param = ""
    parent = ""
    definition = ""
    full_result = []
    if request.POST:
      form = ConceptSearchFormES(request.POST)
      if form.is_valid():
        #do your search here
        search_param = request.POST['concept_search']
        definition = ConceptEs.objects.filter(name_es__icontains=search_param)[:query_limit]
        if definition:
          for i in definition:
            #look for this concept in the parent Concepts
            parent = Concept.objects.get(concept_es__id=i.id)
            full_result.append(parent)
    else:
        form = ConceptSearchFormES()

    concepts = zip(full_result,definition)
    return render(request, 'search_es.html', {'form': form,'definition':definition,'search_param':search_param,'parent':parent,'concepts':concepts})

def compositeconcept(concept_id):
    resultset = Concept.objects.get(pk=concept_id)
    return resultset


def definition(request,lang_id,concept_id):
    try:
      resultset = Concept.objects.get(pk=concept_id)
      concept_requested = eval('resultset.concept_'+lang_id)
      if concept_requested:
        return render_to_response('show_definition_'+lang_id+'.html', {'concept': concept_requested,})
      else:
        raise Http404
    except:
      raise Http404
