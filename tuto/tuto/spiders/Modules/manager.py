import sqlite3


class Manager:

    def __init__(self, db_file):
        self.categories = []
        self.conn = sqlite3.connect(db_file)
        cursor = self.conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS articleData (pmid integer, title text, content text, author text )')
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def insert_articles_content(self, id, title, content, authors):
        self.cursor.execute('INSERT INTO articleData VALUES (?, ?, ?, ?)', (id, title, content,authors))
        self.conn.commit()

    def get_ids(self):
        return [id for id in self.cursor.execute('SELECT id FROM articleData')]

    def get_article_by_id(self, id):
        return str(self.cleaner.clean_text(self.cursor.execute('SELECT content FROM wikiData WHERE id=?', id)
                    .fetchone()[0]))

    def __iter__(self):
        for id in self.get_ids():
            article = self.get_article_by_id(id)
            yield self.cleaner.clean_text(article).split()
