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

import HTMLParser


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
    new_values = {}
    if request.POST:
      form = ImportConcept(request.POST)
      print request.POST
      if form.is_valid():
        url = request.POST['url']
        kind = request.POST['kind']
        bullet = request.POST['bullet']
        document_id = url.split('CELEX:')[1]
        dict_tree = {}
        p = subprocess.Popen(["/home/adminuser/Fran2/dictio/wsdl_consumer/article2_parser.py -c "+document_id+" -s "+kind +" --bullet=\""+bullet+"\"" ],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print "EXECUTION"
        print ["/home/adminuser/Fran2/dictio/wsdl_consumer/article2_parser.py -c "+document_id+" -s "+kind +" --bullet=\""+bullet+"\"" ]
        out, err = p.communicate()
        print "OUT"
        print out
        print "ERR"
        print err
        dict_tree = eval(out)
        #print dict_tree['ES']
        values_es = dict_tree['ES'].copy()
        values_en = dict_tree['EN'].copy()
        values_fr = dict_tree['FR'].copy()
        values_de = dict_tree['DE'].copy()
	listed_bullets=sorted(values_es)
	#from 1 to 4 ES EN FR DE
	new_values = {}
        for key in listed_bullets:
          if bullet == 'letters':
            new_values[key]={}
            new_values[key]=[values_es[key],values_en[key],values_fr[key],values_de[key]]
          elif bullet == 'numbers':
            print "I am looing in key:"+key
            new_values[key]={}
            new_values[key]=[values_es[key],values_en[key],values_fr[key],values_de[key]]
            
        ##now we are going to put the keys in place... is horrible... but is fast TODO: sent to another place and get the file instead of re-download it.
	myrequest = request.POST.copy()
        del myrequest['url']
        del myrequest['kind']
        del myrequest['bullet']
        del myrequest['category']
        del myrequest['source']
        del myrequest['separator_en']
        del myrequest['separator_es']
        del myrequest['separator_fr']
        del myrequest['separator_de']
        del myrequest['csrfmiddlewaretoken']
        #has no sense.. but works
	if bool(myrequest):
	  #########################
	  ## We reprocessied the file.. change it!!
	  #########################
          separator_en = request.POST['separator_en']
          separator_es = request.POST['separator_es']
          separator_fr = request.POST['separator_fr']
          separator_de = request.POST['separator_de']
	  ##Get the category and document id 
	  ##answer must be only one otherwise will crash, and I will be happy about it
	  #current_category = Category.objects.filter(name__icontains=request.POST['category'])
	  current_category = request.POST['category']
	  #current_source = SourceDocument.objects.filter(name__icontains=request.POST['source'])
	  current_source = request.POST['source']
	  
	  for key,value in myrequest.iteritems():
            print value, key
            if myrequest[key] == 'Y':
	      #to add a new concept, first, creaate the father of all of them.
              h = HTMLParser.HTMLParser()
              #ToDo:Please, split and make it redeable.
              #from 1 to 4 ES EN FR DE
	      new_concept_es = ConceptEs(name_es=h.unescape(new_values[key][0].split(separator_es)[0]),
                    description_es=h.unescape(separator_es.join(new_values[key][0].split(separator_es)[1:])),
                    category_id=current_category, 
                    sourcedocument_id=current_source )
	      new_concept_en = ConceptEn(name_en=h.unescape(new_values[key][1].split(separator_en)[0]), 
                    description_en=h.unescape(separator_en.join(new_values[key][1].split(separator_en)[1:])),
                    category_id=current_category, 
                    sourcedocument_id=current_source )
	      new_concept_fr = ConceptFr(name_fr=h.unescape(new_values[key][2].split(separator_fr)[0]), 
                    description_fr=h.unescape(separator_fr.join(new_values[key][2].split(separator_fr)[1:])),
                    category_id=current_category,
                    sourcedocument_id=current_source )
	      new_concept_de = ConceptGe(name_ge=h.unescape(new_values[key][3].split(separator_de)[0]), 
                    description_ge=h.unescape(separator_de.join(new_values[key][3].split(separator_de)[1:])),
                    category_id=current_category, 
                    sourcedocument_id=current_source )
	      new_concept_es.save()
	      new_concept_en.save()
	      new_concept_fr.save()
	      new_concept_de.save()
              new_concept = Concept(name= h.unescape(new_values[key][0].split(separator_es)[0]),
			concept_es = new_concept_es,
			concept_en = new_concept_en,
			concept_fr = new_concept_fr,
			concept_ge = new_concept_de
		 )
              new_concept.save()
            elif myrequest[key] == 'D':
              print "We are sending to drafts"
	    else:
              print "we are reqjecting" 

	  #########################
	  #########################
	  #########################
	else:
	  print "first time"
        len(myrequest)
        

    return render(request, 'import.html', {'form':form,'values_es':values_es,'values_en':values_en,'dict_tree':dict_tree,'new_values':new_values})

@login_required(login_url='/login/')
def submit_date(request):
  pass

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
