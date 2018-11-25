from pymongo import MongoClient
from copy import deepcopy
import json

DB_FILE = 'db_info.dump.backup'

client = MongoClient('localhost', 27017)
meta_coll = client['prod_db']['wiki_meta']
link_coll = client['prod_db']['wiki_link']

def generate_docs(db_file):
    with open(db_file, "r") as fp:
        for line in fp:
            yield json.loads(line.strip())

def populate_meta_col(doc):
    new_doc = dict((k, doc[k]) for k in ('id', 'revId', 'title', 'redirect', 'categories', 'timestamp'))
    meta_coll.insert_one(new_doc)

def populate_link_col(doc):
    new_doc = dict((k, doc[k]) for k in ('id', 'revId', 'title', 'redirect'))
    links = doc['links']
    docs = []
    for idx, link in enumerate(links):
        new_doc_duplicate = deepcopy(new_doc)
        new_doc_duplicate.update({
            'referredPage': link,
            'pos': idx
        })
        docs.append(new_doc_duplicate)

    link_coll.insert_many(docs)

for idx, doc in enumerate(generate_docs(DB_FILE)):
    if idx % 10 == 0:
        print("IDX: ", idx)
    populate_meta_col(doc)
    populate_link_col(doc)




