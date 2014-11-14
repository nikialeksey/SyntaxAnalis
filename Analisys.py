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


class SyntaxExceptionOperand(SyntaxException):
    def __init__(self, line, position, founded):
        super(SyntaxExceptionOperand, self).__init__(line, position, "операнд", founded)


class SyntaxExceptionWhile(SyntaxException):
    def __init__(self, line, position, founded):
        super(SyntaxExceptionWhile, self).__init__(line, position, "while", founded)


class SemanticException(Exception):
    def __init__(self, line, position, type_lexeme, lexeme):
        self.line = line
        self.position = position
        self.type_lexeme = type_lexeme
        self.lexeme = lexeme


class SemanticExceptionUndescribe(SemanticException):
    def __init__(self, line, position, type_lexeme, lexeme):
        super(SemanticExceptionUndescribe, self).__init__(line, position, type_lexeme, lexeme)

    def __str__(self):
        return "В строке " + str(self.line) + " в позиции " + str(self.position) +\
                " не описана " + str(self.type_lexeme) + " " + str(self.lexeme)


class SemanticExceptionUndescribeVar(SemanticExceptionUndescribe):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionUndescribeVar, self).__init__(line, position, "переменная", lexeme)


class SemanticExceptionUndescribeFunction(SemanticExceptionUndescribe):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionUndescribeFunction, self).__init__(line, position, "функция", lexeme)


class Node:
    def __init__(self, type_object, type_data, lexeme, count_parameter):
        self.type_object = type_object
        self.type_data = type_data
        self.lexeme = lexeme
        self.count_parameter = count_parameter

    def set_left_node(self, node):
        self.__left = node

    def set_right_node(self, node):
        self.__right = node

    def set_parent_node(self, node):
        self.__parent = node

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def get_parent(self):
        return self.__parent


class SemanticTree:
    def __init__(self):
        self.variable_object = 0
        self.function_object = 1
        self.special_object = 2
        self.dummy = Node(-1, -1, -1, -1)
        root = Node(self.special_object, -1, -1, -1)

        self.__root = root
        self.__root.set_left_node(self.dummy)
        self.__root.set_right_node(self.dummy)
        self.__root.set_parent_node(self.dummy)
        self.pointer = root
        self.__current_type = lId.TInt
        self.current_count_parameter = 0

    def get_current_type(self):
        return self.__current_type

    def set_current_type(self, current_type):
        self.__current_type = current_type

    def go_left(self):
        if self.pointer.get_left() != self.dummy:
            self.pointer = self.pointer.get_left()

    def go_right(self):
        if self.pointer.get_right() != self.dummy:
            self.pointer = self.pointer.get_right()

    def is_describe_var_early(self, lexeme):
        p = self.pointer
        while p != self.__root:
            if p.lexeme == lexeme and p.type_object == self.variable_object:
                return True
            p = p.get_parent()
        return False

    def is_describe_function_early(self, lexeme, count_parameter):
        p = self.pointer
        while p != self.__root:
            if p.lexeme == lexeme and p.count_parameter == count_parameter and p.type_object == self.function_object:
                return True
            p = p.get_parent()
        return False

    def is_overlay_lexeme(self, lexeme):
        p = self.pointer
        while p.type_object != self.special_object:
            if p.lexeme == lexeme:
                return True
            p = p.get_parent()
        return False

    def add_neighbor(self, type_object, lexeme, count_parameter):
        neighbor = Node(type_object, self.__current_type, lexeme, count_parameter)
        neighbor.set_left_node(self.dummy)
        neighbor.set_right_node(self.dummy)
        neighbor.set_parent_node(self.pointer)
        self.pointer.set_left_node(neighbor)
        self.pointer = neighbor

    def add_special_node(self):
        special = Node(self.special_object, -1, -1, -1)
        special.set_left_node(self.dummy)
        special.set_right_node(self.dummy)
        special.set_parent_node(self.pointer)
        self.pointer.set_right_node(special)
        self.pointer = special

    def add_child(self, type_object, lexeme, count_parameter):
        self.add_special_node()
        self.add_neighbor(type_object, self.__current_type, lexeme, count_parameter)


