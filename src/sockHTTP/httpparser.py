import sockHTTP.errorlogger
import gzip

# split head and content; possibly more (x-form or sth)

def split_segments(rawresp):

    index = rawresp.find(b'\r\n\r\n')
    if index != -1:
        return rawresp[:index], rawresp[(index+4):]
    
    return None, rawresp


def parse_headers(headbytes):
    headstr = headbytes.decode()

    lines = headstr.split("\r\n")[1:] # (skip HTTP/1.1  ...)

    header_dict = dict()

    for line in lines:
        split_index = line.find(": ")

        if split_index == -1:
            sockHTTP.errorlogger.main.saveError('Error on parsing headers')
        else:
            header_name = line[:split_index]
            header_val = line[(split_index+2):]

            header_dict[header_name] = header_val
                

    if len(header_dict) == 0: header_dict = None

    return header_dict

        
        

def process_tranfer_chunked(raw):
    
    length = len(raw)

    processed = ""

    num_chars = 0
    a = 0
    prev = 0

    # handle errors ? (int conversion if message is corrupted), check how long is int (there should be max value for chunked discribed somewhere)

    while a != length-1:
        prev = a

        processed += raw[a+1:a+1+num_chars]

        a = raw.find(a+num_chars,"\r\n")
        num_chars = int(raw[prev+num_chars:a])

    return processed


def quickparse(rawresp: bytes):
    

    headbytes, contentbytes = split_segments(rawresp)

    if headbytes == None:

        sockHTTP.errorlogger.main.saveError('Error on loading headers')

    headers = None
    if headbytes != None:
        headers = parse_headers(headbytes)

    keys = headers.keys()

    if not "Content-Length" in keys:

        sockHTTP.errorlogger.main.saveError('Error on headers - no Content-Length')
    

    else: 
        if not int(headers["Content-Length"]) == len(contentbytes):

            sockHTTP.errorlogger.main.saveError('Error on headers - Content-Length doesn\'t match length')

    if "Transfer-Encoding" in keys:
        if headers["Transfer-Encoding"] == "chunked":
            contentbytes = process_tranfer_chunked(contentbytes)

    if "Content-Encoding" in keys:
        if headers["Content-Encoding"] == "gzip":
            contentbytes = gzip.decompress(contentbytes)

    return headers, contentbytes



def calc_len(rawresp: bytes):

    headbytes, contentbytes = split_segments(rawresp)


    return len(contentbytes)


