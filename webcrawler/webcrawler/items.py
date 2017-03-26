import scrapy
from scrapy.item import Item 

class StackItem(scrapy.Item):
    title = scrapy.Field()
    req_url = scrapy.Field()
    respond_url = scrapy.Field()
    login = scrapy.Field()
