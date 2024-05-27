import sockHTTP.errorlogger


# split head and content; possibly more (x-form or sth)

def split_segments(rawresp):

    index = rawresp.find(b'\r\n\r\n')
    if index != -1:
        return rawresp[:index], rawresp[(index+4):]
    
    return None, rawresp


def parse_headers(headbytes):
    headstr = str(headbytes)

    lines = headstr.split("\r\n")

    header_dict = dict()

    for line in lines:
        split_index = line.find(": ")

        if split_index == -1:
            sockHTTP.errorlogger.main.saveError('Error on parsing headers')
        else:
            header_name = line[:split_index]
            header_val = line[(split_index+2):]

            if " " not in header_name : 
                header_dict[header_name] = header_val

    if len(header_dict) == 0: header_dict = None

    return header_dict

        
        




def quickparse(rawresp: bytes):
    

    headbytes, contentbytes = split_segments(rawresp)

    if headbytes == None:

        sockHTTP.errorlogger.main.saveError('Error on loading headers')

    headers = None
    if headbytes != None:
        headers = parse_headers(headbytes)

    if not "Content-Length" in headers.keys():

        sockHTTP.errorlogger.main.saveError('Error on headers - no Content-Length')
    

    else: 
        if not int(headers["Content-Length"]) == len(contentbytes):

            sockHTTP.errorlogger.main.saveError('Error on headers - Content-Length doesn\'t match length')


    return headers, contentbytes



def calc_len(rawresp: bytes):

    headbytes, contentbytes = split_segments(rawresp)


    return len(contentbytes)

