from codegen.classes import *
from codegen.classes import Bool as b
from utils.liquidCheck import *

types = ['integer','real','string','boolean','void','char']

class Any(object):
    def __eq__(self,o):
        return True
    def __ne__(self,o):
        return False

class Context(object):
    def __init__(self,name=None):
        self.variables = {}
        self.var_count = {}
        self.name = name
    
    def has_var(self,name):
        return name in self.variables
    
    def get_var(self,name):
        return self.variables[name]
    
    def get_var_count(self,name):
        return self.var_count[name]
    
    def set_var(self,name,typ, changeble):
        self.variables[name] = (typ, changeble)
        self.var_count[name] = 0
        
contexts = []
functions = {
    'print_int':('void',[
            ("a",'int')
        ]),
    'print':('void',[
            ("a",Any())
        ]),
    'print_bool':('void',[
            ("a",'bool')
        ]),
    'print_float':('void',[
            ("a",'float')
        ]),
    'print_string':('void',[
            ("a",Array_Type("char"))
        ]),
    'print_array':('void',[
            ("a",'array')
        ])
}


def pop():
    count = contexts[-1].var_count
    for v in count:
        if count[v] == 0:
            print ("Warning: variable %s was declared, but not used." % v)
    contexts.pop()
    
def check_if_function(var):
    if var.lower() in functions and not is_function_name(var.lower()):
        raise Exception("A function called %s already exists" % var)
        
def is_function_name(var):
    for i in contexts[::-1]:
        if i.name == var:
            return True
    return False

def has_var(varn):
    var = varn.lower()
    check_if_function(var)
    for c in contexts[::-1]:
        if c.has_var(var):
            return True
    return False

def get_var_count(varn):
    var = varn.lower()
    for c in contexts[::-1]:
        if c.has_var(var):
            c.var_count[var] += 1
            return c.get_var_count(var)
    raise Exception("Variable %s is referenced before assignment" % var)

def get_var(varn):
    var = varn.lower()
    for c in contexts[::-1]:
        if c.has_var(var):
            c.var_count[var] += 1
            return c.get_var(var)
    raise Exception ("Variable %s is referenced before assignment" % var)
    
def set_var(varn,typ, changeble):
    var = varn.lower()
    check_if_function(var)
    now = contexts[-1]
    if now.has_var(var):
        raise Exception( "Variable %s already defined" % var)
    else:
        if isinstance(typ, Array_Type):
            now.set_var(var,typ,changeble)
        else:
            now.set_var(var,typ.lower(),changeble)
    
def get_params(node):
    if node.type == "parameter":
        return [check(node.args[0])]
    else:
        l = []
        for i in node.args:
            l.extend(get_params(i))
        return l

