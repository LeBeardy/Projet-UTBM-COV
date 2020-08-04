import sqlite3
from Modules.LDA.Cleaner import Cleaner
from json import loads

def format_to_json ( article):
    return {"pmid": article[0], "pmcid": article[1], "title": article[2], "content_abstract": article[3], "content_full": article[4],
    "authors": loads(article[5]), "date_pub": article[6], "journal_pub": article[7]}


class Manager:

    def __init__(self, db_file):
        self.categories = []
        self.conn = sqlite3.connect(db_file)
        cursor = self.conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS articleData (pmid text NOT NULL PRIMARY KEY, pmcid text, title text, content_abstract text, content_full, author text, date_pub text, journal_pub text)')
        self.conn.commit()
        self.cursor = self.conn.cursor()
        self.cleaner = Cleaner()

    def insert_article(self, pmid, pmcid, title, content_abstract, content_full, authors, date_pub, journal_pub):
        self.cursor.execute('REPLACE INTO articleData VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
         (pmid, pmcid, title, content_abstract, content_full,authors, date_pub, journal_pub))
        self.conn.commit()

    def complete_article(self, pmid, pmcid, content_full):
        self.cursor.execute('UPDATE articleData SET pmcid=?, content_full=? WHERE pmid=?', (pmcid, content_full, pmid))
        self.conn.commit()

    def get_pmids(self):
        return [pmid for pmid in self.cursor.execute('SELECT pmid FROM articleData')]

    def get_content_by_pmid(self, pmid):
        abstact, full = self.cursor.execute('SELECT content_abstract, content_full FROM articleData WHERE pmid=?', pmid).fetchone()
        content = full if full != '' else abstact
        return str(self.cleaner.clean_text(content))



    def get_articles(self):
        articles =[]
        request = self.cursor.execute('SELECT * FROM articleData')
        for article in request:
            articles.append(format_to_json(article))
        return articles

    def get_article(self, pmid):
        article = self.cursor.execute('SELECT * FROM articleData WHERE pmid=%i' % pmid).fetchone()
        return format_to_json(article)



    def __iter__(self):
        for pmid in self.get_pmids():
            content = self.get_content_by_pmid(pmid)
            yield self.cleaner.clean_text(content).split()
