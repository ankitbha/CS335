Specifications of our compiler:

  Source language: Oberon
  Implementation language: Python3
  Target language: MIPS

Task 1
To run the testfiles, execute the following commands from the main directory:
1) make
2) To run test1.OBE:
   bin/lexer test/test1.OBE
   Use test2.OBE, test3.OBE etc to run other testfiles.

Task 2
To run the program:
1) make
2) bin/codegen test/code.txt
   Change filename as suitable.

Explanation:
Task 1
We have used the PLY tool to build this lexer. PLY stands for Python Lex Yacc. By this tool's help we can take advantage of defining tokens by matching their regex to analyze the input file data and breaking it into consequent lexemes and tokens.
Task 2
We have implemented the code generator which forms MIPS assembly code from intermediate code taken from an input file. The compiler data structures implemented are:
1) Symbol Table consisting of class containing type and lexeme of the variable.
2) Address Descriptor which contains the address of variables.
3) Next Use Table which contains status and next use occurrence of all variables each line.
4) Register Descriptor which is implemented as a dictionary mapping ragisters to symbol objects of variables.
