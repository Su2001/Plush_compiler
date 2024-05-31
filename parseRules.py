from numbers import Number
from tokens import *
from codegen.classes import *
     

precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "EQ", "NEQ","GT", "LT", "GTEQ", "LTEQ"),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
   
    ('left', 'MUL', 'MOD'),
    ("right", "UMINUS"),
    
)

def p_start(t):
    """start : excute_list """
    t[0] = Node(t[1])

# Non-empty record field or function parameter list.
def p_excute_list(p):
    """
    excute_list : excute_list_end
               | excute_list_iter
    """
    p[0] = p[1]

def p_excute_list_iter(p):
    "excute_list_iter : excute_list excute_node"
    p[0] = p[1]
    p[0].append(p[2])


def p_excute_list_end(p):
    "excute_list_end : excute_node"
    p[0] = [p[1]]

def p_excute_node(t):
    """excute_node : variable_declaration
                    | function_dec"""
    t[0] = t[1]

def p_variable_declaration(t):
    """variable_declaration : VAR declaration END
                            | VAL declaration END"""
    if t[1] == "var":
        t[0] = Variable_type(t[2],True)
    else:
        t[0] = Variable_type(t[2],False)


def p_declaration(t):
    """declaration : ID DEF type liquid_type """
    t[0] = Variable(name=t[1],type=t[3], liquid=t[4][0],value=t[4][1])

def p_liquid_type(t):
    """liquid_type : LPAREN expression RPAREN give_value
                    | give_value"""
    if len(t) == 5:
        t[0] = (t[2],t[4])
    else:
        t[0] = (None,t[1])

def p_give_value(t):
    """give_value : ASSIGN value
                    |"""
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = None

def p_type(t):
    """type : INT
            | FLOAT
            | STRING
            | BOOL
            | VOID
            | CHAR
            | LSQBRAC type RSQBRAC"""
    if len(t) == 2:
        if t[1] == "string":
            t[0] = Array_Type("char")
        else:
            t[0] = t[1]
    else :
        t[0] = Array_Type(t[2])

def p_value(t):
    """value : expression
            | stringv
            | charv
            | NEWARRAY LSQBRAC expression RSQBRAC ps
            |"""
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 1:
        t[0] = None
    else:
        t[0] = CreateArray(t[3],t[5])

def p_ps(t):
    """ps : LSQBRAC expression RSQBRAC ps
            |"""
    if len(t) > 1:
        t[0] = CreateArray(t[2],t[4])
    else:
        t[0] = None


def p_array_or_func(t):
    """array_or_func : LSQBRAC expression RSQBRAC assg_arr_value
                | assgn_statement_or_func_call
                | """
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 1:
        t[0] = Var_Call(name="")
    else:
        if not t[4]:
            t[0] = Array("",t[2])
        else:
            t[0] = Assignment_Array("",t[2],t[4])

def p_assg_arr_value(t):
    """assg_arr_value : give_value
                        | array_or_func
                        |"""
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = None

def p_number_expression(t):
    """expression : expression_v PLUS expression
                  | expression_v MINUS expression
                  | expression_v TIMES expression
                  | expression_v DIVIDE expression
                  | expression_v MOD expression
                  | expression_v MUL expression
                  | expression_v 
                  | unary_minus_exp"""
    if len(t) != 2:
        if t[2] == '+'  : t[0] = MathOp("+", t[1], t[3])
        elif t[2] == '-': t[0] = MathOp("-", t[1], t[3])
        elif t[2] == '*': t[0] = MathOp("*", t[1], t[3])
        elif t[2] == '/': t[0] = MathOp("/", t[1], t[3])
        elif t[2] == '%': t[0] = MathOp("%", t[1], t[3])
        elif t[2] == '^': t[0] = MathOp("^", t[1], t[3])
    else:
        t[0] = t[1]

def p_unary_minus_exp(t):
    "unary_minus_exp : MINUS expression %prec UMINUS"
    if isinstance(t[2], Number):
        t[2].value = t[2].value * -1
        t[0] = t[2]
    else:    
        t[0] = Neg(value=t[2])

def p_expression_group(t):
    'expression_v : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_v(t):
    """expression_v : number
                    | real
                    | boolv
                    | ID array_or_func"""
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 3:
        t[2].name = t[1]
        t[0] = t[2]

def p_stringv(t):
    "stringv : STRINGV"
    t[0] = String(value=t[1])

def p_charv(t):
    "charv : CHARV"
    t[0] = Char(value=t[1])

def p_number(t):
    "number : NUMBER"
    t[0] = Integer(t[1])

def p_real(t):
    "real : REAL"
    t[0] = Float(t[1])

def p_boolv(t):
    "boolv : BOOLV"
    n = t[1] == "true"
    t[0] = Bool(n)

def p_expression_logic(t):
    """expression : expression OR expression
                        |   expression AND expression
                        |   NEG expression"""
    if t[2] == '||'  : t[0] = BoolOp("or", t[1], t[3])
    elif t[2] == '&&': t[0] = BoolOp("and", t[1], t[3])
    elif t[1] == '!': t[0] = BoolOp("NEG", t[2], None)

def p_expression_math(t):
    """expression : expression GT expression
                        |   expression GTEQ expression
                        |   expression LT expression
                        |   expression LTEQ expression
                        |   expression EQ expression
                        |   expression NEQ expression"""
    if t[2] == '>'  : t[0] = Comp(">", t[1], t[3])
    elif t[2] == '>=': t[0] = Comp(">=", t[1], t[3])
    elif t[2] == '<': t[0] = Comp("<", t[1], t[3])
    elif t[2] == '<=': t[0] = Comp("<=", t[1], t[3])
    elif t[2] == '==': t[0] = Comp("==", t[1], t[3])
    elif t[2] == '!=': t[0] = Comp("!=", t[1], t[3])


