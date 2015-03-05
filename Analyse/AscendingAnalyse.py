from Syntax import LexemId as lId


class AscendingAnalyse:

    def __init__(self, scanner):
        self.scanner = scanner
        self.stack = []
        self.stack.append(lId.TEndFile)

    def run(self):
        st = self.stack
        sc = self.scanner
        lexeme = sc.next_lexeme()
        try:
            while not (len(st) == 2 and st[0] == lId.TEndFile and st[1] == 'main_program'):
                sign = self.get_sign(st[len(st) - 1], lexeme)
                if sign <= 0:
                    st.append(lexeme)
                    lexeme = sc.next_lexeme()
                else:
                    rule = []
                    # print("before: " + str(st))
                    while self.get_sign(st[len(st) - 2], st[len(st) - 1]) != -1:
                        rule.append(st.pop())
                    rule.append(st.pop())
                    rule.reverse()
                    # print(str(rule))
                    # print("middle: " + str(st))
                    st.append(self.get_rule(rule))
                    # print("after:  " + str(st))
        except Exception as e:
            print(e)
            raise Exception("line: " + str(sc.get_pointer_line()) + "\nposition: " + str(sc.get_pointer_position()))

    def get_rule(self, rule):
        if len(rule) == 4 and (rule[0] == 3 or rule[0] == 4 or rule[0] == 5) and rule[1] == 0 and rule[2] == "description" and rule[3] == "main_program":
            return "main_program"
        if len(rule) == 3 and (rule[0] == 3 or rule[0] == 4 or rule[0] == 5) and rule[1] == 0 and rule[2] == "description":
            return "main_program"
        if len(rule) == 1 and rule[0] == "descriptionF":
            return "description"
        if len(rule) == 3 and rule[0] == 27 and rule[1] == "B9" and rule[2] == 34:
            return "description"
        if len(rule) == 1 and rule[0] == "expression":
            return "B9"
        if len(rule) == 3 and rule[0] == 10 and rule[1] == 11 and rule[2] == "body_function":
            return "descriptionF"
        if len(rule) == 4 and rule[0] == 10 and rule[1] == "PEVF" and rule[2] == 11 and rule[3] == "body_function":
            return "descriptionF"
        if len(rule) == 1 and rule[0] == "param":
            return "PEVF"
        if len(rule) == 2 and rule[0] == "param" and rule[1] == "EVF":
            return "PEVF"
        if len(rule) == 3 and rule[0] == 33 and rule[1] == "param" and rule[2] == "EVF":
            return "EVF"
        if len(rule) == 2 and rule[0] == 33 and rule[1] == "param":
            return "EVF"
        if len(rule) == 2 and (rule[0] == 3 or rule[0] == 4 or rule[0] == 5) and rule[1] == 0:
            return "param"
        if len(rule) == 2 and rule[0] == 12 and rule[1] == 13:
            return "body_function"
        if len(rule) == 3 and rule[0] == 12 and rule[1] == "B10" and rule[2] == 13:
            return "body_function"
        if len(rule) == 1 and rule[0] == "enum_operator":
            return "B10"
        if len(rule) == 2 and rule[0] == "O" and rule[1] == "enum_operator":
            return "enum_operator"
        if len(rule) == 1 and rule[0] == "O":
            return "enum_operator"
        if len(rule) == 2 and rule[0] == "operator" and rule[1] == 34:
            return "O"
        if len(rule) == 1 and rule[0] == "body_function":
            return "O"
        if len(rule) == 1 and rule[0] == 34:
            return "O"
        if len(rule) == 2 and rule[0] == "B9" and rule[1] == 34:
            return "O"
        if len(rule) == 6 and rule[0] == 6 and rule[1] == "body_function" and rule[2] == 7 and rule[3] == 10 and rule[4] == "expression" and rule[5] == "B7":
            return "operator"
        if len(rule) == 2 and rule[0] == 9 and rule[1] == "expression":
            return "operator"
        if len(rule) == 1 and rule[0] == 11:
            return "B7"
        if len(rule) == 1 and rule[0] == "A2":
            return "expression"
        if len(rule) == 3 and rule[0] == "A2" and rule[1] == 25 and rule[2] == "B1":
            return "A2"
        if len(rule) == 3 and rule[0] == "A2" and rule[1] == 26 and rule[2] == "B1":
            return "A2"
        if len(rule) == 1 and rule[0] == "B1":
            return "A2"
        if len(rule) == 1 and rule[0] == "A3":
            return "B1"
        if len(rule) == 3 and rule[0] == "A3" and rule[1] == 21 and rule[2] == "B2":
            return "A3"
        if len(rule) == 3 and rule[0] == "A3" and rule[1] == 22 and rule[2] == "B2":
            return "A3"
        if len(rule) == 3 and rule[0] == "A3" and rule[1] == 24 and rule[2] == "B2":
            return "A3"
        if len(rule) == 3 and rule[0] == "A3" and rule[1] == 23 and rule[2] == "B2":
            return "A3"
        if len(rule) == 1 and rule[0] == "B2":
            return "A3"
        if len(rule) == 1 and rule[0] == "A4":
            return "B2"
        if len(rule) == 3 and rule[0] == "A4" and rule[1] == 14 and rule[2] == "B3":
            return "A4"
        if len(rule) == 3 and rule[0] == "A4" and rule[1] == 15 and rule[2] == "B3":
            return "A4"
        if len(rule) == 1 and rule[0] == "B3":
            return "A4"
        if len(rule) == 1 and rule[0] == "A5":
            return "B3"
        if len(rule) == 3 and rule[0] == "A5" and rule[1] == 20 and rule[2] == "A6":
            return "A5"
        if len(rule) == 3 and rule[0] == "A5" and rule[1] == 18 and rule[2] == "A6":
            return "A5"
        if len(rule) == 3 and rule[0] == "A5" and rule[1] == 19 and rule[2] == "A6":
            return "A5"
        if len(rule) == 1 and rule[0] == "A6":
            return "A5"
        if len(rule) == 2 and rule[0] == 17 and rule[1] == "A7":
            return "A6"
        if len(rule) == 2 and rule[0] == 16 and rule[1] == "A7":
            return "A6"
        if len(rule) == 2 and rule[0] == "A7" and rule[1] == 17:
            return "A6"
        if len(rule) == 2 and rule[0] == "A7" and rule[1] == 16:
            return "A6"
        if len(rule) == 1 and rule[0] == "A7":
            return "A6"
        if len(rule) == 3 and rule[0] == 10 and rule[1] == "expression" and rule[2] == "B7":
            return "A7"
        if len(rule) == 1 and rule[0] == "operand":
            return "A7"
        if len(rule) == 2 and rule[0] == 0 and rule[1] == "B45":
            return "A7"
        if len(rule) == 3 and rule[0] == 10 and rule[1] == "PEO" and rule[2] == 11:
            return "B45"
        if len(rule) == 2 and rule[0] == 10 and rule[1] == 11:
            return "B45"
        if len(rule) == 2 and rule[0] == "operand" and rule[1] == 12:
            return "PEO"
        if len(rule) == 3 and rule[0] == "operand" and rule[1] == 12 and rule[2] == "EO":
            return "PEO"
        if len(rule) == 4 and rule[0] == 33 and rule[1] == "operand" and rule[2] == 12 and rule[3] == "EO":
            return "EO"
        if len(rule) == 3 and rule[0] == 33 and rule[1] == "operand" and rule[2] == 12:
            return "EO"
        if len(rule) == 1 and rule[0] == 0:
            return "operand"
        if len(rule) == 1 and rule[0] == 2:
            return "operand"
        if len(rule) == 1 and rule[0] == 1:
            return "operand"
        raise Exception('Error! get_rule:' + str(rule))

    def get_sign(self, lexeme1, lexeme2):
        if lexeme1 == 26 and lexeme2 == 10:
            return -1
        if lexeme1 == 26 and lexeme2 == 16:
            return -1
        if lexeme1 == 26 and lexeme2 == 17:
            return -1
        if lexeme1 == 26 and lexeme2 == "A3":
            return -1
        if lexeme1 == 26 and lexeme2 == "A4":
            return -1
        if lexeme1 == 26 and lexeme2 == "A5":
            return -1
        if lexeme1 == 26 and lexeme2 == "A6":
            return -1
        if lexeme1 == 26 and lexeme2 == "A7":
            return -1
        if lexeme1 == 26 and lexeme2 == "B1":
            return 0
        if lexeme1 == 26 and lexeme2 == "B2":
            return -1
        if lexeme1 == 26 and lexeme2 == "B3":
            return -1
        if lexeme1 == 26 and lexeme2 == 1:
            return -1
        if lexeme1 == 26 and lexeme2 == 2:
            return -1
        if lexeme1 == 26 and lexeme2 == 0:
            return -1
        if lexeme1 == 26 and lexeme2 == "operand":
            return -1
        if lexeme1 == 19 and lexeme2 == 10:
            return -1
        if lexeme1 == 19 and lexeme2 == 16:
            return -1
        if lexeme1 == 19 and lexeme2 == 17:
            return -1
        if lexeme1 == 19 and lexeme2 == "A6":
            return 0
        if lexeme1 == 19 and lexeme2 == "A7":
            return -1
        if lexeme1 == 19 and lexeme2 == 1:
            return -1
        if lexeme1 == 19 and lexeme2 == 2:
            return -1
        if lexeme1 == 19 and lexeme2 == 0:
            return -1
        if lexeme1 == 19 and lexeme2 == "operand":
            return -1
        if lexeme1 == 10 and lexeme2 == 10:
            return -1
        if lexeme1 == 10 and lexeme2 == 11:
            return 0
        if lexeme1 == 10 and lexeme2 == 16:
            return -1
        if lexeme1 == 10 and lexeme2 == 17:
            return -1
        if lexeme1 == 10 and lexeme2 == "A2":
            return -1
        if lexeme1 == 10 and lexeme2 == "A3":
            return -1
        if lexeme1 == 10 and lexeme2 == "A4":
            return -1
        if lexeme1 == 10 and lexeme2 == "A5":
            return -1
        if lexeme1 == 10 and lexeme2 == "A6":
            return -1
        if lexeme1 == 10 and lexeme2 == "A7":
            return -1
        if lexeme1 == 10 and lexeme2 == "B1":
            return -1
        if lexeme1 == 10 and lexeme2 == "B2":
            return -1
        if lexeme1 == 10 and lexeme2 == "B3":
            return -1
        if lexeme1 == 10 and lexeme2 == "PEO":
            return 0
        if lexeme1 == 10 and lexeme2 == "PEVF":
            return 0
        if lexeme1 == 10 and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return -1
        if lexeme1 == 10 and lexeme2 == 1:
            return -1
        if lexeme1 == 10 and lexeme2 == "expression":
            return 0
        if lexeme1 == 10 and lexeme2 == 2:
            return -1
        if lexeme1 == 10 and lexeme2 == 0:
            return -1
        if lexeme1 == 10 and lexeme2 == "operand":
            return -1
        if lexeme1 == 10 and lexeme2 == "param":
            return -1
        if lexeme1 == 11 and lexeme2 == 26:
            return 1
        if lexeme1 == 11 and lexeme2 == 19:
            return 1
        if lexeme1 == 11 and lexeme2 == 11:
            return 1
        if lexeme1 == 11 and lexeme2 == 20:
            return 1
        if lexeme1 == 11 and lexeme2 == 14:
            return 1
        if lexeme1 == 11 and lexeme2 == 16:
            return 1
        if lexeme1 == 11 and lexeme2 == 15:
            return 1
        if lexeme1 == 11 and lexeme2 == 17:
            return 1
        if lexeme1 == 11 and lexeme2 == 18:
            return 1
        if lexeme1 == 11 and lexeme2 == 34:
            return 1
        if lexeme1 == 11 and lexeme2 == 22:
            return 1
        if lexeme1 == 11 and lexeme2 == 24:
            return 1
        if lexeme1 == 11 and lexeme2 == 25:
            return 1
        if lexeme1 == 11 and lexeme2 == 21:
            return 1
        if lexeme1 == 11 and lexeme2 == 23:
            return 1
        if lexeme1 == 11 and lexeme2 == "body_function":
            return 0
        if lexeme1 == 11 and lexeme2 == 12:
            return -1
        if lexeme1 == 20 and lexeme2 == 10:
            return -1
        if lexeme1 == 20 and lexeme2 == 16:
            return -1
        if lexeme1 == 20 and lexeme2 == 17:
            return -1
        if lexeme1 == 20 and lexeme2 == "A6":
            return 0
        if lexeme1 == 20 and lexeme2 == "A7":
            return -1
        if lexeme1 == 20 and lexeme2 == 1:
            return -1
        if lexeme1 == 20 and lexeme2 == 2:
            return -1
        if lexeme1 == 20 and lexeme2 == 0:
            return -1
        if lexeme1 == 20 and lexeme2 == "operand":
            return -1
        if lexeme1 == 14 and lexeme2 == 10:
            return -1
        if lexeme1 == 14 and lexeme2 == 16:
            return -1
        if lexeme1 == 14 and lexeme2 == 17:
            return -1
        if lexeme1 == 14 and lexeme2 == "A5":
            return -1
        if lexeme1 == 14 and lexeme2 == "A6":
            return -1
        if lexeme1 == 14 and lexeme2 == "A7":
            return -1
        if lexeme1 == 14 and lexeme2 == "B3":
            return 0
        if lexeme1 == 14 and lexeme2 == 1:
            return -1
        if lexeme1 == 14 and lexeme2 == 2:
            return -1
        if lexeme1 == 14 and lexeme2 == 0:
            return -1
        if lexeme1 == 14 and lexeme2 == "operand":
            return -1
        if lexeme1 == 16 and lexeme2 == 26:
            return 1
        if lexeme1 == 16 and lexeme2 == 19:
            return 1
        if lexeme1 == 16 and lexeme2 == 10:
            return -1
        if lexeme1 == 16 and lexeme2 == 11:
            return 1
        if lexeme1 == 16 and lexeme2 == 20:
            return 1
        if lexeme1 == 16 and lexeme2 == 14:
            return 1
        if lexeme1 == 16 and lexeme2 == 15:
            return 1
        if lexeme1 == 16 and lexeme2 == 18:
            return 1
        if lexeme1 == 16 and lexeme2 == 34:
            return 1
        if lexeme1 == 16 and lexeme2 == 22:
            return 1
        if lexeme1 == 16 and lexeme2 == 24:
            return 1
        if lexeme1 == 16 and lexeme2 == 25:
            return 1
        if lexeme1 == 16 and lexeme2 == 21:
            return 1
        if lexeme1 == 16 and lexeme2 == 23:
            return 1
        if lexeme1 == 16 and lexeme2 == "A7":
            return 0
        if lexeme1 == 16 and lexeme2 == 1:
            return -1
        if lexeme1 == 16 and lexeme2 == 2:
            return -1
        if lexeme1 == 16 and lexeme2 == 0:
            return -1
        if lexeme1 == 16 and lexeme2 == "operand":
            return -1
        if lexeme1 == 33 and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return -1
        if lexeme1 == 33 and lexeme2 == 1:
            return -1
        if lexeme1 == 33 and lexeme2 == 2:
            return -1
        if lexeme1 == 33 and lexeme2 == 0:
            return -1
        if lexeme1 == 33 and lexeme2 == "operand":
            return 0
        if lexeme1 == 33 and lexeme2 == "param":
            return 0
        if lexeme1 == 15 and lexeme2 == 10:
            return -1
        if lexeme1 == 15 and lexeme2 == 16:
            return -1
        if lexeme1 == 15 and lexeme2 == 17:
            return -1
        if lexeme1 == 15 and lexeme2 == "A5":
            return -1
        if lexeme1 == 15 and lexeme2 == "A6":
            return -1
        if lexeme1 == 15 and lexeme2 == "A7":
            return -1
        if lexeme1 == 15 and lexeme2 == "B3":
            return 0
        if lexeme1 == 15 and lexeme2 == 1:
            return -1
        if lexeme1 == 15 and lexeme2 == 2:
            return -1
        if lexeme1 == 15 and lexeme2 == 0:
            return -1
        if lexeme1 == 15 and lexeme2 == "operand":
            return -1
        if lexeme1 == 17 and lexeme2 == 26:
            return 1
        if lexeme1 == 17 and lexeme2 == 19:
            return 1
        if lexeme1 == 17 and lexeme2 == 10:
            return -1
        if lexeme1 == 17 and lexeme2 == 11:
            return 1
        if lexeme1 == 17 and lexeme2 == 20:
            return 1
        if lexeme1 == 17 and lexeme2 == 14:
            return 1
        if lexeme1 == 17 and lexeme2 == 15:
            return 1
        if lexeme1 == 17 and lexeme2 == 18:
            return 1
        if lexeme1 == 17 and lexeme2 == 34:
            return 1
        if lexeme1 == 17 and lexeme2 == 22:
            return 1
        if lexeme1 == 17 and lexeme2 == 24:
            return 1
        if lexeme1 == 17 and lexeme2 == 25:
            return 1
        if lexeme1 == 17 and lexeme2 == 21:
            return 1
        if lexeme1 == 17 and lexeme2 == 23:
            return 1
        if lexeme1 == 17 and lexeme2 == "A7":
            return 0
        if lexeme1 == 17 and lexeme2 == 1:
            return -1
        if lexeme1 == 17 and lexeme2 == 2:
            return -1
        if lexeme1 == 17 and lexeme2 == 0:
            return -1
        if lexeme1 == 17 and lexeme2 == "operand":
            return -1
        if lexeme1 == 18 and lexeme2 == 10:
            return -1
        if lexeme1 == 18 and lexeme2 == 16:
            return -1
        if lexeme1 == 18 and lexeme2 == 17:
            return -1
        if lexeme1 == 18 and lexeme2 == "A6":
            return 0
        if lexeme1 == 18 and lexeme2 == "A7":
            return -1
        if lexeme1 == 18 and lexeme2 == 1:
            return -1
        if lexeme1 == 18 and lexeme2 == 2:
            return -1
        if lexeme1 == 18 and lexeme2 == 0:
            return -1
        if lexeme1 == 18 and lexeme2 == "operand":
            return -1
        if lexeme1 == 34 and lexeme2 == 10:
            return 1
        if lexeme1 == 34 and lexeme2 == 16:
            return 1
        if lexeme1 == 34 and lexeme2 == 17:
            return 1
        if lexeme1 == 34 and lexeme2 == 34:
            return 1
        if lexeme1 == 34 and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return 1
        if lexeme1 == 34 and lexeme2 == 1:
            return 1
        if lexeme1 == 34 and lexeme2 == 6:
            return 1
        if lexeme1 == 34 and lexeme2 == 36:
            return 1
        if lexeme1 == 34 and lexeme2 == 2:
            return 1
        if lexeme1 == 34 and lexeme2 == 0:
            return 1
        if lexeme1 == 34 and lexeme2 == 9:
            return 1
        if lexeme1 == 34 and lexeme2 == 12:
            return 1
        if lexeme1 == 34 and lexeme2 == 13:
            return 1
        if lexeme1 == 22 and lexeme2 == 10:
            return -1
        if lexeme1 == 22 and lexeme2 == 16:
            return -1
        if lexeme1 == 22 and lexeme2 == 17:
            return -1
        if lexeme1 == 22 and lexeme2 == "A4":
            return -1
        if lexeme1 == 22 and lexeme2 == "A5":
            return -1
        if lexeme1 == 22 and lexeme2 == "A6":
            return -1
        if lexeme1 == 22 and lexeme2 == "A7":
            return -1
        if lexeme1 == 22 and lexeme2 == "B2":
            return 0
        if lexeme1 == 22 and lexeme2 == "B3":
            return -1
        if lexeme1 == 22 and lexeme2 == 1:
            return -1
        if lexeme1 == 22 and lexeme2 == 2:
            return -1
        if lexeme1 == 22 and lexeme2 == 0:
            return -1
        if lexeme1 == 22 and lexeme2 == "operand":
            return -1
        if lexeme1 == 24 and lexeme2 == 10:
            return -1
        if lexeme1 == 24 and lexeme2 == 16:
            return -1
        if lexeme1 == 24 and lexeme2 == 17:
            return -1
        if lexeme1 == 24 and lexeme2 == "A4":
            return -1
        if lexeme1 == 24 and lexeme2 == "A5":
            return -1
        if lexeme1 == 24 and lexeme2 == "A6":
            return -1
        if lexeme1 == 24 and lexeme2 == "A7":
            return -1
        if lexeme1 == 24 and lexeme2 == "B2":
            return 0
        if lexeme1 == 24 and lexeme2 == "B3":
            return -1
        if lexeme1 == 24 and lexeme2 == 1:
            return -1
        if lexeme1 == 24 and lexeme2 == 2:
            return -1
        if lexeme1 == 24 and lexeme2 == 0:
            return -1
        if lexeme1 == 24 and lexeme2 == "operand":
            return -1
        if lexeme1 == 27 and lexeme2 == 10:
            return -1
        if lexeme1 == 27 and lexeme2 == 16:
            return -1
        if lexeme1 == 27 and lexeme2 == 17:
            return -1
        if lexeme1 == 27 and lexeme2 == "A2":
            return -1
        if lexeme1 == 27 and lexeme2 == "A3":
            return -1
        if lexeme1 == 27 and lexeme2 == "A4":
            return -1
        if lexeme1 == 27 and lexeme2 == "A5":
            return -1
        if lexeme1 == 27 and lexeme2 == "A6":
            return -1
        if lexeme1 == 27 and lexeme2 == "A7":
            return -1
        if lexeme1 == 27 and lexeme2 == "B1":
            return -1
        if lexeme1 == 27 and lexeme2 == "B2":
            return -1
        if lexeme1 == 27 and lexeme2 == "B3":
            return -1
        if lexeme1 == 27 and lexeme2 == "B9":
            return 0
        if lexeme1 == 27 and lexeme2 == 1:
            return -1
        if lexeme1 == 27 and lexeme2 == "expression":
            return -1
        if lexeme1 == 27 and lexeme2 == 2:
            return -1
        if lexeme1 == 27 and lexeme2 == 0:
            return -1
        if lexeme1 == 27 and lexeme2 == "operand":
            return -1
        if lexeme1 == 25 and lexeme2 == 10:
            return -1
        if lexeme1 == 25 and lexeme2 == 16:
            return -1
        if lexeme1 == 25 and lexeme2 == 17:
            return -1
        if lexeme1 == 25 and lexeme2 == "A3":
            return -1
        if lexeme1 == 25 and lexeme2 == "A4":
            return -1
        if lexeme1 == 25 and lexeme2 == "A5":
            return -1
        if lexeme1 == 25 and lexeme2 == "A6":
            return -1
        if lexeme1 == 25 and lexeme2 == "A7":
            return -1
        if lexeme1 == 25 and lexeme2 == "B1":
            return 0
        if lexeme1 == 25 and lexeme2 == "B2":
            return -1
        if lexeme1 == 25 and lexeme2 == "B3":
            return -1
        if lexeme1 == 25 and lexeme2 == 1:
            return -1
        if lexeme1 == 25 and lexeme2 == 2:
            return -1
        if lexeme1 == 25 and lexeme2 == 0:
            return -1
        if lexeme1 == 25 and lexeme2 == "operand":
            return -1
        if lexeme1 == 21 and lexeme2 == 10:
            return -1
        if lexeme1 == 21 and lexeme2 == 16:
            return -1
        if lexeme1 == 21 and lexeme2 == 17:
            return -1
        if lexeme1 == 21 and lexeme2 == "A4":
            return -1
        if lexeme1 == 21 and lexeme2 == "A5":
            return -1
        if lexeme1 == 21 and lexeme2 == "A6":
            return -1
        if lexeme1 == 21 and lexeme2 == "A7":
            return -1
        if lexeme1 == 21 and lexeme2 == "B2":
            return 0
        if lexeme1 == 21 and lexeme2 == "B3":
            return -1
        if lexeme1 == 21 and lexeme2 == 1:
            return -1
        if lexeme1 == 21 and lexeme2 == 2:
            return -1
        if lexeme1 == 21 and lexeme2 == 0:
            return -1
        if lexeme1 == 21 and lexeme2 == "operand":
            return -1
        if lexeme1 == 23 and lexeme2 == 10:
            return -1
        if lexeme1 == 23 and lexeme2 == 16:
            return -1
        if lexeme1 == 23 and lexeme2 == 17:
            return -1
        if lexeme1 == 23 and lexeme2 == "A4":
            return -1
        if lexeme1 == 23 and lexeme2 == "A5":
            return -1
        if lexeme1 == 23 and lexeme2 == "A6":
            return -1
        if lexeme1 == 23 and lexeme2 == "A7":
            return -1
        if lexeme1 == 23 and lexeme2 == "B2":
            return 0
        if lexeme1 == 23 and lexeme2 == "B3":
            return -1
        if lexeme1 == 23 and lexeme2 == 1:
            return -1
        if lexeme1 == 23 and lexeme2 == 2:
            return -1
        if lexeme1 == 23 and lexeme2 == 0:
            return -1
        if lexeme1 == 23 and lexeme2 == "operand":
            return -1
        if lexeme1 == "A2" and lexeme2 == 26:
            return 0
        if lexeme1 == "A2" and lexeme2 == 11:
            return 1
        if lexeme1 == "A2" and lexeme2 == 34:
            return 1
        if lexeme1 == "A2" and lexeme2 == 25:
            return 0
        if lexeme1 == "A3" and lexeme2 == 26:
            return 1
        if lexeme1 == "A3" and lexeme2 == 11:
            return 1
        if lexeme1 == "A3" and lexeme2 == 34:
            return 1
        if lexeme1 == "A3" and lexeme2 == 22:
            return 0
        if lexeme1 == "A3" and lexeme2 == 24:
            return 0
        if lexeme1 == "A3" and lexeme2 == 25:
            return 1
        if lexeme1 == "A3" and lexeme2 == 21:
            return 0
        if lexeme1 == "A3" and lexeme2 == 23:
            return 0
        if lexeme1 == "A4" and lexeme2 == 26:
            return 1
        if lexeme1 == "A4" and lexeme2 == 11:
            return 1
        if lexeme1 == "A4" and lexeme2 == 14:
            return 0
        if lexeme1 == "A4" and lexeme2 == 15:
            return 0
        if lexeme1 == "A4" and lexeme2 == 34:
            return 1
        if lexeme1 == "A4" and lexeme2 == 22:
            return 1
        if lexeme1 == "A4" and lexeme2 == 24:
            return 1
        if lexeme1 == "A4" and lexeme2 == 25:
            return 1
        if lexeme1 == "A4" and lexeme2 == 21:
            return 1
        if lexeme1 == "A4" and lexeme2 == 23:
            return 1
        if lexeme1 == "A5" and lexeme2 == 26:
            return 1
        if lexeme1 == "A5" and lexeme2 == 19:
            return 0
        if lexeme1 == "A5" and lexeme2 == 11:
            return 1
        if lexeme1 == "A5" and lexeme2 == 20:
            return 0
        if lexeme1 == "A5" and lexeme2 == 14:
            return 1
        if lexeme1 == "A5" and lexeme2 == 15:
            return 1
        if lexeme1 == "A5" and lexeme2 == 18:
            return 0
        if lexeme1 == "A5" and lexeme2 == 34:
            return 1
        if lexeme1 == "A5" and lexeme2 == 22:
            return 1
        if lexeme1 == "A5" and lexeme2 == 24:
            return 1
        if lexeme1 == "A5" and lexeme2 == 25:
            return 1
        if lexeme1 == "A5" and lexeme2 == 21:
            return 1
        if lexeme1 == "A5" and lexeme2 == 23:
            return 1
        if lexeme1 == "A6" and lexeme2 == 26:
            return 1
        if lexeme1 == "A6" and lexeme2 == 19:
            return 1
        if lexeme1 == "A6" and lexeme2 == 11:
            return 1
        if lexeme1 == "A6" and lexeme2 == 20:
            return 1
        if lexeme1 == "A6" and lexeme2 == 14:
            return 1
        if lexeme1 == "A6" and lexeme2 == 15:
            return 1
        if lexeme1 == "A6" and lexeme2 == 18:
            return 1
        if lexeme1 == "A6" and lexeme2 == 34:
            return 1
        if lexeme1 == "A6" and lexeme2 == 22:
            return 1
        if lexeme1 == "A6" and lexeme2 == 24:
            return 1
        if lexeme1 == "A6" and lexeme2 == 25:
            return 1
        if lexeme1 == "A6" and lexeme2 == 21:
            return 1
        if lexeme1 == "A6" and lexeme2 == 23:
            return 1
        if lexeme1 == "A7" and lexeme2 == 26:
            return 1
        if lexeme1 == "A7" and lexeme2 == 19:
            return 1
        if lexeme1 == "A7" and lexeme2 == 11:
            return 1
        if lexeme1 == "A7" and lexeme2 == 20:
            return 1
        if lexeme1 == "A7" and lexeme2 == 14:
            return 1
        if lexeme1 == "A7" and lexeme2 == 16:
            return 0
        if lexeme1 == "A7" and lexeme2 == 15:
            return 1
        if lexeme1 == "A7" and lexeme2 == 17:
            return 0
        if lexeme1 == "A7" and lexeme2 == 18:
            return 1
        if lexeme1 == "A7" and lexeme2 == 34:
            return 1
        if lexeme1 == "A7" and lexeme2 == 22:
            return 1
        if lexeme1 == "A7" and lexeme2 == 24:
            return 1
        if lexeme1 == "A7" and lexeme2 == 25:
            return 1
        if lexeme1 == "A7" and lexeme2 == 21:
            return 1
        if lexeme1 == "A7" and lexeme2 == 23:
            return 1
        if lexeme1 == "B1" and lexeme2 == 26:
            return 1
        if lexeme1 == "B1" and lexeme2 == 11:
            return 1
        if lexeme1 == "B1" and lexeme2 == 34:
            return 1
        if lexeme1 == "B1" and lexeme2 == 25:
            return 1
        if lexeme1 == "B10" and lexeme2 == 13:
            return 0
        if lexeme1 == "B2" and lexeme2 == 26:
            return 1
        if lexeme1 == "B2" and lexeme2 == 11:
            return 1
        if lexeme1 == "B2" and lexeme2 == 34:
            return 1
        if lexeme1 == "B2" and lexeme2 == 22:
            return 1
        if lexeme1 == "B2" and lexeme2 == 24:
            return 1
        if lexeme1 == "B2" and lexeme2 == 25:
            return 1
        if lexeme1 == "B2" and lexeme2 == 21:
            return 1
        if lexeme1 == "B2" and lexeme2 == 23:
            return 1
        if lexeme1 == "B3" and lexeme2 == 26:
            return 1
        if lexeme1 == "B3" and lexeme2 == 11:
            return 1
        if lexeme1 == "B3" and lexeme2 == 14:
            return 1
        if lexeme1 == "B3" and lexeme2 == 15:
            return 1
        if lexeme1 == "B3" and lexeme2 == 34:
            return 1
        if lexeme1 == "B3" and lexeme2 == 22:
            return 1
        if lexeme1 == "B3" and lexeme2 == 24:
            return 1
        if lexeme1 == "B3" and lexeme2 == 25:
            return 1
        if lexeme1 == "B3" and lexeme2 == 21:
            return 1
        if lexeme1 == "B3" and lexeme2 == 23:
            return 1
        if lexeme1 == "B45" and lexeme2 == 26:
            return 1
        if lexeme1 == "B45" and lexeme2 == 19:
            return 1
        if lexeme1 == "B45" and lexeme2 == 11:
            return 1
        if lexeme1 == "B45" and lexeme2 == 20:
            return 1
        if lexeme1 == "B45" and lexeme2 == 14:
            return 1
        if lexeme1 == "B45" and lexeme2 == 16:
            return 1
        if lexeme1 == "B45" and lexeme2 == 15:
            return 1
        if lexeme1 == "B45" and lexeme2 == 17:
            return 1
        if lexeme1 == "B45" and lexeme2 == 18:
            return 1
        if lexeme1 == "B45" and lexeme2 == 34:
            return 1
        if lexeme1 == "B45" and lexeme2 == 22:
            return 1
        if lexeme1 == "B45" and lexeme2 == 24:
            return 1
        if lexeme1 == "B45" and lexeme2 == 25:
            return 1
        if lexeme1 == "B45" and lexeme2 == 21:
            return 1
        if lexeme1 == "B45" and lexeme2 == 23:
            return 1
        if lexeme1 == "B7" and lexeme2 == 26:
            return 1
        if lexeme1 == "B7" and lexeme2 == 19:
            return 1
        if lexeme1 == "B7" and lexeme2 == 11:
            return 1
        if lexeme1 == "B7" and lexeme2 == 20:
            return 1
        if lexeme1 == "B7" and lexeme2 == 14:
            return 1
        if lexeme1 == "B7" and lexeme2 == 16:
            return 1
        if lexeme1 == "B7" and lexeme2 == 15:
            return 1
        if lexeme1 == "B7" and lexeme2 == 17:
            return 1
        if lexeme1 == "B7" and lexeme2 == 18:
            return 1
        if lexeme1 == "B7" and lexeme2 == 34:
            return 1
        if lexeme1 == "B7" and lexeme2 == 22:
            return 1
        if lexeme1 == "B7" and lexeme2 == 24:
            return 1
        if lexeme1 == "B7" and lexeme2 == 25:
            return 1
        if lexeme1 == "B7" and lexeme2 == 21:
            return 1
        if lexeme1 == "B7" and lexeme2 == 23:
            return 1
        if lexeme1 == "B9" and lexeme2 == 34:
            return 0
        if lexeme1 == "EO" and lexeme2 == 11:
            return 1
        if lexeme1 == "EVF" and lexeme2 == 11:
            return 1
        if lexeme1 == "O" and lexeme2 == 10:
            return -1
        if lexeme1 == "O" and lexeme2 == 16:
            return -1
        if lexeme1 == "O" and lexeme2 == 17:
            return -1
        if lexeme1 == "O" and lexeme2 == 34:
            return -1
        if lexeme1 == "O" and lexeme2 == "A2":
            return -1
        if lexeme1 == "O" and lexeme2 == "A3":
            return -1
        if lexeme1 == "O" and lexeme2 == "A4":
            return -1
        if lexeme1 == "O" and lexeme2 == "A5":
            return -1
        if lexeme1 == "O" and lexeme2 == "A6":
            return -1
        if lexeme1 == "O" and lexeme2 == "A7":
            return -1
        if lexeme1 == "O" and lexeme2 == "B1":
            return -1
        if lexeme1 == "O" and lexeme2 == "B2":
            return -1
        if lexeme1 == "O" and lexeme2 == "B3":
            return -1
        if lexeme1 == "O" and lexeme2 == "B9":
            return -1
        if lexeme1 == "O" and lexeme2 == "O":
            return -1
        if lexeme1 == "O" and lexeme2 == "body_function":
            return -1
        if lexeme1 == "O" and lexeme2 == 1:
            return -1
        if lexeme1 == "O" and lexeme2 == 6:
            return -1
        if lexeme1 == "O" and lexeme2 == "enum_operator":
            return 0
        if lexeme1 == "O" and lexeme2 == "expression":
            return -1
        if lexeme1 == "O" and lexeme2 == 2:
            return -1
        if lexeme1 == "O" and lexeme2 == 0:
            return -1
        if lexeme1 == "O" and lexeme2 == "operand":
            return -1
        if lexeme1 == "O" and lexeme2 == "operator":
            return -1
        if lexeme1 == "O" and lexeme2 == 9:
            return -1
        if lexeme1 == "O" and lexeme2 == 12:
            return -1
        if lexeme1 == "O" and lexeme2 == 13:
            return 1
        if lexeme1 == "PEO" and lexeme2 == 11:
            return 0
        if lexeme1 == "PEVF" and lexeme2 == 11:
            return 0
        if lexeme1 == "body_function" and lexeme2 == 10:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 16:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 17:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 34:
            return 1
        if lexeme1 == "body_function" and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return 1
        if lexeme1 == "body_function" and lexeme2 == 1:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 6:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 36:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 2:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 0:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 9:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 7:
            return 0
        if lexeme1 == "body_function" and lexeme2 == 12:
            return 1
        if lexeme1 == "body_function" and lexeme2 == 13:
            return 1
        if (lexeme1 == 3 or lexeme1 == 4 or lexeme1 == 5) and lexeme2 == 0:
            return 0
        if lexeme1 == 1 and lexeme2 == 26:
            return 1
        if lexeme1 == 1 and lexeme2 == 19:
            return 1
        if lexeme1 == 1 and lexeme2 == 11:
            return 1
        if lexeme1 == 1 and lexeme2 == 20:
            return 1
        if lexeme1 == 1 and lexeme2 == 14:
            return 1
        if lexeme1 == 1 and lexeme2 == 16:
            return 1
        if lexeme1 == 1 and lexeme2 == 15:
            return 1
        if lexeme1 == 1 and lexeme2 == 17:
            return 1
        if lexeme1 == 1 and lexeme2 == 18:
            return 1
        if lexeme1 == 1 and lexeme2 == 34:
            return 1
        if lexeme1 == 1 and lexeme2 == 22:
            return 1
        if lexeme1 == 1 and lexeme2 == 24:
            return 1
        if lexeme1 == 1 and lexeme2 == 25:
            return 1
        if lexeme1 == 1 and lexeme2 == 21:
            return 1
        if lexeme1 == 1 and lexeme2 == 23:
            return 1
        if lexeme1 == 1 and lexeme2 == 12:
            return 1
        if lexeme1 == "description" and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return -1
        if lexeme1 == "description" and lexeme2 == 36:
            return 1
        if lexeme1 == "description" and lexeme2 == "main_program":
            return 0
        if lexeme1 == "descriptionF" and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return 1
        if lexeme1 == "descriptionF" and lexeme2 == 36:
            return 1
        if lexeme1 == 6 and lexeme2 == "body_function":
            return 0
        if lexeme1 == 6 and lexeme2 == 12:
            return -1
        if lexeme1 == 36 and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return -1
        if lexeme1 == "enum_operator" and lexeme2 == 13:
            return 1
        if lexeme1 == "expression" and lexeme2 == 11:
            return -1
        if lexeme1 == "expression" and lexeme2 == 34:
            return 1
        if lexeme1 == "expression" and lexeme2 == "B7":
            return 0
        if lexeme1 == 2 and lexeme2 == 26:
            return 1
        if lexeme1 == 2 and lexeme2 == 19:
            return 1
        if lexeme1 == 2 and lexeme2 == 11:
            return 1
        if lexeme1 == 2 and lexeme2 == 20:
            return 1
        if lexeme1 == 2 and lexeme2 == 14:
            return 1
        if lexeme1 == 2 and lexeme2 == 16:
            return 1
        if lexeme1 == 2 and lexeme2 == 15:
            return 1
        if lexeme1 == 2 and lexeme2 == 17:
            return 1
        if lexeme1 == 2 and lexeme2 == 18:
            return 1
        if lexeme1 == 2 and lexeme2 == 34:
            return 1
        if lexeme1 == 2 and lexeme2 == 22:
            return 1
        if lexeme1 == 2 and lexeme2 == 24:
            return 1
        if lexeme1 == 2 and lexeme2 == 25:
            return 1
        if lexeme1 == 2 and lexeme2 == 21:
            return 1
        if lexeme1 == 2 and lexeme2 == 23:
            return 1
        if lexeme1 == 2 and lexeme2 == 12:
            return 1
        if lexeme1 == 0 and lexeme2 == 26:
            return 1
        if lexeme1 == 0 and lexeme2 == 19:
            return 1
        if lexeme1 == 0 and lexeme2 == 10:
            return -1
        if lexeme1 == 0 and lexeme2 == 11:
            return 1
        if lexeme1 == 0 and lexeme2 == 20:
            return 1
        if lexeme1 == 0 and lexeme2 == 14:
            return 1
        if lexeme1 == 0 and lexeme2 == 16:
            return 1
        if lexeme1 == 0 and lexeme2 == 33:
            return 1
        if lexeme1 == 0 and lexeme2 == 15:
            return 1
        if lexeme1 == 0 and lexeme2 == 17:
            return 1
        if lexeme1 == 0 and lexeme2 == 18:
            return 1
        if lexeme1 == 0 and lexeme2 == 34:
            return 1
        if lexeme1 == 0 and lexeme2 == 22:
            return 1
        if lexeme1 == 0 and lexeme2 == 24:
            return 1
        if lexeme1 == 0 and lexeme2 == 27:
            return -1
        if lexeme1 == 0 and lexeme2 == 25:
            return 1
        if lexeme1 == 0 and lexeme2 == 21:
            return 1
        if lexeme1 == 0 and lexeme2 == 23:
            return 1
        if lexeme1 == 0 and lexeme2 == "B45":
            return 0
        if lexeme1 == 0 and lexeme2 == "description":
            return 0
        if lexeme1 == 0 and lexeme2 == "descriptionF":
            return -1
        if lexeme1 == 0 and lexeme2 == 12:
            return 1
        if lexeme1 == "main_program" and lexeme2 == 36:
            return 1
        if lexeme1 == "operand" and lexeme2 == 26:
            return 1
        if lexeme1 == "operand" and lexeme2 == 19:
            return 1
        if lexeme1 == "operand" and lexeme2 == 11:
            return 1
        if lexeme1 == "operand" and lexeme2 == 20:
            return 1
        if lexeme1 == "operand" and lexeme2 == 14:
            return 1
        if lexeme1 == "operand" and lexeme2 == 16:
            return 1
        if lexeme1 == "operand" and lexeme2 == 15:
            return 1
        if lexeme1 == "operand" and lexeme2 == 17:
            return 1
        if lexeme1 == "operand" and lexeme2 == 18:
            return 1
        if lexeme1 == "operand" and lexeme2 == 34:
            return 1
        if lexeme1 == "operand" and lexeme2 == 22:
            return 1
        if lexeme1 == "operand" and lexeme2 == 24:
            return 1
        if lexeme1 == "operand" and lexeme2 == 25:
            return 1
        if lexeme1 == "operand" and lexeme2 == 21:
            return 1
        if lexeme1 == "operand" and lexeme2 == 23:
            return 1
        if lexeme1 == "operand" and lexeme2 == 12:
            return 0
        if lexeme1 == "operator" and lexeme2 == 34:
            return 0
        if lexeme1 == "param" and lexeme2 == 11:
            return 1
        if lexeme1 == "param" and lexeme2 == 33:
            return -1
        if lexeme1 == "param" and lexeme2 == "EVF":
            return 0
        if lexeme1 == 9 and lexeme2 == 10:
            return -1
        if lexeme1 == 9 and lexeme2 == 16:
            return -1
        if lexeme1 == 9 and lexeme2 == 17:
            return -1
        if lexeme1 == 9 and lexeme2 == "A2":
            return -1
        if lexeme1 == 9 and lexeme2 == "A3":
            return -1
        if lexeme1 == 9 and lexeme2 == "A4":
            return -1
        if lexeme1 == 9 and lexeme2 == "A5":
            return -1
        if lexeme1 == 9 and lexeme2 == "A6":
            return -1
        if lexeme1 == 9 and lexeme2 == "A7":
            return -1
        if lexeme1 == 9 and lexeme2 == "B1":
            return -1
        if lexeme1 == 9 and lexeme2 == "B2":
            return -1
        if lexeme1 == 9 and lexeme2 == "B3":
            return -1
        if lexeme1 == 9 and lexeme2 == 1:
            return -1
        if lexeme1 == 9 and lexeme2 == "expression":
            return 0
        if lexeme1 == 9 and lexeme2 == 2:
            return -1
        if lexeme1 == 9 and lexeme2 == 0:
            return -1
        if lexeme1 == 9 and lexeme2 == "operand":
            return -1
        if lexeme1 == 7 and lexeme2 == 10:
            return 0
        if lexeme1 == 12 and lexeme2 == 10:
            return -1
        if lexeme1 == 12 and lexeme2 == 11:
            return 1
        if lexeme1 == 12 and lexeme2 == 16:
            return -1
        if lexeme1 == 12 and lexeme2 == 33:
            return -1
        if lexeme1 == 12 and lexeme2 == 17:
            return -1
        if lexeme1 == 12 and lexeme2 == 34:
            return -1
        if lexeme1 == 12 and lexeme2 == "A2":
            return -1
        if lexeme1 == 12 and lexeme2 == "A3":
            return -1
        if lexeme1 == 12 and lexeme2 == "A4":
            return -1
        if lexeme1 == 12 and lexeme2 == "A5":
            return -1
        if lexeme1 == 12 and lexeme2 == "A6":
            return -1
        if lexeme1 == 12 and lexeme2 == "A7":
            return -1
        if lexeme1 == 12 and lexeme2 == "B1":
            return -1
        if lexeme1 == 12 and lexeme2 == "B10":
            return 0
        if lexeme1 == 12 and lexeme2 == "B2":
            return -1
        if lexeme1 == 12 and lexeme2 == "B3":
            return -1
        if lexeme1 == 12 and lexeme2 == "B9":
            return -1
        if lexeme1 == 12 and lexeme2 == "EO":
            return 0
        if lexeme1 == 12 and lexeme2 == "O":
            return -1
        if lexeme1 == 12 and lexeme2 == "body_function":
            return -1
        if lexeme1 == 12 and lexeme2 == 1:
            return -1
        if lexeme1 == 12 and lexeme2 == 6:
            return -1
        if lexeme1 == 12 and lexeme2 == "enum_operator":
            return -1
        if lexeme1 == 12 and lexeme2 == "expression":
            return -1
        if lexeme1 == 12 and lexeme2 == 2:
            return -1
        if lexeme1 == 12 and lexeme2 == 0:
            return -1
        if lexeme1 == 12 and lexeme2 == "operand":
            return -1
        if lexeme1 == 12 and lexeme2 == "operator":
            return -1
        if lexeme1 == 12 and lexeme2 == 9:
            return -1
        if lexeme1 == 12 and lexeme2 == 12:
            return -1
        if lexeme1 == 12 and lexeme2 == 13:
            return 0
        if lexeme1 == 13 and lexeme2 == 10:
            return 1
        if lexeme1 == 13 and lexeme2 == 16:
            return 1
        if lexeme1 == 13 and lexeme2 == 17:
            return 1
        if lexeme1 == 13 and lexeme2 == 34:
            return 1
        if lexeme1 == 13 and (lexeme2 == 3 or lexeme2 == 4 or lexeme2 == 5):
            return 1
        if lexeme1 == 13 and lexeme2 == 1:
            return 1
        if lexeme1 == 13 and lexeme2 == 6:
            return 1
        if lexeme1 == 13 and lexeme2 == 36:
            return 1
        if lexeme1 == 13 and lexeme2 == 2:
            return 1
        if lexeme1 == 13 and lexeme2 == 0:
            return 1
        if lexeme1 == 13 and lexeme2 == 9:
            return 1
        if lexeme1 == 13 and lexeme2 == 7:
            return 1
        if lexeme1 == 13 and lexeme2 == 12:
            return 1
        if lexeme1 == 13 and lexeme2 == 13:
            return 1
        raise Exception('Error! get_sign:' + str(lexeme1) + ' ' + str(lexeme2))
