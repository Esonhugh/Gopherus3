class LineN: 
    def pipe(self, line):
        return line.replace("%0d%0a", '%0a').replace("%0D%0A", '%0A')


class LineRN:
    def pipe(self, line):
        return line.replace("%0a", '%0d%0a').replace("%0A", '%0D%0A')
    
class EndWith00:
    def pipe(self, line):
        return line + '%00'

class Default:
    def pipe(self, line):
        return line