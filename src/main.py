from ply import lex, yacc
from parseRules import *
from tokens import *
from semantic import *
from codegen.codegen import Compiler
from llvmlite import ir
import llvmlite.binding as llvm
from argparse import ArgumentParser, Namespace, ArgumentError
from utils.tojson import toJson

def parse_arguments() -> Namespace:
    arg_parser: ArgumentParser = ArgumentParser(
        description="Plush v0.0.1-alpha"
    )
    # Required Arguments
    arg_parser.add_argument("file_path", type=str, help="Path to your entry point plush file (ex. `main.pl`)")
    arg_parser.add_argument("--tree", action="store_true", help="print syntax tree")
    return arg_parser.parse_args()


lexer = lex.lex()
parser = yacc.yacc()

if __name__ == "__main__":
    args = parse_arguments()
    with open(args.file_path, "r") as f:
        code: str = f.read()
    # Tokenize

    ast =parser.parse(code)
    check(ast)
    if args.tree:
        toJson(ast)
    c = Compiler()
    c.compile(ast)
    module: ir.Module= c.module
    module.triple = llvm.get_default_triple()
    final = str(module)
    lines = final.split('\n')

    # Remove the first three lines
    lines = lines[3:]

    # Join the remaining lines back into a single string
    output_str = '\n'.join(lines)
    total = "result" + ".ll"
    with open(total, "w") as f:
            f.write(output_str)