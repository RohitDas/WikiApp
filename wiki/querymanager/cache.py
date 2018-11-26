"""
    Caching layer for the mysql queries.
"""

from datetime import datetime

class Cache(object):
    """
        A very simple LRU Cache implementation of size of num_entries.
        put(): Worst case time complexity is O(num_entries), has it iterates for the keys to find the oldest timestamped key
        In the next implementation: shall use a combination of HashMap and linked list to reduce the time complexity.
    """
    def __init__(self, num_entries):
        self.hash_to_value = {}
        self.num_entries =  num_entries

    def has_key(self, key):
        return hash(key) in self.hash_to_value

    def put(self, key, val):
        if hash(key) in self.hash_to_value:
            self.hash_to_value.update({
                hash(key): (val, datetime.now())
            })
        else:
            current = datetime.now()
            oldest_accessed, max_duration = None, None
            if len(self.hash_to_value) == self.num_entries:
                for key, val in self.hash_to_value.items():
                    if oldest_accessed is None or current - val[1] > max_duration:
                        max_duration = current - val[1]
                        oldest_accessed = key
                del self.hash_to_value[oldest_accessed]
            self.hash_to_value.update({
                hash(key): (val, current)
            })

    def get(self, key):
        if hash(key) not in self.hash_to_value:
            raise Exception("Key not found")
        #update the timestamp
        val = self.hash_to_value[hash(key)]
        self.hash_to_value[hash(key)] = (val[0], datetime.now())
        return val[0]

cache = Cache(500)