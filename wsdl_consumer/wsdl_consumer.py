import urllib2
f = "".join(open('case2', 'r'))
r = urllib2.Request("http://eur-lex.europa.eu/EURLexWebService", f ,
                     headers={'Content-Type': 'application/soap+xml;charset="utf-8"'})
u = urllib2.urlopen(r)
response = u.read()
print response
