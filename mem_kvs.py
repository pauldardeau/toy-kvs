
class MemKeyValueStore(object):

    def __init__(self):
        self.kvs = {}

    def put(self, key, value):
        self.kvs[key] = value

    def get(self, key):
        if key in self.kvs:
            return self.kvs[key]
        else:
            return None

    def delete(self, key):
        if key in self.kvs:
            del self.kvs[key]

    def contains_key(self, key):
        return key in self.kvs


if __name__=='__main__':
    kvs = MemKeyValueStore()
    kvs.put('stooge1', 'Moe')
    kvs.delete('stooge1')
