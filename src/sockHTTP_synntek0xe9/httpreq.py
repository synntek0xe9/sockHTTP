
import socket
import ssl
import time

import httpreqCrafter



def recvall(sock, space_max_tries=2, init_max_tries=100):
    BUFF_SIZE = 65536 # 64 KiB
    data = b''
    none_count = 0
    time.sleep(0.1)
    sock.settimeout(0.01)
    while True:
        #print(null_count, end=" ")
        part = b""
        try:
            part = sock.recv(BUFF_SIZE)
        except TimeoutError:
            part=b""
        data += part
        #print(part)
        if len(part) == 0:
            none_count+=1
            if len(data) == 0:
                if none_count >= init_max_tries:
                    break
            elif none_count >= space_max_tries: # max 3 can configure
                # either 0 or end of data
                break
        else:
            #print(none_count, len(data))
            none_count = 0
    #print("\n")
    return data


# notes - lack many features, unstable, works


def httpreq(hostname, port=80, path="/", method="GET", customReqBody=None, sock=None):
    
    opened_sock = True

    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    else:
        opened_sock = False
    
    #print(f"Connected by {addr}")

    if customReqBody != None:
        sock.sendall(customReqBody)
    else: 
        sock.sendall( httpreqCrafter.craftHttpReq(hostname, method, path).encode() )

    output = recvall(sock)

    if opened_sock: sock.close()

    return output


# notes - lack many features, unstable, works

def httpsreq(hostname, port=443, path="/",method="GET", customReqBody=None, sock_wrap=None):
    
    opened_sock = True
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1) could be usefull is some scenarios
    if sock_wrap is None:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_wrap = ssl.create_default_context().wrap_socket(sock, server_hostname=hostname)
        sock_wrap.connect((hostname, port))
    else:
        opened_sock = False

    if customReqBody != None:
        sock_wrap.sendall(customReqBody)
    else: 
        sock_wrap.sendall( httpreqCrafter.craftHttpReq(hostname, method, path).encode() )

    output = recvall(sock_wrap)

    if opened_sock: sock_wrap.close()

    return output
