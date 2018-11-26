import MySQLdb

def get_sql_connection(conf):
    return MySQLdb.connect(host=conf['host'],
                           user=conf["user"],
                           password=conf["password"],
                           database=conf["database"])

local_conf = {
    'host': 'localhost',
    'user': 'root',
    'password': 'wolverin',
    'database': 'test_db'
}

connection = get_sql_connection(local_conf)

def process_links(conn):
    cursor = connection.cursor()
    sql = "select * from pagelinks"
    cursor.execute(sql)
    rows = cursor.fetchall()
    pageid_to_links = {}
    for row in rows:
        pageid_to_links.setdefault(row[0], []).append(row[2])
    return pageid_to_links

print(process_links(connection))