class Syntax:
    def __init__(self, scanner):
        self.scanner = scanner
        self.semantic_tree = SemanticTree()

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
            if self.is_data_type(lexeme_data_type) and \
                            lexeme_name_var == lId.TId and \
                            lexeme_open_bracket != lId.TOpen:
                self.description_var()
            else:
                self.description_function()

    def description_var(self):
        sc = self.scanner
        lexeme_data_type = sc.next_lexeme()
        if not self.is_data_type(lexeme_data_type):
            raise SyntaxExceptionType(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        self.semantic_tree.set_current_type(lexeme_data_type)
        # semantic

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

        # semantic
        self.semantic_tree.add_neighbor(self.semantic_tree.variable_object, sc.lexeme, 0)
        # semantic

        old_pointer = sc.get_pointer()
        lexeme_assign = sc.next_lexeme()
        if lexeme_assign == lId.TAssign:
            self.expression()
        else:
            sc.set_pointer(old_pointer)

    def expression(self):
        self.a2()
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_assign = sc.next_lexeme()
        while lexeme_assign == lId.TAssign or lexeme_assign == lId.TPlusAssign or lexeme_assign == lId.TMinusAssign or \
                lexeme_assign == lId.TMulAssign or lexeme_assign == lId.TDivAssign or lexeme_assign == lId.TModAssign:
            self.a2()
            old_pointer = sc.get_pointer()
            lexeme_assign = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a2(self):
        self.a3()
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_equal = sc.next_lexeme()
        while lexeme_equal == lId.TEq or lexeme_equal == lId.TUnEq:
            self.a3()
            old_pointer = sc.get_pointer()
            lexeme_equal = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a3(self):
        self.a4()
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_lege = sc.next_lexeme()
        while lexeme_lege == lId.TLess or lexeme_lege == lId.TGreater or \
                lexeme_lege == lId.TLessEq or lexeme_lege == lId.TGreaterEq:
            self.a4()
            old_pointer = sc.get_pointer()
            lexeme_lege = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a4(self):
        self.a5()
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_plus_minus = sc.next_lexeme()
        while lexeme_plus_minus == lId.TPlus or lexeme_plus_minus == lId.TMinus:
            self.a5()
            old_pointer = sc.get_pointer()
            lexeme_plus_minus = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a5(self):
        self.a6()
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_mul_div_mod = sc.next_lexeme()
        while lexeme_mul_div_mod == lId.TMul or lexeme_mul_div_mod == lId.TDiv or lexeme_mul_div_mod == lId.TMod:
            self.a6()
            old_pointer = sc.get_pointer()
            lexeme_mul_div_mod = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a6(self):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_pref = sc.next_lexeme()
        if lexeme_pref == lId.TMinus or lexeme_pref == lId.TPlus or \
                lexeme_pref == lId.TMinusMinus or lexeme_pref == lId.TPlusPlus:
            self.a7()
        else:
            sc.set_pointer(old_pointer)
            self.a7()
            old_pointer = sc.get_pointer()
            lexeme_suff = sc.next_lexeme()
            if lexeme_suff != lId.TPlusPlus and lexeme_suff != lId.TMinusMinus:
                sc.set_pointer(old_pointer)

    def a7(self):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_open_bracket = sc.next_lexeme()
        if lexeme_open_bracket == lId.TOpen:
            self.expression()
            lexeme_close_bracket = sc.next_lexeme()
            if lexeme_close_bracket != lId.TClose:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)
        elif sc.next_lexeme() == lId.TOpen:
            sc.set_pointer(old_pointer)
            self.call_function()
        else:
            sc.set_pointer(old_pointer)
            lexeme_operand = sc.next_lexeme()
            if lexeme_operand != lId.TId and lexeme_operand != lId.TNum10 and lexeme_operand != lId.TNum16:
                raise SyntaxExceptionOperand(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

            # semantic
            if lexeme_operand == lId.TId and (not self.semantic_tree.is_describe_var_early(sc.lexeme)):
                raise SemanticExceptionUndescribeVar(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
            # semantic

    def description_function(self):
        sc = self.scanner
        lexeme_data_type = sc.next_lexeme()
        if not self.is_data_type(lexeme_data_type):
            raise SyntaxExceptionType(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        self.semantic_tree.set_current_type(lexeme_data_type)
        # semantic

        self.head_function()
        self.body_function()

    def head_function(self):
        sc = self.scanner
        lexeme_id = sc.next_lexeme()
        if lexeme_id != lId.TId:
            raise SyntaxExceptionIdentifier(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        self.semantic_tree.add_neighbor(self.semantic_tree.function_object, sc.lexeme, 0)
        self.semantic_tree.current_count_parameter = 0
        pointer = self.semantic_tree.pointer
        self.semantic_tree.add_special_node()
        # semantic

        lexeme_open_bracket = sc.next_lexeme()
        if lexeme_open_bracket != lId.TOpen:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "(", sc.lexeme)
        self.enum_param()

        # semantic
        pointer.count_parameter = self.semantic_tree.current_count_parameter
        # semantic

        lexeme_close_bracket = sc.next_lexeme()
        if lexeme_close_bracket != lId.TClose:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)

    def enum_param(self):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme = sc.next_lexeme()
        if lexeme != lId.TClose:
            sc.set_pointer(old_pointer)
            self.param()

            old_pointer = sc.get_pointer()
            lexeme = sc.next_lexeme()
            while lexeme == lId.TComma:
                self.param()
                old_pointer = sc.get_pointer()
                lexeme = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def param(self):
        sc = self.scanner
        lexeme = sc.next_lexeme()
        if not self.is_data_type(lexeme):
            raise SyntaxExceptionType(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        self.semantic_tree.set_current_type(lexeme)
        # semantic

        lexeme = sc.next_lexeme()
        if lexeme != lId.TId:
            raise SyntaxExceptionIdentifier(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        self.semantic_tree.add_neighbor(self.semantic_tree.variable_object, sc.lexeme, 0)
        self.semantic_tree.current_count_parameter += 1
        # semantic

    def call_function(self):
        sc = self.scanner
        lexeme_id = sc.next_lexeme()
        if lexeme_id != lId.TId:
            raise SyntaxExceptionIdentifier(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
        lexeme_open_bracket = sc.next_lexeme()
        if lexeme_open_bracket != lId.TOpen:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "(", sc.lexeme)
        self.enum_operand()
        lexeme_close_bracket = sc.next_lexeme()
        if lexeme_close_bracket != lId.TClose:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)

    def enum_operand(self):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme = sc.next_lexeme()
        if lexeme != lId.TClose:
            sc.set_pointer(old_pointer)
            self.operand()

            old_pointer = sc.get_pointer()
            lexeme = sc.next_lexeme()
            while lexeme == lId.TComma:
                self.operand()
                old_pointer = sc.get_pointer()
                lexeme = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def operand(self):
        sc = self.scanner
        lexeme = sc.next_lexeme()
        if lexeme != lId.TId and lexeme != lId.TNum10 and lexeme != lId.TNum16:
            raise SyntaxExceptionOperand(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

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
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme = sc.next_lexeme()

        while lexeme != lId.TCloseFigure:
            if self.is_data_type(lexeme):
                sc.set_pointer(old_pointer)
                self.description_var()
            else:
                sc.set_pointer(old_pointer)
                self.operator()
            old_pointer = sc.get_pointer()
            lexeme = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def operator(self):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme = sc.next_lexeme()
        if lexeme == lId.TOpenFigure:
            sc.set_pointer(old_pointer)
            self.body_function()
        elif lexeme == lId.TSemicolon:
            ...
        elif lexeme == lId.TDo:
            self.operator()
            lexeme_while = sc.next_lexeme()
            if lexeme_while != lId.TWhile:
                raise SyntaxExceptionWhile(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
            lexeme_open_bracket = sc.next_lexeme()
            if lexeme_open_bracket != lId.TOpen:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "(", sc.lexeme)
            self.expression()
            lexeme_close_bracket = sc.next_lexeme()
            if lexeme_close_bracket != lId.TClose:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)
            lexeme_semicolon = sc.next_lexeme()
            if lexeme_semicolon != lId.TSemicolon:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ";", sc.lexeme)
        elif lexeme == lId.TReturn:
            self.expression()
            lexeme_semicolon = sc.next_lexeme()
            if lexeme_semicolon != lId.TSemicolon:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ";", sc.lexeme)
        else:
            sc.set_pointer(old_pointer)
            self.expression()
            lexeme_semicolon = sc.next_lexeme()
            if lexeme_semicolon != lId.TSemicolon:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ";", sc.lexeme)

    @staticmethod
    def is_data_type(lexeme_id):
        """
        Проверяет тип лексемы c типами данных
        """
        return lexeme_id == lId.TInt or lexeme_id == lId.TShort or lexeme_id == lId.TLong


if __name__ == "__main__":
    print(help(Syntax.main_program))