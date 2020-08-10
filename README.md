# Projet-UTBM-COV
<a href="https://codeclimate.com/github/Paul-AntoinePechmeja-Richard/Projet-UTBM-COV/maintainability"><img src="https://api.codeclimate.com/v1/badges/3ac20147cbaf04868448/maintainability" /></a>

This project is a LDA-based covid article recommender system for the UTBM (Université de technologie de Belfort Montbéliard) a french university.
This project use sqlite3 to store the data.
This projet can be divided into 3 differents parts.

## The crawler

To fetch the differents data about the articles, we use Scrapy to fetch the list of articles.

First we read the RSS of [LitCovid](https://www.ncbi.nlm.nih.gov/research/coronavirus/docsum) to fetch the differents pmid of the article.
Then we ask the [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/index.html?view=docsum&query=$LitCovid) API to get the article's data.

Few exemple of the data we got :

The [RSS](https://www.ncbi.nlm.nih.gov/research/coronavirus-api/feed/?filters=%7B%7D)
The [abstact article](https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=32729463)
The [full artcle](https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmcids=PMC7251362,PMC7392602)
The [conversion pmid to pmcid](https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=32729463)

## The LDA

Once we got all the data of the articles, we generate the LDA model.
First we clean with the Cleaner, then we generate the model with gensim, we save the ressources generated into the data/LDA folder
The Evaluator class allows to generate the recommendations from an article's content

## The API

We can have access to all the previous element through an API.
You can have acces of all the endpoints here : http://localhost:5000/api/ui/

## The database

We stock the article's data into the table articleData.


|     pmid     |  pmcid     | title  |     content_abstract     |  content_full     | authors  |     date_pub     |  journal_pub     |
| :----------: |:----------:| :-----:| :----------------------: |:-----------------:| :-------:| :--------------: |:----------------:|
| 32729463     | PMC7251362 | title  | content                  | content           | authors  | 01/01/2020       | journal          |


## Usage

To launch the API
  ```bash
  python ./api.py
  ```
Then you can use the differents endpoints find here : http://localhost:5000/api/ui/

## Miscellaneous

If you got errors when you install pycurl: https://stackoverflow.com/questions/37669428/error-in-installation-pycurl-7-19-0
