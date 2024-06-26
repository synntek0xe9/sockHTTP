
import socket
import ssl
import time
import math


import sockHTTP.ReqCrafter



def recvall(sock, initWait=0, initMaxTries=50, initTimeout=0.1, betweenMaxTries=3, betweenTimeout=0.01):
    BUFF_SIZE = 65536 # 64 KiB
    data = b''
    none_count = 0
    time.sleep(initWait)
    sock.settimeout(initTimeout)
    while True:
        #print(null_count, end=" ")
        part = b""
        try:
            part = sock.recv(BUFF_SIZE)
            if len(data) == 0:
                sock.settimeout(betweenTimeout)
        except TimeoutError:
            part=b""
        data += part
        #print(part)
        if len(part) == 0:
            none_count+=1
            if len(data) == 0:
                if none_count >= initMaxTries:
                    break
            elif none_count >= betweenMaxTries: # max 3 can configure
                # either 0 or end of data
                break
        else:
            #print(none_count, len(data))
            none_count = 0
    #print("\n")
    return data


# notes - lack many features, unstable, works


def httpReq(hostname, port=80, path="/", method="GET", customReqBody=None, sock=None, timeout=5, timeoutAdvOpt=None):
    
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
        sock.sendall( sockHTTP.ReqCrafter.craftHttpReq(hostname, method, path).encode() )

    output = None

    received = False

    if type(timeoutAdvOpt) == dict:
        
        if all([key in timeoutAdvOpt.keys() for key in ['initWait', 'initMaxTries', 'initTimeout', 'betweenMaxTries', 'betweenTimeout']]):

            received = True
            output = recvall(sock, initWait=timeoutAdvOpt['initWait'], initMaxTries=timeoutAdvOpt['initMaxTries'], initTimeout=timeoutAdvOpt['initTimeout'], betweenMaxTries=timeoutAdvOpt['betweenMaxTries'], betweenTimeout=timeoutAdvOpt['betweenTimeout'])
            

    
    if not received:
        if type(timeout) == int and timeout > 0:
            initTimeout = 0.1
            initMaxTries = math.ceil(timeout / initTimeout)
            output = recvall(sock, initMaxTries=initMaxTries, initTimeout=initTimeout)
        else:
            output = recvall(sock)


    if opened_sock: sock.close()

    return output


# notes - lack many features, unstable, works

def httpsReq(hostname, port=443, path="/",method="GET", customReqBody=None, sock_wrap=None):
    
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
        sock_wrap.sendall( sockHTTP.ReqCrafter.craftHttpReq(hostname, method, path).encode() )

    output = recvall(sock_wrap)

    if opened_sock: sock_wrap.close()

    return output
