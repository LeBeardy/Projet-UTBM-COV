import sqlite3
from Modules.Cleaner import Cleaner

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


    def __iter__(self):
        for pmid in self.get_pmids():
            article = self.get_content_by_pmid(pmid)
            yield self.cleaner.clean_text(article).split()
