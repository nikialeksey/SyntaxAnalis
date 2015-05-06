from Syntax.Scanner import Scanner
from Analyse.LL1 import LL1
# from subprocess import call

program_file = open("input.txt", "r")
program = ""
for line in program_file:
    program += line
program += "\0"
program_file.close()

scanner = Scanner(program)
syntax = LL1(scanner)

try:
    syntax.run()
except Exception as e:
    print(e)
else:
    print('Синтаксис не содержит ошибок')

# syntax.semantic_tree.write('semantic.dot')
# call(["C:\\Python27\\python.exe", "draw_semantic_graph.py"])
