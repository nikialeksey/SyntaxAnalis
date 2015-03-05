import LexemId as lId


class Scanner:
    def __init__(self, program):
        self.program = program
        self.lexemeId = lId.TStart
        self.lexeme = ""
        self.__pointer = 0
        self.location = [{'line': 0, 'position': 0}]

    def get_pointer(self):
        return self.__pointer

    def set_pointer(self, pointer):
        if 0 <= pointer < len(self.program):
            self.__pointer = pointer

    def inc_pointer(self):
        self.__pointer += 1
        self.__update_pointer_location()

    def __iter__(self):
        return self

    def __next__(self):
        lexeme_id = self.next_lexeme()
        if lexeme_id == lId.TEndFile:
            raise StopIteration
        return lexeme_id

    def next_lexeme(self):
        p = self.program
        self.lexeme = ""
        self.__ignore_symbol()

        if p[self.__pointer] == "\0":
            self.lexemeId = lId.TEndFile
            return self.lexemeId

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
            self.__put_next_char_into_lexeme_buffer()
            self.lexemeId = lId.TOpen
        elif p[self.__pointer] == ")":
            self.__put_next_char_into_lexeme_buffer()
            self.lexemeId = lId.TClose
        elif p[self.__pointer] == "{":
            self.__put_next_char_into_lexeme_buffer()
            self.lexemeId = lId.TOpenFigure
        elif p[self.__pointer] == "}":
            self.__put_next_char_into_lexeme_buffer()
            self.lexemeId = lId.TCloseFigure
        elif p[self.__pointer] == ",":
            self.__put_next_char_into_lexeme_buffer()
            self.lexemeId = lId.TComma
        elif p[self.__pointer] == ";":
            self.__put_next_char_into_lexeme_buffer()
            self.lexemeId = lId.TSemicolon
        elif p[self.__pointer] == "+":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "+":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TPlusPlus
            elif p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TPlusAssign
            else:
                self.lexemeId = lId.TPlus
        elif p[self.__pointer] == "-":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "-":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TMinusMinus
            elif p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TMinusAssign
            else:
                self.lexemeId = lId.TMinus
        elif p[self.__pointer] == "*":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TMinusAssign
            else:
                self.lexemeId = lId.TMul
        elif p[self.__pointer] == "/":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TDivAssign
            else:
                self.lexemeId = lId.TDiv
        elif p[self.__pointer] == "%":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TModAssign
            else:
                self.lexemeId = lId.TMod
        elif p[self.__pointer] == "<":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TLessEq
            else:
                self.lexemeId = lId.TLess
        elif p[self.__pointer] == ">":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TGreaterEq
            else:
                self.lexemeId = lId.TGreater
        elif p[self.__pointer] == "=":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TEq
            else:
                self.lexemeId = lId.TAssign
        elif p[self.__pointer] == "!":
            self.__put_next_char_into_lexeme_buffer()
            if p[self.__pointer] == "=":
                self.__put_next_char_into_lexeme_buffer()
                self.lexemeId = lId.TUnEq
            else:
                self.lexemeId = lId.TError
        else:
            self.__put_next_char_into_lexeme_buffer()
            self.lexemeId = lId.TError

        if self.lexemeId == lId.TId:
            self.lexemeId = self.__identifier_recognition(self.lexeme)
        return self.lexemeId

    def __identifier_recognition(self, lexeme):
        for type in lId.keyWords:
            if lexeme == lId.keyWords[type]:
                return type
        return lId.TId

    def __put_next_char_into_lexeme_buffer(self):
        self.lexeme += self.program[self.__pointer]
        self.inc_pointer()

    def __num10(self):
        p = self.program
        while "0" <= p[self.__pointer] <= "9":
            self.__put_next_char_into_lexeme_buffer()

    def __num16(self):
        p = self.program
        self.__put_next_char_into_lexeme_buffer()
        self.__put_next_char_into_lexeme_buffer()
        while "0" <= p[self.__pointer] <= "9" or "a" <= p[self.__pointer] <= "f" or "A" <= p[self.__pointer] <= "F":
            self.__put_next_char_into_lexeme_buffer()

    def __identifier(self):
        p = self.program
        while "a" <= p[self.__pointer] <= "z" or "A" <= p[self.__pointer] <= "Z" or p[self.__pointer] == "_" or "0" <= \
                p[
                    self.__pointer] <= "9":
            self.__put_next_char_into_lexeme_buffer()

    def __ignore_symbol(self):
        p = self.program
        while p[self.__pointer] == " " or p[self.__pointer] == "\t" or p[self.__pointer] == "\n":
            self.inc_pointer()

        if p[self.__pointer] == "/" and p[self.__pointer + 1] == "/":
            self.inc_pointer()
            self.inc_pointer()
            self.__ignore_one_line_comment()
        if p[self.__pointer] == "/" and p[self.__pointer + 1] == "*":
            self.inc_pointer()
            self.inc_pointer()
            self.__ignore_multi_line_comment()
        if p[self.__pointer] == " " or p[self.__pointer] == "\t" or p[self.__pointer] == "\n":
            self.__ignore_symbol()

    def __update_pointer_location(self):
        if self.__pointer == 0:
            self.location[self.__pointer] = {'line': 0, 'position': 0}
        else:
            cur_line = self.location[self.__pointer - 1]['line']
            cur_position = self.location[self.__pointer - 1]['position'] + 1
            if self.program[self.__pointer - 1] == "\n":
                cur_line += 1
                cur_position = 0
            if self.__pointer < len(self.location):
                return
            self.location.append({'line': cur_line, 'position': cur_position})

    def __ignore_one_line_comment(self):
        p = self.program
        while p[self.__pointer] != "\n" and p[self.__pointer] != "\0":
            self.inc_pointer()

    def __ignore_multi_line_comment(self):
        p = self.program
        while p[self.__pointer] != "\0" and not (p[self.__pointer] == "*" and p[self.__pointer + 1] == "/"):
            self.inc_pointer()
        if p[self.__pointer] != "\0":
            self.inc_pointer()
            self.inc_pointer()

    def get_pointer_line(self):
        return self.location[self.get_pointer()]['line'] + 1

    def get_pointer_position(self):
        return self.location[self.get_pointer()]['position'] + 1
