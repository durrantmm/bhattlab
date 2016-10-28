
import urllib, urllib2
from bs4 import BeautifulSoup

isfinder_url = "https://www-is.biotoul.fr/search.php"
values = {'tout' : 'bacteroides'}

data = urllib.urlencode(values)
req = urllib2.Request(isfinder_url, data)
response = urllib2.urlopen(req)
the_page = response.read()
the_url  = response.geturl()


print the_url
soup = BeautifulSoup(the_page, "html.parser")

all_links = soup.find_all("a")
for link in all_links:
    print link