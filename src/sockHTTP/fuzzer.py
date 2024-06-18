
import sockHTTP.Req
import socket
import ssl



def httpFuzzer(wordlist, url, path="/", port=80, options={}):
    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url, 80))

    for wordlist_entry in wordlist:
        resp = sockHTTP.Req.httpReq(url, path=path + wordlist_entry,sock=sock)
        print(wordlist_entry, len(resp))
    
    sock.close()

    


def httpsFuzzer(wordlist, hostname, path="/", port=443, options={}):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_wrap = ssl.create_default_context().wrap_socket(sock, server_hostname=hostname)
    sock_wrap.connect((hostname, port))

    for wordlist_entry in wordlist:
        resp = sockHTTP.Req.httpsReq(hostname, path = path + wordlist_entry, sock_wrap=sock_wrap)
        print(wordlist_entry, len(resp))
    
    sock_wrap.close()



def fuzzer(wordlist, url, options):

    split = url.split("://")

    if split[0] == "http":
        httpFuzzer(wordlist, url, options)

    elif split[0] == "https":
        httpsFuzzer(wordlist, url, options)