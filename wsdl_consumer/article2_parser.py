#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Prototype with: http://eur-lex.europa.eu/legal-content/ES/TXT/?qid=1416887080147&uri=CELEX:32014R0165
#input values 1.- "CELEX"
#input values 2.- "Start Article"
#input values 3.- "letters or numbers"
from subprocess import Popen
from subprocess import call
import xml.etree.ElementTree as ET
import sys,getopt
import os

#celex_id= "32014R0165"
#start_string= "article2"
#bullet  = "letters"


download_folder = '/home/adminuser/Fran2/dictio/wsdl_consumer/downloaded/'
executable_folder = '/home/adminuser/Fran2/dictio/wsdl_consumer/'

def remove_tags(text):
    ''.join(ET.fromstring(text).itertext())

import re
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def read_in_lines(file_object):
    """Lazy function (generator) to read a file line by line
    """
    while True:
        data = file_object.readline()
        if not data:
            break
        yield data

def get_articles_es(my_file,bullet_separator,bullet_starter,lang_header,lang_footer):
  articles = {}
  #my_file = read_in_lines(f_es)
  try:
    while True:
      line = next(my_file)
      if lang_header  in line:
        while True:
          line = next(my_file)
          if "a)" in line:
            while True:
              #print line
              if lang_footer not in line:
		my_line = striphtml(line)
		if my_line != '':
		  if bullet_separator in my_line:
                    articles[my_line.split(bullet_separator)[0].replace(" ", "")]=my_line.split(bullet_separator)[1]
                    #articles[my_line.split(bullet_separator)[0]]=my_line.split(bullet_separator)[1]
              else:
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles

def get_articles_en(my_file,bullet_separator,bullet_starter,lang_header,lang_footer):
  articles = {}
  #my_file = read_in_lines(f_es)
  try:
    while True:
      line = next(my_file)
      if lang_header  in line:
        while True:
          line = next(my_file)
          if "a)" in line:
            while True:
              #print line
              if lang_footer not in line:
                my_line = striphtml(line)
                if my_line != '':
                  if bullet_separator in my_line:
		    partial_current_bullet = my_line.split(bullet_separator)[0]
		    current_bullet = partial_current_bullet.split('(')[1]
                    #articles[my_line.split(bullet_separator)[0]]=my_line.split(bullet_separator)[1]
		    line = next(my_file)
		    #after the bullet, there is a empty line 
		    if not re.match(r'^\s*$', line):
		      line = next(my_file)
		      clean_definition = striphtml(line)
                      articles[current_bullet]=clean_definition
              else:
                #print "We reach the end of the article!!"
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles

def get_articles_fr(my_file,bullet_separator,bullet_starter,lang_header,lang_footer):
  articles = {}
  #my_file = read_in_lines(f_es)
  try:
    while True:
      line = next(my_file)
      if lang_header  in line:
        while True:
          line = next(my_file)
          if "a)" in line:
            while True:
              #print line
              if lang_footer not in line:
                my_line = striphtml(line)
                if my_line != '':
                  if bullet_separator in my_line:
                    partial_current_bullet = my_line.split(bullet_separator)[0]
                    current_bullet = partial_current_bullet.replace(" ","")
                    #articles[my_line.split(bullet_separator)[0]]=my_line.split(bullet_separator)[1]
                    line = next(my_file)
                    #after the bullet, there is a empty line 
                    if not re.match(r'^\s*$', line):
                      line = next(my_file)
                      clean_definition = striphtml(line)
                      articles[current_bullet]=clean_definition
              else:
                #print "We reach the end of the article!!"
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles

def get_articles_de(my_file,bullet_separator,bullet_starter,lang_header,lang_footer):
  articles = {}
  #my_file = read_in_lines(f_es)
  try:
    while True:
      line = next(my_file)
      if lang_header  in line:
        while True:
          line = next(my_file)
          if "a)" in line:
            while True:
              #print line
              if lang_footer not in line:
                my_line = striphtml(line)
                if my_line != '':
                  if bullet_separator in my_line:
                    partial_current_bullet = my_line.split(bullet_separator)[0]
                    current_bullet = partial_current_bullet.replace(" ","")
                    #articles[my_line.split(bullet_separator)[0]]=my_line.split(bullet_separator)[1]
                    line = next(my_file)
                    #after the bullet, there is a empty line 
                    if not re.match(r'^\s*$', line):
                      line = next(my_file)
                      clean_definition = striphtml(line)
                      articles[current_bullet]=clean_definition
              else:
                #print "We reach the end of the article!!"
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles


