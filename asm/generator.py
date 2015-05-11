from Semantic.SemanticTree import *
from Syntax.LexemId import *


is_free_register = {'ebx': True, 'ecx': True, 'edx': True, 'edi': True, 'esi': True}
trio_to_register = {}


def give_free_register():
    for reg, is_free in is_free_register.items():
        if is_free:
            is_free_register[reg] = False
            return reg
    raise Exception('stack overflow')


def release_register(reg):
    is_free_register[reg] = True


def release_all_register():
    for reg, is_free in is_free_register.items():
        is_free_register[reg] = True


def generate_definition_var(type_var, name_var, out):
    type_to_asm_type = {
        TShort: 'dw',
        TInt: 'dd',
        TLong: 'dq',
    }
    out.write(name_var + ' ' + type_to_asm_type[type_var] + ' 01H DUP(?)' + '\n')


def give_jump_operation(oper):
    if oper == '==':
        return 'je'
    elif oper == '!=':
        return 'jne'
    elif oper == '<':
        return 'jl'
    elif oper == '<=':
        return 'jle'
    elif oper == '>':
        return 'jg'
    elif oper == '>=':
        return 'jge'

def give_comp_operation(oper):
    if oper == '==':
        return 'eq'
    elif oper == '!=':
        return 'ne'
    elif oper == '<':
        return 'lt'
    elif oper == '<=':
        return 'le'
    elif oper == '>':
        return 'gt'
    elif oper == '>=':
        return 'ge'


def give_next_label():
    give_next_label.label += 1
    return 'label' + str(give_next_label.label - 1)
give_next_label.label = 0


def generate_operation(trio, oper, op1, op2, out):
    out.write('\n')

    is_in_register = lambda op: '(' in op

    def write_asm(reg_op1, reg_op2, oper, trio):
        out.write('cmp ' + reg_op1 + ', ' + reg_op2 + '\n')
        jump = give_jump_operation(oper)
        reg = give_free_register()
        label1 = give_next_label()
        label2 = give_next_label()
        out.write(jump + ' ' + label1 + '\n')
        out.write('mov ' + reg + ', 0' + '\n')
        out.write('jmp ' + label2 + '\n')
        out.write(label1 + ': ' + '\n')
        out.write('mov ' + reg + ', 1' + '\n')
        out.write(label2 + ': ' + '\n')
        trio_to_register[trio] = reg

    if oper == '=':
        if is_in_register(op2):
            op2 = trio_to_register[op2]
        out.write('mov eax,' + ' ' + op2 + '\n')
        out.write('mov ' + op1 + ', eax' + '\n')
        trio_to_register.clear()
        release_all_register()
    else:
        if is_in_register(op1) and is_in_register(op2):
            reg_op1 = trio_to_register[op1]
            reg_op2 = trio_to_register[op2]
            release_register(reg_op1)
            release_register(reg_op2)
            write_asm(reg_op1, reg_op2, oper, trio)
        elif is_in_register(op1) and not is_in_register(op2):
            reg_op1 = trio_to_register[op1]
            release_register(reg_op1)
            write_asm(reg_op1, op2, oper, trio)
        elif not is_in_register(op1) and is_in_register(op2):
            reg_op2 = trio_to_register[op2]
            release_register(reg_op2)
            write_asm(op1, reg_op2, oper, trio)
        else:
            reg = give_free_register()
            trio_to_register[trio] = reg
            out.write('mov ' + reg + ', ' + op1 + ' ' +  give_comp_operation(oper) + ' ' + op2 + '\n')


def generate_init_block(trios: list, out):
    out.write('\n; dynamic initialization block \n')

    for trio in trios:
        splitted_trio = trio[trio.index(')') + 2:-1].split()
        op1 = splitted_trio[0]
        op2 = splitted_trio[2]
        oper = splitted_trio[1]
        generate_operation('(' + trio.split(')')[0] + ')', oper, op1, op2, out)

    out.write('; end initialization block \n\n')


def get_init_trios(trio_file) -> list:
    trios = []
    is_init_trio = True
    for trio in trio_file:
        if 'proc' in trio:
            is_init_trio = False
        elif 'endp' in trio:
            is_init_trio = True
        elif is_init_trio:
            trios.append(trio)
    return trios


class ASMGenerator:

    def __init__(self, semantic_tree: SemanticTree, trio_file_name, out_file_name):
        self.semantic_tree = semantic_tree
        self.trio_file_name = trio_file_name
        self.out_file_name = out_file_name

    def generate(self):
        out = open(self.out_file_name, 'w')

        semantic = self.semantic_tree
        trio_file = open(self.trio_file_name)
        p = semantic.get_root()
        while p != semantic.dummy:
            if p.type_object == Node.VARIABLE:
                generate_definition_var(p.type_data, p.lexeme, out)
            p = p.get_left()

        generate_init_block(get_init_trios(trio_file), out)


        trio_file.close()

        out.close()