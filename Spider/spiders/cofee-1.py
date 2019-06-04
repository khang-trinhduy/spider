import scrapy
import re

class CofeeSpider(scrapy.Spider):
    name = 'cofee1'
    start_urls = [
        # 'http://cafef.vn/timeline/31/trang-1.chn', 
        # 'http://cafef.vn/timeline/112/trang-1.chn',
        # 'http://cafef.vn/timeline/35/trang-1.chn',
        'http://cafef.vn/timeline/36/trang-301.chn',
        'http://cafef.vn/timeline/34/trang-301.chn',
        'http://cafef.vn/timeline/32/trang-301.chn',
        # 'http://cafef.vn/timeline/33/trang-1.chn',
        # 'http://cafef.vn/timeline/114/trang-1.chn',
        # 'http://cafef.vn/timeline/39/trang-1.chn',
    ]
    
    def next(self, url):
        current = re.findall(r'[a-z]+-[0-9]+', url)[0]
        if current is not None:
            page = int(current.split('-')[1]) + 1
            return (url.replace(current, current.split('-')[0] + '-' + str(page)), page)

    def exceed_page_number(self, depth, page):
        return page > depth

    def parse(self, response):
        yield response.follow(response.request.url, self.parse_page)

    def parse_page(self, response, depth=350):
        articles = response.css('.tlitem a::attr(href)').getall()
        next_page, page_number = self.next(response.request.url)
        for a in articles:
            yield response.follow(a, self.parse_contents)
        if self.exceed_page_number(depth, page_number):
            return
        if next_page is not None:
            yield response.follow(next_page, self.parse_page)

    def parse_contents(self, response):
        contents = {}
        contents['title'] = [x.replace('\r\n', '').strip() for x in response.css(".left_cate .title::text").getall()]
        contents['contents'] = response.css(".contentdetail p::text").getall()
        contents['author'] = response.css(".contentdetail .author::text").getall()
        contents['source'] = response.css(".contentdetail .source::text").getall()
        return contents
    # .listchungkhoannew li .knswli h3 a title/href
    #  #listNewhead ul li a title/href

    # ck: http://cafef.vn/timeline/31/trang-1.chn
    # ts: http://cafef.vn/timeline/112/trang-2.chn
    # bds: http://cafef.vn/timeline/35/trang-2.chn
    # dn: http://cafef.vn/timeline/36/trang-2.chn
    # nh: http://cafef.vn/timeline/34/trang-2.chn
    # tcqt: http://cafef.vn/timeline/32/trang-2.chn
    # vm: http://cafef.vn/timeline/33/trang-2.chn
    # s: http://cafef.vn/timeline/114/trang-2.chn
    # tt: http://cafef.vn/timeline/39/trang-2.chn
    # da: http://cafef.vn/du-an.chn (different)

    #contents:
    '''
    title: .left_cate .title
    contents: .contentdetail p
    author: .contentdetail .author
    source: .contentdetaul .source
    '''
