import argparse
import logging as log

from enum import Enum
from .encoding import percent_encode_bytes, quote_payload, quote_plus_payload


class PAYLOAD_TYPE(Enum):
    NONE = "NONE"
    QUOTE_PLUS = "QUOTE_PLUS"
    QUOTE = "QUOTE"
    QUOTE_SAFE = "QUOTE_SAFE"
    HEX = "HEX"
    HEX_UPCASE = "HEX_UPCASE"


map_payload_type = {
    "NONE": PAYLOAD_TYPE.NONE,
    "QUOTE_PLUS": PAYLOAD_TYPE.QUOTE_PLUS,
    "QUOTE": PAYLOAD_TYPE.QUOTE,
    "QUOTE_SAFE": PAYLOAD_TYPE.QUOTE_SAFE,
    "HEX": PAYLOAD_TYPE.HEX,
    "HEX_UPCASE": PAYLOAD_TYPE.HEX_UPCASE,
}


class GENERATOR(object):
    default_port = 12345
    default_options = {
        "port": 0,
        "host": "127.1",
        "mode": PAYLOAD_TYPE.QUOTE_PLUS,
    }

    def __init__(self, parser=None, options=None):
        self.arg_parser = parser or argparse.ArgumentParser(add_help=False)
        normalized_options = dict(self.default_options)
        if options:
            normalized_options.update(options)
        self.argv = normalized_options.pop("argv", None)
        if normalized_options.get("port", 0) == 0:
            normalized_options["port"] = self.default_port
        for key, value in normalized_options.items():
            self.__setattr__(key, value)

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

    def set_requirement(self, requirement=None):
        self.requirement = list(requirement or [])
        for req in self.requirement:
            if req == "mode":
                self.arg_parser.add_argument(f"--mode", help=f"mode value", default="QUOTE_PLUS", choices=map_payload_type.keys())
            else:
                self.arg_parser.add_argument(f"--{req}", help=f"{req} value", default="")
        self.arg_parser.add_argument("-h","--help", help="show this help message", action="store_true")

    def help(self):
        return self.arg_parser.print_help()

    def get_requirement(self):
        args = self.arg_parser.parse_args(self.argv)
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

    def encode_payload(self, payload):
        mode = self.mode
        if mode == PAYLOAD_TYPE.NONE:
            return payload if isinstance(payload, str) else payload.decode("latin-1")
        if mode == PAYLOAD_TYPE.QUOTE_PLUS:
            return quote_plus_payload(payload)
        if mode == PAYLOAD_TYPE.QUOTE:
            return quote_payload(payload, safe="/")
        if mode == PAYLOAD_TYPE.QUOTE_SAFE:
            return quote_payload(payload)
        if mode == PAYLOAD_TYPE.HEX:
            return percent_encode_bytes(payload)
        if mode == PAYLOAD_TYPE.HEX_UPCASE:
            return percent_encode_bytes(payload, uppercase=True)
        log.error(f"Unknown mode: {mode}")
        return payload

    def set_payload(self, payload):
        self.raw_payload = payload
        self.payload = self.encode_payload(payload)
        self.log(f"Payload set to: {self.payload}")
        return self

    def set_url_payload(self, payload):
        self.set_mode(PAYLOAD_TYPE.QUOTE_SAFE)
        return self.set_payload(payload)

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
