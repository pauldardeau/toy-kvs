import socket
import sys
import json


HOST, PORT = "localhost", 9999


def run(req_payload):
    req_json = json.dumps(req_payload)
    resp_payload = None

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(req_json + "\n")

        # Receive data from the server and shut down
        resp_json = sock.recv(1024)
        resp_payload = json.loads(resp_json)
    finally:
        sock.close()

    return resp_payload


if __name__=='__main__':
    if len(sys.argv) < 3:
        print("missing command")
        sys.exit(1)
    cmd = sys.argv[1]
    req_payload = {}
    key = None
    container = None
    value = None
    valid_cmds = ['put','get','delete','container-put','container-get','container-delete']
    if cmd in valid_cmds:
        if cmd == 'put':
            if len(sys.argv) > 3:
                key = sys.argv[2]
                value = sys.argv[3]
            else:
                print("error: missing value for put")
                sys.exit(1)
        elif cmd in ['get','delete']:
            key = sys.argv[2]
        elif cmd == 'container-put':
            if len(sys.argv) > 4:
                container = sys.argv[2]
                key = sys.argv[3]
                value = sys.argv[4]
                cmd = cmd[10:]
            else:
                print("error: missing arguments for container-put") 
                sys.exit(1)
        elif cmd in ['container-get','container-delete']:
            if len(sys.argv) > 3:
                container = sys.argv[2]
                key = sys.argv[3]
                cmd = cmd[10:]
            else:
                print("error: missing arguments for container operation")
                sys.exit(1)
    else:
        print("unrecognized command: '%s'" % cmd)
        sys.exit(1)
    req_payload['key'] = key
    req_payload['op'] = cmd
    if value is not None:
        req_payload['value'] = value
    if container is not None:
        req_payload['container'] = container
    resp_payload = run(req_payload)
    print("resp payload: %s" % repr(resp_payload))
