import urllib2
from bs4 import BeautifulSoup

wiki = "https://www-is.biotoul.fr/search.php"
page = urllib2.urlopen(wiki)

soup = BeautifulSoup(page)

print soup.prettify()