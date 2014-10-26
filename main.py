from Analisys import Scanner
from Analisys import Syntax
from Analisys import SyntaxException
import LexemId as lId

fprog = open("input.txt", "r")
program = ""
for line in fprog:
    program += line
program += "\0"

scanner = Scanner(program)
syntax = Syntax(scanner)

try:
    syntax.main_program()
except SyntaxException as e:
    print(e)
else:
    print('Синтаксис не содержит ошибок')