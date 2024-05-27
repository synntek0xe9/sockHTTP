
def craftHttpReq(hostname, method, path, additional_headers=""):
    
    # validate?

    if len(additional_headers) > 0: 
        if additional_headers[-1] != "\n": additional_headers += "\n"
    
    req_pre =  """{method} {path} HTTP/1.1
Host: {hostname}
User-Agent: Mozilla/5.0 (python) Gecko/20100101 Firefox/126.0
Accept-Encoding: gzip, deflate, br, zstd
Accept: */*
{additional_headers}
"""
    
    req_str = req_pre.format(hostname=hostname, method=method, path=path, additional_headers=additional_headers).replace("\n","\r\n")

    
    return req_str




#print(craftHttpReq("127.0.0.1","GET","/"))