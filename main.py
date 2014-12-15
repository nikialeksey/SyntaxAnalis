from Analisys import Scanner
from Analisys import Syntax
from Analisys import LL1
from Analisys import AscendingAnalise

fprog = open("input.txt", "r")
program = ""
for line in fprog:
    program += line
program += "\0"
fprog.close()

scanner = Scanner(program)
# syntax = Syntax(scanner)
# syntax = LL1(scanner)
syntax = AscendingAnalise(scanner)

try:
    syntax.run()
except Exception as e:
    print(e)
else:
    print('Синтаксис не содержит ошибок')
