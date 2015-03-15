from Syntax import LexemId as lId
from Exceptions.SyntaxException import *
from Exceptions.SemanticException import *
from Semantic.SemanticTree import SemanticTree
from Interpreter import Interpreter
from Semantic.ValueObj import ValueObj


class DescendingAnalyse:
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
            value_obj = ValueObj()
            self.expression(value_obj)

            # Interpreter
            self.semantic_tree.set_value_obj(value_obj)
            # Interpreter
        else:
            sc.set_pointer(old_pointer)

    def expression(self, value_obj):
        self.a2(value_obj)
        # закоментированная ниже часть предназначалась для множественного присваивания,
        # но она трудна в реализации для интерпретатора, поэтому множественное присваивание отменено
        # sc = self.scanner
        # old_pointer = sc.get_pointer()
        # lexeme_assign = sc.next_lexeme()
        # while lexeme_assign == lId.TAssign or lexeme_assign == lId.TPlusAssign or lexeme_assign == lId.TMinusAssign or \
        #                 lexeme_assign == lId.TMulAssign or lexeme_assign == lId.TDivAssign or lexeme_assign == lId.TModAssign:
        #     self.a2()
        #     old_pointer = sc.get_pointer()
        #     lexeme_assign = sc.next_lexeme()
        # sc.set_pointer(old_pointer)

    def a2(self, value_obj):
        self.a3(value_obj)

        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_equal = sc.next_lexeme()
        while lexeme_equal == lId.TEq or lexeme_equal == lId.TUnEq:
            _value_obj = ValueObj()
            self.a3(_value_obj)

            # interpreter
            if lexeme_equal == lId.TEq:
                Interpreter.verify_equal(value_obj, _value_obj)
            else:
                Interpreter.verify_unequal(value_obj, _value_obj)
            # interpreter

            old_pointer = sc.get_pointer()
            lexeme_equal = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a3(self, value_obj):
        self.a4(value_obj)
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_lege = sc.next_lexeme()
        while lexeme_lege == lId.TLess or lexeme_lege == lId.TGreater or \
                        lexeme_lege == lId.TLessEq or lexeme_lege == lId.TGreaterEq:
            _value_obj = ValueObj()
            self.a4(_value_obj)

            # interpreter
            if lexeme_lege == lId.TLess:
                Interpreter.verify_less(value_obj, _value_obj)
            elif lexeme_lege == lId.TLessEq:
                Interpreter.verify_less_eq(value_obj, _value_obj)
            elif lexeme_lege == lId.TGreater:
                Interpreter.verify_greater(value_obj, _value_obj)
            else:
                Interpreter.verify_greater_eq(value_obj, _value_obj)
            # interpreter

            old_pointer = sc.get_pointer()
            lexeme_lege = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a4(self, value_obj):
        self.a5(value_obj)
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_plus_minus = sc.next_lexeme()
        while lexeme_plus_minus == lId.TPlus or lexeme_plus_minus == lId.TMinus:
            _value_obj = ValueObj()
            self.a5(_value_obj)

            # interpreter
            if lexeme_plus_minus == lId.TPlus:
                Interpreter.sum(value_obj, _value_obj)
            else:
                Interpreter.sub(value_obj, _value_obj)
            # interpreter

            old_pointer = sc.get_pointer()
            lexeme_plus_minus = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a5(self, value_obj):
        self.a6(value_obj)
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_mul_div_mod = sc.next_lexeme()
        while lexeme_mul_div_mod == lId.TMul or lexeme_mul_div_mod == lId.TDiv or lexeme_mul_div_mod == lId.TMod:
            _value_obj = ValueObj()
            self.a6(_value_obj)

            # interpreter
            if lexeme_mul_div_mod == lId.TMul:
                Interpreter.mul(value_obj, _value_obj)
            elif lexeme_mul_div_mod == lId.TDiv:
                Interpreter.div(value_obj, _value_obj)
            else:
                Interpreter.mod(value_obj, _value_obj)
            # interpreter

            old_pointer = sc.get_pointer()
            lexeme_mul_div_mod = sc.next_lexeme()
        sc.set_pointer(old_pointer)

    def a6(self, value_obj):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_pref = sc.next_lexeme()
        if lexeme_pref == lId.TMinus or lexeme_pref == lId.TPlus:
                #or lexeme_pref == lId.TMinusMinus or lexeme_pref == lId.TPlusPlus:

            # Interpreter
            if lexeme_pref == lId.TMinus:
                Interpreter.sub({'value': 0, 'type': lId.TShort}, value_obj)
            # Interpreter

            self.a7(value_obj)
        else:
            sc.set_pointer(old_pointer)
            self.a7(value_obj)
            # old_pointer = sc.get_pointer()
            # lexeme_suff = sc.next_lexeme()
            # if lexeme_suff != lId.TPlusPlus and lexeme_suff != lId.TMinusMinus:
            #     sc.set_pointer(old_pointer)

    def a7(self, value_obj):
        sc = self.scanner
        old_pointer = sc.get_pointer()
        lexeme_open_bracket = sc.next_lexeme()
        if lexeme_open_bracket == lId.TOpen:
            self.expression(value_obj)
            lexeme_close_bracket = sc.next_lexeme()
            if lexeme_close_bracket != lId.TClose:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)
        elif sc.next_lexeme() == lId.TOpen:
            sc.set_pointer(old_pointer)
            self.call_function(value_obj)
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

            # Interpreter
            if lexeme_operand == lId.TId:
                _value_obj = self.semantic_tree.get_variable_value_obj(sc.lexeme)
                value_obj.value = _value_obj.value
                value_obj.type = _value_obj.type
            elif lexeme_operand == lId.TNum10:
                Interpreter.set_value_obj_from_num10(value_obj, sc.lexeme)
            else:
                Interpreter.set_value_obj_from_num16(value_obj, sc.lexeme)
            # Interpreter

    def description_function(self):
        sc = self.scanner
        lexeme_data_type = sc.next_lexeme()
        if not self.is_data_type(lexeme_data_type):
            raise SyntaxExceptionType(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)

        # semantic
        self.semantic_tree.set_current_type(lexeme_data_type)
        # semantic

        self.head_function()

        # Interpreter
        node_fun = self.semantic_tree.get_node_of_parent_function()
        if node_fun.lexeme == 'main':  # Выполнять только главную функцию
            self.body_function()
        # Interpreter

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

        # Interpreter
        pointer.entry_point = sc.get_pointer()  # Запомним точку входа для функции
        # Interpreter

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
            value_obj = ValueObj()
            self.expression(value_obj)

            # Interpreter
            if value_obj.value != 0:
                sc.set_pointer(old_pointer)
                return
            # Interpreter

            lexeme_close_bracket = sc.next_lexeme()
            if lexeme_close_bracket != lId.TClose:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ")", sc.lexeme)
            lexeme_semicolon = sc.next_lexeme()
            if lexeme_semicolon != lId.TSemicolon:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ";", sc.lexeme)
        elif lexeme == lId.TReturn:
            value_obj = ValueObj()
            self.expression(value_obj)
            lexeme_semicolon = sc.next_lexeme()
            if lexeme_semicolon != lId.TSemicolon:
                raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ";", sc.lexeme)
        else:
            sc.set_pointer(old_pointer)

            lexeme_identifier = sc.next_lexeme()
            if lexeme_identifier == lId.TId and sc.next_lexeme() == lId.TAssign:
                sc.set_pointer(old_pointer)
                self.assign()
            else:
                sc.set_pointer(old_pointer)

                value_obj = ValueObj()
                self.expression(value_obj)

                lexeme_semicolon = sc.next_lexeme()
                if lexeme_semicolon != lId.TSemicolon:
                    raise SyntaxExceptionCharacter(sc.get_pointer_line(), sc.get_pointer_position(), ";", sc.lexeme)

    def assign(self):
        sc = self.scanner
        lexeme_identifier = sc.next_lexeme()

        # semantic
        if not self.semantic_tree.is_describe_var_early(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme):
            raise SemanticExceptionUndescribeVar(sc.get_pointer_line(), sc.get_pointer_position(), sc.lexeme)
        # semantic

        # Interpreter
        node = self.semantic_tree.get_variable_node(sc.lexeme)
        # Interpreter

        sc.next_lexeme()  # =

        value_obj = ValueObj()
        self.expression(value_obj)

        # Interpreter
        Interpreter.to_type(value_obj, node.type_data)
        node.value = value_obj.value
        # Interpreter

    @staticmethod
    def is_data_type(lexeme_id):
        """
        Проверяет тип лексемы c типами данных
        """
        return lexeme_id == lId.TInt or lexeme_id == lId.TShort or lexeme_id == lId.TLong