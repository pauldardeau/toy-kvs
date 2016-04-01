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
    key = sys.argv[2]
    req_payload = {}
    req_payload['op'] = cmd
    req_payload['key'] = key
    valid_cmds = ['put','get','delete']
    if cmd in valid_cmds:
        if cmd == 'put':
            if len(sys.argv) > 3:
                value = sys.argv[3]
                req_payload['value'] = value
            else:
                print("error: missing value for put")
                sys.exit(1)
    else:
        print("unrecognized command: '%s'" % cmd)
        sys.exit(1)
    resp_payload = run(req_payload)
    print("resp payload: %s" % repr(resp_payload))
