import sqlite3
import os


path = os.getcwd() + '\\data\\wikiData.db'
conn = sqlite3.connect(path)
cursor = conn.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS test (id text)')
conn.commit()
