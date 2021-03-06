import re
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from hse.items import PostItem

campus_pattern = re.compile(r'\w+(?=\.hse)')
campus_dict = {'nnov': 'Нижний Новгород', 'spb': 'Санкт-Петербург', 'perm': 'Пермь'}


class HSESpider(CrawlSpider):
    name = 'hse'
    allowed_domains = ['hse.ru']
    start_urls = [
        'https://www.hse.ru/news/admission/page1.html',
        'https://www.hse.ru/news/edu/page1.html',
        'https://www.hse.ru/news/science/page1.html',
        'https://www.hse.ru/news/expertise/page1.html',
        'https://www.hse.ru/news/community/page1.html',
        'https://www.hse.ru/news/communication/page1.html',
        'https://www.hse.ru/news/life/page1.html',
    ]

    rules = [Rule(LinkExtractor(allow=(r'/page[0-9]{1,4}',)), callback='parse', follow=True)]

    def parse(self, response):
        posts = response.css('[class="posts posts_general"] [class^="post "]')

        for post in posts:
            loader = ItemLoader(item=PostItem(), selector=post)
            loader.add_css('title', 'h2 a')
            loader.add_css('description', '.post__text p:nth-child(2)')
            loader.add_css('date', '.post-meta__date')
            loader.add_css('section', '.tag-set a[class*="rubric rubric_"] span::text')
            loader.add_css('tags', '.tag-set a.tag::text')
            loader.add_value('parent_link', response.url)
            post_item = loader.load_item()

            post_url = post.css(r'.first_child a::attr(href)').get()

            yield response.follow(post_url, callback=self.parse_post, meta={'post_item': post_item})

    def parse_post(self, response):
        post_item = response.meta['post_item']

        loader = ItemLoader(item=post_item, response=response)
        loader.add_value('visit_ts', datetime.now())
        loader.add_css('text', '.post__text')
        # loader.add_css('sections', '.articleMetaItem__content a[class*="rubric rubric_"] span::text')
        # loader.add_css('tags', '.articleMetaItem__content a.tag::text')
        loader.add_css('people', '.articleMetaItem__content div.b-peoples span::text')
        loader.add_css('branches', '.articleMetaItem__content span.small a')

        loader.add_value('link', response.url)
        # loader.add_value('parent_link', response.request.headers.get('Referer'))

        campus = campus_pattern.search(response.url).group()
        loader.add_value('campus', campus_dict.get(campus, 'Москва'))

        yield loader.load_item()
