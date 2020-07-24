

import scrapy
from datetime import date, timedelta
import requests
import os.path
from os import path
import ndjson
from  json import dumps
from Modules.manager import Manager

def createFile( path_file, data):
    option = 'w'
    if path.exists(path_file) :
        option = 'a'

    with open(path_file, option) as f:
        f.write(data)

class QuotesSpider(scrapy.Spider):
    name = "getpmids"
    start_urls = [
        'https://www.ncbi.nlm.nih.gov/research/coronavirus-api/feed/?filters=%7B%7D',
    ]

    def parse(self, response):
        today = date.today() - timedelta(days=1)
        today = today.strftime("%d %b %Y")
        url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        path_to_data =  os.getcwd() +"\\data"
        filename_log = '\\log_'+today+'.jl'
        filename_data = '\\data_'+today+'.jl'
        pmids = []

        if not os.path.exists('data'):
            os.makedirs('data')

        #database_manager = Manager('data/wikiData.db')

        for post in response.xpath('//channel/item'):
            if today in post.xpath('pubDate//text()').extract_first():
                pmids.append( post.xpath('link//text()').extract_first().split("/")[6])


        json ={"pmids": pmids }
        rep = requests.post(url, json=json)
        resp = rep.json(cls=ndjson.Decoder)

        for item in resp:
            article ={"id": item["id"], "title": item["passages"][0]["text"], "text": item["passages"][1]["text"], "authors": item["authors"]}
            createFile(path_to_data+filename_data, dumps(article))


            #print(resp[0]["id"])
            #print(resp[0]["passages"][0]["text"])
            #print(resp[0]["passages"][1]["text"])
            #print(resp[0]["authors"])

            #print(item["passages"])
            #database_manager.insert_articles_content(item["id"],item["title"],item["content"])

        #createFile(path_to_data+filename_data, rep.text)
        #createFile(path_to_data+filename_log, dumps(json))
