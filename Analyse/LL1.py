from Syntax import LexemId as lId
from Semantic.SemanticTree import SemanticTree
from Semantic.SemanticTree import Node


class LL1Exception(Exception):
    def __init__(self, line, position, message):
        self.line = line
        self.position = position
        self.message = message

    def __str__(self):
        return "В строке " + str(self.line) + " в позиции " + str(self.position) + " " + str(self.message)


class LL1:
    def __init__(self, scanner):
        self.semantic_tree = SemanticTree()
        self.scanner = scanner
        self.past_lexeme_img = ''
        self.past_lexeme = 0
        self.current_var = None
        self.current_function = None
        self.stack = []
        self.stack.append(lId.TEndFile)
        self.stack.append('main_program')

        self.R = []
        self.number_trio = 0

        self.non_terminal_to_method = {
            'main_program': self.main_program, 'description': self.description, 'EV': self.EV, 'head_var': self.head_var,
            'EVF': self.EVF, 'PEVF': self.PEVF, 'param': self.param, 'body_function': self.body_function,
            'enum_operator': self.enum_operator, 'O': self.O, 'operator': self.operator, 'expression': self.expression,
            'A3': self.A3, 'A31': self.A31, 'A4': self.A4, 'A41': self.A41, 'A5': self.A5, 'A51': self.A51,
            'A6': self.A6, 'A61': self.A61, 'A7': self.A7, 'A710': self.A710, 'A7110': self.A7110, 'EO': self.EO,
            'enum_operand': self.enum_operand,

            # +++++++++++++++++++++
            #      СЕМАНТИКА
            # +++++++++++++++++++++
            'write_current_type': self.write_current_type, 'verify_overlap': self.verify_overlap,
            'create_var': self.create_var, 'create_special': self.create_special,
            'reset_param_cnt': self.reset_param_cnt, 'write_param_cnt': self.write_param_cnt,
            'out_from_block': self.out_from_block, 'inc_param_cnt': self.inc_param_cnt,
            'find_var_for_assigning_in_tree': self.find_var_for_assigning_in_tree, 'verify_param_cnt': self.verify_param_cnt,
            'change_type_to_func': self.change_type_to_func, 'find_node_with_lexeme': self.find_node_with_lexeme,
            'verify_variable_node': self.verify_variable_node, 'verify_function_node': self.verify_function_node,

            # +++++++++++++++++++++
            #         СУП
            # +++++++++++++++++++++
            'add_current_result_to_R': self.add_current_result_to_R, 'add_lexeme_to_R': self.add_lexeme_to_R,
            'print_assign_trio': self.print_assign_trio, 'print_div_trio': self.print_div_trio,
            'print_greater_or_eq_trio': self.print_greater_or_eq_trio, 'print_greater_trio': self.print_greater_trio,
            'print_less_or_eq_trio': self.print_less_or_eq_trio, 'print_less_trio': self.print_less_trio,
            'print_minus_trio': self.print_minus_trio, 'print_mod_trio': self.print_mod_trio,
            'print_mul_trio': self.print_mul_trio, 'print_plus_trio': self.print_plus_trio,
            'print_unary_minus_trio': self.print_unary_minus_trio, 'print_unary_plus_trio': self.print_unary_plus_trio,
            'print_eq_trio': self.print_eq_trio, 'print_uneq_trio': self.print_uneq_trio,
        }

    def __getitem__(self, item):
        return self.non_terminal_to_method.get(item)

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
                    self.past_lexeme_img = self.scanner.lexeme
                    self.past_lexeme = lexeme
                    lexeme = sc.next_lexeme()
                else:
                    raise LL1Exception(sc.get_pointer_line(), sc.get_pointer_position(),
                               "ожидалась конструкция " + lId.lexemIdToStr[l] + ", найдено " + str(sc.lexeme))
            else:
                self[l](lexeme)
            # print(str(self.stack) + ' ' + str(self.past_lexeme_img))

    def main_program(self, lexeme):
        if self.is_data_type(lexeme):
            self.stack.append('main_program')
            self.stack.append('description')
            self.stack.append('add_lexeme_to_R')
            self.stack.append('create_var')
            self.stack.append('verify_overlap')
            self.stack.append(lId.TId)
            self.stack.append('write_current_type')
            self.stack.append(lId.TInt)

    def description(self, lexeme):
        if lexeme == lId.TOpen:
            self.stack.append('out_from_block')
            self.stack.append('body_function')
            self.stack.append(lId.TClose)
            self.stack.append('write_param_cnt')
            self.stack.append('PEVF')
            self.stack.append('reset_param_cnt')
            self.stack.append(lId.TOpen)
            self.stack.append('create_special')
            self.stack.append('change_type_to_func')
        else:
            self.stack.append(lId.TSemicolon)
            self.stack.append('EV')
            self.stack.append('head_var')

    def EV(self, lexeme):
        if lexeme == lId.TComma:
            self.stack.append('EV')
            self.stack.append('head_var')
            self.stack.append('add_lexeme_to_R')
            self.stack.append('create_var')
            self.stack.append('verify_overlap')
            self.stack.append(lId.TId)
            self.stack.append(lId.TComma)

    def head_var(self, lexeme):
        if lexeme == lId.TAssign:
            self.stack.append('print_assign_trio')
            self.stack.append('expression')
            self.stack.append(lId.TAssign)

    def PEVF(self, lexeme):
        if self.is_data_type(lexeme):
            self.stack.append('EVF')
            self.stack.append('inc_param_cnt')
            self.stack.append('param')

    def EVF(self, lexeme):
        if lexeme == lId.TComma:
            self.stack.append('EVF')
            self.stack.append('inc_param_cnt')
            self.stack.append('param')
            self.stack.append(lId.TComma)

    def param(self, lexeme):
        if self.is_data_type(lexeme):
            self.stack.append('create_var')
            self.stack.append('verify_overlap')
            self.stack.append(lId.TId)
            self.stack.append(lId.TInt)
        else:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),\
                               "ожидался тип данных, найдено " + str(self.scanner.lexeme))

    def body_function(self, lexeme):
        if lexeme == lId.TOpenFigure:
            self.stack.append('out_from_block')
            self.stack.append(lId.TCloseFigure)
            self.stack.append('enum_operator')
            self.stack.append(lId.TOpenFigure)
            self.stack.append('create_special')
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
            self.stack.append('add_lexeme_to_R')
            self.stack.append('create_var')
            self.stack.append('verify_overlap')
            self.stack.append(lId.TId)
            self.stack.append('write_current_type')
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
            self.stack.append('print_assign_trio')
            self.stack.append('expression')
            self.stack.append(lId.TAssign)
            self.stack.append('add_lexeme_to_R')
            self.stack.append('find_var_for_assigning_in_tree')
            self.stack.append(lId.TId)

    def expression(self, lexeme):
        self.stack.append('A31')
        self.stack.append('A3')

    def A31(self, lexeme):
        if lexeme == lId.TEq or lexeme == lId.TUnEq:
            self.stack.append('A31')
            self.stack.append('add_current_result_to_R')
            if lexeme == lId.TEq:
                self.stack.append('print_eq_trio')
                self.stack.append('A3')
                self.stack.append(lId.TEq)
            elif lexeme == lId.TUnEq:
                self.stack.append('print_uneq_trio')
                self.stack.append('A3')
                self.stack.append(lId.TUnEq)

    def A3(self, lexeme):
        self.stack.append('A41')
        self.stack.append('A4')

    def A41(self, lexeme):
        if lexeme == lId.TLess or lexeme == lId.TLessEq or lexeme == lId.TGreater or lexeme == lId.TGreaterEq:
            self.stack.append('A41')
            self.stack.append('add_current_result_to_R')
            if lexeme == lId.TLess:
                self.stack.append('print_less_trio')
                self.stack.append('A4')
                self.stack.append(lId.TLess)
            elif lexeme == lId.TLessEq:
                self.stack.append('print_less_or_eq_trio')
                self.stack.append('A4')
                self.stack.append(lId.TLessEq)
            elif lexeme == lId.TGreater:
                self.stack.append('print_greater_trio')
                self.stack.append('A4')
                self.stack.append(lId.TGreater)
            elif lexeme == lId.TGreaterEq:
                self.stack.append('print_greater_or_eq_trio')
                self.stack.append('A4')
                self.stack.append(lId.TGreaterEq)

    def A4(self, lexeme):
        self.stack.append('A51')
        self.stack.append('A5')

    def A51(self, lexeme):
        if lexeme == lId.TPlus or lexeme == lId.TMinus:
            self.stack.append('A51')
            self.stack.append('add_current_result_to_R')
            if lexeme == lId.TPlus:
                self.stack.append('print_plus_trio')
                self.stack.append('A5')
                self.stack.append(lId.TPlus)
            elif lexeme == lId.TMinus:
                self.stack.append('print_minus_trio')
                self.stack.append('A5')
                self.stack.append(lId.TMinus)

    def A5(self, lexeme):
        self.stack.append('A61')
        self.stack.append('A6')

    def A61(self, lexeme):
        if lexeme == lId.TMul or lexeme == lId.TDiv or lexeme == lId.TMod:
            self.stack.append('A61')
            self.stack.append('add_current_result_to_R')
            if lexeme == lId.TMul:
                self.stack.append('print_mul_trio')
                self.stack.append('A6')
                self.stack.append(lId.TMul)
            elif lexeme == lId.TDiv:
                self.stack.append('print_div_trio')
                self.stack.append('A6')
                self.stack.append(lId.TDiv)
            elif lexeme == lId.TMod:
                self.stack.append('print_mod_trio')
                self.stack.append('A6')
                self.stack.append(lId.TMod)

    def A6(self, lexeme):
        if lexeme == lId.TPlus or lexeme == lId.TMinus:
            self.stack.append('add_current_result_to_R')
            if lexeme == lId.TPlus:
                self.stack.append('print_unary_plus_trio')
                self.stack.append('A7')
                self.stack.append(lId.TPlus)
            elif lexeme == lId.TMinus:
                self.stack.append('print_unary_minus_trio')
                self.stack.append('A7')
                self.stack.append(lId.TMinus)
        else:
            self.stack.append('A7')

    def A7(self, lexeme):
        if lexeme == lId.TOpen:
            self.stack.append(lId.TClose)
            self.stack.append('expression')
            self.stack.append(lId.TOpen)
        elif lexeme == lId.TNum10:
            self.stack.append('add_lexeme_to_R')
            self.stack.append(lId.TNum10)
        elif lexeme == lId.TNum16:
            self.stack.append('add_lexeme_to_R')
            self.stack.append(lId.TNum16)
        else:
            self.stack.append('A710')

    def A710(self, lexeme):
        self.stack.append('A7110')
        self.stack.append('find_node_with_lexeme')
        self.stack.append(lId.TId)

    def A7110(self, lexeme):
        if lexeme == lId.TOpen:
            self.stack.append(lId.TClose)
            self.stack.append('verify_param_cnt')
            self.stack.append('EO')
            self.stack.append('reset_param_cnt')
            self.stack.append(lId.TOpen)
            self.stack.append('verify_function_node')
        else:
            self.stack.append('verify_variable_node')

    def EO(self, lexeme):
        if lexeme != lId.TClose:
            self.stack.append('enum_operand')
            self.stack.append('inc_param_cnt')
            self.stack.append('expression')

    def enum_operand(self, lexeme):
        if lexeme == lId.TComma:
            self.stack.append('enum_operand')
            self.stack.append('inc_param_cnt')
            self.stack.append('expression')
            self.stack.append(lId.TComma)

    # +++++++++++++++++++++
    #      СЕМАНТИКА
    # +++++++++++++++++++++

    def inc_param_cnt(self, lexeme):
        self.semantic_tree.current_count_parameter += 1

    def verify_variable_node(self, lexeme):
        if self.current_var is None:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),
                               "переменная " + self.past_lexeme_img + " не определена")
        if self.current_var.type_object != Node.VARIABLE:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),
                               "функцию " + self.past_lexeme_img + " нельзя использовать как переменную")

    def verify_function_node(self, lexeme):
        if self.current_var is None:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),
                               "функция " + self.past_lexeme_img + " не определена")

        if self.current_var.type_object != Node.FUNCTION:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),
                               "переменную " + self.past_lexeme_img + " нельзя использовать как функцию")
        else:
            self.current_function = self.current_var
            self.current_var = None

    def verify_param_cnt(self, lexeme):
        if self.current_function.count_parameter != self.semantic_tree.current_count_parameter:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),
                               "неверное количество параметров у функции " + self.current_function.lexeme)

    def find_node_with_lexeme(self, lexeme):
        self.current_var = self.semantic_tree.get_variable_node(self.past_lexeme_img)

    def find_var_for_assigning_in_tree(self, lexeme):
        var_node = self.semantic_tree.get_variable_node(self.past_lexeme_img)
        sc = self.scanner
        if var_node is None:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),
                               "переменная " + str(self.past_lexeme_img) + " не найдена")
        if var_node.type_object == Node.FUNCTION:
            raise LL1Exception(self.scanner.get_pointer_line(), self.scanner.get_pointer_position(),
                               "функции " + str(self.past_lexeme_img) + " нельзя присвоить значение")

    def change_type_to_func(self, lexeme):
        self.current_function = self.current_var
        self.current_function.type_object = Node.FUNCTION
        self.current_var = None

    def create_special(self, lexeme):
        self.semantic_tree.add_special()

    def reset_param_cnt(self, lexeme):
        self.semantic_tree.current_count_parameter = 0

    def write_param_cnt(self, lexeme):
        self.current_function.count_parameter = self.semantic_tree.current_count_parameter

    def out_from_block(self, lexeme):
        self.semantic_tree.go_out()

    def write_current_type(self, lexeme):
        self.semantic_tree.set_current_type(self.past_lexeme)

    def verify_overlap(self, lexeme):
        sc = self.scanner
        if self.semantic_tree.is_overlay_lexeme(self.past_lexeme_img):
            raise LL1Exception(
                sc.get_pointer_line(),
                sc.get_pointer_position(),
                'лексема ' + self.past_lexeme_img + ' используется второй раз'
            )

    def create_var(self, lexeme):
        self.semantic_tree.add_neighbor(Node.VARIABLE, self.past_lexeme_img, 0)
        self.current_var = self.semantic_tree.pointer

    # +++++++++++++++++++++
    #         СУП
    # +++++++++++++++++++++

    def add_lexeme_to_R(self, lexeme):
        self.R.append(self.past_lexeme_img)

    def add_current_result_to_R(self, lexeme):
        self.R.append('(' + str(self.number_trio - 1) + ')')

    def print_eq_trio(self, lexeme):
        self.print_binary_trio('==')

    def print_uneq_trio(self, lexeme):
        self.print_binary_trio('!=')

    def print_assign_trio(self, lexeme):
        self.print_binary_trio('=')

    def print_less_trio(self, lexeme):
        self.print_binary_trio('<')

    def print_less_or_eq_trio(self, lexeme):
        self.print_binary_trio('<=')

    def print_greater_trio(self, lexeme):
        self.print_binary_trio('>')

    def print_greater_or_eq_trio(self, lexeme):
        self.print_binary_trio('>=')

    def print_plus_trio(self, lexeme):
        self.print_binary_trio('+')

    def print_minus_trio(self, lexeme):
        self.print_binary_trio('-')

    def print_mul_trio(self, lexeme):
        self.print_binary_trio('*')

    def print_div_trio(self, lexeme):
        self.print_binary_trio('/')

    def print_mod_trio(self, lexeme):
        self.print_binary_trio('%')

    def print_unary_plus_trio(self, lexeme):
        self.print_unary_trio('+')

    def print_unary_minus_trio(self, lexeme):
        self.print_unary_trio('-')

    def print_binary_trio(self, operation):
        op2 = self.R.pop()
        op1 = self.R.pop()
        print(str(self.number_trio) + ') ' + str(op1) + ' ' + str(operation) + ' ' + str(op2))
        self.number_trio += 1

    def print_unary_trio(self, operation):
        op = self.R.pop()
        print(str(self.number_trio) + ') ' + str(operation) + ' ' + str(op))
        self.number_trio += 1

    @staticmethod
    def is_terminal(l):
        return str(l).isdigit()

    @staticmethod
    def is_data_type(lexeme_id):
        return lexeme_id == lId.TInt or lexeme_id == lId.TShort or lexeme_id == lId.TLong

