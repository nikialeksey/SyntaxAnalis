from Syntax.Scanner import Scanner
from Analyse.DescendingAnalyse import DescendingAnalyse
from subprocess import call

program_file = open("input.txt", "r")
program = ""
for line in program_file:
    program += line
program += "\0"
program_file.close()

scanner = Scanner(program)
syntax = DescendingAnalyse(scanner)

try:
    syntax.main_program()
except Exception as e:
    print(e)
else:
    print('Синтаксис не содержит ошибок')

syntax.semantic_tree.write('semantic.dot')
call(["C:\\Python27\\python.exe", "draw_semantic_graph.py"])
