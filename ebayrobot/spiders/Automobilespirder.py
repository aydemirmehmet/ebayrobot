import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy.spiders
from  ..items import EbayrobotItem





class  Automobilespirder(scrapy.Spider):
    name="ebay"
    allowed_domains = ["ebay-kleinanzeigen.de"]
    start_urls=['https://www.ebay-kleinanzeigen.de/s-autos/anbieter:privat/preis::3500/c216']

   

   
    def parse(self,response):
      #is-highlight
               for sel in  reversed(response.xpath('//ul[@id="srchrslt-adtable"]/li[ not(contains(@class,"is-highlight") ) and not(contains(@class,"is-topad"))]/article')):
            
                   item=EbayrobotItem()
                   try:
                       item["resim"]=""
                       item["link"]="https://www.ebay-kleinanzeigen.de"+' '.join(sel.css(".ellipsis::attr(href)").extract())
                       item["autoid"]=' '.join(sel.css(".ellipsis::attr(name)").extract())
                       item["fiyat"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./div[3]/strong/text()').extract())
                       item["km"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./div[2]/p[2]/span[1]/text()').extract())
                       item["marka"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./div[2]/h2/a/text()').extract())
                       item["modelyil"]=' '.join(a.strip().replace("'","") for a in sel.xpath('./div[2]/p[2]/span[2]/text()').extract())
                       trans_table = {ord(c): None for c in u'\r\n\t'}
                       item["sehir"]=' '.join(s.strip().translate(trans_table) for s in sel.xpath('./div[3]/text()').extract()) + ' '.join(s.strip().translate(trans_table) for s in sel.xpath('./div[4]/text()').extract())
                       item["telefon"]="-"
                       autoid=item["link"].split("/")[5].split("-")[0]
                       item["durum"]= item["link"].split("/")[5].split("-")[0]
                       item["siteId"]=1
                       if item["autoid"]!="":
                            item["autoid"]= float( item["autoid"])
                       else:
                            item["autoid"]=float(autoid)
                      
                   except IndexError:
                       item["autoid"]=float("0")
                        
                    
                   yield item 
                   yield scrapy.Request(response.url, meta={'dont_merge_cookies': True}, callback=self.parse, dont_filter=True)

