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
                " неизвестная " + str(self.type_lexeme) + " " + str(self.lexeme)


class SemanticExceptionUndescribeVar(SemanticExceptionUndescribe):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionUndescribeVar, self).__init__(line, position, "переменная", lexeme)


class SemanticExceptionUndescribeFunction(SemanticExceptionUndescribe):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionUndescribeFunction, self).__init__(line, position, "функция", lexeme)


class SemanticExceptionOverlay(SemanticException):
    def __init__(self, line, position, type_lexeme, lexeme):
        super(SemanticExceptionOverlay, self).__init__(line, position, type_lexeme, lexeme)

    def __str__(self):
        return "В строке " + str(self.line) + " в позиции " + str(self.position) +\
                " ожидалась " + str(self.type_lexeme) + " " + str(self.lexeme)


class SemanticExceptionOverlayVar(SemanticExceptionOverlay):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionOverlayVar, self).__init__(line, position, "переменная", lexeme)


class SemanticExceptionOverlayFunction(SemanticExceptionOverlay):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionOverlayFunction, self).__init__(line, position, "функция", lexeme)


class SemanticExceptionOverlayFunctionParam(SemanticExceptionOverlay):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionOverlayFunctionParam, self).__init__(line, position, "функция", lexeme)

    def __str__(self):
        return "В строке " + str(self.line) + " в позиции " + str(self.position) +\
                " не правильное количество параметров у функции " + str(self.lexeme)


class SemanticExceptionOverlayLexeme(SemanticException):
    def __init__(self, line, position, lexeme):
        super(SemanticExceptionOverlayLexeme, self).__init__(line, position, "лексема", lexeme)

    def __str__(self):
        return "В строке " + str(self.line) + " в позиции " + str(self.position) +\
                " дважды используемая лексема " + str(self.lexeme)


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

    def go_up(self):
        if self.pointer.get_parent() != self.dummy:
            self.pointer = self.pointer.get_parent()

    def go_out(self):
        p = self.pointer
        while p != self.__root and p.type_object != self.special_object:
            p = p.get_parent()
        if p.type_object == self.special_object:
            p = p.get_parent()
            self.pointer = p

    def is_describe_var_early(self, lexeme_line, lexeme_position, lexeme):
        p = self.pointer
        while p != self.__root:
            if p.lexeme == lexeme:
                if p.type_object == self.variable_object:
                    return True
                else:
                    raise SemanticExceptionOverlayFunction(lexeme_line, lexeme_position, lexeme)
            p = p.get_parent()
        return False

    def is_describe_function_early(self, lexeme_line, lexeme_position, lexeme, count_parameter):
        p = self.pointer
        while p != self.__root:
            if p.lexeme == lexeme:
                if p.type_object != self.function_object:
                    raise SemanticExceptionOverlayVar(lexeme_line, lexeme_position, lexeme)
                if p.count_parameter != count_parameter:
                    raise SemanticExceptionOverlayFunctionParam(lexeme_line, lexeme_position, lexeme)
                return True
            p = p.get_parent()
        return False

    def is_overlay_lexeme(self, lexeme):
        p = self.pointer
        while p.type_object != self.special_object and p != self.__root:
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
        self.go_left()

    def add_special_node(self):
        special = Node(self.special_object, -1, -1, -1)
        special.set_left_node(self.dummy)
        special.set_right_node(self.dummy)
        special.set_parent_node(self.pointer)
        self.pointer.set_right_node(special)
        self.go_right()

    def add_child(self, type_object, lexeme, count_parameter):
        self.add_special_node()
        self.add_neighbor(type_object, lexeme, count_parameter)


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

        if self.semantic_tree.is_overlay_lexeme(sc.lexeme):
            raise SemanticExceptionOverlayLexeme(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        lexeme = sc.lexeme

        # semantic
        self.semantic_tree.add_neighbor(self.semantic_tree.variable_object, lexeme, 0)
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
            if lexeme_operand == lId.TId:
                if not self.semantic_tree.is_describe_var_early(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme):
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

        # semantic
        self.semantic_tree.go_out()
        # semantic

    def head_function(self):
        sc = self.scanner
        lexeme_id = sc.next_lexeme()
        if lexeme_id != lId.TId:
            raise SyntaxExceptionIdentifier(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        if self.semantic_tree.is_overlay_lexeme(sc.lexeme):
            raise SemanticExceptionOverlayLexeme(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
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
        if self.semantic_tree.is_overlay_lexeme(sc.lexeme):
            raise SemanticExceptionOverlayVar(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
        self.semantic_tree.add_neighbor(self.semantic_tree.variable_object, sc.lexeme, 0)
        self.semantic_tree.current_count_parameter += 1
        # semantic

    def call_function(self):
        sc = self.scanner
        lexeme_id = sc.next_lexeme()
        if lexeme_id != lId.TId:
            raise SyntaxExceptionIdentifier(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        lexeme = sc.lexeme
        lexeme_line = sc.get_pointer_line()
        lexeme_position = sc.get_pointer_position()
        self.semantic_tree.current_count_parameter = 0
        # semantic

        lexeme_open_bracket = sc.next_lexeme()
        if lexeme_open_bracket != lId.TOpen:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "(", sc.lexeme)
        self.enum_operand()
        lexeme_close_bracket = sc.next_lexeme()
        if lexeme_close_bracket != lId.TClose:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)

        # semantic
        if not self.semantic_tree.is_describe_function_early(lexeme_line, lexeme_position, lexeme, self.semantic_tree.current_count_parameter):
            raise SemanticExceptionUndescribeFunction(lexeme_line, lexeme_position, lexeme)
        # semantic

    def enum_operand(self):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme = sc.next_lexeme()
        if lexeme != lId.TClose:
            sc.set_pointer(old_pointer)
            self.expression()

            # semantic
            self.semantic_tree.current_count_parameter += 1
            # semantic

            old_pointer = sc.get_pointer()
            lexeme = sc.next_lexeme()
            while lexeme == lId.TComma:
                self.expression()
                # semantic
                self.semantic_tree.current_count_parameter += 1
                # semantic
                old_pointer = sc.get_pointer()
                lexeme = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def body_function(self):
        sc = self.scanner
        lexeme_open_figure = sc.next_lexeme()
        if lexeme_open_figure != lId.TOpenFigure:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "{", sc.lexeme)

        # semantic
        self.semantic_tree.add_special_node()
        # semantic

        self.enum_operator()
        lexeme_close_figure = sc.next_lexeme()
        if lexeme_close_figure != lId.TCloseFigure:
            raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), "}", sc.lexeme)

        # semantic
        self.semantic_tree.go_out()
        # semantic

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


