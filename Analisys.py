from _ctypes import pointer
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
        return self.lexemeId

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
        while p[self.__pointer] != "\0" and not(p[self.__pointer] == "*" and p[self.__pointer + 1] == "/"):
            self.inc_pointer()
        if p[self.__pointer] != "\0":
            self.inc_pointer()
            self.inc_pointer()

    def get_pointer_line(self):
        return self.location[self.get_pointer()]['line'] + 1

    def get_pointer_position(self):
        return self.location[self.get_pointer()]['position'] + 1


class SyntaxException(Exception):
    def __init__(self, line, position, expected, founded):
        self.line = line
        self.position = position
        self.expected = expected
        self.founded = founded

    def __str__(self):
        return "В строке " + str(self.line) + " в позиции " + str(self.position) + " ожидалось - " \
               + str(self.expected) + ", найдено - " + str(self.founded)


class SyntaxExceptionType(SyntaxException):
    def __init__(self, line, position, founded):
        super(SyntaxExceptionType, self).__init__(line, position, "тип данных", founded)


class SyntaxExceptionCharacter(SyntaxException):
    def __init__(self, line, position, character, founded):
        super(SyntaxExceptionCharacter, self).__init__(line, position, character, founded)


class SyntaxExceptionIdentifier(SyntaxException):
    def __init__(self, line, position, founded):
        super(SyntaxExceptionIdentifier, self).__init__(line, position, "идентификатор", founded)


class Syntax:
    def __init__(self, scanner):
        self.scanner = scanner

    def main_program(self):
        sc = self.scanner
        while 1:
            old_pointer = sc.get_pointer()
            if sc.next_lexeme() == lId.TEndFile:
                break
            sc.set_pointer(old_pointer)

            lexeme_data_type = sc.next_lexeme()
            lexeme_name_var = sc.next_lexeme()
            lexeme_open_bracket = sc.next_lexeme()

            sc.set_pointer(old_pointer)
            if (not self.is_data_type(lexeme_data_type)) or \
                            lexeme_name_var != lId.TId or \
                            lexeme_open_bracket != lId.TOpen:
                self.description_var()
            else:
                self.description_function()

    def description_var(self):
        sc = self.scanner
        lexeme_data_type = sc.next_lexeme()
        if lexeme_data_type != lId.TId:
            raise SyntaxExceptionType(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
        self.enum_var()
        lexeme_semicolon = sc.next_lexeme()
        if lexeme_semicolon != lId.TSemicolon:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ";", sc.lexeme)

    def enum_var(self):
        self.head_var()
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_comma = sc.next_lexeme()
        while lexeme_comma == lId.TComma:
            self.head_var()
            old_pointer = sc.get_pointer()
            lexeme_comma = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def head_var(self):
        sc = self.scanner
        lexeme_id = sc.next_lexeme()
        if lexeme_id != lId.TId:
            raise SyntaxExceptionIdentifier(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
        old_pointer = sc.get_pointer()
        lexeme_assign = sc.next_lexeme()
        if lexeme_assign == lId.TAssign:
            self.expression()
        else:
            sc.set_pointer(old_pointer)

    def expression(self):
        ...

    def description_function(self):
        sc = self.scanner
        lexeme_data_type = sc.next_lexeme()
        if lexeme_data_type != lId.TId:
            raise SyntaxExceptionType(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
        self.head_function()
        self.body_function()

    def head_function(self):
        sc = self.scanner
        lexeme_id = sc.next_lexeme()
        if lexeme_id != lId.TId:
            raise SyntaxExceptionIdentifier(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
        lexeme_open_bracket = sc.next_lexeme()
        if lexeme_open_bracket != lId.TOpen:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "(", sc.lexeme)
        lexeme_close_bracket = sc.next_lexeme()
        if lexeme_close_bracket != lId.TClose:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)

    def body_function(self):
        sc = self.scanner
        lexeme_open_figure = sc.next_lexeme()
        if lexeme_open_figure != lId.TOpenFigure:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "{", sc.lexeme)
        self.enum_operator()
        lexeme_close_figure = sc.next_lexeme()
        if lexeme_close_figure != lId.TCloseFigure:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "}", sc.lexeme)

    def enum_operator(self):
        ...

    @staticmethod
    def is_data_type(lexeme_type):
        """
        Проверяет тип лексемы c типами данных
        """
        return lexeme_type == lId.TInt or lexeme_type == lId.TShort or lexeme_type == lId.TLong


if __name__ == "__main__":
    print(help(Syntax.main_program))