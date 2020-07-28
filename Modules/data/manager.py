import sqlite3
from Modules.LDA.Cleaner import Cleaner

class Manager:

    def __init__(self, db_file):
        self.categories = []
        self.conn = sqlite3.connect(db_file)
        cursor = self.conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS articleData (pmid integer, title text, content text, author text )')
        self.conn.commit()
        self.cursor = self.conn.cursor()
        self.cleaner = Cleaner()

    def insert_articles_content(self, pmid, title, content, authors):
        self.cursor.execute('INSERT INTO articleData VALUES (?, ?, ?, ?)', (pmid, title, content,authors))
        self.conn.commit()

    def get_pmids(self):
        return [pmid for pmid in self.cursor.execute('SELECT pmid FROM articleData')]

    def get_content_by_pmid(self, pmid):
        return str(self.cleaner.clean_text(self.cursor.execute('SELECT content FROM articleData WHERE pmid=?', pmid)
                    .fetchone()[0]))
    def get_articles(self):
        articles =[]
        request = self.cursor.execute('SELECT * FROM articleData')
        for article in request:
            articles.append({"pmid": article[0], "title": article[1], "content": article[2], "authors": article[3]})
        return articles

    def get_article(self, pmid):
        article = self.cursor.execute('SELECT * FROM articleData WHERE pmid=%i' % pmid).fetchone()

        return {"pmid": article[0], "title": article[1], "content": article[2], "authors": article[3]}

    def __iter__(self):
        for pmid in self.get_pmids():
            article = self.get_content_by_pmid(pmid)
            yield self.cleaner.clean_text(article).split()
