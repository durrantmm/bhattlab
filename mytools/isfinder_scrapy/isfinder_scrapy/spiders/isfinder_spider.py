import scrapy


class QuotesSpider(scrapy.Spider):
    name = "isfinder"

    def start_requests(self):
        genera_file = "/home/mdurrant/my_code_bhatt/mytools/bacterial_genera_small.tsv"
        isfinder_url = "https://www-is.biotoul.fr/search.php"

        search_queries = []
        with open(genera_file, 'r') as infile:
            search_queries = [line.strip() for line in infile]

        for query in search_queries:
            yield scrapy.FormRequest(url=isfinder_url, formdata={'tout': query})


    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'isfinder_results-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)