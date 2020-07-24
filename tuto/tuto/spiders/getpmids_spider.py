

import scrapy
from datetime import date, timedelta
import requests
import os.path
from os import path
import ndjson
from  json import dumps
from tuto.spiders.Modules.manager import Manager

class QuotesSpider(scrapy.Spider):
    name = "getpmids"
    start_urls = [ 'https://www.ncbi.nlm.nih.gov/research/coronavirus-api/feed/?filters=%7B%7D', ]

    def parse(self, response):
        today = date.today() - timedelta(days=1)
        today = today.strftime("%d %b %Y")
        url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        pmids = []

        if not os.path.exists('data'):
            os.makedirs('data')

        database_manager = Manager('data/data.db')

        for post in response.xpath('//channel/item'):
            if today in post.xpath('pubDate//text()').extract_first():
                pmids.append( post.xpath('link//text()').extract_first().split("/")[6])


        json ={"pmids": pmids }
        rep = requests.post(url, json=json)
        resp = rep.json(cls=ndjson.Decoder)

        for item in resp:
            database_manager.insert_articles_content( item["id"],item["passages"][0]["text"], item["passages"][1]["text"], dumps(item["authors"]))
