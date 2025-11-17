import time
import json
import redis


class BaseCache:
    def kv_set(self, key, value):
        raise NotImplementedError

    def kv_get(self, key):
        raise NotImplementedError

    def kv_scan(self, pattern):
        raise NotImplementedError

    def list_push(self, key, value):
        raise NotImplementedError

    def list_pop(self, key, numel=1):
        raise NotImplementedError

    def set_members(self, key):
        raise NotImplementedError


class DictCache(BaseCache):
    """
    Thin wrapper around Redis for typed operations:
    - kv_* for key/value (strings)
    - list_* for queue-style operations
    - set_* for collections
    """

    def __init__(self):
        self.kv = dict()
        self.sets = dict()
        self.lists = dict()

    # -----------------
    # Key/Value (string)
    # -----------------
    def kv_set(self, key, value):
        """Set scalar value (JSON-encoded)."""
        self.kv[key] = json.dumps(value)

    def kv_get(self, key):
        """Get scalar value (JSON-decoded)."""
        val = self.kv.get(key)
        return json.loads(val) if val else None

    def kv_scan(self, pattern):
        """Get all key/values matching a pattern like 'node-*:latest'."""
        results = dict()
        keys = [key for key in self.kv.keys() if pattern.strip('*') in key]
        for key in keys:
            results[key.strip(pattern)] = json.loads(self.kv.get(key))
        return results

    # # -----------
    # # Lists/Queue
    # # -----------
    def list_push(self, key, value):
        """Append a value to a list (queue)."""
        if key not in self.lists:
            self.lists[key] = [value]
        else:
            self.lists[key].append(value)

    def list_pop(self, key, numel=1):
        """Pop N elements from the left of the list."""
        if numel > len(self.lists[key]):
            self.lists[key] = []
        else:
            self.lists[key] = self.lists[key][numel:]

    def list_peek(self, key, numel=1):
        """Look at the first N elements without removing them."""
        if numel > len(self.lists[key]):
            return self.lists[key]
        else:
            return self.lists[key][0:numel]

    # ----
    # Sets
    # ----
    def set_add(self, key, value):
        """Add value to a set."""
        if key in self.sets:
            self.sets[key].add(value)
        else:
            self.sets[key] = set()
            self.sets[key].add(value)

    def set_members(self, key):
        """Get all members of a set."""
        return self.sets.get(key)


class RedisCache(BaseCache):
    """
    Thin wrapper around Redis for typed operations:
    - kv_* for key/value (strings)
    - list_* for queue-style operations
    - set_* for collections
    """

    def __init__(self, host="localhost", port=6379, db=0, decode_responses=True):
        self.r = redis.Redis(host=host, port=port, db=db,
                             decode_responses=decode_responses)

    # -----------------
    # Key/Value (string)
    # -----------------
    def kv_set(self, key, value):
        """Set scalar value (JSON-encoded)."""
        self.r.set(key, json.dumps(value))

    def kv_get(self, key):
        """Get scalar value (JSON-decoded)."""
        val = self.r.get(key)
        return json.loads(val) if val else None

    def kv_scan(self, pattern):
        """Get all key/values matching a pattern like 'node-*:latest'."""
        cursor, results = 0, {}
        while True:
            cursor, keys = self.r.scan(cursor=cursor, match=pattern, count=100)
            for key in keys:
                results[key] = json.loads(self.r.get(key))
            if cursor == 0:
                break
        return results

    # -----------
    # Lists/Queue
    # -----------
    def list_push(self, key, value):
        """Append a value to a list (queue)."""
        self.r.rpush(key, json.dumps(value))

    def list_pop(self, key, numel=1):
        """Pop N elements from the left of the list."""
        values = self.r.lrange(key, 0, numel - 1)
        self.r.ltrim(key, len(values), -1)
        return [json.loads(v) for v in values] if values else []

    def list_peek(self, key, numel=1):
        """Look at the first N elements without removing them."""
        values = self.r.lrange(key, 0, numel - 1)
        return [json.loads(v) for v in values] if values else []

    # ----
    # Sets
    # ----
    def set_add(self, key, value):
        """Add value to a set."""
        self.r.sadd(key, value)

    def set_members(self, key):
        """Get all members of a set."""
        return self.r.smembers(key)
