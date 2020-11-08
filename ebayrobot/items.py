# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayrobotItem(scrapy.Item):
    autoid = scrapy.Field()
    resim=scrapy.Field()
    marka=scrapy.Field()
    link=scrapy.Field()
    modelyil=scrapy.Field()
    fiyat=scrapy.Field()
    km=scrapy.Field()
    sehir=scrapy.Field()
    telefon=scrapy.Field()
    durum=scrapy.Field()
    siteId=scrapy.Field()
