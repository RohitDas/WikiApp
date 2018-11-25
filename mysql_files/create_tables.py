import MySQLdb

def get_sql_connection(conf):
    return MySQLdb.connect(host=conf['host'],
                           user=conf["user"],
                           password=conf["password"],
                           database=conf["database"])


def create_tabes(db):
    cursor = db.cursor()
    # Wiki Table: id, revId
    cursor.execute("create table wiki_meta (wid int not null, revId varchar(256), title varchar(256), redirect varchar(256), category varchar(256), ts datetime)")
    cursor.execute("create table wiki_link (wid int not null, title varchar(256), link varchar(256), pos int)")
    cursor.close()

conf = {
    'host': 'localhost',
    'user': 'root',
    'password': 'wolverin',
    'database': 'test_db'
}

db = get_sql_connection(conf)
create_tabes(db)

# #Create Database
# try:
#     cursor.execute("create database if not exists test_db")
# except Exception as e:
#     print("Error: ", str(e))


