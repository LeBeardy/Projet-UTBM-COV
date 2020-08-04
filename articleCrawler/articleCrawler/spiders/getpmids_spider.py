

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
        pmids.append( post.xpath('link//text()').extract_first().split("/")[6])

    print("nombre de pmids recupere : %i" % len(pmids) )
    return pmids

def create_url_to_pmcids(ids):
    print("-----------------------------------------------------")
    print("generation des urls de recuperation des ids correspondants")
    print("-----------------------------------------------------")

    url_ids = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids="
    convert_url = []
    for groupe in grouper(ids, 200):
        groupe = list(filter(None,list(groupe)))
        print("division en groupe de %i" % len(groupe))
        parameters=""
        for id in groupe:
            parameters = parameters + id +","
        parameters = parameters[:-1] + "&format=json"
        convert_url.append(url_ids + parameters)

    print( "%i appels a l'api gouv" % len(convert_url))
    return convert_url

def get_pmcids( pmids):
    convert_url = create_url_to_pmcids(pmids)

    print("-----------------------------------------------------")
    print("Récuperation des pmcids depuis ncbi")
    print("-----------------------------------------------------")

    pmcids=[]
    for url in convert_url:
        resp = requests.get(url).json()
        for elem in resp["records"]:
            if "pmcid" in elem:
                pmcids.append(elem["pmcid"])


    print("%i article complet" % len(pmcids) )

    return pmcids

def send_request(type, url, ids):
    print(url)
    json = {type: ids}
    req = requests.post(url, json=json)
    print(req)
    resp = req.json(cls=ndjson.Decoder)
    print("%i articles recupere" % len(resp))

    return resp


def get_full_articles(  ids, url, database_manager):
    print("-----------------------------------------------------")
    print("Récuperation des articles full")
    print("-----------------------------------------------------")

    for groupe  in grouper(ids, 1000):
        groupe = list(filter(None,list(groupe)))
        print("groupe de taille : %i" % len(groupe))
        resp = send_request("pmcids",url, groupe)

        pmcids_fetched = []
        for article in resp:
            pmcid= article["pmcid"]
            pmid = article["pmid"]
            pmcids_fetched.append(id)
            title=article["passages"][0]["text"]
            content=""
            for cont in article["passages"]:
                if cont["infons"]["section"] not in[ "References", "Conflicts of Interest"]:
                    content= content + cont["text"] + "\n"
            authors=dumps(article["authors"])


            print("\t-----------------------------------------------------")
            print("\tInsertion des données")
            print("\t-----------------------------------------------------")
            database_manager.complete_article(pmid, pmcid, content )


def get_abstract_articles(ids, url, database_manager):
    print("-----------------------------------------------------")
    print("Récuperation des articles abstract")
    print("-----------------------------------------------------")
    for groupe  in grouper(ids, 1000):
        groupe = list(filter(None,list(groupe)))
        print("groupe de taille : %i" % len(groupe))

        resp = send_request("pmids",url, groupe)

        for article in resp:
            content = article["passages"][1]["text"] if article["passages"][1]["text"] else ""
            infons = article["passages"][0]["infons"]
            date_pub = infons["journal"].split(";")[1].split(".")[0][:12] if "journal" in infons  else""
            journal_pub = infons["journal"].split(";")[0] if "journal" in infons  else""
            database_manager.insert_article(article["id"], "", article["passages"][0]["text"], content, "", dumps(article["authors"]), date_pub, journal_pub)


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

        database_manager = Manager(os.getcwd() + '/data/database/data.db')
        pmids = get_pmids(today,response)

        if pmids:
            get_abstract_articles(pmids, url, database_manager)
            full_article = get_pmcids(pmids)
            get_full_articles( full_article, url,database_manager)
            print ("Data successfully fetched", 201)
        else :
            print ("No data found on : \"https://www.ncbi.nlm.nih.gov/research/pubtator/index.html?view=docsum&query=$LitCovid\"", 404)
