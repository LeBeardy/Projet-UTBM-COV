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
