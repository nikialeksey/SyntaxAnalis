from Syntax import LexemId as lId
from Exceptions.SemanticException import *
from collections import deque
from Interpreter import Interpreter
from Semantic.ValueObj import ValueObj


class Node:
    VARIABLE = 0
    FUNCTION = 1
    SPECIAL = 2

    __id = 0  # уникальный идентификатор

    def __init__(self, type_object, type_data, lexeme, count_parameter):
        self.type_object = type_object  # Тип объекта (функция или переменная или специальный объект)
        self.type_data = type_data  # Тип данных (short, int, long)
        self.lexeme = lexeme  # Представление переменной или функции (имя)
        self.count_parameter = count_parameter  # Количество параметров функции
        self.value = 0  # Значение переменной или возвращаемое значение функции

        self.id = Node.__id
        Node.__id += 1

        self.__left = None
        self.__right = None
        self.__parent = None

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

    def is_special_node(self):
        return self.type_object == Node.SPECIAL

    def is_variable_node(self):
        return self.type_object == Node.VARIABLE

    def is_function_node(self):
        return self.type_object == Node.FUNCTION


class SemanticTree:
    def __init__(self):
        self.variable_object = Node.VARIABLE
        self.function_object = Node.FUNCTION
        self.special_object = Node.SPECIAL

        self.dummy = Node(-1, -1, -1, -1)
        root = Node(self.special_object, -1, -1, -1)

        self.__root = root
        self.__root.set_left_node(self.dummy)
        self.__root.set_right_node(self.dummy)
        self.__root.set_parent_node(self.dummy)
        self.pointer = root
        self.__current_type = lId.TInt
        self.current_count_parameter = 0

    def get_root(self):
        return self.__root

    def get_dummy(self):
        return self.dummy

    def get_current_type(self):
        return self.__current_type

    def set_current_type(self, current_type):
        self.__current_type = current_type

    def set_value_obj(self, value_obj):
        Interpreter.to_type(value_obj, self.pointer.type_data)
        self.pointer.value = value_obj.value

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

    def get_variable_value_obj(self, lexeme):
        p = self.pointer
        while p != self.__root:
            if p.lexeme == lexeme:
                return ValueObj(value=p.value, type=p.type_data)
            p = p.get_parent()

    def get_variable_node(self, lexeme):
        p = self.pointer
        while p != self.__root:
            if p.lexeme == lexeme:
                return p
            p = p.get_parent()

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

    def write(self, file_name):
        f = open(file_name, mode='w')
        f.write("digraph semantic {\n")

        # set custom
        f.write('ratio=fill; node [margin=0, color="#aaaa33", style="filled", shape=box, fontsize=8];'
                '\ngraph [ordering="out"];\n')

        # add edges
        def next_dummy_name():
            next_dummy_name.cnt_dummy += 1
            return "dummy" + str(next_dummy_name.cnt_dummy)
        next_dummy_name.cnt_dummy = 0

        def write_dummy(parent_id):
            dummy_name = next_dummy_name()
            f.write(dummy_name + " [shape=point];\n")
            f.write(str(parent_id) + " -> " + dummy_name + ";\n")

        def function_label(node):
            s = "<b>fun:</b> " + node.lexeme + "<br align='left'/><b>type:</b> " + str(lId.lexemIdToStr[node.type_data])
            s = s + "<br align='left'/><b>parameters:</b> " + str(node.count_parameter)
            s = s + "<br align='left'/><b align='left'>value:</b> " + str(node.value)
            return s

        def variable_label(node):
            s = "<b>var:</b> " + node.lexeme + "<br align='left'/><b>type</b>: " + str(lId.lexemIdToStr[node.type_data])
            s = s + "<br align='left'/><b>value:</b> " + str(node.value)
            return s

        root = self.get_root()
        dummy = self.get_dummy()
        queue = deque()
        queue.append(root)
        while len(queue) > 0:
            node = queue.popleft()

            if node.is_special_node():
                f.write(str(node.id) + ' [label=< >, fillcolor="#ff0000", shape=circle, width=0.1];\n')
            else:
                label = function_label(node) if node.is_function_node() else variable_label(node)
                f.write(str(node.id) + ' [label=<' + label + '>];\n')

            if node.get_left() != dummy:
                left = node.get_left()
                f.write(str(node.id) + " -> " + str(left.id) + ";\n")
                queue.append(left)
            else:
                write_dummy(node.id)

            if node.get_right() != dummy:
                right = node.get_right()
                f.write(str(node.id) + " -> " + str(right.id) + ";\n")
                queue.append(right)
            else:
                write_dummy(node.id)

        f.write("}")