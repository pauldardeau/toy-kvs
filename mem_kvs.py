
class MemKeyValueStore(object):

    def __init__(self):
        self.kvs = {}
        self.containers = {}

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

    def container_exists(self, container):
        return container in self.containers

    def container_put(self, container, key, value):
        if container in self.containers:
            container_kvs = self.containers[container]
            container_kvs[key] = value
        else:
            container_kvs = {}
            container_kvs[key] = value
            self.containers[container] = container_kvs

    def container_get(self, container, key):
        if container in self.containers:
            container_kvs = self.containers[container]
            if key in container_kvs:
                return container_kvs[key]
        return None

    def container_delete(self, container, key):
        if container in self.containers:
            container_kvs = self.containers[container]
            if key in container_kvs:
                del container_kvs[key]

    def container_contains_key(self, container, key):
        if container in self.containers:
            container_kvs = self.containers[container]
            return key in container_kvs
        else:
            return False


if __name__=='__main__':
    kvs = MemKeyValueStore()
    kvs.put('stooge1', 'Moe')
    kvs.delete('stooge1')
