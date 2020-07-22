import scrapy
import json
from json import dumps
from xml.etree import ElementTree
from datetime import date
import requests


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.ncbi.nlm.nih.gov/research/coronavirus-api/feed/?filters=%7B%7D',
    ]

    def parse(self, response):
        today = date.today().strftime("%d %b %Y")
        url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        pmids = []

        for post in response.xpath('//channel/item'):
            if today in post.xpath('pubDate//text()').extract_first():
                #yield {
                #    'title' : post.xpath('title//text()').extract_first(),
                #    'link': post.xpath('link//text()').extract_first(),
                #    'pubDate' : post.xpath('pubDate//text()').extract_first(),
                #    'id' : post.xpath('link//text()').extract_first().split("/")[6],
                #}
                pmids.append( post.xpath('link//text()').extract_first().split("/")[6])


        json ={"pmids": pmids }

        rep = requests.post(url, json=json)

        filename = 'pdm.jl'
        with open(filename, 'wb') as f:
            f.write(str.encode(rep.text))

        filename = 'pdm_pmids.jl'
        with open(filename, 'wb') as f:
            f.write(str.encode(dumps(json)))
