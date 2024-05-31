# Plush Compiler

Author: Lishun Su fc56375

## Introduction
PLush is new a programming language, designed to teach programming. It's goal is to be simple, and modular.

# Structure of the project
The project is structured by lexer, parser, type checker and code generator.

## Lexer
The lexer uses the lex module from the PLY library. It receives the .pl file, tokenizes it, and passes the tokens to the parser. For more details, see `src/tokens.py`.

## Parser
The parser uses the yacc module from the PLY library. It receives tokens from the lexer, transforms them into an Abstract Syntax Tree (AST), and passes the AST to the type checker. For more details, see `src/parseRules.py`.

## Type Checker
The type checker walks through the AST to verify the correctness of element types, ensure functions have return statements, and perform liquid type checking. For more details, see `src/semantic.py `.

## Code Generator
The code generator uses the llvmlite library. It receives the AST and generates LLVM code. For more details, see `src/codegen/codegen.py`.

# Extra Feature
This project includes a Liquid Type Checker in the type checker. The data types supported for liquid type checking are *boolean*, *integer* and the *float*.
You can use the Liquid Type Check like this:
```
function void main(){
    var a:int (a > 10):=11;
    var b : int (a > 10 && b < 10) := 9;
    
} 
```
After declaring the type, specify the condition inside parentheses.

# How to excute

1. Excute the command `sh setup.sh` (it will build the docker image and run a container)

2. Use the command `sh plush.sh --tree examples/<filename>.pl`, if you want to generate the .ll file and check the generated AST tree in the terminal or `sh plush.sh examples/<filename>.pl`, if you only want to generate the .ll file. 

3. Excute the command `sh excute_plush.sh`, if you want to get the excutable of the file .ll