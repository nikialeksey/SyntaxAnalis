import LexemId as lId


class Scanner:
    def __init__(self, program):
        self.program = program
        self.lexemeId = lId.TStart
        self.lexeme = ""
        self.__pointer = 0

    def __iter__(self):
        return self

    def __next__(self):
        p = self.program
        self.lexeme = ""
        self.__ignoreSymbol()

        if p[self.__pointer] == "\0":
            self.lexemeId = lId.TEndFile
            raise StopIteration

        if "0" <= p[self.__pointer] <= "9":
            start = p[self.__pointer: self.__pointer + 2]
            if start == "0x" or start == "0X":
                self.__num16()
                self.lexemeId = lId.TNum16
            else:
                self.__num10()
                self.lexemeId = lId.TNum10
        elif "a" <= p[self.__pointer] <= "z" or "A" <= p[self.__pointer] <= "Z" or p[self.__pointer] == "_":
            self.__identifier()
            self.lexemeId = lId.TId
        elif p[self.__pointer] == "(":
            self.__putNextCharIntoLexemBuffer()
            self.lexemeId = lId.TOpen
        elif p[self.__pointer] == ")":
            self.__putNextCharIntoLexemBuffer()
            self.lexemeId = lId.TClose
        elif p[self.__pointer] == "{":
            self.__putNextCharIntoLexemBuffer()
            self.lexemeId = lId.TOpenFigure
        elif p[self.__pointer] == "}":
            self.__putNextCharIntoLexemBuffer()
            self.lexemeId = lId.TCloseFigure
        elif p[self.__pointer] == ",":
            self.__putNextCharIntoLexemBuffer()
            self.lexemeId = lId.TComma
        elif p[self.__pointer] == ";":
            self.__putNextCharIntoLexemBuffer()
            self.lexemeId = lId.TSemicolon
        elif p[self.__pointer] == "+":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "+":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TPlusPlus
            elif p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TPlusAssign
            else:
                self.lexemeId = lId.TPlus
        elif p[self.__pointer] == "-":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "-":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TMinusMinus
            elif p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TMinusAssign
            else:
                self.lexemeId = lId.TMinus
        elif p[self.__pointer] == "*":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TMinusAssign
            else:
                self.lexemeId = lId.TMul
        elif p[self.__pointer] == "/":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TDivAssign
            else:
                self.lexemeId = lId.TDiv
        elif p[self.__pointer] == "%":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TModAssign
            else:
                self.lexemeId = lId.TMod
        elif p[self.__pointer] == "<":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TLessEq
            else:
                self.lexemeId = lId.TLess
        elif p[self.__pointer] == ">":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TGreaterEq
            else:
                self.lexemeId = lId.TGreater
        elif p[self.__pointer] == "=":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TEq
            else:
                self.lexemeId = lId.TAssign
        elif p[self.__pointer] == "!":
            self.__putNextCharIntoLexemBuffer()
            if p[self.__pointer] == "=":
                self.__putNextCharIntoLexemBuffer()
                self.lexemeId = lId.TUnEq
            else:
                self.lexemeId = lId.TError
        else:
            self.__putNextCharIntoLexemBuffer()
            self.lexemeId = lId.TError
        return self.lexemeId

    def __putNextCharIntoLexemBuffer(self):
        self.lexeme += self.program[self.__pointer]
        self.__pointer += 1

    def __num10(self):
        p = self.program
        while "0" <= p[self.__pointer] <= "9":
            self.__putNextCharIntoLexemBuffer()

    def __num16(self):
        p = self.program
        self.__putNextCharIntoLexemBuffer()
        self.__putNextCharIntoLexemBuffer()
        while "0" <= p[self.__pointer] <= "9" or "a" <= p[self.__pointer] <= "f" or "A" <= p[self.__pointer] <= "F":
            self.__putNextCharIntoLexemBuffer()

    def __identifier(self):
        p = self.program
        while "a" <= p[self.__pointer] <= "z" or "A" <= p[self.__pointer] <= "Z" or p[self.__pointer] == "_" or "0" <= p[
            self.__pointer] <= "9":
            self.__putNextCharIntoLexemBuffer()

    def __ignoreSymbol(self):
        p = self.program
        while p[self.__pointer] == " " or p[self.__pointer] == "\t" or p[self.__pointer] == "\n":
            self.__pointer += 1
        if p[self.__pointer] == "/" and p[self.__pointer + 1] == "/":
            self.__pointer += 2
            self.__ignoreOneLineComment()
        if p[self.__pointer] == "/" and p[self.__pointer + 1] == "*":
            self.__pointer += 2
            self.__ignoreMultiLineComment()
        if p[self.__pointer] == " " or p[self.__pointer] == "\t" or p[self.__pointer] == "\n":
            self.__ignoreSymbol()

    def __ignoreOneLineComment(self):
        p = self.program
        while p[self.__pointer] != "\n" and p[self.__pointer] != "\0":
            self.__pointer += 1

    def __ignoreMultiLineComment(self):
        p = self.program
        while p[self.__pointer] != "*" and p[self.__pointer + 1] != "/" and p[self.__pointer] != "\0":
            self.__pointer += 1
        if p[self.__pointer] != "\0":
            self.__pointer += 2

    # def get


class Syntax:
    def __init__(self, scanner):
        self.sc = scanner

    def mainProgramm(self):
        sc = self.sc
        if sc.lexemId == lId.TEndFile:
            return


    ...


if __name__ == "__main__":
    ...