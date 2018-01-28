Specifications of our compiler:

  Source language: Oberon
  Implementation language: Python3
  Target language: MIPS

To run the testfiles, execute the following commands from the main directory:
1) make
2) To run test1.OBE:
   bin/lexer test/test1.OBE
   Use test2.OBE, test3.OBE etc to run other testfiles.

Explanation:
We have used the PLY tool to build this lexer. PLY stands for Python Lex Yacc. By this tool's help we can take advantage of defining tokens by matching their regex to analyze the input file data and breaking it into consequent lexemes and tokens.
