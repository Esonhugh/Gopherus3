from .base import *

class PlainText(GENERATOR):
    requirement = ["filename", "mode"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 25
        super().__init__(parser,options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.filename == "":
            self.filename = self.wizard()
        else:
            self.filename = arg.filename
        self.set_mode_str(arg.mode)

    def generate(self):
        payload = readfile(self.filename) 
        self.set_payload(payload).\
            replace("+", "%20").\
            replace("%2F", "/")
        return super().generate()

    def wizard(self):  
        filename = input("\033[96m" +"Give the file name you want to read: "+ "\033[0m")
        return filename
        pass


def readfile(filename):
    payload = ''
    with open(filename, 'r') as f:
        payload = f.read()
    return payload