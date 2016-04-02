import SocketServer
import json
import mem_kvs


class MemKVSTCPHandler(SocketServer.BaseRequestHandler):

    def do_put(self, key, value, container=None):
        if container is not None:
            kvs.container_put(container, key, value)
            return kvs.container_contains_key(container, key)
        else:
            kvs.put(key, value)
            return kvs.contains_key(key)

    def do_get(self, key, container=None):
        if container is not None:
            if kvs.container_contains_key(container, key):
                return (True, kvs.container_get(container, key))
        else:
            if kvs.contains_key(key):
                return (True, kvs.get(key))
        return False, None

    def do_delete(self, key, container=None):
        if container is not None:
            if kvs.container_contains_key(container, key):
                kvs.container_delete(container, key)
                return not kvs.container_contains_key(container, key)
        else:
            if kvs.contains_key(key):
                kvs.delete(key)
                return not kvs.contains_key(key)
        return False

    def handle(self):
        # self.request is the TCP socket connected to the client
        req_json = self.request.recv(1024).strip()
        resp_payload = {}
        msg = ""
        op = ""
        self.key = ""
        container = None
        success = False
        value = None
        if req_json is not None and len(req_json) > 0:
            self.req_payload = json.loads(req_json)
            if 'op' in self.req_payload:
                if 'container' in self.req_payload:
                    container = self.req_payload['container']
                op = self.req_payload['op']
                if op in ['get','put','delete']:
                    if 'key' in self.req_payload:
                        self.key = self.req_payload['key']
                        if len(self.key) > 0:
                            if op == 'put':
                                if 'value' in self.req_payload:
                                    self.value = self.req_payload['value']
                                    if self.value is None:
                                        msg = "invalid value for put"
                                    else:
                                        success = self.do_put(self.key, self.value, container)
                                else:
                                    msg = "missing value for put"
                            else:
                                if op == 'get':
                                    success, value = self.do_get(self.key, container)
                                elif op == 'delete':
                                    success = self.do_delete(self.key, container)
                        else:
                            # invalid key
                            msg = "invalid key"
                    else:
                        # missing key
                        msg = "missing key"
                else:
                    # invalid operation
                    msg = "invalid operation"
            else:
                # missing operation
                msg = "missing operation"
        else:
            # missing request payload
            msg = "missing request payload"

        if success:
            resp_payload['success'] = 'true'
        else:
            resp_payload['success'] = 'false'

        resp_payload['msg'] = msg
        resp_payload['op'] = op
        resp_payload['key'] = self.key
        if container is not None:
            resp_payload['container'] = container
        if value is not None:
            resp_payload['value'] = value

        self.request.sendall(json.dumps(resp_payload))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    kvs = mem_kvs.MemKeyValueStore()

    # Create the server, binding to localhost on port 9999
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MemKVSTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

