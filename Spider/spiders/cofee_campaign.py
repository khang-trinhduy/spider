import scrapy

class CofeeCampaign(scrapy.Spider):
    start_urls = ['http://cafef.vn/du-an.chn']

    def parse(self, response):
        yield response.follow(response, self.parse_page)

    def parse_page(self, response):
        
        return