import urllib2
from bs4 import BeautifulSoup

wiki = "https://www-is.biotoul.fr/search.php"
page = urllib2.urlopen(wiki)

soup = BeautifulSoup(page, "html.parser")

print soup.title

all_links = soup.find_all("a")

for link in all_links:
    print link