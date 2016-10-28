import urllib, urllib2
from bs4 import BeautifulSoup
import mechanize
import sys, os
import argparse




def main(args):
    page = submit_search(args['search_query'], args['search_field'], args['isfinder_search_url'])

    IS_links = get_IS_links(BeautifulSoup(page, 'lxml'))

    for link in IS_links:
        r = urllib.urlopen(args['search_result_prefix_url'] + link).read()
        soup = BeautifulSoup(r, 'lxml')
        print soup.find_all("div", {"id": "seq_ident"})
        break






def get_IS_links(soup):
    all_links = soup.find_all("a")
    links = []
    for link in all_links:
        href = link.get("href")
        if "ficheIS" in href:
            links.append(href)
    return links


def submit_search(search_query, search_field, isfinder_url):
    br = mechanize.Browser()
    br.open(isfinder_url)
    br.select_form("search")
    br[search_field] = search_query
    response = br.submit()

    return response.read()




if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('search_query', help='The ISFinder search query of interest.')

    parser.add_argument('--search_field', required=False, type=str,
                        default="host",
                        help='The url of the ISFinder Website')

    parser.add_argument('--isfinder_search_url', required=False, type=str,
                        default="https://www-is.biotoul.fr/search.php",
                        help='The url of the ISFinder Website')

    parser.add_argument('--search_result_prefix_url', required=False, type=str,
                        default="https://www-is.biotoul.fr/scripts/",
                        help='The url of the ISFinder results pages.')

    parser.add_argument('--output_dir', required=False, type=str,
                        default= os.path.join(current_dir, "output"),
                        help='The output directory for the results')

    args = parser.parse_args()
    args = vars(args)

    main(args)