

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

def get_pmids( datepub, response):
    print("-----------------------------------------------------")
    print("Récuperation des pmids depuis le rss de litcovid")
    print("-----------------------------------------------------")

    pmids = []
    for post in response.xpath('//channel/item'):
        if datepub in post.xpath('pubDate//text()').extract_first():
            pmids.append( post.xpath('link//text()').extract_first().split("/")[6])

    print("nombre de pmids recupere : %i" % len(pmids) )
    return pmids

def create_url_topmcids(pmids):
    print("-----------------------------------------------------")
    print("generation des urls de recuperation des pmcids")
    print("-----------------------------------------------------")

    url_pmcids = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids="
    convert_url = []
    for groupe in grouper(pmids, 200):
        groupe = list(filter(None,list(groupe)))
        print("division en groupe de %i" % len(groupe))
        parameters=""
        for pmid in groupe:
            parameters = parameters + pmid +","
        parameters = parameters[:-1] + "&format=json"
        convert_url.append(url_pmcids + parameters)

    print( "%i appels a l'api gouv" % len(convert_url))
    return convert_url

def get_pmcids( pmids):
    convert_url = create_url_topmcids(pmids)

    print("-----------------------------------------------------")
    print("Récuperation des pmcids depuis ncbi")
    print("-----------------------------------------------------")

    pmcids=[]
    pmids_abstract=[]
    for url in convert_url:
        resp = requests.get(url).json()

        for elem in resp["records"]:
            if "pmcid" in elem:
                pmcids.append(elem["pmcid"])
            else :
                pmids_abstract.append( elem["pmid"])

    print("%i article complet | %i article abstract" % (len(pmcids), len(pmids_abstract)) )
    return pmcids, pmids_abstract


def get_articles( type, ids, url):
    print("-----------------------------------------------------")
    print("Récuperation des articles")
    print("-----------------------------------------------------")
    database_manager = Manager(os.getcwd() + '/data/database/data.db')

    for groupe  in grouper(ids, 1000):
        groupe = list(filter(None,list(groupe)))
        print("groupe de taille : %i" % len(groupe))
        json = dumps({type: groupe})
        req = requests.post(url, json=json)
        print(req)
        resp = req.json(cls=ndjson.Decoder)
        print(resp)
        print("%i articles recupere" % len(resp))
        insertData( resp, database_manager)


def insertData( resp, database_manager):
    print("\t-----------------------------------------------------")
    print("\tInsertion des données")
    print("\t-----------------------------------------------------")

    for item in resp:
        database_manager.insert_articles_content( item["id"],item["passages"][0]["text"], item["passages"][1]["text"], dumps(item["authors"]))
        print("article %s inseré" % item["id"])


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

        print("fetch pour le jour : " + today)


        pmids = get_pmids(today,response)

        if pmids:
            article, article_abstract = get_pmcids(pmids)
            get_articles("pmcids", article, url)
            print ("Data successfully fetched", 201)
        else :
            print ("No data found on : \"https://www.ncbi.nlm.nih.gov/research/pubtator/index.html?view=docsum&query=$LitCovid\"", 404)
