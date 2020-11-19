import scrapy
from w3lib.html import replace_escape_chars
from twisted.internet import reactor
from twisted.internet.task import deferLater
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ..items import EbayrobotItem
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.twisted import TwistedScheduler

class  Automobilespirder(scrapy.Spider):
    name="ebay"
    allowed_domains = ["ebay-kleinanzeigen.de"]
    start_urls=['https://www.ebay-kleinanzeigen.de/s-autos/anbieter:privat/preis::3500/c216']

   
    def parse(self,response):
      
            for sel in  reversed(response.xpath('//ul[@id="srchrslt-adtable"]/li[ not(contains(.,"is-topad") )]')):
            
                item=EbayrobotItem()
                item["resim"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./article/div[@class="aditem-image"]/div[@class="imagebox srpimagebox"]/@data-imgsrc').extract())
                item["link"]="https://www.ebay-kleinanzeigen.de"+' '.join(a.strip().replace("'","") for a in sel.xpath('./article/div[2]/h2/a[@class="ellipsis"]/@href').extract())
                item["autoid"]=''.join(a.strip().replace("'","") for a in sel.xpath('./article/div[2]/h2/a[@class="ellipsis"]/@name').extract())
                item["fiyat"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./article/div[3]/strong/text()').extract())
                item["km"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./article/div[2]/p[2]/span[1]/text()').extract())
                item["marka"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./article/div[2]/h2/a/text()').extract())
                item["modelyil"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./article/div[2]/p[2]/span[2]/text()').extract())
                trans_table = {ord(c): None for c in u'\r\n\t'}
                item["sehir"]=' '.join(s.strip().translate(trans_table) for s in sel.xpath('./article/div[3]/text()').extract())
                item["telefon"]="-"
                item["durum"]="1"
                item["siteId"]=1
                
                yield item 


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)


process = CrawlerProcess(get_project_settings())


def _crawl(result, spider):
    deferred = process.crawl(spider)
    deferred.addCallback(lambda results: print('waiting 30 seconds before restart...'))
    deferred.addCallback(sleep, seconds=10)
    deferred.addCallback(_crawl, spider)
    return deferred


_crawl(None, Automobilespirder)
process.start()         




     


