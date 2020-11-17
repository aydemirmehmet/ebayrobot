# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EbayrobotPipeline:
    collection_name = "EbayListe"
  
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
      
       
    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
            
          
        )
    
    def open_spider(self, spider):
        
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #self.db.create_collection(
        #    'EbayListe', 
         #    capped=True, 
          #    size=50000, 
          #   max=50)

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        exists = self.db['EbayTable'].find_one({"autoid": dict(item)["autoid"]})
        if not exists:
            self.db['EbayTable'].insert_one(dict(item))
        return item
        
