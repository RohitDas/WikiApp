"""
    Most of sql tables are dump downloaded from the internet.
    However, we create a wiki_meta and wiki_link table, by parsing the meta_data xml file.
"""
import MySQLdb

def get_sql_connection(conf):
    return MySQLdb.connect(host=conf['host'],
                           user=conf["user"],
                           password=conf["password"],
                           database=conf["database"])


def create_tabes(db):
    cursor = db.cursor()
    cursor.execute("create table wiki_meta (wid int not null, revId varchar(256), title varchar(256), redirect varchar(256), category varchar(256), ts datetime)")
    cursor.execute("create table wiki_link (wid int not null, title varchar(256), link varchar(256), pos int)")
    cursor.close()

local_conf = {
    'host': 'localhost',
    'user': 'rohit',
    'password': 'wolverin',
    'database': 'test_db'
}

""" 
    'master_conf = {
    'host': 'localhost',
    'user': 'aws',
    'password': 'passw',
    'database': 'test_db'
}
"""

db = get_sql_connection(local_conf)
create_tabes(db)

# #Create Database
# try:
#     cursor.execute("create database if not exists test_db")
# except Exception as e:
#     print("Error: ", str(e))


