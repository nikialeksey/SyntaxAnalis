from Syntax.Scanner import Scanner
from Analyse.DescendingAnalyse import Syntax

program_file = open("input.txt", "r")
program = ""
for line in program_file:
    program += line
program += "\0"
program_file.close()

scanner = Scanner(program)
syntax = Syntax(scanner)

try:
    syntax.main_program()
except Exception as e:
    print(e)
else:
    print('Синтаксис не содержит ошибок')
