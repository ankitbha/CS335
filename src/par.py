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
			module : KEY_MODULE IDENT SCOLON declarationSequence KEY_BEGIN statementSequence KEY_END IDENT DOT
		'''

	def p_declarationSequence(self, p):
		'''
			declarationsequence : declarationSequence LCB KEY_CONST LCB constantDeclaration SCOLON RCB
								| declarationSequence KEY_TYPE LCB typeDeclaration SCOLON RCB
								| declarationSequence KEY_VAR LCB variableDeclaration SCOLON RCB
								| declarationSequence LCB procedureDeclaration SCOLON RCB
								| empty
		'''

	def p_statementSequence(self, p):
		'''
			statementSequence : statement LCB SCOLON statement RCB
		'''

	def p_constantDeclaration(self, p):
		'''
			constantDeclaration : IDENT ASSIGN expression
		'''

	def p_expression(self, p):
		'''
			expression : simpleExpression LSB relation simpleExpression RSB
		'''

	def p_simpleExpression(self, p):
		'''
			simpleExpression : LSB PLUS RSB term LCB addOperator term RCB
			 				 | LSB MINUS RSB term LCB addOperator term RCB
		'''

	def p_term(self, p):
		'''
			term : factor LCB mulOperator factor RCB
		'''

	def p_factor(self, p):
		'''
			factor : number
				   | char
				   | string
				   | KEY_NIL
				   | set
				   | designator
				   | LSB actualParameters
				   | LRB expression RRB
				   | NOT factor
				   | KEY_ABS factor
				   | KEY_CHR factor
				   | KEY_ORD factor
				   | KEY_INTEGER
				   | KEY_BOOLEAN
				   | KEY_CHAR
				   | KEY_STRING
				   | KEY_REAL
				   | KEY_SET
		'''

	def p_number(self, p):
		'''
			number : VINTEGER | VREAL
		'''

	def p_char(self, p):
		'''
			char : VCHAR
		'''

	def p_set(self, p):
		'''
			set : LCB LSB element COMMA element RSB RCB
		'''

	def p_element(self, p):
		'''
			element : expression
		'''

	def p_designator(self, p):
		'''
			designator : qualident designator2
		'''

	def p_designator2(self, p):
		'''
			designator2 : designator2 DOT identdef
						| designator2 LSB expList RSB
						| LRB qualident RRB
		'''

	def p_qualident(self, p):
		'''
			qualident : LSB identdef DOT RSB identdef
		'''

	def p_identdef(self, p):
		'''
			identdef : LSB MULTIPLY RSB IDENT
		'''

	def p_expList(self, p):
		'''
			expList : expression LCB COMMA expression RCB
		'''

	def p_actualParameters(self, p):
		'''
			actualParameters : LRB LSB expList RSB RRB
		'''

	def p_mulOperator(self, p):
		'''
			mulOperator : MULTIPLY
						| DIVIDE
						| MODULUS
						| AND
		'''

	def p_addOperator(self, p):
		'''
			addOperator : PLUS
						| MINUS
						| OR
		'''

	def p_relation(self, p):
		'''
			relation : EQUAL
					 | NEQUAL
					 | LT
					 | LTEQ
					 | GT
					 | GTEQ
					 | KEY_IN
					 | KEY_IS
		'''

	def p_typeDeclaration(self, p):
		'''
			typeDeclaration : IDENT EQUAL type
		'''

	def p_type(self, p):
		'''
			type : IDENT
				 | varType
				 | arrayType
				 | recordType
				 | pointerType
		'''

	def p_varType(self, p):
		'''
			varType : KEY_INTEGER
					| KEY_BOOLEAN
					| KEY_CHAR
					| KEY_STRING
					| KEY_REAL
					| KEY_SET
		'''

	def p_arrayType(self, p):
		'''
			arrayType : KEY_ARRAY length LCB COMMA length RCB KEY_OF type
		'''

	def p_length(self, p):
		'''
			length : expression
		'''

	def p_recordType(self, p):
		'''
			recordType : KEY_RECORD LSB LRB baseType RRB RSB fieldListSequence KEY_END
		'''

	def p_baseType(self, p):
		'''
			baseType : qualident
		'''

	def p_fieldListSequence(self, p):
		'''
			fieldListSequence : fieldList LCB SCOLON fieldList RCB
		'''

	def p_fieldList(self, p):
		'''
			fieldList : LSB identList COLON type RSB
		'''

	def p_identList(self, p):
		'''
			identList : IDENT LCB COMMA IDENT RCB
		'''

	def p_pointerType(self, p):
		'''
			pointerType : KEY_POINTER KEY_TO type
		'''


	def p_variableDeclaration(self, p):
		'''
			variableDeclaration : identList COLON type
		'''

	def p_procedureDeclaration(self, p):
		'''
			procedureDeclaration : procedureHeading SCOLON procedureBody IDENT SCOLON
		'''

	def p_procedureHeading(self, p):
		'''
			procedureHeading : KEY_PROCEDURE IDENT LSB formalParameters RSB COLON type
		'''

	def p_formalParameters(self, p):
		'''
			formalParameters : LRB LSB FPSection LCB SCOLON FPSection RCB RSB RRB
		'''

	def p_FPSection(self, p):
		'''
			FPSection : IDENT LCB COMMA IDENT RCB COLON type
		'''

	def p_procedureBody(self, p):
		'''
			procedureBody : declarationSequence KEY_BEGIN statementSequence KEY_END
		'''

	def p_statement(self, p):
		'''
			statement : LSB assignment RSB
					  | LSB procedureCall RSB
					  | LSB ifStatement RSB
					  | LSB switchStatement RSB
					  | LSB whileStatement RSB
					  | LSB forStatement RSB
					  | LSB doWhileStatement RSB
					  | KEY_EXIT
					  | KEY_RETURN LSB expression RSB
					  | ioStatement
					  | fileStatement
					  | KEY_BREAK
					  | KEY_CONTINUE
		'''

	def p_assignment(self, p):
		'''
			assignment : designator ASSIGN expression
		'''

	def p_procedureCall(self, p):
		'''
			procedureCall : designator LSB actualParameters RSB
		'''

	def p_ifStatement(self, p):
		'''
			ifStatement : KEY_IF expression KEY_THEN statementSequence LCB KEY_ELSEIF expression KEY_THEN statementSequence RCB LSB KEY_ELSE statementSequence RSB KEY_END
		'''

	def p_switchStatement(self, p):
		'''
			switchStatement : KEY_SWITCH expression KEY_BEGIN case LCB OR case RCB LSB KEY_ELSE COLON statementSequence RSB KEY_END
		'''

	def p_case(self, p):
		'''
			case : KEY_CASE COLON expression statementSequence
		'''

	def p_whileStatement(self, p):
		'''
			whileStatement : KEY_WHILE expression KEY_BEGIN statementSequence KEY_END
		'''

	def p_forStatement(self, p):
		'''
			forStatement : KEY_FOR LRB assignment SCOLON expression SCOLON assignment RRB KEY_BEGIN statementSequence KEY_END
		'''

	def p_doWhileStatement(self, p):
		'''
			doWhileStatement : KEY_DO statementSequence KEY_WHILE expression
		'''

	def p_ioStatement(self, p):
		'''
			ioStatement : KEY_WRITE LRB expression RRB
						| KEY_WRITELN LRB expression RRB
						| KEY_READ LRB expression RRB
		'''

	def p_fileStatement(self, p):
		'''
			fileStatement : identdef EQUAL KEY_FOPEN LRB string COMMA char RRB
						  | KEY_FCLOSE LRB identdef RRB
						  | KEY_FPRINTF LRB identdef COMMA string RRB
						  | KEY_FREAD LRB identdef COMMA identdef COMMA VINTEGER RRB
		'''

	def p_empty(self, p):
        '''
            empty :
        '''
        pass


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