current =0
checker = Checker()
def check(node):
    global current
    match node:
        case Node():
            contexts.append(Context())
            checker.push_context()
            for i in node.nodes:
                check(i)
            checker.pop_context()
            pop()
        case Variable_type():
            var_name = node.variable.name
            var_type = node.variable.type
            if has_var(var_name):
                raise Exception( "the variable %s is already declared."% var_name)
            if var_type == 'void':
                raise Exception( "the variable cant be declared as void")
            current = var_type
            if node.variable.value:
                v_type =check(node.variable.value)
                if v_type != var_type:
                    raise Exception("Variable %s is of type %s and does not support %s" % (var_name, var_type, v_type))
            set_var(var_name, var_type, node.changeble)
            if var_type in ["int","bool","float"]:
                    checker.add_to(name= var_name, typ=var_type, value=node.variable.value, c=node.variable.liquid)
        case Function():
            name = node.name
            check_if_function(name)
            args = []
            if len(node.variables) != 0:
                for v in node.variables:
                    args.append((v.variable.name,v.variable.type, v.changeble)) 
                
            functions[name] = (node.type,args)
            contexts.append(Context(name))
            checker.push_context()
            set_var(name, node.type, True)
            for i in args:
                set_var(i[0],i[1],i[2])
            if node.body:
                for i in node.body:
                    check(i)
                if get_var_count(name) == 1 and node.type != 'void':
                    raise Exception("Function %s must has return" % fname)
            checker.pop_context()
            pop()
        case Function_Call():
            fname = node.name
            if fname not in functions:
                raise Exception ("Function %s is not defined" % fname)
            if node.variables[0] != None:
                args = node.variables
            else:
                args = []
            rettype,vargs = functions[fname]
        
            if len(args) != len(vargs):
                raise Exception( "Function %s is expecting %d parameters and got %d" % (fname, len(vargs), len(args)))
            else:
                for i in range(len(vargs)):
                    check_type =check(args[i].value)
                    if vargs[i][1] != check_type:
                        raise Exception( "Parameter #%d passed to function %s should be of type %s and not %s" % (i+1,fname,vargs[i][1],check_type))
            
            return rettype
        case Assignment():
            varn = node.name
            if is_function_name(varn):
                vartype = functions[varn]
                get_var_count(varn)
            else:
                if not has_var(varn):
                    raise Exception ("Variable %s not declared" % varn)
                vartype = get_var(varn)
            if node.value:
                assgntype = check(node.value)
                if not vartype[1]:  
                    raise Exception("Variable %s is defined as val you cant change this variable" % (varn)) 
                if vartype[0] != assgntype:
                    raise Exception("Variable %s is of type %s and does not support %s" % (varn, vartype[0], assgntype))
                if vartype[0] in ["int","bool","float"]:
                    checker.solve(name= varn, newvalue=node.value)
            else:
                return vartype[0]
        case Array():
            varn = node.name
            if check(node.pos) != 'int':
                raise Exception ("index of array must be integer")
            if not has_var(varn):
                raise Exception ("Variable %s not declared" % varn)
            vartype = check(get_var(varn)[0])
            return vartype
        case Assignment_Array():
            varn = node.name
            if check(node.index) != 'int':
                raise Exception ("index of array must be integer")
            if not has_var(varn):
                raise Exception ("Variable %s not declared" % varn)
            vartype = check(get_var(varn)[0])
            next = node.value
            while isinstance(next, Assignment_Array) and next.name=='':
                if check(next.index) != 'int':
                    raise Exception ("index of array must be integer")
                try:
                    vartype = vartype.type
                except:
                    raise Exception("you are given more indexes in this array %s", varn)
                next = next.value
            if isinstance(next, Array):
                if check(next.pos) != 'int':
                    raise Exception ("index of array must be integer")
                try:
                    vartype = vartype.type
                except:
                    raise Exception("you are given more indexes in this array %s", varn)
                return vartype
            
            
            assgntype = check(next)
            if vartype != assgntype:
                raise Exception("Variable %s is of type %s but receives this %s" % (varn, vartype, assgntype))
        case Comp():
            for i in (node.param1, node.param2):
                a = check(i)
                if a != "int":
                    raise Exception( " requires a number. Got %s instead." % (a))
            return "bool"
        case BoolOp():
            op = node.operation
            if op == "NEG":
                check_set = (node.param1)
            else:
                check_set= (node.param1, node.param2)   
            for i in check_set:
                a = check(i)
                if a != "bool":
                    raise Exception("%s requires a boolean. Got %s instead." % (op,a))
            return "bool"
        case MathOp():
            op = node.operation
            vt1 = check(node.param1)
            vt2 = check(node.param2)

            if vt1 != vt2:
                raise Exception ("Arguments of operation '%s' must be of the same type. Got %s and %s." % (op,vt1,vt2))
                
            if op in ['Mod']:
                if vt1 != 'int':
                    raise Exception("Operation %s requires integers." % op)
                
            if op == "Div":
                return 'float'
            else:
                return vt1 
        case While():
            t = check(node.condition)
            if t != 'bool':
                raise Exception ("while condition requires a boolean. Got %s instead." % (t))
            contexts.append(Context("while"))
            # check body
            for i in node.body:
                check(i)
            pop()
        case If():
            t = check(node.condition)
            if t != 'bool':
                raise Exception ("condition requires a boolean. Got %s instead." % (t))
            contexts.append(Context("if"))
            # check then
            for i in node.thenPart:
                check(i)
            #check else
            pop()
            if node.elsePart:
                if isinstance(node.elsePart, If):
                    check(node.elsePart)
                else:
                    contexts.append(Context("else"))
                    for i in node.elsePart:
                        check(i)  
                    pop()
        case Neg():
            t = check(node.value)
            if t != 'int' | t != 'float':
                raise Exception ("the value must be number")
        case Var_Call():
            if not has_var(node.name):
                raise Exception("the variable with this name %s is not defined" % (node.name))
            return get_var(node.name)[0]
        
        case CreateArray():
            if not isinstance(node.size, Integer):
                raise Exception ("index of array must be integer Literal")
            if node.nextD:
                return Array_Type(check(node.nextD))
            else:
                return Array_Type(to_end(current))
        case Array_Type():
            return node.type
        case Float():
            return "float"
        case Integer():
            return "int"
        case String():
            return Array_Type("char")
        case Char():
            return "char"
        case b():
            return "bool"
        case Void():
            return "void"
        case _:
            print("semantic missing:")

def to_end(t:Array_Type):
    if isinstance(t.type,Array_Type):
        return to_end(t.type)
    else:
        return t.type
