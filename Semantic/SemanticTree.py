from Syntax import LexemId as lId
from Exceptions.SemanticException import *

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

