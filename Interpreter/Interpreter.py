__author__ = 'Alexey Nikitin'
from Syntax import LexemId as lId
from Semantic.ValueObj import ValueObj

interpreter_flag = False


def to_type(value_obj, type):
    value_obj.type = type

    # TO DO привидение типов (нужно побитовое и)
    if type == lId.TShort:
        value_obj.value &= (1 << 16) - 1
        if value_obj.value & (1 << 16):
            value_obj.value &= 1 << 16
            value_obj.value *= -1
    elif type == lId.TInt:
        value_obj.value &= (1 << 32) - 1
        if value_obj.value & (1 << 32):
            value_obj.value &= 1 << 32
            value_obj.value *= -1
    else:
        value_obj.value &= (1 << 64) - 1
        if value_obj.value & (1 << 64):
            value_obj.value &= 1 << 64
            value_obj.value *= -1

def get_value_obj_num10(lexeme_num10):
    value = int(lexeme_num10)
    if -32768 <= value <= 32767:
        return ValueObj(value=value, type=lId.TShort)
    elif -2147483648 <= value <= -2147483647:
        return ValueObj(value=value, type=lId.TInt)
    else:
        # TO DO побитовое и с ((1 << 64) - 1)
        return ValueObj(value=value & ((1 << 64) - 1), type=lId.TLong)


def set_value_obj_from_num10(value_obj, lexeme_num10):
    _value_obj = get_value_obj_num10(lexeme_num10)
    value_obj.value = _value_obj.value
    value_obj.type = _value_obj.type


def get_value_obj_num16(lexeme_num16):
    value = int(lexeme_num16, 16)
    if -32768 <= value <= 32767:
        return ValueObj(value=value, type=lId.TShort)
    elif -2147483648 <= value <= -2147483647:
        return ValueObj(value=value, type=lId.TInt)
    else:
        # TO DO побитовое и с ((1 << 64) - 1)
        return ValueObj(value=value & ((1 << 64) - 1), type=lId.TLong)


def set_value_obj_from_num16(value_obj, lexeme_num16):
    _value_obj = get_value_obj_num16(lexeme_num16)
    value_obj.value = _value_obj.value
    value_obj.type = _value_obj.type


def verify_equal(value_obj1, value_obj2):
    value_obj1.value = 1 if value_obj1.value == value_obj2.value else 0


def verify_unequal(value_obj1, value_obj2):
    value_obj1.value = 1 if value_obj1.value != value_obj2.value else 0


def verify_greater(value_obj1, value_obj2):
    value_obj1.value = 1 if value_obj1.value > value_obj2.value else 0


def verify_greater_eq(value_obj1, value_obj2):
    value_obj1.value = 1 if value_obj1.value >= value_obj2.value else 0


def verify_less(value_obj1, value_obj2):
    value_obj1.value = 1 if value_obj1.value < value_obj2.value else 0


def verify_less_eq(value_obj1, value_obj2):
    value_obj1.value = 1 if value_obj1.value <= value_obj2.value else 0


def type_of(value_obj1, value_obj2):
    if value_obj1.type == lId.TShort:
        return value_obj2.type
    elif value_obj1.type == lId.TInt:
        if value_obj2.type == lId.TLong:
            return value_obj2.type
        else:
            return value_obj1.type
    else:
        return value_obj1.type


def mul(value_obj1, value_obj2):
    _type = type_of(value_obj1, value_obj2)
    value_obj1.type = _type
    value_obj2.type = _type
    if _type == lId.TShort:
        mul_short(value_obj1, value_obj2)
    elif _type == lId.TInt:
        mul_int(value_obj1, value_obj2)
    else:
        mul_long(value_obj1, value_obj2)


def div(value_obj1, value_obj2):
    _type = type_of(value_obj1, value_obj2)
    value_obj1.type = _type
    value_obj2.type = _type
    if _type == lId.TShort:
        div_short(value_obj1, value_obj2)
    elif _type == lId.TInt:
        div_int(value_obj1, value_obj2)
    else:
        div_long(value_obj1, value_obj2)


def mod(value_obj1, value_obj2):
    _type = type_of(value_obj1, value_obj2)
    value_obj1.type = _type
    value_obj2.type = _type
    if _type == lId.TShort:
        mod_short(value_obj1, value_obj2)
    elif _type == lId.TInt:
        mod_int(value_obj1, value_obj2)
    else:
        mod_long(value_obj1, value_obj2)


def sub(value_obj1, value_obj2):
    value_obj2.value *= -1
    sum(value_obj1, value_obj2)


def sum(value_obj1, value_obj2):
    _type = type_of(value_obj1, value_obj2)
    value_obj1.type = _type
    value_obj2.type = _type
    if _type == lId.TShort:
        sum_short(value_obj1, value_obj2)
    elif _type == lId.TInt:
        sum_int(value_obj1, value_obj2)
    else:
        sum_long(value_obj1, value_obj2)


def sum_short(value_obj1, value_obj2):
    # TO DO сделать битовое и с ((1 << 16) - 1)
    value_obj1.value = value_obj1.value + value_obj2.value


def sum_int(value_obj1, value_obj2):
    # TO DO сделать битовое и с ((1 << 32) - 1)
    value_obj1.value = value_obj1.value + value_obj2.value


def sum_long(value_obj1, value_obj2):
    # TO DO сделать битовое и с ((1 << 64) - 1)
    value_obj1.value = value_obj1.value + value_obj2.value


def mul_short(value_obj1, value_obj2):
    # TO DO сделать битовое и с ((1 << 16) - 1)
    value_obj1.value = value_obj1.value * value_obj2.value


def mul_int(value_obj1, value_obj2):
    # TO DO сделать битовое и с ((1 << 32) - 1)
    value_obj1.value = value_obj1.value * value_obj2.value


def mul_long(value_obj1, value_obj2):
    # TO DO сделать битовое и с ((1 << 64) - 1)
    value_obj1.value = value_obj1.value * value_obj2.value


def div_short(value_obj1, value_obj2):
    value_obj1.value = value_obj1.value // value_obj2.value


def div_int(value_obj1, value_obj2):
    value_obj1.value = value_obj1.value // value_obj2.value


def div_long(value_obj1, value_obj2):
    value_obj1.value = value_obj1.value // value_obj2.value


def mod_short(value_obj1, value_obj2):
    value_obj1.value = value_obj1.value % value_obj2.value


def mod_int(value_obj1, value_obj2):
    value_obj1.value = value_obj1.value % value_obj2.value


def mod_long(value_obj1, value_obj2):
    value_obj1.value = value_obj1.value % value_obj2.value