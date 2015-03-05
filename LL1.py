import LexemId as lId


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
        return lexeme_id == lId.TInt or lexeme_id == lId.TShort or lexeme_id == lId.TLong

