import time
import json
import redis


class BaseCache:
    def set(self, key, value, ttl=None):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError
    
    def get_by_key(self, keyword):
        raise NotImplementedError


class DictCache(BaseCache):
    def __init__(self):
        self.store = {}

    def set(self, key, value, ttl=None):
        # expires = time.time() + ttl if ttl else None
        # self.store[key] = {"value": value, "expires": expires}
        self.store[key] = {'value': json.dumps(value)}


    def get(self, key):
        item = self.store.get(key)
        if not item:
            return None
        # if item["expires"] and item["expires"] < time.time():
        #     del self.store[key]
        #     return None
        return json.loads(item["value"])
    
    def get_by_key(self, keyword):
        keyword = keyword.strip('*')

        key_list = [key for key in self.store if keyword in key]

        return_dict = dict()
        
        for key in key_list:
            return_dict[key.strip(keyword)] = self.get(key)

        return return_dict
    

class RedisCache(BaseCache):
    def __init__(self, host="localhost", port=6379, db=0):
        self.r = redis.StrictRedis(host=host, port=port, db=db)

    def set(self, key, value):
        self.r.set(key, json.dumps(value))

    def get(self, key):
        val = self.r.get(key)
        return json.loads(val) if val else None

    def get_by_key(self, keyword):
        """
        Returns only keys ending with ':latest', 
        using SCAN to avoid blocking.
        """
        cursor = 0
        results = {}
        while True:
            cursor, keys = self.r.scan(cursor=cursor, match=keyword, count=100)
            for key in keys:
                node_id = key.decode().replace(keyword, "")
                results[node_id] = json.loads(self.r.get(key))
            if cursor == 0:
                break
        return results
