from .base import *
import sys

class PlainText(GENERATOR):
    default_port = 25
    requirement = ["filename", "mode"]

    def __init__(self, parser, options=None):
        super().__init__(parser, options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.filename == "":
            self.filename = self.wizard()
        else:
            self.filename = arg.filename
        self.set_mode_str(arg.mode)

    def generate(self):
        payload = readfile(self.filename)
        if self.mode == PAYLOAD_TYPE.QUOTE_PLUS:
            self.set_url_payload(payload)
        else:
            self.set_payload(payload)
        return super().generate()

    def wizard(self):
        return input("\033[96m" + "Give the file name you want to read: " + "\033[0m")


def readfile(filename):
    payload = ''
    if filename == "-":
        payload = sys.stdin.read()
    else:
        with open(filename, 'r') as f:
            payload = f.read()
    return payload