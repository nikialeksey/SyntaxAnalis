from Analisys import Scanner
import LexemId as lId

fprog = open("input.txt", "r")
program = ""
for line in fprog:
    program += line
program += "\0"

sc = Scanner(program)
types = []
image = []
for typeLexem in iter(sc):
    types.append(lId.lexemIdToStr[typeLexem])
    image.append(sc.lexeme)

print(types)
print(image)