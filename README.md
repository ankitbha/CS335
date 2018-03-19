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

Task 3
To run the parser, run these commands from the main directory:
1) make ass3
2) bin/parser num
  Range num from 0 to 29 to check testcodes from testCode1.txt to testCode29.txt
3) firefox test.html

Explanations:

Task 1
We have used the PLY tool to build this lexer. PLY stands for Python Lex Yacc. By this tool's help we can take advantage of defining tokens by matching their regex to analyze the input file data and breaking it into consequent lexemes and tokens.

Task 2
We have implemented the code generator which forms MIPS assembly code from intermediate code taken from an input file. The compiler data structures implemented are:
1) Symbol Table consisting of class containing type and lexeme of the variable.
2) Address Descriptor which contains the address of variables.
3) Next Use Table which contains status and next use occurrence of all variables each line.
4) Register Descriptor which is implemented as a dictionary mapping ragisters to symbol objects of variables.

Task 3
The output of the parser prints the rightmost derivation of the input program in a nicely formatted html file. The non-terminal being expanded is marked in red color to make it easy to follow the derivation.
The way we have done this is to first generate the rightmost derivation in reverse and then use the “tac” command to reverse the file.