class LL1Exception(Exception):
    def __init__(self, line, position, message):
        self.line = line
        self.position = position
        self.message = message

    def __str__(self):
        return "В строке " + str(self.line) + " в позиции " + str(self.position) + " " + str(self.message)

class LL1:
    def __init__(self, scanner):
        self.scanner = scanner
        self.stack = []
        self.stack.append(lId.TEndFile)
        self.stack.append('main_program')

    def __getitem__(self, item):
        if item == 'main_program':
            return self.main_program
        elif item == 'description':
            return self.description
        elif item == 'EV':
            return self.EV
        elif item == 'head_var':
            return self.head_var
        elif item == 'EVF':
            return self.EVF
        elif item == 'PEVF':
            return self.PEVF
        elif item == 'param':
            return self.param
        elif item == 'body_function':
            return self.body_function
        elif item == 'enum_operator':
            return self.enum_operator
        elif item == 'O':
            return self.O
        elif item == 'operator':
            return self.operator
        elif item == 'expression':
            return self.expression
        elif item == 'eq2':
            return self.eq2
        elif item == 'eq1':
            return self.eq1
        elif item == 'A2':
            return self.A2
        elif item == 'A31':
            return self.A31
        elif item == 'A311':
            return self.A311
        elif item == 'A3':
            return self.A3
        elif item == 'A41':
            return self.A41
        elif item == 'A411':
            return self.A411
        elif item == 'A4':
            return self.A4
        elif item == 'A51':
            return self.A51
        elif item == 'A511':
            return self.A511
        elif item == 'A5':
            return self.A5
        elif item == 'A61':
            return self.A61
        elif item == 'A611':
            return self.A611
        elif item == 'A6':
            return self.A6
        elif item == 'A71':
            return self.A71
        elif item == 'A711':
            return self.A711
        elif item == 'A7':
            return self.A7
        elif item == 'A710':
            return self.A710
        elif item == 'A7110':
            return self.A7110
        elif item == 'EO':
            return self.EO
        elif item == 'enum_operand':
            return self.enum_operand
        else:
            print('Not found ' + str(item))

    def run(self):
        sc = self.scanner
        lexeme = sc.next_lexeme()
        while True:
            l = self.stack.pop()
            # print('stack: ' + str(l) + " lexeme: " + str(lexeme))
            if self.is_terminal(l):
                if lexeme == l or (self.is_data_type(lexeme) and l == lId.TInt):
                    if l == lId.TEndFile:
                        break
                    lexeme = sc.next_lexeme()
                else:
                    raise LL1Exception(sc.get_pointer_line(), sc.get_pointer_position(),\
                               "ожидалась конструкция " + lId.lexemIdToStr[l] + ", найдено " + str(sc.lexeme))
            else:
                self[l](lexeme)

    def main_program(self, lexeme):
        if self.is_data_type(lexeme):
            self.stack.append('main_program')
            self.stack.append('description')
            self.stack.append(lId.TId)
            self.stack.append(lId.TInt)

    def description(self, lexeme):
        if lexeme == lId.TOpen:
            self.stack.append('body_function')
            self.stack.append(lId.TClose)
            self.stack.append('PEVF')
            self.stack.append(lId.TOpen)
        else:
            self.stack.append(lId.TSemicolon)
            self.stack.append('EV')
            self.stack.append('head_var')

    def EV(self, lexeme):
        if lexeme == lId.TComma:
            self.stack.append('EV')
            self.stack.append('head_var')
            self.stack.append(lId.TId)
            self.stack.append(lId.TComma)

    def head_var(self, lexeme):
        if lexeme == lId.TAssign:
            self.stack.append('expression')
            self.stack.append(lId.TAssign)

    def PEVF(self, lexeme):
        if self.is_data_type(lexeme):
            self.stack.append('EVF')
            self.stack.append('param')

    def EVF(self, lexeme):
        if lexeme == lId.TComma:
            self.stack.append('EVF')
            self.stack.append('param')
            self.stack.append(lId.TComma)

    def param(self, lexeme):
        if self.is_data_type(lexeme):
            self.stack.append(lId.TId)
            self.stack.append(lId.TInt)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидался тип данных, найдено " + str(self.scanner.lexeme))

    def body_function(self, lexeme):
        if lexeme == lId.TOpenFigure:
            self.stack.append(lId.TCloseFigure)
            self.stack.append('enum_operator')
            self.stack.append(lId.TOpenFigure)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидался символ '{', найдено " + str(self.scanner.lexeme))

    def enum_operator(self, lexeme):
        if lexeme != lId.TCloseFigure:
            self.stack.append('enum_operator')
            self.stack.append('O')

    def O(self, lexeme):
        if self.is_data_type(lexeme):
            self.stack.append(lId.TSemicolon)
            self.stack.append('EV')
            self.stack.append('head_var')
            self.stack.append(lId.TId)
            self.stack.append(lId.TInt)
        else:
            self.stack.append('operator')

    def operator(self, lexeme):
        if lexeme == lId.TOpenFigure:
            self.stack.append('body_function')
        elif lexeme == lId.TDo:
            self.stack.append(lId.TSemicolon)
            self.stack.append(lId.TClose)
            self.stack.append('expression')
            self.stack.append(lId.TOpen)
            self.stack.append(lId.TWhile)
            self.stack.append('operator')
            self.stack.append(lId.TDo)
        elif lexeme == lId.TReturn:
            self.stack.append(lId.TSemicolon)
            self.stack.append('expression')
            self.stack.append(lId.TReturn)
        elif lexeme == lId.TSemicolon:
            self.stack.append(lId.TSemicolon)
        else:
            self.stack.append(lId.TSemicolon)
            self.stack.append('expression')

    def expression(self, lexeme):
        self.stack.append('eq2')
        self.stack.append('A2')

    def eq2(self, lexeme):
        if lexeme == lId.TAssign or lexeme == lId.TPlusAssign or lexeme == lId.TMinusAssign or\
            lexeme == lId.TMulAssign or lexeme == lId.TDivAssign or lexeme == lId.TModAssign:
            self.stack.append('expression')
            self.stack.append('eq1')

    def eq1(self, lexeme):
        if lexeme == lId.TAssign:
            self.stack.append(lId.TAssign)
        elif lexeme == lId.TPlusAssign:
            self.stack.append(lId.TPlusAssign)
        elif lexeme == lId.TMinusAssign:
            self.stack.append(lId.TMinusAssign)
        elif lexeme == lId.TMulAssign:
            self.stack.append(lId.TMulAssign)
        elif lexeme == lId.TDivAssign:
            self.stack.append(lId.TDivAssign)
        elif lexeme == lId.TModAssign:
            self.stack.append(lId.TModAssign)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидался оператор присваивания, найдено " + str(self.scanner.lexeme))

    def A2(self, lexeme):
        self.stack.append('A31')
        self.stack.append('A3')

    def A31(self, lexeme):
        if lexeme == lId.TEq or lexeme == lId.TUnEq:
            self.stack.append('A31')
            self.stack.append('A3')
            self.stack.append('A311')

    def A311(self, lexeme):
        if lexeme == lId.TEq:
            self.stack.append(lId.TEq)
        elif lexeme == lId.TUnEq:
            self.stack.append(lId.TUnEq)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидалась операция эквивалентности (==, !=), найдено " + str(self.scanner.lexeme))

    def A3(self, lexeme):
        self.stack.append('A41')
        self.stack.append('A4')

    def A41(self, lexeme):
        if lexeme == lId.TLess or lexeme == lId.TLessEq or lexeme == lId.TGreater or lexeme == lId.TGreaterEq:
            self.stack.append('A41')
            self.stack.append('A4')
            self.stack.append('A411')

    def A411(self, lexeme):
        if lexeme == lId.TLess:
            self.stack.append(lId.TLess)
        elif lexeme == lId.TLessEq:
            self.stack.append(lId.TLessEq)
        elif lexeme == lId.TGreater:
            self.stack.append(lId.TGreater)
        elif lexeme == lId.TGreaterEq:
            self.stack.append(lId.TGreaterEq)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидалась операция сравнения (<,>,<=,>=), найдено " + str(self.scanner.lexeme))

    def A4(self, lexeme):
        self.stack.append('A51')
        self.stack.append('A5')

    def A51(self, lexeme):
        if lexeme == lId.TPlus or lexeme == lId.TMinus:
            self.stack.append('A51')
            self.stack.append('A5')
            self.stack.append('A511')

    def A511(self, lexeme):
        if lexeme == lId.TPlus:
            self.stack.append(lId.TPlus)
        elif lexeme == lId.TMinus:
            self.stack.append(lId.TMinus)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидалась знаковая операция (+, -), найдено " + str(self.scanner.lexeme))

    def A5(self, lexeme):
        self.stack.append('A61')
        self.stack.append('A6')

    def A61(self, lexeme):
        if lexeme == lId.TMul or lexeme == lId.TDiv or lexeme == lId.TMod:
            self.stack.append('A61')
            self.stack.append('A6')
            self.stack.append('A611')

    def A611(self, lexeme):
        if lexeme == lId.TMul:
            self.stack.append(lId.TMul)
        elif lexeme == lId.TDiv:
            self.stack.append(lId.TDiv)
        elif lexeme == lId.TMod:
            self.stack.append(lId.TMod)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидалась операция умножения или деления (/, *, %), найдено " + str(self.scanner.lexeme))

    def A6(self, lexeme):
        if lexeme == lId.TPlus or lexeme == lId.TPlusPlus or lexeme == lId.TMinus or lexeme == lId.TMinusMinus:
            self.stack.append('A7')
            self.stack.append('A71')
        else:
            self.stack.append('A711')
            self.stack.append('A7')

    def A71(self, lexeme):
        if lexeme == lId.TPlus:
            self.stack.append(lId.TPlus)
        elif lexeme == lId.TPlusPlus:
            self.stack.append(lId.TPlusPlus)
        elif lexeme == lId.TMinus:
            self.stack.append(lId.TMinus)
        elif lexeme == lId.TMinusMinus:
            self.stack.append(lId.TMinusMinus)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидалась операция инкремента или знаковая (++, --, +, -), найдено " + str(self.scanner.lexeme))

    def A711(self, lexeme):
        if lexeme == lId.TPlusPlus:
            self.stack.append(lId.TPlusPlus)
        elif lexeme == lId.TMinusMinus:
            self.stack.append(lId.TMinusMinus)

    def A7(self, lexeme):
        if lexeme == lId.TOpen:
            self.stack.append(lId.TClose)
            self.stack.append('expression')
            self.stack.append(lId.TOpen)
        elif lexeme == lId.TNum10:
            self.stack.append(lId.TNum10)
        elif lexeme == lId.TNum16:
            self.stack.append(lId.TNum16)
        else:
            self.stack.append('A710')

    def A710(self, lexeme):
        self.stack.append('A7110')
        self.stack.append(lId.TId)

    def A7110(self, lexeme):
        if lexeme == lId.TOpen:
            self.stack.append(lId.TClose)
            self.stack.append('EO')
            self.stack.append(lId.TOpen)

    def EO(self, lexeme):
        if lexeme != lId.TClose:
            self.stack.append('enum_operand')
            self.stack.append('expression')

    def enum_operand(self, lexeme):
        if lexeme == lId.TComma:
            self.stack.append('enum_operand')
            self.stack.append('expression')
            self.stack.append(lId.TComma)

    @staticmethod
    def is_terminal(l):
        return str(l).isdigit()

    @staticmethod
    def is_data_type(lexeme_id):
        """
        Проверяет тип лексемы c типами данных
        """
        return lexeme_id == lId.TInt or lexeme_id == lId.TShort or lexeme_id == lId.TLong


class AscendingAnalise:

    def __init(self, scanner):
        self.scanner = scanner


if __name__ == "__main__":
    print(help(Syntax.main_program))