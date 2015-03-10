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

