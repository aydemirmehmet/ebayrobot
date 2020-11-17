import scrapy
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from ebayrobot.spiders.Automobilespirder import Automobilespirder

process = CrawlerProcess(get_project_settings())
sched = TwistedScheduler()
sched.add_job(process.crawl, 'interval', args=[Automobilespirder], seconds=10)
sched.start()
process.start(False)