#----------------------------------------------------------------------

def p_function_dec(t):
    """
    function_dec : FUNCTION ID field_list with_type_or_not with_body_or_not  
    """
    t[0] = Function(t[2],t[4], t[3], t[5])

def p_function_with_type_or_not(t):
    """
    with_type_or_not :  DEF type 
                        | 
    """
    if len(t)==3:
        t[0] = t[2]
    else:
        t[0] = "void"

def p_with_body_or_not(t):
     """with_body_or_not : function_dec_no_body
                        | function_dec_with_body """
     t[0] = t[1]

def p_function_dec_with_body(t):
    """function_dec_with_body : LCBRAC body RCBRAC"""
    t[0] = t[2]

def p_function_dec_no_body(t):
    """function_dec_no_body : END"""
    t[0] = None

def p_field_list(t):
    """field_list : LPAREN empty_or_field RPAREN """
    t[0] = t[2]

def p_empty_or_field(t):
    """empty_or_field : empty_list
                        | ne_field_list"""
    t[0] = t[1]

# Non-empty record field or function parameter list.
def p_ne_field_list(p):
    """
    ne_field_list : ne_field_list_end
               | ne_field_list_iter
    """
    p[0] = p[1]


def p_ne_field_list_iter(p):
    "ne_field_list_iter : ne_field_list COMMA field"
    p[0] = p[1]
    p[0].append(p[3])


def p_ne_field_list_end(p):
    "ne_field_list_end : field"
    p[0] = [p[1]]

def p_field(p):
    """field : VAL ID DEF type
            | VAR ID DEF type"""
    if p[1] == "var":
         c = True
    else:
         c = False
    p[0] = Variable_type(Variable(name=p[2],type=p[4], liquid=None,value=None), c)

def p_statement_body(t):
	"""body : statement_list """
	t[0] = t[1]
     
def p_statement_list(p):
    """
    statement_list : statement_list_end
               | statement_list_iter
    """
    p[0] = p[1]


def p_statement_list_iter(p):
    "statement_list_iter : statement_list statement"
    p[0] = p[1]
    p[0].append(p[2])


def p_statement_list_end(p):
    "statement_list_end : statement"
    p[0] = [p[1]]

def p_statement(p):
    """statement : variable_declaration
                | value END
                | if_statement
                | while_statement
    """
    p[0] = p[1]

def p_assgn_statement_or_func_call(t):
     """assgn_statement_or_func_call : assignment_statement
                                    | procedure_or_function_call"""
     t[0] = t[1]
          
def p_assignment_statement(t):
	"""assignment_statement : give_value"""
	t[0] = Assignment(None,t[1])

#----------------------------------------------------------------------
         
def p_procedure_or_function_call(t):
	""" procedure_or_function_call : param_list"""
	
	t[0] = Function_Call("function_call", t[1])


def p_param_list(t):
    """param_list : LPAREN empty_or_param RPAREN """
    t[0] = t[2]

def p_empty_or_param(t):
    """empty_or_param : ne_param_list"""
    t[0] = t[1]

# Non-empty record param or function parameter list.
def p_ne_param_list(p):
    """
    ne_param_list : ne_param_list_end
               | ne_param_list_iter
    """
    p[0] = p[1]


def p_ne_param_list_iter(p):
    "ne_param_list_iter : empty_or_param COMMA value"
    p[0] = p[1]
    p[0].append(Param(p[3]))


def p_ne_param_list_end(p):
    "ne_param_list_end : value"
    p[0] = [Param(p[1])]
          
#---------------------------------------------------------------------------
          
def p_if_statement(t):
	"""if_statement : IF expression LCBRAC statement_list RCBRAC else_statement 
	"""
	
	t[0] = If(t[2],t[4],t[6])
     
def p_else_statement(t):
    """else_statement : ELSE else_or_if
                        | """
    if len(t) != 1:
        t[0] = t[2]
    else :
        t[0] = None

def p_else_or_if(t):
    """else_or_if : LCBRAC statement_list RCBRAC
                    | if_statement"""
    if len(t) == 2:
        t[0] = t[1]
    else :
        t[0] = t[2]
	
def p_while_statement(t):
	"""while_statement : WHILE expression LCBRAC statement_list RCBRAC"""
	t[0] = While(t[2],t[4])

# EMPTY
def p_empty(p):
    "empty :"
    pass


def p_empty_list(p):
    "empty_list : empty"
    p[0] = []

def p_error(t):
    print("Syntax error at '%s'" % t.value)

from ply import lex, yacc

lexer = lex.lex()
parser = yacc.yacc()

# raw_input = """
# var jk : int := 76;
# function main() {
#     var i : int := 3 ^ 5;
# 	print_int(i);
# }
# """
# from semantic import *
# from codegen.cedegen2 import Compiler
# from llvmlite import ir
# import llvmlite.binding as llvm
# from ctypes import CFUNCTYPE, c_int, c_float

# file_input = "plush_testsuite/0_valid/maxRangeSquared.pl"
# if __name__ == "__main__":

#     #f = open(file_input, "r")
#     #data = f.read()
#     #f.close()
#     data = raw_input
#     t = 1
#     # Tokenize

#     ast =parser.parse(data)
#     print(ast)
#     check(ast)
    
#     c = Compiler()
#     c.compile(ast)
#     module: ir.Module= c.module
#     module.triple = llvm.get_default_triple()
#     final = str(module)
#     lines = final.split('\n')

#     # Remove the first three lines
#     lines = lines[3:]

#     # Join the remaining lines back into a single string
#     output_str = '\n'.join(lines)
#     print(output_str)
#     with open("debug/test.ll", "w") as f:
#             f.write(output_str)
