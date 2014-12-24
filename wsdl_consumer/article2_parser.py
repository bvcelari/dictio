#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Prototype with: http://eur-lex.europa.eu/legal-content/ES/TXT/?qid=1416887080147&uri=CELEX:32014R0165
#input values 1.- "CELEX"
#input values 2.- "Start Article"
#input values 3.- "letters or numbers"
from subprocess import Popen
import xml.etree.ElementTree as ET
import sys,getopt
import os

print sys.argv
lang_list_article2 = {
"ES":">Art&iacute;culo 2<",
"EN":">Article 2<",
"FR":">Article 2<",
"DE":">Artikel 2<" 
}
lang_list_article3 = {
"ES":">Art&iacute;culo 3<",
"EN":">Article 3<",
"FR":">Article 3<",
"DE":">Artikel 3<"
}

#debugg
celex_id= "32014R0165"
start_string= "article2"
bullet  = "letters"


download_folder = './downloaded/'
executable_folder = './'

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

def get_articles_es(my_file,bullet_separator,lang_header,lang_footer):
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
              else:
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles

def get_articles_en(my_file,bullet_separator,lang_header,lang_footer):
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
                print "We reach the end of the article!!"
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles

def get_articles_fr(my_file,bullet_separator,lang_header,lang_footer):
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
                    current_bullet = partial_current_bullet.replace(" ", "")
                    #articles[my_line.split(bullet_separator)[0]]=my_line.split(bullet_separator)[1]
                    line = next(my_file)
                    #after the bullet, there is a empty line 
                    if not re.match(r'^\s*$', line):
                      line = next(my_file)
                      clean_definition = striphtml(line)
                      articles[current_bullet]=clean_definition
              else:
                print "We reach the end of the article!!"
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles

def get_articles_de(my_file,bullet_separator,lang_header,lang_footer):
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
                    current_bullet = partial_current_bullet.replace(" ", "")
                    #articles[my_line.split(bullet_separator)[0]]=my_line.split(bullet_separator)[1]
                    line = next(my_file)
                    #after the bullet, there is a empty line 
                    if not re.match(r'^\s*$', line):
                      line = next(my_file)
                      clean_definition = striphtml(line)
                      articles[current_bullet]=clean_definition
              else:
                print "We reach the end of the article!!"
                raise StopIteration
              line = next(my_file)
  except StopIteration:
      pass
  finally:
      del my_file
  return articles


def main(argv):
  print "we are in"
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


  #Download the document for each language,
  for i in lang_list_article2:
    #TODO:DOwnload the files, remove comments from here!!!
    #p = Popen([executable_folder+"get_one_document_rc2.sh",download_folder , celex_id ,i])
    #p.communicate() #now wait
    #call([executable_folder+"get_one_document_rc2.sh",download_folder , celex_id ,i ])
    pass
    #TODO:wait till finish the download...  
  #now we are going to open all of them
  f_es = open(download_folder+''+celex_id+'.ES'+'.txt','r')
  f_en = open(download_folder+''+celex_id+'.EN'+'.txt','r')
  f_de = open(download_folder+''+celex_id+'.DE'+'.txt','r')
  f_fr = open(download_folder+''+celex_id+'.FR'+'.txt','r')
  
  #Process bullet, letters, means a) , b) ...
  if bullet == "letters":
    bullet_separator = ')'

  #go to "article 2" "definition", or any other input provided.(have fun with the translations and html)
  #ES: Art&iacute;culo 2 Definiciones
  #EN: Article 2 Definitions
  #FR: Article 2 Définitions
  #DE: Artikel 2 Begriffsbestimmungen
  if start_string  == "article2":
    print "we are in article 2 extraction method"
    #lines_es = f_es.readlines()
    #starting_line(lines_es,lang_list_article2['ES'])
  
  my_file_es = read_in_lines(f_es)
  my_file_en = read_in_lines(f_en)
  my_file_fr = read_in_lines(f_fr)
  my_file_de = read_in_lines(f_de)
  articles_es = get_articles_es(my_file_es,bullet_separator,lang_list_article2['ES'],lang_list_article3['ES'])
  articles_en = get_articles_en(my_file_en,bullet_separator,lang_list_article2['EN'],lang_list_article3['EN'])
  articles_fr = get_articles_fr(my_file_fr,bullet_separator,lang_list_article2['FR'],lang_list_article3['FR'])
  articles_de = get_articles_de(my_file_de,bullet_separator,lang_list_article2['DE'],lang_list_article3['DE'])
  print " ES "
  print articles_es
  print " EN "
  print articles_en
  print " FR "
  print articles_fr
  print " DE "
  print articles_de


    
  #go throw articles number (or letter!!) 


  #Close files
  f_es.close()
  f_en.close()
  f_de.close()
  f_fr.close()
if __name__ == "__main__":
   main(sys.argv[1:])