def main(argv):
  #print "we are in"
  celex_id = ''
  start_string = ''
  bullet = ''
  #helpstr = 'sincro_repo.py -s <report_source> -d <report_destination> |OPTIONAL --date <date_to_be_synced YYYY-MM-DD>'
  helpstr = 'article2_parser.py -c <celex_id> -s <start_string> -b <kind_of_bullet>'

  try:
     opts, args = getopt.getopt(argv,"hc:s:b",["celex_id=","string=","bullet="])
  except getopt.GetoptError:
     print helpstr
     sys.exit(2)
  for opt, arg in opts:
     if opt in ("-c", "--celex_id"):
        celex_id = arg
     if opt in ("-s", "--string"):
        start_string = arg
     if opt in ("-b", "--bullet"):
        bullet = arg

  if len(opts) < 3:
       print helpstr
       sys.exit()

  #go to "article 2" "definition", or any other input provided.(have fun with the translations and html)
  #ES: Art&iacute;culo 2 Definiciones
  #EN: Article 2 Definitions
  #FR: Article 2 Définitions
  #DE: Artikel 2 Begriffsbestimmungen
  if start_string  == "article1":
    lang_list_article = {
    "ES":">Art&iacute;culo 1<",
    "EN":">Article 1<",
    "FR":">Article 1<",
    "DE":">Artikel 1<"
    }
  elif start_string  == "article2":
    lang_list_article = {
    "ES":">Art&iacute;culo 2<",
    "EN":">Article 2<",
    "FR":">Article 2<",
    "DE":">Artikel 2<"
    }
  elif start_string  == "article3":
    lang_list_article = {
    "ES":">Art&iacute;culo 3<",
    "EN":">Article 3<",
    "FR":">Article 3<",
    "DE":">Artikel 3<"
    }

  #Download the document for each language,
  #TODO:DOwnload the files, remove comments from here!!!
  #for i in lang_list_article:
  #  import urllib
  #  url="http://eur-lex.europa.eu/legal-content/"+i+"/TXT/HTML/?uri=CELEX:"+celex_id+"&from=ES"
  #  urllib.urlretrieve(url, filename=download_folder+celex_id+"."+i+".txt")

  #now we are going to open all of them
  f_es = open(download_folder+''+celex_id+'.ES'+'.txt','r')
  f_en = open(download_folder+''+celex_id+'.EN'+'.txt','r')
  f_de = open(download_folder+''+celex_id+'.DE'+'.txt','r')
  f_fr = open(download_folder+''+celex_id+'.FR'+'.txt','r')
  
  #Process bullet, letters, means a) , b) ...
  if bullet == "letters":
    bullet_separator = ')'
    bullet_starter = 'a)'
  elif bullet == "numbers":
    bullet_separator = ')'
    bullet_starter = '1)'


  #go to "article 2" "definition", or any other input provided.(have fun with the translations and html)
  #ES: Art&iacute;culo 2 Definiciones
  #EN: Article 2 Definitions
  #FR: Article 2 Définitions
  #DE: Artikel 2 Begriffsbestimmungen
  ### Should be homogeinized if there is no corner cases with articles headers
  if start_string  == "article1":
    lang_list_article = {
    "ES":">Art&iacute;culo 1<",
    "EN":">Article 1<",
    "FR":">Article 1<",
    "DE":">Artikel 1<"
    }
    lang_list_footer = {
    "ES":">Art&iacute;culo 2<",
    "EN":">Article 2<",
    "FR":">Article 2<",
    "DE":">Artikel 2<"
    }

  elif start_string  == "article2":
    lang_list_article = {
    "ES":">Art&iacute;culo 2<",
    "EN":">Article 2<",
    "FR":">Article 2<",
    "DE":">Artikel 2<"
    }
    lang_list_footer = {
    "ES":">Art&iacute;culo 3<",
    "EN":">Article 3<",
    "FR":">Article 3<",
    "DE":">Artikel 3<"
    }

  elif start_string  == "article3":
    lang_list_article = {
    "ES":">Art&iacute;culo 3<",
    "EN":">Article 3<",
    "FR":">Article 3<",
    "DE":">Artikel 3<"
    }
    lang_list_footer = {
    "ES":">Art&iacute;culo 4<",
    "EN":">Article 4<",
    "FR":">Article 4<",
    "DE":">Artikel 4<"
    }

 
  my_file_es = read_in_lines(f_es)
  my_file_en = read_in_lines(f_en)
  my_file_fr = read_in_lines(f_fr)
  my_file_de = read_in_lines(f_de)
  articles_es = get_articles_es(my_file_es,bullet_separator,bullet_starter,lang_list_article['ES'],lang_list_footer['ES'])
  articles_en = get_articles_en(my_file_en,bullet_separator,bullet_starter,lang_list_article['EN'],lang_list_footer['EN'])
  articles_fr = get_articles_fr(my_file_fr,bullet_separator,bullet_starter,lang_list_article['FR'],lang_list_footer['FR'])
  articles_de = get_articles_de(my_file_de,bullet_separator,bullet_starter,lang_list_article['DE'],lang_list_footer['DE'])
  #I am Sure that there is 100 ways betters to do it... 
  print " {'ES':  "
  print articles_es
  print "  ,'EN': "
  print articles_en
  print "  ,'FR': "
  print articles_fr
  print "  ,'DE': "
  print articles_de
  print "  } "

    
  #go throw articles number (or letter!!) 


  #Close files
  f_es.close()
  f_en.close()
  f_de.close()
  f_fr.close()
if __name__ == "__main__":
   main(sys.argv[1:])

