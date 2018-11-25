import MySQLdb
from copy import deepcopy
import json
from datetime import datetime

# DB_FILE = '../db_info.dump.backup'
#
# db = MySQLdb.connect(host="localhost",
#                      user="root",
#                      password="wolverin",
#                      database="test_db")
# db.set_character_set('utf8')
# cursor = db.cursor()
#
# cursor.execute('SET NAMES utf8;')
# cursor.execute('SET CHARACTER SET utf8;')
# cursor.execute('SET character_set_connection=utf8;')

class MysqlPopulator(object):
    def __init__(self, db, encoding='utf8'):
        self.db = db
        self.cursor = db.cursor()
        self.set_character_encoding(encoding)

    def set_character_encoding(self, encoding):
        self.db.set_character_set(encoding)
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def generate_docs(self, db_file):
        with open(db_file, "r") as fp:
            for line in fp:
                yield json.loads(line.strip())

    def populate_meta_col(self, doc):
        ts = datetime.strptime(doc['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        new_doc = dict((k, doc[k]) for k in ('id', 'revId', 'title', 'redirect'))
        new_doc.update({
            'ts': ts
        })
        categories = doc['categories']

        sql = "insert into wiki_meta (id, revId, title, redirect, category, ts) values (%s, %s, %s, %s, %s, %s)"

        for category in categories:
            new_doc_duplicate = deepcopy(new_doc)
            new_doc_duplicate.update({
                "category": category
            })
            new_doc_tuple = tuple([new_doc_duplicate[k] for k in ('id', 'revId', 'title', 'redirect', 'category', 'ts')])
            try:
                self.cursor.execute(sql, new_doc_tuple)
            except Exception as e:
                print("Error: " + str(e))

    def populate_link_col(self, doc):
        new_doc = dict((k, doc[k]) for k in ('id', 'title'))
        links = doc['links']
        sql = "insert into wiki_link (id, title, link, pos) values (%s, %s, %s, %s)"
        for idx, link in enumerate(links):
            new_doc_duplicate = deepcopy(new_doc)
            new_doc_duplicate.update({
                'link': link,
                'pos': idx
            })
            new_doc_tuple = tuple([new_doc_duplicate[k] for k in ('id', 'title', 'link', 'pos')])
            try:
                self.cursor.execute(sql, new_doc_tuple)
            except Exception as e:
                print("Error: " + str(e))

    def populate(self, db_file):
        for idx, doc in enumerate(self.generate_docs(db_file)):
            if idx % 100 == 0:
                print("IDX: ", idx)
            print("Populating Meta doc...")
            self.populate_meta_col(doc)
            print("Populating Link Col")
            self.populate_link_col(doc)
        db.commit()

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         password="wolverin",
                         database="test_db")

    DB_FILE = '../db_info.dump.backup'
    mysql_populator = MysqlPopulator(db)
    mysql_populator.populate(DB_FILE)



