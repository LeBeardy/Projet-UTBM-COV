import scrapy
import json
from json import dumps
from xml.etree import ElementTree
from datetime import date, timedelta
import requests
import os.path
from os import path

class QuotesSpider(scrapy.Spider):
    name = "getpmids"
    start_urls = [
        'https://www.ncbi.nlm.nih.gov/research/coronavirus-api/feed/?filters=%7B%7D',
    ]

    def parse(self, response):
        today = date.today() - timedelta(days=1)
        today = today.strftime("%d %b %Y")
        url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        pmids = []

        for post in response.xpath('//channel/item'):
            if today in post.xpath('pubDate//text()').extract_first():
                pmids.append( post.xpath('link//text()').extract_first().split("/")[6])


        json ={"pmids": pmids }
        path_to_data =  os.getcwd() +"\\data"
        rep = requests.post(url, json=json)

        filename = '\\pdm_'+today+'.jl'
        option = 'wb'
        print(path_to_data)
        if path.exists(path_to_data+filename) :
            option = 'a'

        with open(path_to_data+filename, option) as f:
            f.write(rep.text)

        filename = '\\pdm_pmids_'+today+'.jl'
        option = 'wb'

        if not os.path.exists('data'):
            os.makedirs('data')

        if path.exists(path_to_data+filename) :
            option = 'a'

        with open(path_to_data+filename, option) as f:
            f.write(dumps(json))
