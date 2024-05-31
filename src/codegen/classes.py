from dataclasses import dataclass
from typing import Any, List, Union

class ParsingException(Exception):
    pass

@dataclass
class Operation():
    pass

@dataclass
class Number():
    pass

@dataclass
class Integer(Number):
    value : int

    def to_dict(self) -> dict:
        return {
            'value': self.value
        }

@dataclass
class Float(Integer):
    value : float

    def to_dict(self) -> dict:
        return {
            'value': self.value
        }

@dataclass
class Bool():
    value : bool
    def to_dict(self) -> dict:
        return {
            'value': self.value
        }

@dataclass
class String():
    value : str
    def to_dict(self) -> dict:
        return {
            'value': self.value
        }
    
@dataclass
class Char():
    value : str
    def to_dict(self) -> dict:
        return {
            'value': self.value
        }

@dataclass 
class Void():
    pass

@dataclass
class Content():
    pass

@dataclass
class Variable():
    name: str
    type: Union[str,'Array_Type']
    liquid: Union['Comp', 'BoolOp', None]
    value: Any

    def to_dict(self) -> dict:
        if hasattr(self.value,'to_dict'):
            v = self.value.to_dict()
        else:
            v = self.value

        if hasattr(self.type,'to_dict'):
            t = self.type.to_dict()
        else:
            t = self.type

        if hasattr(self.liquid,'to_dict'):
            l = self.liquid.to_dict()
        else:
            l = self.liquid
        return {
            'name': self.name,
            'type': t,
            'liquidCheck': l,
            'value': v
        }

@dataclass
class Variable_type(Operation, Content):
    variable: Variable
    changeble: bool

    def to_dict(self) -> dict:
        return {
            'variable': self.variable.to_dict(),
            'changeble': self.changeble
        }

@dataclass
class MathOp(Operation):
    operation: str
    param1: Union["MathOp", Number]
    param2: Union["MathOp", Number]

    def to_dict(self) -> dict:
        return {
            'operation': self.operation,
            'left_value': self.param1.to_dict(),
            'right_value': self.param2.to_dict()
        }

@dataclass
class Comp(Operation):
    operation: str
    param1: MathOp | Number
    param2: MathOp | Number

    def to_dict(self) -> dict:
        return {
            'operation': self.operation,
            'left_value': self.param1.to_dict(),
            'right_value': self.param2.to_dict()
        }

@dataclass
class BoolOp(Operation):
    operation: str
    param1: Union["BoolOp", Comp]
    param2: Union["BoolOp", Comp]

    def to_dict(self) -> dict:
        return {
            'operation': self.operation,
            'left_value': self.param1.to_dict(),
            'right_value': self.param2.to_dict()
        }

@dataclass
class Function(Content):
    name: str
    type: str
    variables: List[Variable_type]
    body: List[Operation]

    def to_dict(self) -> dict:
        lv = []
        lb = []
        for i in self.variables:
            lv.append(i.to_dict())
        for i in self.body:
            lb.append(i.to_dict())
        return {
            'name': self.name,
            'type': self.type,
            'params': lv,
            'body': lb
        }

@dataclass
class Param():
    value: Any

    def to_dict(self) -> dict:
        if hasattr(self.value,'to_dict'):
            v = self.value.to_dict()
        else:
            v = self.value
        return {
            'value': v
        }

@dataclass
class Function_Call(Operation):
    name: str
    variables: List[Param]

    def to_dict(self) -> dict:
        lp = []
        for i in self.variables:
            lp.append(i.to_dict())
        return {
            'name': self.name,
            'params': lp
        }

@dataclass
class Var_Call(Operation):
    name: str

    def to_dict(self) -> dict:
        return {
            'name': self.name
        }

@dataclass
class If(Operation):
    condition: BoolOp
    thenPart: List[Operation]
    elsePart: List[Operation]

    def to_dict(self) -> dict:
        lt = []
        for i in self.thenPart:
            lt.append(i.to_dict())
        le = []
        if self.elsePart:
            for i in self.elsePart:
                le.append(i.to_dict())
        return {
            'condition': self.condition.to_dict(),
            'thenPart': lt,
            'elsePart': le
        }

@dataclass
class While(Operation):
    condition: BoolOp
    body: List[Operation]

    def to_dict(self) -> dict:
        lb = []
        for i in self.body:
            lb.append(i.to_dict())
        return {
            'condition': self.condition.to_dict(),
            'body': lb
        }

@dataclass
class Assignment(Operation):
    name: str
    value: Any

    def to_dict(self) -> dict:
        if hasattr(self.value,'to_dict'):
            v = self.value.to_dict()
        else:
            v = self.value
        return {
            'name': self.name,
            'value': v
        }

@dataclass
class Assignment_Array(Operation):
    name: str
    index: int
    value: Any

    def to_dict(self) -> dict:
        if hasattr(self.value,'to_dict'):
            v = self.value.to_dict()
        else:
            v = self.value

        return {
            'name': self.name,
            'index': self.index,
            'value': v
        }

@dataclass
class Array(Operation):
    name: str
    pos: Any

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'index': self.pos.to_dict()
        }

@dataclass
class CreateArray(Operation):
    size: Any
    nextD: Union['CreateArray', None]

    def to_dict(self) -> dict:
        if hasattr(self.nextD,'to_dict'):
            nd = self.nextD.to_dict()
        else:
            nd = self.nextD
        return {
            'size': self.size,
            'nextDimension': nd
        }

@dataclass
class Array_Type(Operation):
    type: Union["Array_Type", str]

    def to_dict(self) -> dict:
        if hasattr(self.type,'to_dict'):
            t = self.type.to_dict()
        else:
            t = self.type
        return {
            'array': t
        }

@dataclass
class Node():
    nodes : List[Content]

    def to_dict(self) -> dict:
        l = []
        for i in self.nodes:
            l.append(i.to_dict())
        return {
            'program': l
        }

@dataclass
class Neg():
    value : MathOp | Number

    def to_dict(self) -> dict:
        return {
            'value': self.value.to_dict()
        }


     
