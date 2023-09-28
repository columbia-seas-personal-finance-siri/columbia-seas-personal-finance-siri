import scrapy
#from websitescraper.items import nefeItem

class NefespiderSpider(scrapy.Spider):
    name = 'nefespider'
    allowed_domains = ['www.nefe.org']
    start_urls = ['http://www.nefe.org/research/polls/default.aspx#filter-all']

    def parse(self, response):
        references = response.css('div.col12')
        #nefe_item = nefeItem()

        for ref in references[1:-1]: #references[0] and references[-1] does not link to any article on the page 
            try: 
                yield {
                'title': ref.css('a h3::text').get(),
                'date': ref.css('.postDate::text').get(),
                'content' :  ref.css('.intro::text').get(),
                'link':  ref.css('a::attr(href)').get(default=''),
                'tags': ref.css('.postDate::text')[1].get().strip().split('/')  
                }
            except IndexError:
                print(f"Index is out of range.")