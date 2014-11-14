from Analisys import Scanner
from Analisys import Syntax

fprog = open("input.txt", "r")
program = ""
for line in fprog:
    program += line
program += "\0"

scanner = Scanner(program)
syntax = Syntax(scanner)

try:
    syntax.main_program()
except Exception as e:
    print(e)
else:
    print('Синтаксис не содержит ошибок')