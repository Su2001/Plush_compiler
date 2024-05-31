from typing import List
from codegen.classes import *
from codegen.classes import Bool as b
from z3 import Int, Solver, sat, Bool, And, Or, Not, Real

class Checker:
    def __init__(self) -> None:
        self.context: List[dict]=[]
        self.temp =[]

    def push_context(self):
        self.context.append({})

    def pop_context(self):
        self.context.pop()

    def add_to(self,name:str, typ, value, c):
        self.temp =[]
        n = self.context[-1]
        if typ == "int":
            x = Int(name)
        elif typ == "float":
            x = Real(name)
        else:
            x = Bool(name)
        newc = c
        if c:
            newc = self.process_cond(x, c, name)
        n[name] =(typ, value, x, newc, self.temp)    
        if value :
            self.solve(name, value)   
    
    def get(self, name):
        for i in self.context[::-1]:
            if name in i.keys():
                return i[name]
        raise Exception("not contains") 
    
    def set(self, name, newv):
        for i in self.context[::-1]:
            if name in i.keys():
                i[name] = newv
                return
        raise Exception("not contains") 

    def solve(self, name,  newvalue):
        solver = Solver()

        o_typ, _, o_x, o_c, o_dep = self.get(name)
        for i in o_dep :
            _, temp_v, temp_x, _, _ = self.get(i)
            solver.add(temp_x == temp_v)
        if  o_c == None:
            return
        newv =self.solve_value(newvalue)
        solver.add(o_x == newv)
        solver.add(o_c)
        if solver.check() != sat:
            raise ValueError(f"Value {newv} does not satisfy the constraint {o_c}")
        else:
            self.set(name, (o_typ, newv, o_x, o_c, self.temp))

    def solve_value(self, value):
        match value:
            case Integer():
                return value.value
            case Float():
                return value.value
            case b():
                return value.value
            case Neg():
                return -(self.solve_value(value.value))
            case Assignment():
                _, v, _, _, _ = self.get(value.name)
                return v
            case BoolOp():
                op = value.operation
                if op == 'or'  : return self.solve_value(value.param1) or self.solve_value(value.param2)
                elif op == 'and': return self.solve_value(value.param1) and self.solve_value(value.param2)
                elif op == 'NEG': return not self.solve_value(value.param1) 
            case Comp():
                op = value.operation
                if op == '>'  : return self.solve_value(value.param1) > self.solve_value(value.param2)
                elif op == '>=': return self.solve_value(value.param1) >= self.solve_value(value.param2)
                elif op == '<': return self.solve_value(value.param1) < self.solve_value(value.param2)
                elif op == '<=': return self.solve_value(value.param1) <= self.solve_value(value.param2)
                elif op == '==': return self.solve_value(value.param1) == self.solve_value(value.param2)
                elif op == '!=': return self.solve_value(value.param1) != self.solve_value(value.param2)
            case MathOp():
                op = value.operation
                if op == '+'  : return self.solve_value(value.param1) + self.solve_value(value.param2)
                elif op == '-': return self.solve_value(value.param1) - self.solve_value(value.param2)
                elif op == '*': return self.solve_value(value.param1) * self.solve_value(value.param2)
                elif op == '/': return self.solve_value(value.param1) / self.solve_value(value.param2)
                elif op == '%': return self.solve_value(value.param1) % self.solve_value(value.param2)
                elif op == '^': return self.solve_value(value.param1) ** self.solve_value(value.param2)
            case _:
                raise Exception("Cant process function call or access array in liquid type check")

    def process_cond(self, x, c, name):
        match c:
            case BoolOp():
                op = c.operation
                if op == 'or'  : return Or(self.process_cond(x,c.param1, name), self.process_cond(x,c.param2, name))
                elif op == 'and': return And(self.process_cond(x,c.param1, name), self.process_cond(x,c.param2, name))
                elif op == 'NEG': return Not(self.process_cond(x,c.param1, name))
            case Comp():
                op = c.operation
                if op == '>'  : return self.process_cond(x,c.param1, name) > self.process_cond(x,c.param2, name)
                elif op == '>=': return self.process_cond(x,c.param1, name) >= self.process_cond(x,c.param2, name)
                elif op == '<': return self.process_cond(x,c.param1, name) < self.process_cond(x,c.param2, name)
                elif op == '<=': return self.process_cond(x,c.param1, name) <= self.process_cond(x,c.param2, name)
                elif op == '==': return self.process_cond(x,c.param1, name) == self.process_cond(x,c.param2, name)
                elif op == '!=': return self.process_cond(x,c.param1, name) != self.process_cond(x,c.param2, name)
            case Assignment():
                if name != c.name:
                    _, _, o_x, _, _ = self.get(c.name)
                    self.temp.append(c.name)
                    return o_x
                else:
                    return x           
            case Integer():
                return c.value
            case Neg():
                return -(self.process_cond(x,c.value, name))
            case Float():
                return c.value
            case b():
                return c.value
            case _:
                raise Exception("Cant process function call or access array in liquid type check")