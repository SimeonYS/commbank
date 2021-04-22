import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CcommbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class CcommbankSpider(scrapy.Spider):
	name = 'commbank'
	start_urls = ['https://www.commbank.com.au/newsroom.html?ei=CB-footer_newsroom']

	def parse(self, response):
		post_links = response.xpath('//h4/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="banner-content no-offer"]/p/text()').get()
		title = response.xpath('////div[@class="banner-content no-offer"]/h1/text()').get()
		content = response.xpath('//div[@class="cmp-text"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=CcommbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
