import urllib.parse
import argparse

import logging as log

from enum import Enum
class PAYLOAD_TYPE(Enum):
    NONE = "NONE"
    QUOTE_PLUS = "QUOTE_PLUS"
    QUOTE = "QUOTE"
    HEX = "HEX"
    HEX_UPCASE = "HEX_UPCASE"

map_payload_type = {
    "NONE": PAYLOAD_TYPE.NONE,
    "QUOTE_PLUS": PAYLOAD_TYPE.QUOTE_PLUS,
    "QUOTE": PAYLOAD_TYPE.QUOTE,
    "HEX": PAYLOAD_TYPE.HEX,
    "HEX_UPCASE": PAYLOAD_TYPE.HEX_UPCASE
}

class GENERATOR(object):
    default_options = {
        "port": 12345,
        "host": "127.1",
        "requirement": [],
        "mode": PAYLOAD_TYPE.QUOTE_PLUS
    }

    def __init__(self, parser, options=default_options):
        self.arg_parser = parser
        if options == {}:
            self.options = self.default_options
        for key in options:
            self.__setattr__(key, options[key])

    def log(self, msg):
        log.debug(f"[{self.__class__.__name__}] {msg}")

    def set_host(self, host="127.0.0.1"):
        self.host = host

    def set_port(self, port=12345):
        self.port = port

    def set_mode(self, mode=PAYLOAD_TYPE.QUOTE_PLUS):
        self.mode = mode
        return self
    
    def set_mode_str(self, mode="QUOTE_PLUS"):
        return self.set_mode(map_payload_type[mode])

    def set_requirement(self, requirement=[]):
        self.requirement = requirement
        for req in self.requirement:
            if req == "mode":
                self.arg_parser.add_argument(f"--mode", help=f"mode value", default="QUOTE_PLUS", choices=map_payload_type.keys())
            else:
                self.arg_parser.add_argument(f"--{req}", help=f"{req} value", default="")
        self.arg_parser.add_argument("-h","--help", help="show this help message", action="store_true")

    def help(self):
        return self.arg_parser.print_help()

    def get_requirement(self):
        args = self.arg_parser.parse_args()
        if args.help:
            self.help()
            exit(0)
        return args

    def replace(self, key, value):
        if not hasattr(self, "payload"):
            raise Exception("Payload not set, Cannot replace")
        self.payload = self.payload.replace(key, value)
        log.debug(f"Payload after replace: {self.payload}")
        return self
    
    def prefix(self, prefix):
        if not hasattr(self, "payload"):
            raise Exception("Payload not set, Cannot prefix")
        self.payload = prefix + self.payload
        return self
    
    def suffix(self, suffix):
        if not hasattr(self, "payload"):
            raise Exception("Payload not set, Cannot suffix")
        self.payload = self.payload + suffix
        return self

    def set_payload(self, payload):
        mode = self.mode
        self.raw_payload = payload
        if mode == PAYLOAD_TYPE.NONE:
            self.payload = payload
        elif mode == PAYLOAD_TYPE.QUOTE_PLUS:
            self.payload = urllib.parse.quote_plus(payload)
        elif mode == PAYLOAD_TYPE.QUOTE:
            self.payload = urllib.parse.quote(payload)
        elif mode == PAYLOAD_TYPE.HEX:
            self.payload = ""
            for c in payload:
                self.payload += hex(ord(c)).replace("0x", "%")
        elif mode == PAYLOAD_TYPE.HEX_UPCASE:
            self.payload = ""
            for c in payload:
                self.payload += hex(ord(c)).replace("0x", "%").upper()
        else:
            log.error(f"Unknown mode: {mode}")
        self.log(f"Payload set to: {self.payload}")
        return self

    def generate(self):
        if not hasattr(self, "payload"):
            log.error("Payload not set")
            return f"gopher://{self.host}:{self.port}/_"
        generated = f"gopher://{self.host}:{self.port}/_{self.payload}"
        log.debug("Final Generated: " + generated)
        return generated
     
    def debug_dump(self):
        for attr in self.__dict__.keys():
            self.log(f"{attr}: {self.__dict__[attr]}")
        if hasattr(self, "payload"):
            self.log(f"payload: {self.payload}")
        else:
            self.log("payload is empty")
        if hasattr(self, "raw_payload"):
            self.log(f"raw_payload: {self.raw_payload}")
        else:
            self.log("raw_payload is empty")

    def notice(self, msg):
        print("\033[93m" + msg + "\033[0m")

    def tailcall(self):
        pass

    def wizard(self, message, field):
        self.__setattr__(field, input("\033[96m" + message + "\033[0m"))