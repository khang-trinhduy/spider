import scrapy
import re

class VnecoSpider(scrapy.Spider):
    name = 'vneco'
    start_urls = ['http://vneconomy.vn/timeline/9920/trang-1.htm', #thoi su
                    # 'http://vneconomy.vn/tai-chinh.htm', #http://vneconomy.vn/timeline/6/trang-1.htm
                    # 'http://vneconomy.vn/chung-khoan.htm',  #http://vneconomy.vn/timeline/7/trang-1.htm
                    # 'http://vneconomy.vn/doanh-nhan.htm', #http://vneconomy.vn/timeline/5/trang-1.htm
                    # 'http://vneconomy.vn/dia-oc.htm', #http://vneconomy.vn/timeline/17/trang-1.htm
                    # 'http://vneconomy.vn/thi-truong.htm',  #http://vneconomy.vn/timeline/19/trang-1.htm
                    # 'http://vneconomy.vn/the-gioi.htm',  #http://vneconomy.vn/timeline/99/trang-1.htm
                    # 'http://vneconomy.vn/cuoc-song-so.htm', #http://vneconomy.vn/timeline/16/trang-1.htm
                    # 'http://vneconomy.vn/xe-360.htm' #http://vneconomy.vn/timeline/23/trang-1.htm
    ]

    def parse(self, response):
        yield response.follow(response.request.url, self.parse_page)

    def next(self, url):
        current = re.findall(r'[a-z]+-[0-9]+', url)[0]
        if current is not None:
            page = int(current.split('-')[1]) + 1
            return (url.replace(current, current.split('-')[0] + '-' + str(page)), page)

    def exceed_page_number(self, depth, page):
        return page > depth

    def parse(self, response):
        yield response.follow(response.request.url, self.parse_page)

    def parse_page(self, response, depth=1600):
        articles = response.css('.infonews a::attr(href)').getall()
        next_page, page_number = self.next(response.request.url)
        for a in articles:
            yield response.follow(a, self.parse_contents)
        if self.exceed_page_number(depth, page_number):
            return
        if next_page is not None:
            yield response.follow(next_page, self.parse_page)

    def parse_contents(self, response):
        contents = {}
        contents['title'] = [x.replace('\r\n', '').strip() for x in response.css(".contentleft .title::text").getall()]
        contents['contents'] = response.css(".contentdetail p::text").getall()
        contents['author'] = response.css(".author .name a::text").getall()
        return contents

