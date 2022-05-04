from __future__ import annotations
from typing import List, Tuple

input = f'logic_processing_operation.txt'

'''
largest valid(z = 0) 14-digit MTL no 0
13579246899999
algorithm:
register, stack pop append
splitlines() inp w = line[0] operation, var1, var2 = line[1:].split()
operators:
'add' var1 = var1 + var2/inp
'mod' var1 = var1 % var2/inp math_floor var2/inp > 0
'mul' var1 = var1 * var2/inp if var2/inp = 1:
'div' var1 = var1 // var2/inp var2/inp != 0
'eql' if var1 = var2: var1 == 1 else var1 == 0

var1 lowest(1's) bit
var2 second-lowest(2's) bit
var3 third-lowest(3's) bit
inp w fourth-lowest(4's) bit

operation:
if == 0: continue
model_no = []
for line in s:
    operator(inp)
    if z == 0:
        model_no.append(z)
for i in range(len(model_no) - 1w):
    largest = max(int(model_no[i]))

return largest
'''
class ALR:
    def __set__name__(self, owner: object, name: str):
        self.name = name
    def __get__(self, obj: object, objtype = None) -> int:
        return getattr(obj, '_registers')[self.name]
    def __set__(self, obj: object, value: int):
        getattr(obj, '_registers')[self.name] = value
class ALU:
    w = ALR()
    x = ALR()
    y = ALR()
    z = ALR()
    def __init__(self, w: int = 0, x: int = 0, y: int = 0, z: int = 0) -> None:
        self._registers = {'w': w, 'x': x, 'y': y, 'z': z}
    def exe(self, ins_s: List[str], inputs: List[int] = None) -> None:
        inputs = inputs.copy() if inputs else []
        operations = {'inp': lambda a, b: int(inputs.pop(0)), 'add': lambda a, b: self._registers[a] + b, \
        'mul': lambda a, b: self._registers[a] * b, 'div': lambda a, b: int(self._registers[a] / b), \
        'mod': lambda a, b: self._registers[a] % b, 'eql': lambda a, b: int(self._registers[a] == b)}
        for ins in ins_s:
            operation, arg_a, arg_b = (ins_s + '0').split(' ')[:3]
            arg_b = self._registers[arg_b] if arg_b.isalpha() else int(arg_b)
            self._registers[arg_a] = operations[operation](arg_a, arg_b)
def ck_model_no(ins_s: List[int], model_no: int) -> bool:
    alu = ALU()
    alu.exe(ins_s, [int(d) for d in list(str(model_no))])
    return not alu.z
def find_dig(l: int, r: int, find_max: bool = True) -> Tuple[int, int]:
    if find_max:
        if l + r <= 0:
            return 9, 9 + l + r
        else:
            return 9 - l - r, 9
    else:
        if l + r <= 0:
            return 1 - l - r, 1
        else:
            return 1, 1 + l + r
def model_no(ins_s: List[str], find_max: bool = True) -> int:
    ins_st = []
    for ins in ins_s:
        if ins.startswith('inp'):
            ins_st.append([])
        ins_st[-1].append(ins)
    ver_num_dig: List = [None] * len(ins_st)
    l_dig_st = []
    for i in range(len(ins_st)):
        if ins_st[i][4] == 'div z 1':
            l_dig_st.append((i, ins_st[i]))
        else:
            l_i, l_ins_s = l_dig_st.pop()
            l_incre = int(l_ins_s[15].split(' ')[2])
            r_incre = int(ins_st[i][5].split(' ')[2])
            ver_num_dig[l_i], ver_num_dig[i] = find_dig(l_incre, r_incre, find_max)
    return int(''.join([str(d) for d in ver_num_dig]))
def load_data(s: str) -> List[str]:
    with open(s,'r', encoding = 'ascii') as txt:
        return [line.strip() for line in txt.readlines()]
def p1(s: str) -> int:
    data_p1 = load_data(s)
    return model_no(data_p1)
def p2(s: str) -> int:
    data_p2 = load_data(s)
    return model_no(data_p2, False)

if __name__ == '__main__':
    p1(input)
    print(f'p1: {p1(input)}')
    p2(input)
    print(f'p2: {p2(input)}')










# end
