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

