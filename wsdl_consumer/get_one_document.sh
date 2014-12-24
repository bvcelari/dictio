#$1 id
#$2 Lang, ES,EN,GE,FR
wget -O $1.$2.txt  http://eur-lex.europa.eu/legal-content/$2/TXT/HTML/?uri=CELEX:$1&from=ES 
