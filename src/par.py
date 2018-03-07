import os
import sys
import lex
import yacc
from tokenizer import tokenizer

class Parser(object):

	tokens = tokenizer.tokens

	precedence = (
		('right', 'ASSIGN'),
		('left', 'OR'),
		('left', 'AND'),
		('left', 'OR'),
		('left', 'AND'),
		('left', 'EQUAL', 'NEQUAL'),
		('left', 'GT', 'GTEQ', 'LT', 'LTEQ'),
		('left', 'PLUS', 'MINUS'),
		('left', 'MULTIPLY', 'DIVIDE', 'MODULUS'),
		('right', 'NOT'),
		('left', 'DOT') ## member access
	)

	def __init__(self, lexer):
		self.lexer = lex.lex(module=tokenizer())

	def p_module(self, p):
		'''
			module : KEY_MODULE IDENT SCOLON KEY_BEGIN ifStatement KEY_END IDENT DOT
		'''
	def p_ifStatement(self,p):
		'''
			ifStatement  :  KEY_IF KEY_THEN KEY_END
		'''	
	# def ident(self, p):
	# 	'''
	# 		ident : IDENT
	# 	'''
		
	def declarationsequence(self, p):
		'''
			declarationsequence : LCB CONST LCB constantdeclaration SCOLON RCB | TYPE LCB typedeclaration SCOLON RCB | VAR LCB variabledeclaration SCOLON RCB | LCB proceduredeclaration SCOLON RCB RCB
		'''
#======================================= need to finish grammar part ===========================	


class Parserrr(object):

	def __init__(self):
		self.lexer = lex.lex(module=tokenizer())
		self.parserObj = Parser(self.lexer)
		self.parser = yacc.yacc(module=self.parserObj, start='module')

	def read_file(self, _file):
		if type(_file) == str:
			_file = open(_file)
		content = _file.read()
		_file.close()
		return content

	# def tokenize_string(self, code):
	#     self.lexer.input(code)
	#     for token in self.lexer:
	#         print(token)

	# def tokenize_file(self, _file):
	#     content = self.read_file(_file)
	#     return self.tokenize_string(content)

	# def parse_string(self, code, debug=False, lineno=1):
	#     return self.parser.parse(code, lexer=self.lexer, debug=debug)

	def parse_file(self, _file, debug=False):
		content = self.read_file(_file)
		parse_ret = self.parser.parse(content, lexer=self.lexer, debug=debug)
		return parse_ret	

if __name__=="__main__":
	# initialize Parser
	parser = Parserrr()
	# handle_errors(argv)

	# for Tokenizing a file
	# if argv[1] == '-l':
	#     parser.tokenize_file(argv[2])
	#     exit()

	# else:
		# if argv[1] == '-p':
		#     filename = argv[2]
		# else:
	filename = sys.argv[1]

	result = parser.parse_file(filename, debug = True)        						