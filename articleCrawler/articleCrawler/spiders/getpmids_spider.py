

import scrapy
from datetime import date, timedelta
import requests
import os
import ndjson
from  json import dumps
from Modules.data.manager import Manager
from json import loads
from itertools import islice
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class AticleItem(scrapy.Item):
    pmid = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    authors = scrapy.Field()

class ArticlesSpider(scrapy.Spider):
    name = "getpmids"
    start_urls = [ 'https://www.ncbi.nlm.nih.gov/research/coronavirus-api/feed/?filters=%7B%7D']

    def parse(self, response):

        today = (date.today() - timedelta(days=1)).strftime("%d %b %Y")
        url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        pmids = []
        print("fetch pour le jour : " + today)
        database_manager = Manager(os.getcwd() + '/data/database/data.db')

        for post in response.xpath('//channel/item'):
            if today in post.xpath('pubDate//text()').extract_first():
                pmids.append( post.xpath('link//text()').extract_first().split("/")[6])

        if pmids:
            for groupe in grouper(pmids, 1000) :
                print("groupe de taile :" + len(groupe))
                json ={"pmids": list(filter(None,list(groupe))) }
                rep = requests.post(url, json=json)
                resp = rep.json(cls=ndjson.Decoder)

                for item in resp:
                    database_manager.insert_articles_content( item["id"],item["passages"][0]["text"], item["passages"][1]["text"], dumps(item["authors"]))
                    print("article %s inseré" % item["id"])
            print ("Data successfully fetched", 201)
        else :
            print ("No data found on : \"https://www.ncbi.nlm.nih.gov/research/pubtator/index.html?view=docsum&query=$LitCovid\"", 404)
