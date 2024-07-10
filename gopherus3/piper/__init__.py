class LineN: 
    def pipe(self, line):
        return line.replace("%%0d%%0a", '%%0d')


class LineRN:
    def pipe(self, line):
        return line.replace("%%0a", '%%0d%%0a')
    
class EndWith00:
    def pipe(self, line):
        return line + '%%00'

class Default:
    def pipe(self, line):
        return line