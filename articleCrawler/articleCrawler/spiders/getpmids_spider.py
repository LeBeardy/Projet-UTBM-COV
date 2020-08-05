

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

def get_pmids( response):
    pmids = []
    for post in response.xpath('//channel/item'):
        pmids.append( post.xpath('link//text()').extract_first().split("/")[6])
    return pmids

def create_url_to_pmcids(ids):
    url_ids = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids="
    convert_url = []
    for groupe in grouper(ids, 200):
        groupe = list(filter(None,list(groupe)))
        parameters=""
        for id in groupe:
            parameters = parameters + id +","
        parameters = parameters[:-1] + "&format=json"
        convert_url.append(url_ids + parameters)
    return convert_url

def get_pmcids( pmids):
    convert_url = create_url_to_pmcids(pmids)
    pmcids=[]
    for url in convert_url:
        resp = requests.get(url).json()
        for elem in resp["records"]:
            if "pmcid" in elem:
                pmcids.append(elem["pmcid"])
    return pmcids

def send_request(type, url, ids):
    json = {type: ids}
    req = requests.post(url, json=json)
    resp = req.json(cls=ndjson.Decoder)
    return resp

def get_full_articles(  ids, url, database_manager):
    for groupe  in grouper(ids, 1000):
        groupe = list(filter(None,list(groupe)))
        resp = send_request("pmcids",url, groupe)
        for article in resp:
            title=article["passages"][0]["text"]
            content=""
            for cont in article["passages"]:
                if cont["infons"]["section"] not in[ "References", "Conflicts of Interest"]:
                    content= content + cont["text"] + "\n"
            database_manager.complete_article(article["pmid"], article["pmcid"], content )


def get_abstract_articles(ids, url, database_manager):
    for groupe  in grouper(ids, 1000):
        groupe = list(filter(None,list(groupe)))
        resp = send_request("pmids",url, groupe)

        for article in resp:
            infons = article["passages"][0]["infons"]
            database_manager.insert_article(article["id"], "", article["passages"][0]["text"],
            article["passages"][1]["text"] if article["passages"][1]["text"] else "", "", dumps(article["authors"]),
            infons["journal"].split(";")[1].split(".")[0][:12] if "journal" in infons  else"",
            infons["journal"].split(";")[0] if "journal" in infons  else"")

class AticleItem(scrapy.Item):
    pmid = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    authors = scrapy.Field()

class ArticlesSpider(scrapy.Spider):
    name = "getpmids"
    start_urls = [ 'https://www.ncbi.nlm.nih.gov/research/coronavirus-api/feed/?filters=%7B%7D']

    def parse(self, response):
        url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        database_manager = Manager(os.getcwd() + '/data/database/data.db')
        pmids = get_pmids(response)

        if pmids:
            get_abstract_articles(pmids, url, database_manager)
            full_article = get_pmcids(pmids)
            get_full_articles( full_article, url,database_manager)
