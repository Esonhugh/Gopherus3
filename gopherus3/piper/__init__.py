import re


class LineN:
    def pipe(self, line):
        return re.sub(r"%0d%0a", "%0A", line, flags=re.IGNORECASE)


class LineRN:
    def pipe(self, line):
        return re.sub(r"(?<!%0d)%0a", "%0D%0A", line, flags=re.IGNORECASE)
    
class EndWith00:
    def pipe(self, line):
        return line + '%00'

class Default:
    def pipe(self, line):
        return line