import scrapy
import io
import re


class VnexpSpider(scrapy.Spider):
    name = 'vne'
    start_urls = ['https://vnexpress.vn', ]
    skip_domains = ['video', 'cuoi', 'tam-su', 'y-kien', 'khoa-hoc', 'du-lich',
     'doi-song', 'suc-khoe', 'giao-duc', 
     'phap-luat', 'the-thao', 'giai-tri',
     'so-hoa', 'oto-xe-may', 'kinh-doanh',
     'thoi-su', 'giao-duc']
    title = ['.sidebar_1 header + h1::text']
    date = ['.sidebar_1 header span::text']
    description = ['.sidebar_1 .description::text']
    contents = ['.sidebar_1 article .Normal::text',]
    author = ['.sidebar_1 article .Normal strong::text']
    source = ['.sidebar_1 article p em::text']

    def exceed_page_limit(self, depth, current_page):
        page_number = re.findall(r'[p][0-9]+', current_page)[0]
        return depth < int(page_number[1:])

    def parse(self, response):
        for href in response.css('nav.p_menu a::attr(href)'):
            yield response.follow(href, self.parse_category)

    def parse_category(self, response, depth=1000000):
        for domain in self.skip_domains:
            if domain in response.url:
                return

        articles = response.css(
            '.sidebar_1 article h4 a:first-child::attr(href)').getall()
        main_article = response.css(
            '.featured article .title_news a:first-child::attr(href)').get()
        next_page = response.css(
            '#pagination .active + a::attr(href)')[0].get()

        for a in articles:
            yield response.follow(a, self.parse_content)
        if main_article != None:
            yield response.follow(main_article, self.parse_content)
        if not self.exceed_page_limit(depth, next_page):
            yield response.follow(next_page, self.parse_category)

    def parse_subcategory(self, response):
        for href in response.css('h3 a::attr(href'):
            yield {
                'href': href.get(),
            }

    def parse_content(self, response):
        contents = {}
        contents['author'] = [response.css(x).getall() for x in self.author]
        contents['description'] = [response.css(x).getall() for x in self.description]
        contents['contents'] = [response.css(x).getall() for x in self.contents]
        contents['date'] = [response.css(x).getall() for x in self.date]
        contents['title'] = [response.css(x).getall() for x in self.title]
        contents['source'] = [response.css(x).getall() for x in self.source]
        yield contents

    # article h1/h4.title_news a::atr(title/href)
    # hgroup h2 a
    #   h3 a
    # [content, author, date, title, description]

    # header: .sidebar_1 header + h1::text
    # date: .sidebar_1 header span::text
    # description: .sidebar_1 .description::text
    # content: .sidebar_1 article .Normal::text
    # content: .sidebar_1 article p::text
    # author: .sidebar_1 article .Normal strong::text
    # source: .sidebar_1 article p em::text.getall
