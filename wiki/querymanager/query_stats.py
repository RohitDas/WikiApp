import subprocess
import re
from threading import Thread

class QueryStats(object):
    """
        Reads the log file and generates stats for queries.
        Currently, it shows the recent queries.
        Later, it can support other types such as most popular queries or
        most popular pages that were queried.
    """
    def __init__(self, log_file, n_recent):
        self.log_file = log_file
        self.query_regx = re.compile(".*Running query: (.*)")
        self.recent_queries = []
        self.n_recent = n_recent

    def put(self, query):
        self.recent_queries.append(query)
        if len(self.recent_queries) > self.n_recent:
            self.recent_queries = self.recent_queries[len(self.recent_queries) - self.n_recent:]

    def get_latest(self):
        return self.recent_queries

    def start_tailing(self):
        f = subprocess.Popen(['tail', '-F', self.log_file],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        while True:
            line = f.stdout.readline().decode('utf8')
            if 'Running query' in line:
                query = self.query_regx.match(line).group(1).strip()
                self.put(query)


query_stats = QueryStats("/home/rohittulu/WikiApp/wiki/log/info.log", 50)
thread = Thread(target=query_stats.start_tailing)
thread.start()



