# sockHTTP python lib & examples on HTTP using sockets 

This project uses standars socket library.
Main reason by which project was created is bit more of speed (like 8x more comparing to requests library).
It should be great choice to use it or at least inspire of code when building python fuzzer or crawler basing on sockets.  
It's a bit slower than ffuf (like 20% on same amount of threads), but it's scriptable so should be of use.

# Instalation
Download recent package using releases button (sorry not added to pip packages yet)  
  
then install with  
```pip install ./sockHTTP(...).tar.gz```

# Usage
 
quick http request
```py
raw_resp = sockHTTP.httpreq.httpsreq("www.example.com",path="/")
headers, body = sockHTTP.httpparser.quickparse(raw_resp)

```

control over handling http response
```py 
import gzip

raw_resp = sockHTTP.httpreq.httpsreq("www.example.com",path="/")
raw_head, raw_body = sockHTTP.httpparser.split_segments(raw_resp)
headers = sockHTTP.httpparser.parse_headers(raw_head)
# print(headers)
body = raw_body # if nothing happens
if "Transfer-Encoding" in headers.keys():
    if headers["Transfer-Encoding"] == "chunked":
        raw_body = sockHTTP.httpparser.process_tranfer_chunked("")

if "Content-Encoding" in headers.keys():
    if headers["Content-Encoding"] == "gzip":
        body = gzip.decompress(raw_body)

# above handling should work in like 95% scenarios. I would propably add more features some day

print(body)
print(headers)
print(len(body))

```  
  
