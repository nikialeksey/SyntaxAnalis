from Syntax.Scanner import Scanner
from Analyse.DescendingAnalyse import Syntax

fprog = open("input.txt", "r")
program = ""
for line in fprog:
    program += line
program += "\0"
fprog.close()

scanner = Scanner(program)
syntax = Syntax(scanner)

try:
    syntax.main_program()
except Exception as e:
    print(e)
else:
    print('Синтаксис не содержит ошибок')
