from articleCrawler.articleCrawler.spiders.getpmids_spider import ArticlesSpider

import scrapy
from scrapy.crawler import CrawlerProcess

class Manager:

  def __init__(self):
    # Punctuations and stopwords
    self.version = "1.0"


  def launch_spider(self):

      process = CrawlerProcess(settings={
          "FEEDS": {
              "items.json": {"format": "json"},
          },
      })

      process.crawl(ArticlesSpider)
      process.start() # the script will block here until the crawling is finished
