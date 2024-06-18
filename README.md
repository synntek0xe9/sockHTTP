# sockHTTP python lib & examples on HTTP using sockets 

This project uses standars socket library.
Main reason by which project was created is bit more of speed (like 8x more comparing to requests library when requesting same host multiple times with same socket if not it's like 1.5x/2x more).
This lib should be great choice to use (or at least inspire) when building python fuzzer or crawler basing on sockets.  
It's a bit slower than ffuf (like 20% on same amount of threads), but it's scriptable so should be of use.

# Instalation
Download recent package using releases button (sorry not added to pip packages yet)  
  
then install with  
```pip install ./sockHTTP(...).tar.gz```

# Usage
 
quick http request
```py
raw_resp = sockHTTP.Req.httpsReq("www.example.com",path="/")
headers, body = sockHTTP.Parser.quickParse(raw_resp)

```

control over handling http response
```py 
import gzip

raw_resp = sockHTTP.Req.httpsReq("www.example.com",path="/")
raw_head, raw_body = sockHTTP.Parser.splitSegments(raw_resp)
headers = sockHTTP.Parser.parseHeaders(raw_head)
# print(headers)
body = raw_body # if nothing happens
if "Transfer-Encoding" in headers.keys():
    if headers["Transfer-Encoding"] == "chunked":
        body = sockHTTP.Parser.processTranferChunked(body)

if "Content-Encoding" in headers.keys():
    if headers["Content-Encoding"] == "gzip":
        body = gzip.decompress(body)

# above handling should work in like 90% scenarios. It would go up to 95% if you specify bigger timeout like (raw_resp = ...httpReq(... , timeout=10))). I would probably add more features some day

print(body)
print(headers)
print(len(body))

```  
  
