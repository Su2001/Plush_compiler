from llvmlite import ir
from codegen.classes import *
from codegen.classes import Bool as b

from codegen.environment import Environment

class Compiler:
    def __init__(self) -> None:
        self.type_map:dict[str, ir.Type]={
            'int': ir.IntType(32),
            'float': ir.FloatType(),
            'void': ir.VoidType(),
            'bool': ir.IntType(1),
            'string': ir.PointerType(ir.IntType(8)),
            'char': ir.IntType(8)
        }

        self.defaut_fun:dict[str, List[tuple[str,str]]]={
            'print_int':('void',[
                        ("a",'int')
                        ]),
            'print_bool':('void',[
                        ("a",'bool')
                        ]),
            'print_char':('void',[
                        ("a",'char')
                        ]),
            'print_float':('void',[
                        ("a",'float')
                        ]),
            'print_string':('void',[
                        ("a",'string')
                        ]),
            'power_int':('int',[
                        ("a",'int'),("b",'int')
                        ]),
            'power_float':('float',[
                        ("a",'float'),("b",'float')
                        ])
        }

        self.counter: int = 0

        self.env: Environment = Environment()

        self.module: ir.Module = ir.Module('main')
        self.builder : ir.IRBuilder = ir.IRBuilder()

    def __increment_counter(self) -> int:
        self.counter += 1
        return self.counter

    def compile(self, node: Node) -> None:
        for i in node.nodes:
            match i:
                case Function():
                    self.__process_Function(i)
                case Variable_type():
                    self.__process_VarType(i)
    
    def compile_detail(self, no) -> None:
        match no:
            case MathOp():
                self.__process_Op(no)
            case Variable_type():
                self.__process_VarType(no)
            case Assignment():
                self.__process_Assignment(no)
            case If():
                self.__process_If(no)
            case While():
                self.__process_While(no)
            case Function_Call():
                self.__process_Call(no)
            case Assignment_Array():
                self.__process_array_assgn(no)

    def __process_array_assgn(self, node: Assignment_Array) ->None:
        array_name : str = node.name
        index, Type = self.__resolve_value(node.index)
        array_ptr, arr_typ = self.env.lookup(array_name)
        ptr = self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), 0), index])
        next = node.value
        while isinstance(next, Assignment_Array) and next.name=='':
            index, Type = self.__resolve_value(next.index)
            ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), index])
            next = next.value
        save_value, typ = self.__resolve_value(next)
        self.builder.store(save_value, ptr)

    def __process_While(self, node: While) -> None:
        condition = node.condition
        body = node.body

        test, _ = self.__resolve_value(condition)

        # Entry block that runs if the condition is true
        while_loop_entry = self.builder.append_basic_block(f"while_loop_entry_{self.__increment_counter()}")

        # If the condition is false, it runs from this block
        while_loop_otherwise = self.builder.append_basic_block(f"while_loop_otherwise_{self.counter}")

        self.builder.cbranch(test, while_loop_entry, while_loop_otherwise)

        # Setting the builder position-at-start
        self.builder.position_at_start(while_loop_entry)

        # Compile the body of the while statement
        for i in body:
            self.compile_detail(i)

        test, _ = self.__resolve_value(condition)

        self.builder.cbranch(test, while_loop_entry, while_loop_otherwise)
        self.builder.position_at_start(while_loop_otherwise)

    def __process_If(self, node:If) -> None:
        condition:BoolOp = node.condition
        cons = node.thenPart
        alt = node.elsePart
        test, _ = self.__resolve_value(condition)
        if not alt:
            with self.builder.if_then(test):
                for i in cons:
                    self.compile_detail(i)
        else:
            with self.builder.if_else(test) as (true, otherwise):
                with true:
                    for i in cons:
                        self.compile_detail(i)
                with otherwise:
                    if isinstance(alt, If):
                        self.__process_If(alt)
                    else:
                        for i in alt:
                            self.compile_detail(i) 

    def __process_Assignment(self, node:Assignment) -> None:
        name : str = node.name
        value, Type = self.__resolve_value(node.value)
        ptr, _type = self.env.lookup(name)
        self.builder.store(value, ptr)
        self.env.define(name, ptr, _type)

    def __process_VarType(self, node:Variable_type) -> None:
        name: str = node.variable.name
        value = node.variable.value
        if isinstance(node.variable.type, Array_Type):
            if value and (isinstance(value, CreateArray)):
                Type = self.__process_array_type(node.variable.type, value)
            elif value and (not isinstance(value, CreateArray)):
                value, Type = self.__resolve_value(node=value)

                ptr = self.builder.alloca(Type)

                self.builder.store(value,ptr)
                self.env.define(name, ptr, Type)
                return
            else:
                Type = self.__process_array_type(node.variable.type, None)
            ptr = self.builder.alloca(Type)
            self.env.define(name, ptr, Type)
        else:
            Type = self.type_map[node.variable.type]
            if self.env.name == "global":
                global_var = ir.GlobalVariable(self.module, Type, name)
                if value:
                    value, Type = self.__resolve_value(node=value)
                    global_var.initializer = value
                self.env.define(name, global_var, Type)
            elif value:
                value, Type = self.__resolve_value(node=value)

                if self.env.lookup(name) is None:
                    ptr = self.builder.alloca(Type)

                    self.builder.store(value,ptr)

                    self.env.define(name, ptr, Type)
                else: 
                    ptr, _ = self.env.lookup(name)
                    self.builder.store(value, ptr)
            else:
                ptr = self.builder.alloca(Type)
                self.env.define(name, ptr, Type)

    def __process_Function(self, node:Function) -> None:
        func_name: str = node.name
        param_types: list[ir.Type] = []
        param_names: list[str] = []
        for i in node.variables:
            if isinstance(i.variable.type, Array_Type):
                param_types.append(self.__getArrayType(i.variable.type))
            else:
                param_types.append(self.type_map[i.variable.type])
            param_names.append(i.variable.name)
        return_type: ir.Type = self.type_map[node.type]

        fnty = ir.FunctionType(return_type, param_types)
        func = ir.Function(self.module, fnty, name=func_name)
        for i in range(len(node.variables)):
            func.args[i].name = node.variables[i].variable.name
        if node.body:
            block = func.append_basic_block(f"{func_name}_entry")

            previous_builder = self.builder
            self.builder = ir.IRBuilder(block)
            
            params_ptr = []
            for i, typ in enumerate(param_types):
                ptr = self.builder.alloca(typ)
                self.builder.store(func.args[i], ptr)
                params_ptr.append(ptr)
            
            previous_env = self.env
            self.env = Environment(parent= previous_env, name=func_name)
            for i, x in enumerate(zip(param_types,param_names)):
                typ = param_types[i]
                ptr = params_ptr[i]

                self.env.define(x[1], ptr, return_type)

            self.env.define(func_name,func,return_type)
            for stmt in node.body:
                if isinstance(stmt, Assignment) and stmt.name == func_name:
                    self.__process_Return(stmt) 
                else:
                    self.compile_detail(stmt)
            if isinstance(return_type, ir.VoidType):
                self.builder.ret_void()
            self.env = previous_env
            self.builder = previous_builder
        self.env.define(func_name,func,return_type)

    def __process_Return(self, node:Assignment) -> None:
        value = node.value
        value, Type = self.__resolve_value(value)

        self.builder.ret(value)

    def __process_Call(self,node:Function_Call) -> tuple[ir.Instruction, ir.Type]:
        name: str = node.name
        params: List[Param] = node.variables
        if name in self.defaut_fun.keys() and (not self.env.lookup(name)):
            func = self.defaut_fun[name]
            func_name: str = name
            param_types: list[ir.Type] = []
            param_names: list[str] = []
            for i in func[1]:
                param_types.append(self.type_map[i[1]])
                param_names.append(i[0])
            return_type: ir.Type = self.type_map[func[0]]

            fnty = ir.FunctionType(return_type, param_types)
            func = ir.Function(self.module, fnty, name=func_name)
            self.env.define_to(func_name,func,return_type,"global")   
        args = []
        types = []
        if len(params) > 0:
            for i in params:
                p_val, p_type = self.__resolve_value(i.value)
                args.append(p_val)
                types.append(p_type)

        match name:
            case _:
                func, ret_type = self.env.lookup(name)
                ret = self.builder.call(func, args)
        
        return ret, ret_type
    
    def __process_Op(self, node) -> None:
        operator : str = node.operation
        left_value, left_type = self.__resolve_value(node.param1)
        right_value, right_type = self.__resolve_value(node.param2)

        value = None
        Type = None
        if isinstance(right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = self.type_map['int']
            match operator:
                case '+':
                    value = self.builder.add(left_value, right_value)
                case '-':
                    value = self.builder.sub(left_value, right_value)
                case '/':
                    value = self.builder.sdiv(left_value, right_value)
                case '*':
                    value = self.builder.mul(left_value, right_value)
                case '%':
                    value = self.builder.srem(left_value, right_value)
                case '^':
                    value, Type = self.__process_power(left_value, right_value, ir.IntType)
                case '>':
                    value = self.builder.icmp_signed('>', left_value, right_value)
                    Type = self.type_map['bool']
                case '>=':
                    value = self.builder.icmp_signed('>=', left_value, right_value)
                    Type = self.type_map['bool']
                case '<':
                    value = self.builder.icmp_signed('<', left_value, right_value)
                    Type = self.type_map['bool']
                case '<=':
                    value = self.builder.icmp_signed('<=', left_value, right_value)
                    Type = self.type_map['bool']
                case '==':
                    value = self.builder.icmp_signed('==', left_value, right_value)
                    Type = self.type_map['bool']
                case '!=':
                    value = self.builder.icmp_signed('!=', left_value, right_value)
                    Type = self.type_map['bool']
                case 'or':
                    value = self.builder.or_(left_value, right_value)
                    Type = self.type_map['bool']
                case 'and':
                    value = self.builder.and_(left_value, right_value)
                    Type = self.type_map['bool']
                
        elif isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.FloatType):
            match operator:
                case '+':
                    value = self.builder.fadd(left_value, right_value)
                case '-':
                    value = self.builder.fsub(left_value, right_value)
                case '/':
                    value = self.builder.fdiv(left_value, right_value)
                case '*':
                    value = self.builder.fmul(left_value, right_value)
                case '%':
                    value = self.builder.frem(left_value, right_value)
                case '^':
                    value, Type = self.__process_power(left_value, right_value, ir.FloatType)
                case '>':
                    value = self.builder.fcmp_ordered('>', left_value, right_value)
                    Type = self.type_map['bool']
                case '>=':
                    value = self.builder.fcmp_ordered('>=', left_value, right_value)
                    Type = self.type_map['bool']
                case '<':
                    value = self.builder.fcmp_ordered('<', left_value, right_value)
                    Type = self.type_map['bool']
                case '<=':
                    value = self.builder.fcmp_ordered('<=', left_value, right_value)
                    Type = self.type_map['bool']
                case '==':
                    value = self.builder.fcmp_ordered('==', left_value, right_value)
                    Type = self.type_map['bool']
                case '!=':
                    value = self.builder.fcmp_ordered('!=', left_value, right_value)
                    Type = self.type_map['bool']
        return value, Type
    
    def __process_power(self, left_value, right_value, t):
        if t == ir.IntType:
            name = "power_int"
        else:
            name = "power_float"
        if not self.env.lookup(name):
            func = self.defaut_fun[name]
            func_name: str = name
            param_types: list[ir.Type] = []
            param_names: list[str] = []
            for i in func[1]:
                param_types.append(self.type_map[i[1]])
                param_names.append(i[0])
            return_type: ir.Type = self.type_map[func[0]]

            fnty = ir.FunctionType(return_type, param_types)
            func = ir.Function(self.module, fnty, name=func_name)
            self.env.define_to(func_name,func,return_type,"global")
        func, ret_type = self.env.lookup(name)
        ret = self.builder.call(func, [left_value, right_value])
        
        return ret, ret_type
        
        
    
    def __process_Prefix(self, node) ->  tuple[ir.Value, ir.Type]:
        match node:
            case Neg():
                operator: str = '-'
                right_value, right_type = self.__resolve_value(node.value)
            case BoolOp():
                operator: str = node.operation
                right_value, right_type = self.__resolve_value(node.param1)

        Type = None
        value = None
        if isinstance(right_type, ir.FloatType):
            Type = ir.FloatType()
            match operator:
                case '-':
                    value = self.builder.fmul(right_value, ir.Constant(ir.FloatType(), -1.0))
                case '!':
                    value = ir.Constant(ir.IntType(1), 0)
        elif isinstance(right_type, ir.IntType):
            Type = ir.IntType(32)
            match operator:
                case '-':
                    value = self.builder.mul(right_value, ir.Constant(ir.IntType(32), -1))
                case '!':
                    value = self.builder.not_(right_value)

        return value, Type
    
    def __convert_string(self, string: str) -> tuple[ir.Constant, ir.ArrayType]:
        string = string[1:-1]
        string = string.replace('\\n', '\n\0')
        
        fmt: str = f"{string}\0"
        c_fmt: ir.Constant = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))

        # Make the global variable for the string
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=f'__str_{self.__increment_counter()}')
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        ptr_to_str = self.builder.gep(global_fmt, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        return ptr_to_str, ptr_to_str.type

    def __getArrayType(self,node:Array_Type) -> ir.Type:
        if isinstance(node.type, Array_Type):
            return ir.PointerType(self.__getArrayType(node.type))
        else:
            return ir.PointerType(self.type_map[node.type])

    def __resolve_value(self, node) -> tuple[ir.Value, ir.Type]:
        match node:
            case Float():
                value, Type = node.value, self.type_map["float"]
                return ir.Constant(Type, value), Type
            case Integer():
                value, Type = node.value, self.type_map["int"]
                return ir.Constant(Type, value), Type
            case Assignment():
                ptr, Type = self.env.lookup(node.name)
                if isinstance(Type, ir.ArrayType):
                    ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                    Type = ptr.type
                    return ptr, Type
                return self.builder.load(ptr),Type
            case String():
                string, Type = self.__convert_string(node.value)

                return string, Type
            case Char():
                char, Type = ir.Constant(self.type_map["char"], ord(node.value[1:-1])), self.type_map["char"]
                return char, Type
            case b():
                if node.value:
                    n = 1
                else :
                    n = 0
                value, Type = n, self.type_map["bool"]
                return ir.Constant(Type, value), Type
            case BoolOp():
                if node.operation != 'NEG':
                    return self.__process_Op(node)
                else:
                    return self.__process_Prefix(node)
            case Neg():
                return self.__process_Prefix(node)
            case Comp():
                return self.__process_Op(node)
            case MathOp():
                return self.__process_Op(node)
            case Function_Call():
                return self.__process_Call(node)
            case Assignment_Array():
                return self.__read_Array_Ass(node)
            case Array():
                return self.__read_Array(node)
            
    def __read_Array(self, node:Array)-> tuple[ir.Value, ir.Type]:  
        array_name : str = node.name
        index, Type = self.__resolve_value(node.pos)
        array_ptr, arr_typ = self.env.lookup(array_name)
        ptr = self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), 0), index])
        read_value = self.builder.load(ptr)
        return read_value, read_value.type

    def __read_Array_Ass(self, node:Assignment_Array) -> tuple[ir.Value, ir.Type]:
        array_name : str = node.name
        index, Type = self.__resolve_value(node.index)
        array_ptr, arr_typ = self.env.lookup(array_name)
        ptr = self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), 0), index])
        next = node.value
        while isinstance(next, Assignment_Array) and next.name=='':
            index, Type = self.__resolve_value(next.index)
            ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), index])
            next = next.value
        if isinstance(next, Array):
            index, Type = self.__resolve_value(next.pos)
            ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), index])
        read_value = self.builder.load(ptr)
        return read_value, read_value.type

    def __process_array_type(self,typ:Array_Type, size:CreateArray) -> ir.ArrayType:
        if not size:
            if not isinstance(typ.type, Array_Type):
                return ir.ArrayType(self.type_map[typ.type], 1)
            else:
                return ir.ArrayType(self.__process_array_type(typ.type, None),1)
        elif not isinstance(typ.type, Array_Type):
            return ir.ArrayType(self.type_map[typ.type], size.size.value)
        else:
            return ir.ArrayType(self.__process_array_type(typ.type, size.nextD), size.size.value)