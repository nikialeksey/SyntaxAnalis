from Syntax.Scanner import Scanner
from Analyse.LL1 import LL1
from Analyse.DescendingAnalyse import DescendingAnalyse
from subprocess import call
from asm.generator import ASMGenerator

program_file = open("input.txt")
program = ""
for line in program_file:
    program += line
program += "\0"
program_file.close()

scanner = Scanner(program)
syntax = LL1(scanner)
# syntax = DescendingAnalyse(scanner)

try:
    syntax.run()
    # syntax.main_program()
except Exception as e:
    print(e)
else:
    asm = ASMGenerator(syntax.semantic_tree, 'trio.txt', 'program.asm')
    asm.generate()
    print('Синтаксис не содержит ошибок')


# linear optimization
# for _ in range(10):
#     syntax.linear_optimize()
#     with open('optimized_trio.txt') as f:
#         trio = open('trio.txt', 'w')
#         for line in f:
#             trio.write(line)
#         trio.close()

# cycle optimization
# syntax.cycle_optimization()

syntax.semantic_tree.write('semantic.dot')
call(["C:\\Python27\\python.exe", "draw_semantic_graph.py"])
