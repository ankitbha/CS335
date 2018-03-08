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
			declarationSequence : declarationSequence KEY_CONST conss
								| declarationSequence KEY_TYPE typess
								| declarationSequence KEY_VAR varss
								| declarationSequence
								| empty
		'''

	def p_conss(self, p):
		'''
			conss : conss constantDeclaration SCOLON
				  | empty
		'''

	def p_typess(self, p):
		'''
			typess : typess typeDeclaration SCOLON
				  | empty
		'''

	def p_varss(self, p):
		'''
			varss : varss variableDeclaration SCOLON
				  | empty
		'''

	def p_procss(self, p):
		'''
			procss : procss procedureDeclaration SCOLON
				  | empty
		'''

	def p_statementSequence(self, p):
		'''
			statementSequence : statementSequence SCOLON statement
							  | statement
		'''

	def p_constantDeclaration(self, p):
		'''
			constantDeclaration : IDENT ASSIGN expression
		'''

	def p_expression(self, p):
		'''
			expression : simpleExpression
					   | simpleExpression relation simpleExpression
		'''

	def p_simpleExpression(self, p):
		'''
			simpleExpression : PLUS term simpless
							 | term simpless
							 | MINUS term simpless
		'''

	def p_simpless(self, p):
		'''
			simpless : simpless addOperator term
					 | empty
		'''

	def p_term(self, p):
		'''
			term : factor termss
		'''

	def p_termss(self, p):
		'''
			termss : termss mulOperator factor
				   | empty
		'''

	def p_factor(self, p):
		'''
			factor : number
				   | char
				   | string
				   | KEY_NIL
				   | set
				   | designator
				   | designator actualParameters
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
			number : VINTEGER 
				   | VREAL
		'''

	def p_char(self, p):
		'''
			char : VCHAR
		'''

	def p_string(self, p):
		'''
			string : VSTRING
		'''	

	def p_set(self, p):
		'''
			set : LCB element COMMA element RCB
				| LCB RCB
		'''

	def p_element(self, p):
		'''
			element : expression
		'''

	def p_designator(self, p):
		'''
			designator : qualident designator2
					   | qualident
		'''

	def p_designator2(self, p):
		'''
			designator2 : designator2 DOT identdef
						| designator2 LSB expList RSB
						| designator LRB qualident RRB
		'''

	def p_qualident(self, p):
		'''
			qualident : identdef
					  | identdef DOT identdef
		'''

	def p_identdef(self, p):
		'''
			identdef : IDENT
					 | MULTIPLY IDENT
		'''

	def p_expList(self, p):
		'''
			expList : expList COMMA expression
					| expression
		'''

	def p_actualParameters(self, p):
		'''
			actualParameters : LRB expList RRB
							 | LRB RRB
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
			arrayType : KEY_ARRAY length comass KEY_OF type
		'''

	def p_comass(self, p):
		'''
			comass : comass COMMA length
				   | empty
		'''

	def p_length(self, p):
		'''
			length : expression
		'''

	def p_recordType(self, p):
		'''
			recordType : KEY_RECORD fieldListSequence KEY_END
					   | KEY_RECORD LRB baseType RRB fieldListSequence KEY_END
		'''

	def p_baseType(self, p):
		'''
			baseType : qualident
		'''

	def p_fieldListSequence(self, p):
		'''
			fieldListSequence : fieldListSequence SCOLON fieldList
							  | fieldList
		'''

	def p_fieldList(self, p):
		'''
			fieldList : identList COLON type
					  | empty
		'''

	def p_identList(self, p):
		'''
			identList : identList COMMA IDENT
					  | IDENT
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
			procedureHeading : KEY_PROCEDURE IDENT formalParameters COLON type
							 | KEY_PROCEDURE IDENT COLON type
		'''

	def p_formalParameters(self, p):
		'''
			formalParameters : LRB FPSection formalss RRB
							 | LRB RRB
		'''

	def p_formalss(self, p):
		'''
			formalss : formalss SCOLON FPSection
					 | empty
		'''

	def p_FPSection(self, p):
		'''
			FPSection : IDENT FPs COLON type
		'''

	def p_FPs(self, p):
		'''
			FPs : FPs COMMA IDENT
				| empty
		'''

	def p_procedureBody(self, p):
		'''
			procedureBody : declarationSequence KEY_BEGIN statementSequence KEY_END
		'''

	def p_statement(self, p):
		'''
			statement : assignment
					  | procedureCall
					  | ifStatement
					  | switchStatement
					  | whileStatement
					  | forStatement
					  | doWhileStatement
					  | KEY_EXIT
					  | KEY_RETURN expression
					  | KEY_RETURN
					  | ioStatement
					  | fileStatement
					  | KEY_BREAK
					  | KEY_CONTINUE
					  | empty
		'''

	def p_assignment(self, p):
		'''
			assignment : designator ASSIGN expression
		'''

	def p_procedureCall(self, p):
		'''
			procedureCall : designator actualParameters
						  | designator
		'''

	def p_ifStatement(self, p):
		'''
			ifStatement : KEY_IF expression KEY_THEN statementSequence ifss KEY_ELSE statementSequence KEY_END
						| KEY_IF expression KEY_THEN statementSequence ifss KEY_END
		'''

	def p_ifss(self, p):
		'''
			ifss : ifss KEY_ELSEIF expression KEY_THEN statementSequence
				 | empty
		'''

	def p_switchStatement(self, p):
		'''
			switchStatement : KEY_SWITCH expression KEY_BEGIN case casess KEY_ELSE COLON statementSequence KEY_END
							| KEY_SWITCH expression KEY_BEGIN case casess KEY_END
		'''

	def p_casess(self, p):
		'''
			casess : casess OR case
				   | empty
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
