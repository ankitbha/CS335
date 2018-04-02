#!/usr/bin/env python3

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
		('left', 'EQUAL', 'NEQUAL'),
		('left', 'GT', 'GTEQ', 'LT', 'LTEQ'),
		('left', 'PLUS', 'MINUS'),
		('left', 'MULTIPLY', 'DIVIDE', 'MODULUS'),
		('right', 'NOT'),
		('left', 'DOT')
	)

	def __init__(self, lexer):
		self.lexer = lex.lex(module=tokenizer())

	def p_module(self, p):
		'''
			module : KEY_MODULE IDENT SCOLON declarationSequence KEY_BEGIN statementSequence KEY_END IDENT DOT
		'''
		# print(p[0])
		p[0] = {}
		p[0]['code'] = p[6]['code'] + p[4]['code']
		print(p[0]['code'])

	def p_declarationSequence(self, p):
		'''
			declarationSequence : declarationSequence KEY_CONST conss
								| declarationSequence KEY_TYPE typess
								| declarationSequence KEY_VAR varss
								| declarationSequence procss
								| empty
		'''

		if(p[1]==None):
			p[0]={}
			p[0]['code']=''
			# print("##########")
		else:
			# do nothing for now. Thing will be handled in conss typss etc
			p[0]={}
			p[0]['code']=''


	def p_conss(self, p):
		'''
			conss : conss constantDeclaration SCOLON
				  | constantDeclaration SCOLON
		'''

	def p_typess(self, p):
		'''
			typess : typess typeDeclaration SCOLON
				  | typeDeclaration SCOLON
		'''

	def p_varss(self, p):
		'''
			varss : varss variableDeclaration SCOLON
				  | variableDeclaration SCOLON
		'''

	def p_procss(self, p):
		'''
			procss : procss procedureDeclaration SCOLON
				   | procedureDeclaration SCOLON
		'''

	def p_statementSequence(self, p):
		'''
			statementSequence : statementSequence statement SCOLON
							  | empty
		'''
		p[0]={}
		if(str(p.slice[1])=="empty"):
			p[0]['code'] = ''
		else:
			# print("#######################")
			# print(p[2])
			p[0]['code'] = p[1]['code'] + p[2]['code'] 

	def p_constantDeclaration(self, p):
		'''
			constantDeclaration : IDENT ASSIGN expression COLON type
		'''

		# add to sym table

	def p_expression(self, p):
		'''
			expression : simpleExpression
					   | simpleExpression relation simpleExpression
		'''
		p[0] = {}
		p[0]['place'] = 'abc'

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
				   | boolean
				   | char
				   | string
				   | KEY_NIL LRB designator RRB
				   | set
				   | designator
				   | designator actualParameters
				   | LRB expression RRB
				   | NOT factor
				   | KEY_ABS factor
				   | varType
				   | setType
				   | KEY_CHR LRB factor RRB
				   | KEY_ORD LRB factor RRB
		'''

	def p_number(self, p):
		'''
			number : VINTEGER
				   | VREAL
		'''

	def p_boolean(self, p):
		'''
			boolean : VBOOLEAN
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
			set : LCB element RCB
				| LCB RCB
		'''

	def p_element(self, p):
		'''
			element : element COMMA element
			        | expression
		'''

	def p_designator(self, p):
		'''
			designator : qualident designator2
		'''
		p[0] = {}
		p[0]['place'] = p[1]['place']

	def p_designator2(self, p):
		'''
			designator2 : designator2 DOT identdef
						| designator2 LSB expList RSB
						| empty
		'''

	def p_qualident(self, p):
		'''
			qualident : identdef
					  | identdef DOT qualident
		'''
		p[0] = {}
		p[0]['place'] = p[1]['place']

	def p_identdef(self, p):
		'''
			identdef : IDENT
					 | AT IDENT
		'''
		p[0] = {}
		p[0]['place'] = p.slice[1].value

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
		# handle in symbol table

	def p_type(self, p):
		'''
			type : IDENT
				 | varType
				 | arrayType
				 | recordType
				 | pointerType
				 | setType
		'''

	def p_varType(self, p):
		'''
			varType : KEY_INTEGER
					| KEY_BOOLEAN
					| KEY_CHAR
					| KEY_STRING
					| KEY_REAL
					| KEY_FILE
		'''

	def p_arrayType(self, p):
		'''
			arrayType : KEY_ARRAY length comass KEY_OF type
		'''


	def p_setType(self, p):
		'''
			setType : KEY_SET
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
			procedureDeclaration : procedureHeading SCOLON procedureBody IDENT
		'''
		p[0] = {}
		p[0]['code'] = p[1]['code'] + p[3]['code']

	def p_procedureHeading(self, p):
		'''
			procedureHeading : KEY_PROCEDURE IDENT formalParameters COLON type
							 | KEY_PROCEDURE IDENT formalParameters
		'''
		# p[0]={}
		# p[0]['code'] = 

	def p_formalParameters(self, p):
		'''
			formalParameters : LRB fpSection formalss RRB
							 | LRB RRB
		'''

	def p_formalss(self, p):
		'''
			formalss : formalss SCOLON fpSection
					 | empty
		'''

	def p_fpSection(self, p):
		'''
			fpSection : IDENT fps COLON type
		'''

	def p_fps(self, p):
		'''
			fps : fps COMMA IDENT
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
					  | memoryalloc
					  | setStatement
		'''
		p[0]={}
		if(str(p.slice[1])=='assignment' or str(p.slice[1]) == 'ioStatement'):
			print("statament")
			p[0]['code'] = p[1]['code']

	def p_assignment(self, p):
		'''
			assignment : designator ASSIGN expression
		'''
		p[0] = {}
		p[0]['code'] = "=, " + p[1]['place'] + ", " + p[3]['place']

	def p_setStatement(self, p):
		'''
			setStatement : KEY_ADD LRB qualident COMMA expression RRB
						 | KEY_DEL LRB qualident COMMA expression RRB

		'''

	def p_memoryalloc(self, p):
		'''
			memoryalloc : KEY_NEW LRB designator RRB
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
			casess : case casess
				   | empty
		'''

	def p_case(self, p):
		'''
			case : KEY_CASE expression COLON statementSequence
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
			doWhileStatement : KEY_DO KEY_BEGIN statementSequence KEY_END KEY_WHILE expression
		'''

	def p_ioStatement(self, p):
		'''
			ioStatement : KEY_WRITE LRB expression RRB
						| KEY_WRITEINT LRB expression RRB
						| KEY_WRITEREAL LRB expression RRB
						| KEY_WRITECHAR LRB expression RRB
						| KEY_WRITEBOOL LRB expression RRB
						| KEY_WRITELN LRB expression RRB
						| KEY_WRITELN LRB RRB
						| KEY_READ LRB expression RRB
						| KEY_READINT LRB expression RRB
						| KEY_READREAL LRB expression RRB
						| KEY_READCHAR LRB expression RRB
						| KEY_READBOOL LRB expression RRB
		'''
		p[0] = {}
		if(p[1]=='WRITEINT'):
			print("######################")
			p[0]['code'] = 'printint, ' + p[3]['place']


	def p_fileStatement(self, p):
		'''
			fileStatement : identdef EQUAL KEY_FOPEN LRB IDENT COMMA char RRB
						  | identdef EQUAL KEY_FREAD LRB identdef COMMA VINTEGER RRB
						  | KEY_FWRITE LRB identdef COMMA string RRB
						  | KEY_FAPPEND LRB identdef COMMA string RRB
						  | KEY_FCLOSE LRB identdef RRB
		'''

	def p_empty(self, p):
		'''
			empty :
		'''
		pass

	def p_error(self, p):
		print('\n-------------------------------------------------------')

		print('Error: \'{}\' at line no: {}'.format(p.value, p.lineno))

		with open(filename,'r') as fp:
			for i, line in enumerate(fp):
				if i+1 == p.lineno:
					print("\t\t\tin {}".format(line.strip(),))

		print('-------------------------------------------------------\n')

		exit(1)


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

	def parse_file(self, _file, debug=False):
		content = self.read_file(_file)
		parse_ret = self.parser.parse(content, lexer=self.lexer, debug=debug)
		return parse_ret

if __name__=="__main__":
	parser = Parserrr()
	filename = sys.argv[1]

	result = parser.parse_file(filename, debug = True)
