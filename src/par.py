#!/usr/bin/env python3

import os
import sys
import lex
import yacc
from tokenizer import tokenizer
import symtable
import re

# ----------------------------------------- type part -------------------------------------

dterm = {}
sterm = {}
flag = 0
flagg = 0

class Typeclass(object):
	def __init__(self):
		pass

	def type_cast_implicit(self, type1, type2):
		if((type1 == 'REAL' and type2 == 'INTEGER') or (type1 == 'INTEGER' and type2 == 'REAL')):
			return 'REAL'
		return None

	def get_new_object(self, obj1, obj2, token):
		type_list = accepted_types[token]
		type1, value1 = obj1['type'], obj1['place']
		if(obj2 != None):
			type2, value2 = obj2['type'], obj2['place']
			if type1 in type_list and type2 in type_list:
				if (type1 == type2):
					if(type_list[-1] == None):
						return {'type' : type1, 'value1' : value1, 'value2' : value2}
					else:
						return {'type' : type_list[-1], 'value1' : value1, 'value2' : value2}

				else:
					type3 = self.type_cast_implicit(type1, type2)
					if type3 != None:
						return {'type' : type3, 'value1' : value1, 'value2' : value2}
					else:
						raise TypeError("Types are incompatible")
			else:
				raise TypeError("Type is invalid")

		else:
			if type1 in type_list:
				return obj1

			raise TypeError("Invalid Type")

			# see the variable names--------------------------------

	def returnTypeCheck(self, Type, Table):
		if Table.category == SymTab.Category.Function:
			if Table.attr['type'] != Type:
				return False
			return True
		else:
			return self.returnTypeCheck(Type, Table.parent)

 # ---------------------------------------------------------------------------------------



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
		self.tunnelTab = symtable.tunnelTable()
		self.xtras = symtable.xtraNeeds()
		self.Typeclass = Typeclass()

	def printParseTree(self, p):
		flag = False
		if flag:
			print(p.slice)

	def magic(self, incode2):
		count = 0
		found = 0
		labdick = {}
		for line in incode2:
			count=count+1
			if len(line)==1 and (re.match('_L[0-9]+',line[0])):
				labdick[line[0]] = count
				del incode2[count-1]
			incode2[count-1] = [str(count)] + incode2[count-1]
		# for line in incode2:
		# 	print(line)
		# print(labdick)
		for j, line in enumerate(incode2):
			for i,elem in enumerate(line):
				if isinstance(elem, str) and re.match('_L[0-9]+',line[i]):
					incode2[j][i] = str(labdick[line[i]])
		return incode2


	def p_module(self, p):
		'''
			module : KEY_MODULE IDENT SCOLON declarationSequence KEY_BEGIN statementSequence KEY_END IDENT DOT
		'''
		p[0] = {}

		p[0]['code'] = p[4]['code2'] + p[6]['code'] + [['return']] + p[4]['code']
		# print('\n'.join(map(str, p[0]['code'])))
		# self.tunnelTab.rootTable.printMe()
		self.tempir = p[0]['code']
		self.irrcode = self.magic(self.tempir)
		for elem in self.tempir:
			print(elem)

	def p_declarationSequence(self, p):
		'''
			declarationSequence : declarationSequence KEY_CONST conss
								| declarationSequence KEY_TYPE typess
								| declarationSequence KEY_VAR varss
								| declarationSequence procss
								| declarationSequence ioStatement SCOLON
								| empty
		'''
		self.printParseTree(p)
		p[0]={}
		p[0]['code']=[]
		p[0]['code2']=[]
		if(len(p)!=2):
			if(str(p.slice[2])=='procss'):
				p[0]['code'] = p[1]['code'] + p[2]['code']
			elif(str(p.slice[3])=='conss' or str(p.slice[3])=='varss' ):
				p[0]['code2'] = p[1]['code2'] + p[len(p)-1]['code']
			elif(str(p.slice[2])=='ioStatement'):
				p[0]['code2'] = p[1]['code2'] + p[len(p)-2]['code']

	def p_conss(self, p):
		'''
			conss : conss constantDeclaration SCOLON
				  | constantDeclaration SCOLON
		'''
		p[0]={}
		if(len(p)==3):
			p[0]['code'] = p[1]['code']
		else:
			p[0]['code'] = p[0]['code'] + p[1]['code']

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
		p[0] = {}
		if(len(p)==3):
			p[0]['code'] = p[1]['code']
		else:
			p[0]['code'] = p[1]['code'] + p[2]['code']

	def p_procss(self, p):
		'''
			procss : procss procedureDeclaration SCOLON
				   | procedureDeclaration SCOLON
		'''
		p[0] = {}
		if(len(p)==4):
			p[0]['code'] = p[1]['code'] + p[2]['code']
		else:
			p[0]['code'] = p[1]['code']

	def p_statementSequence(self, p):
		'''
			statementSequence : statementSequence statement SCOLON
							  | empty
		'''
		p[0]={}
		if(str(p.slice[1])=="empty"):
			p[0]['code'] = []
		else:
			p[0]['code'] = p[1]['code'] + p[2]['code']

	def p_constantDeclaration(self, p):
		'''
			constantDeclaration : IDENT ASSIGN expression COLON type
		'''
		p[0]={}
		symEnti = self.tunnelTab.currTable.addEntry(p.slice[1].value, p[5]['type'] ,'const')
		p[0]['code'] = p[3]['code'] + [["=", symEnti, p[3]['place']]]

	def p_expression(self, p):
		'''
			expression : simpleExpression
					   | simpleExpression relation simpleExpression
		'''
		p[0] = {}

		if(len(p)==2):
			p[0]['code'] = p[1]['code']
			p[0]['type'] = p[1]['type']
			p[0]['place'] = p[1]['place']
		else:
			temp_var = self.xtras.getNewTemp('BOOLEAN', 'simplevar')
			temp_var = temp_var
			if((p.slice[2].value != 'IN') and (p.slice[2].value != 'IS')):
				p[0]['code'] = p[1]['code'] +  p[3]['code'] + [[p.slice[2].value, temp_var,  p[1]['place'], p[3]['place']]]
			else:
				# need to see this again..........
				if(p[1]['type'] == str(p.slice[3].value)):
					p[0]['code'] = p[1]['code'] + p[3]['code'] + [["=" , temp_var , "true"]]
				else:
					p[0]['code'] = p[1]['code'] + p[3]['code'] + [["=" , temp_var , "false"]]
			p[0]['type'] = 'BOOLEAN'
			p[0]['place'] = temp_var



	def p_simpleExpression(self, p):
		'''
			simpleExpression : PLUS simpless term
							 | simpless term
							 | MINUS simpless term
		'''
		p[0] = {}
		if(p[len(p)-2]['empty']==True):
			p[0]['type'] = p[len(p)-1]['type']
			p[0]['place'] = p[len(p)-1]['place']

			if(p.slice[1].value == '-'):
				p[0]['code'] = p[3]['code'] + [["-" , p[0]['place'], "0" , p[3]['place']]]
			else:
				if(p.slice[1].value == '+'):
					p[0]['code'] = p[3]['code']
				else:
					p[0]['code'] = p[2]['code']
		else:
			p[0]['type'] = p[len(p)-1]['type']
			temp_var = self.xtras.getNewTemp(p[0]['type'], 'simplevar')
			# temp_var = temp_var.lex
			p[0]['place'] = temp_var
			if(len(p)==3):
				p[0]['code'] = p[1]['code'] + p[2]['code'] + [[p[1]['operator'] , p[0]['place'] , p[1]['place'] , p[2]['place']]]
			else:
				if(p.slice[1].value == '+'): # check if this will hold--------------------------------------
					# newobj = get_new_object(p[2], p[3], p[3]['operator'])
					p[0]['code'] = p[2]['code'] + p[3]['code'] + [[p[3]['operator'] , p[0]['place'] , p[2]['place'] , p[3]['place']]]
				else:
					# newobj = get_new_object(p[2], p[3], p[3]['operator'])
					p[0]['code'] = p[2]['code'] + p[3]['code'] + [[p[3]['operator'] , p[0]['place'] , p[2]['place'] , p[3]['place'] ]]
					p[0]['code'] += [["=" , p[0]['place'] , "-" , p[0]['place']]]


	def p_simpless(self, p):
		'''
			simpless : simpless term addOperator
					 | empty
		'''
		global flagg
		p[0] = {}
		p[0]['empty'] = False
		if(len(p)==4):
			if(p[1]['empty']==True):
					p[0]['place'] = p[2]['place']
					p[0]['operator'] = p.slice[3].value
					p[0]['type'] = p[2]['type']
					p[0]['code'] = p[2]['code']
			else:

				temp_var = self.xtras.getNewTemp(p[2]['type'], 'simplevar')
				p[0]['operator'] = p.slice[3].value
				p[0]['type'] = p[2]['type']
				if (flagg==1 and p[0]['type'] != 'BOOLEAN'):
					if p.slice[3].value == "+":
						p[0]['operator'] = "-"
					if p.slice[3].value == "-":
						p[0]['operator'] = "+"
				else:
					p[0]['operator'] = p.slice[3].value
				if(p[0]['operator'] == "-"):
					flagg = 1
				else:
					flagg = 0

				p[0]['place'] = temp_var
				p[0]['code'] = p[1]['code'] + p[2]['code'] + [[p[0]['operator'] , p[0]['place'] , p[1]['place'] , p[2]['place'] ]]
		else:
			p[0]['empty'] = True

	def p_term(self, p):
		'''
			term : termss factor
		'''
		p[0] = {}
		if(p[1]['empty']==True):
			p[0]['type'] = p[2]['type']
			p[0]['code'] = p[2]['code']
			p[0]['place'] = p[2]['place']
		else:
			p[0]['type'] = p[len(p)-1]['type']
			# newobj = get_new_object(p[1], p[2], p[2]['operator'])
			temp_var = self.xtras.getNewTemp(p[0]['type'], 'simplevar')
			#temp_var = temp_var
			p[0]['place'] = temp_var
			p[0]['code'] = p[1]['code'] + p[2]['code'] + [[p[1]['operator'] , p[0]['place'] , p[1]['place'] , p[2]['place'] ]]

	def p_termss(self, p):
		'''
			termss : termss factor mulOperator
				   | empty
		'''


		p[0] = {}
		p[0]['empty'] = False
		if(len(p)==4):
			if(p[1]['empty']==True):
					p[0]['place'] = p[2]['place']
					p[0]['operator'] = p.slice[3].value
					p[0]['type'] = p[2]['type']
					p[0]['code'] = p[2]['code']
			else:
				temp_var = self.xtras.getNewTemp(p[1]['type'], 'simplevar')
				p[0]['type'] = p[2]['type']
				p[0]['place'] = temp_var
				p[0]['operator'] = p.slice[3].value
				p[0]['code'] = p[1]['code'] + [[p[0]['operator'] , p[0]['place'] , p[1]['place'] , p[2]['place'] ]]
		else:
			p[0]['empty'] = True

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
		p[0] = {}
		if (type(p[1]) == dict):
			if ('kind' in p[1].keys()):
				p[0]['kind'] = p[1]['kind']
			else:
				p[0]['kind'] = 'simplevar'
		if(len(p)==2):
			if p[0]['kind'] == 'array':
				temp_var = self.xtras.getNewTemp(p[1]['type'], 'simplevar')
				#temp_var = temp_var
				asscode = [["readarray" , p[1]['place'] , p[1]['offset'] , temp_var ]]
				p[0]['code'] = p[1]['code'] + asscode
				p[0]['place'] = temp_var
				p[0]['type'] = p[1]['type']
			else:
				p[0]['place'] = p[1]['place']
				p[0]['code'] = p[1]['code']
				p[0]['type'] = p[1]['type']

		if(len(p)==3):
			if( str(p.slice[1]) == 'designator'):
				proc = self.tunnelTab.queryProc(p[1]['place'].lex)
				p[0]['type'] = proc['type']
				temp_var = self.xtras.getNewTemp(p[0]['type'], 'simplevar')
				#temp_var = temp_var.lex
				p[0]['place'] = temp_var
				p[0]['code'] = p[2]['code'] + [['call' , p[1]['place'] , p[0]['place'] ]]

			elif(p.slice[1].value == 'ABS'):
				if(p[2]['type'] in ['REAL', 'INTEGER']):
					p[0]['type'] = p[2]['type']
					temp_var = self.xtras.getNewTemp(p[0]['type'], 'simplevar')
					#temp_var = temp_var.lex
					p[0]['place'] = temp_var
					p[0]['code'] = p[2]['code'] + [["abs" , p[0]['place'] , p[2]['place'] ]]
				else:
					print("error in use of ABS")
			elif(p.slice[1].value == '!'):
				if(p[2]['type'] in ['BOOLEAN']):
					p[0]['type'] = p[2]['type']
					temp_var = self.xtras.getNewTemp(p[0]['type'], 'simplevar')
					#temp_var = temp_var.lex
					p[0]['place'] = temp_var
					p[0]['code'] = p[2]['code'] + [["!" , p[0]['place'] , p[2]['place'] ]]
			elif p[1]['kind'] == 'array':
				p[0]['kind'] == 'array'


		if(len(p)==5):
			if(p.slice[1].value == "CHR"):
				if(p[3]['type'] in ['INTEGER']):
					p[0]['type'] = 'CHAR'
					temp_var = self.xtras.getNewTemp(p[0]['type'], 'simplevar')
					#temp_var = temp_var.lex
					p[0]['place'] = temp_var
					p[0]['code'] = p[3]['code'] + [["CHR" , p[0]['place'] , p[3]['place'] ]]
				else:
					print("incorrect use of CHR")
			if(p.slice[1].value == "ORD"):
				if(p[3]['type'] in ['CHAR']):
					p[0]['type'] = 'INTEGER'
					temp_var = self.xtras.getNewTemp(p[0]['type'], 'simplevar')
					# temp_var = temp_var.lex
					p[0]['place'] = temp_var
					p[0]['code'] = p[3]['code'] + [["ORD" , p[0]['place'] , p[3]['place']]]
				else:
					print("incorrect use of ORD")
		if(len(p)==4):
			p[0]['type'] = p[2]['type']
			p[0]['place'] = p[2]['place']
			p[0]['code'] = p[2]['code']

	def p_number(self, p):
		'''
			number : VINTEGER
				   | VREAL
		'''
		p[0] = {}
		p[0]['code'] = []
		if p.slice[1].type=="VINTEGER":
			p[0]['type'] = 'INTEGER'
		else:
			p[0]['type'] = 'REAL'

		p[0]['place'] = p.slice[1].value

	def p_boolean(self, p):
		'''
			boolean : VBOOLEAN
		'''
		p[0] = {}

		p[0]['code'] = []
		p[0]['type'] = 'BOOLEAN'
		p[0]['place'] = p.slice[1].value

	def p_char(self, p):
		'''
			char : VCHAR
		'''
		p[0] = {}

		p[0]['code'] = []
		p[0]['type'] = 'CHAR'
		p[0]['place'] = p.slice[1].value

	def p_string(self, p):
		'''
			string : VSTRING
		'''
		p[0] = {}

		p[0]['code'] = []
		p[0]['type'] = 'STRING'
		p[0]['place'] = p.slice[1].value


# ---------------------------------------------------------------------------

	def p_set(self, p):
		'''
			set : LCB element RCB
				| LCB RCB
		'''
		p[0] = {}
		if(len(p)==3):
			p[0]['code'] = []
			temp_var = self.xtras.getNewTemp('SET', 'simplevar')
			# temp_var = temp_var.lex
			p[0]['place'] = temp_var
			p[0]['type'] = 'SET'
		else:
			p[0]['type'] = 'SET'
			temp_var = self.xtras.getNewTemp('SET', 'simplevar')
			# temp_var = temp_var.lex
			p[0]['place'] = temp_var
			p[0]['code'] = p[2]['code'] + [["SET" , p[0]['place'] , p[2]['place'] ]]

	def p_element(self, p):
		'''
			element : element COMMA element
					| expression
		'''
		p[0] = {}
		if(len(p)==2):
			p[0]['type'] = p[1]['type']
			temp_var = self.xtras.getNewTemp('SET', 'simplevar')
			# temp_var = temp_var.lex
			p[0]['place'] = temp_var
			p[0]['code'] = p[1]['code'] + [["=" , p[0]['place'] , p[1]['place']]]
		else:
			if(p[1]['type'] == p[3]['type']):
				p[0]['type'] = p[1]['type']
			else:
				p[0]['type'] = 'SET'
			p[0]['code'] = p[1]['code'] + [[","]] + p[3]['code']

	def p_designator(self, p):
		'''
			designator : qualident designator2
		'''
		p[0] = {}
		if ( p[2]['kind']=='simplevar' ):
			p[0]['place'] = p[1]['place']
			p[0]['code'] = p[1]['code']
			p[0]['type'] = p[1]['type']
			p[0]['kind'] = 'simplevar'
		elif ( p[2]['kind'] == 'array' ):
			arrayName = p[1]['place'].lex
			arrayent = self.tunnelTab.queryEnt(arrayName, None)
			placistt = arrayent.placist
			offs = p[2]['place']
			offscode = []
			ffplace = '0'
			for i in range(0, len(placistt)):
				finalplace = offs[i]
				for j in range(i+1, len(placistt)):
					# temp = self.xtras.getNewTemp('INTEGER', 'simplevar')
					# templace = temp.lex
					temp2 = self.xtras.getNewTemp('INTEGER', 'simplevar')
					templace2 = temp2
					offscode += [['*' , templace2 , finalplace , placistt[j] ]]
					finalplace = templace2
				ttemp2 = self.xtras.getNewTemp('INTEGER', 'simplevar')
				offscode += [['+' , ttemp2 , ffplace , finalplace ]]
				ffplace = ttemp2

			p[0]['offset'] = ffplace
			p[0]['code'] = p[1]['code'] + p[2]['code'] + offscode
			p[0]['type'] = arrayent.vtype
			p[0]['kind'] = 'array'
			p[0]['place'] = arrayent


	def p_designator2(self, p):
		'''
			designator2 : designator2 DOT identdef
						| designator2 LSB expList RSB
						| empty
		'''
		p[0]={}
		if (len(p)==2):
			p[0]['code'] = []
			p[0]['kind'] = 'simplevar'
		elif (len(p)==5):
			p[0]['code'] = p[1]['code'] + p[3]['code']
			p[0]['kind'] = 'array'
			p[0]['place'] = p[3]['place']
		#TODO elif(len(p)==4):

	def p_qualident(self, p):
		'''
			qualident : identdef
					  | identdef DOT qualident
		'''
		p[0] = {}
		p[0]['place'] = p[1]['place']
		p[0]['code'] = p[1]['code']
		p[0]['type'] = p[1]['type']

	def p_identdef(self, p):
		'''
			identdef : IDENT
					 | AT IDENT
		'''
		p[0] = {}

		if len(p)==2:
			entry = self.tunnelTab.queryEnt(p.slice[1].value, None)
			# if (entry.kind != 'func'):
			p[0]['place'] = entry
			p[0]['code'] = []
			p[0]['type'] = entry.vtype
			# else:
			# 	p[0]['place']
		else:
			entry = self.tunnelTab.queryEnt(p.slice[2].value, None)
			p[0]['place'] = entry
			p[0]['code'] = []
			p[0]['type'] = None

	def p_expList(self, p):
		'''
			expList : expList COMMA expression
					| expression
		'''
		p[0]={}
		p[0]['place'] = []
		p[0]['type'] = []
		if(len(p)==2):
			p[0]['place'] = [p[1]['place']]
			p[0]['type'] = [p[1]['type']]
			p[0]['code'] = p[1]['code']
		else:
			p[0]['place'] = p[1]['place'] + [p[3]['place']]
			p[0]['type'] = p[1]['type'] + [p[3]['type']]
			p[0]['code'] = p[1]['code'] + p[3]['code']

	def p_actualParameters(self, p):
		'''
			actualParameters : LRB expList RRB
							 | LRB RRB
		'''
		p[0] = {}
		if(len(p)==4):
			p[0]['place'] = p[2]['place']
			p[0]['code'] = p[2]['code']
			for param in p[2]['place']:
				p[0]['code'] = p[0]['code'] + [["param" , param ]]
		else:
			p[0]['code'] = []

	def p_mulOperator(self, p):
		'''
			mulOperator : MULTIPLY
						| DIVIDE
						| MODULUS
						| AND
		'''
		p[0] = p.slice[1].value
		# p[0] = {}
		# p[0]['code'] = ''
		# p[0]['place'] = p.slice[1].value


	def p_addOperator(self, p):
		'''
			addOperator : PLUS
						| MINUS
						| OR
		'''
		p[0] = p.slice[1].value
		# p[0] = {}
		# p[0]['code'] = ''
		# p[0]['place'] = p.slice[1].value

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
		p[0] = p.slice[1].value
		# p[0] = {}
		# p[0]['code'] = ''
		# p[0]['place'] = p.slice[1].value

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
		#if ((p.slice[1]) == 'arrayType'):
		p[0] = {}
		p[0]['type'] = p[1]['type']
		if str(p.slice[1]) == 'arrayType':
			p[0]['code'] = p[1]['code']
			p[0]['kind'] = 'array'
			p[0]['place'] = p[1]['place']
			p[0]['placist'] = p[1]['placist']
		elif str(p.slice[1]) == 'pointerType':
			p[0]['code'] = p[1]['code']
			p[0]['kind'] = 'array'
			p[0]['place'] = p[1]['place']
			p[0]['placist'] = p[1]['placist']
		if str(p.slice[1]) == 'varType':
			p[0]['kind'] = 'simplevar'
			p[0]['code'] = []
		# if str(p.slice[1]) == 'recordType':
		# 	p[0]['kind'] = 'recordType'
		# 	p[0]['code'] = []

	def p_varType(self, p):
		'''
			varType : KEY_INTEGER
					| KEY_BOOLEAN
					| KEY_CHAR
					| KEY_STRING
					| KEY_REAL
					| KEY_FILE
		'''
		p[0] = {}
		p[0]['type'] = p.slice[1].value

	def p_arrayType(self, p):
		'''
			arrayType : KEY_ARRAY length comass KEY_OF type
		'''
		p[0] = {}
		temp = self.xtras.getNewTemp('INTEGER', 'simplevar')
		p[0]['place'] = temp
		sizCode = [['*' , p[0]['place'] , p[2]['place'] , p[3]['place']]]
		p[0]['code'] = p[2]['code'] + p[3]['code'] + sizCode
		p[0]['type'] = p[5]['type']
		p[0]['placist'] = []
		#p[0]['placist'].append('1')
		p[0]['placist'].append(p[2]['place'])
		for pl in p[3]['placist']:
			p[0]['placist'].append(pl)

	def p_setType(self, p):
		'''
			setType : KEY_SET
		'''
		p[0] = {}
		p[0]['code'] = []
		p[0]['type'] = p.slice[1].value
		p[0]['place'] = p.slice[1].value


	def p_comass(self, p):
		'''
			comass : comass COMMA length
				   | empty
		'''
		p[0] = {}
		p[0]['placist'] = []
		if (str(p.slice[1]) == 'empty'):
			p[0]['code'] = []
			p[0]['place'] = '1'
		else:
			temp = self.xtras.getNewTemp('INTEGER', 'simplevar')
			p[0]['place'] = temp
			comCode = [['*' , p[0]['place'] , p[1]['place'] , p[3]['place']]]
			p[0]['code'] = p[1]['code'] + p[3]['code'] + comCode
			for pl in p[1]['placist']:
				p[0]['placist'].append(pl)
			p[0]['placist'].append(p[3]['place'])

	def p_length(self, p):
		'''
			length : expression
		'''
		p[0] = {}
		p[0]['code'] = p[1]['code']
		p[0]['place'] = p[1]['place']
		p[0]['type'] = p[1]['type']

	def p_recordType(self, p):
		'''
			recordType : KEY_RECORD mrecord fieldListSequence KEY_END
					   | KEY_RECORD mrecord LRB baseType RRB fieldListSequence KEY_END
		'''


	def p_mrecord(self,p):
		'''
			mrecord : empty
		'''
		self.tunnelTab.currTable.addEntry(p.slice[-1].value , 'RECORD', 'var')

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
		# if(len(p)!=2):
		# 	for var in p[1]:
		# 		self.tunnelTab.currTable.queryEnt()


	def p_identList(self, p):
		'''
			identList : identList COMMA IDENT
					  | IDENT
		'''
		p[0] = []
		if(len(p)==2):
			p[0] = [p.slice[1].value]
		else:
			p[0] = p[1] + [p.slice[3].value]


	def p_pointerType(self, p):
		'''
			pointerType : KEY_POINTER KEY_TO type
		'''


	def p_variableDeclaration(self, p):
		'''
			variableDeclaration : identList COLON type
		'''
		p[0] = {}
		if (p[3]['kind'] == 'simplevar'):
			p[0]['code'] = []
			for var in p[1]:
				self.tunnelTab.currTable.addEntry(var, p[3]['type'] ,'simplevar')
		if (p[3]['kind'] == 'array'):
			declCode = []
			for var in p[1]:
				tt = self.tunnelTab.currTable.addEntry(var, p[3]['type'] ,'array', p[3]['placist'])
				declCode += [['declarray' , tt , p[3]['place']]]
			p[0]['code'] = p[3]['code'] + declCode

	def p_procedureDeclaration(self, p):
		'''
			procedureDeclaration : procedureHeading SCOLON  procedureBody IDENT
		'''
		p[0] = {}
		p[0]['code'] = p[1]['code'] + p[3]['code']
		self.tunnelTab.endScope()
		# p[0]['type'] = p[1]['type']

	def p_procedureHeading(self, p):
		'''
			procedureHeading : KEY_PROCEDURE IDENT mproc formalParameters COLON type
							 | KEY_PROCEDURE IDENT mproc formalParameters
		'''
		p[0]={}
		p[0]['code'] = [['label' , p.slice[2].value]] + p[4]['code']
		p[0]['name'] = p.slice[2].value
		if(len(p)==7):
			self.tunnelTab.currTable.addOns['type'] = p[6]['type']
			p[0]['type'] = p[6]['type']
		else:
			self.tunnelTab.currTable.addOns['type'] = None
			p[0]['type'] = None
		self.tunnelTab.currTable.parent.addEntry(p[0]['name'],p[0]['type'],'func')

	def p_mproc(self,p):
		'''
			mproc : empty
		'''
		p[0]={}
		p[0]['id'] = p[-1]
		self.tunnelTab.startScope('func',p[0])


	def p_formalParameters(self, p):
		'''
			formalParameters : LRB fpSection formalss RRB
							 | LRB RRB
		'''
		p[0]={}
		if(len(p)==3):
			p[0]['code'] = []
		else:
			p[0]['code'] = p[3]['code'] + p[2]['code']

	def p_formalss(self, p):
		'''
			formalss : formalss SCOLON fpSection
					 | empty
		'''
		p[0] = {}
		if(len(p)==2):
			p[0]['code'] = []
		else:
			p[0]['code'] = p[3]['code'] + p[1]['code']

	def p_fpSection(self, p):
		'''
			fpSection : IDENT fps COLON type
		'''
		p[0] = {}
		p[0]['code'] = []
		for var in [p.slice[1].value]+p[2]:
			tt= self.tunnelTab.currTable.addEntry(var,p[4]['type'],'simplevar')
			p[0]['code'] = [['gparam' , tt ]] + p[0]['code']


	def p_fps(self, p):
		'''
			fps : fps COMMA IDENT
				| empty
		'''
		p[0] = []
		if(len(p)!=2):
			p[0] = p[1] + [p.slice[3].value]

	def p_procedureBody(self, p):
		'''
			procedureBody : declarationSequence KEY_BEGIN statementSequence KEY_END
		'''
		p[0]={}
		p[0]['code']=p[3]['code']

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
					  | breakStatement
					  | continueStatement
					  | empty
					  | memoryalloc
					  | setStatement
		'''
		p[0]={}
		if(str(p.slice[1])=='assignment' or str(p.slice[1]) == 'ioStatement'):
			p[0]['code'] = p[1]['code']
		if(p.slice[1].type=='KEY_RETURN'):
			if(len(p)==3):
				p[0]['code'] = p[2]['code'] + [['return' , p[2]['place'] ]]
			else:
				p[0]['code'] = [['return']] # some label
		if(str(p.slice[1])=='procedureCall'):
			p[0]['code'] = p[1]['code']

		if(str(p.slice[1])=='ifStatement'):
			p[0]['code'] = p[1]['code']
		if(str(p.slice[1])=='switchStatement'):
			p[0]['code'] = p[1]['code']
		if(str(p.slice[1])=='whileStatement'):
			p[0]['code'] = p[1]['code']
		if(str(p.slice[1])=='forStatement'):
			p[0]['code'] = p[1]['code']
		if(str(p.slice[1])=='breakStatement'):
			p[0]['code'] = p[1]['code']
		if(str(p.slice[1])=='continueStatement'):
			p[0]['code'] = p[1]['code']
		if(str(p.slice[1])=='memoryalloc'):
			p[0]['code'] = p[1]['code']




	def p_assignment(self, p):
		'''
			assignment : designator ASSIGN expression
		'''
		p[0] = {}
		if (p[1]['kind']=='simplevar'):
			p[0]['code'] = p[3]['code'] + [["=" , p[1]['place'] , p[3]['place'] ]]
		elif (p[1]['kind']=='array'):
			asscode = [["writearray" , p[1]['place'] , p[1]['offset'] , p[3]['place']]]
			p[0]['code'] = p[1]['code'] + p[3]['code'] + asscode

	def p_setStatement(self, p):
		'''
			setStatement : KEY_ADD LRB qualident COMMA expression RRB
						 | KEY_DEL LRB qualident COMMA expression RRB

		'''

	def p_breakStatement(self, p):
		'''
			breakStatement : KEY_BREAK
		'''
		p[0] = {}
		breakCode = [["goto" , self.tunnelTab.queryLabs('suf', self.tunnelTab.currTable) ]]
		p[0]['code'] = breakCode

	def p_continueStatement(self, p):
		'''
			continueStatement : KEY_CONTINUE
		'''
		p[0] = {}
		contCode = [["goto" , self.tunnelTab.queryLabs('loop', self.tunnelTab.currTable)]]
		p[0]['code'] = contCode


	def p_memoryalloc(self, p):
		'''
			memoryalloc : KEY_NEW LRB designator RRB
		'''
		p[0] = {}
		if(p[3]['type']!='pointer'):
			print('error')
		else:
			p[0]['code'] = 'new, ' + p[3]['place'] + '\n'


	def p_procedureCall(self, p):
		'''
			procedureCall : designator actualParameters
		'''
		p[0]={}
		self.tunnelTab.printfull(None)
		print((p[1]['place'].lex))
		proc = self.tunnelTab.queryEnt(p[1]['place'].lex,None)
		print(proc)
		p[0]['type'] = proc.vtype
		if(p[0]['type']!=None):
			print("typeerror")
		p[0]['code'] = p[2]['code'] + [["call" , p[1]['place']]]

	def p_markerif(self,p):
		'''
			markerif : empty
		'''
		self.tunnelTab.startScope('bb', {'id': self.xtras.getNewId()})


	def p_ifStatement(self, p):
		'''
			ifStatement : KEY_IF markerif expression KEY_THEN statementSequence ifss KEY_ELSE statementSequence KEY_END
						| KEY_IF markerif expression KEY_THEN statementSequence ifss KEY_END
		'''
		p[0] = {}
		p[3]['false'] = self.xtras.getNewLabel()
		if(len(p)==8):
			if p[3]['type'] != 'BOOLEAN':
				print("typeerror")
			p[0]['code'] = p[3]['code'] + [["ifgoto" , "=", p[3]['place'] , "false" , p[3]['false']]]
			p[0]['code'] = p[0]['code'] + p[5]['code'] + [[p[3]['false']]] + p[6]['code']
		else:
			if p[3]['type'] != 'BOOLEAN':
				print("typeerror")
			p[0]['code'] = p[3]['code'] + [["ifgoto", "=", p[3]['place'] , "false" , p[3]['false']]]
			p[0]['code'] = p[0]['code'] + p[5]['code'] + [[p[3]['false']]] + p[6]['code'] + p[8]['code']
		self.tunnelTab.endScope()

	def p_ifss(self, p):
		'''
			ifss : ifss KEY_ELSEIF expression KEY_THEN statementSequence
				 | empty
		'''
		p[0]={}
		if(len(p)==2):
			p[0]['code'] = []
		else:
			if p[3]['type'] != 'BOOLEAN':
				print("typeerror")
			p[3]['false'] = self.xtras.getNewLabel()
			p[0]['code'] = p[1]['code'] + p[3]['code'] + [["ifgoto", "=", p[3]['place'] , "false", p[3]['false']]]
			p[0]['code'] = p[0]['code'] + p[5]['code'] + [[p[3]['false']]]


	def p_switchStatement(self, p):
		'''
			switchStatement : KEY_SWITCH expression mswitch KEY_BEGIN case casess KEY_ELSE COLON statementSequence KEY_END
							| KEY_SWITCH expression mswitch KEY_BEGIN case casess KEY_END
		'''
		p[0]={}
		p[0]['next'] = self.xtras.getNewLabel()
		p[0]['test'] = self.xtras.getNewLabel()
		p[0]['code'] = p[2]['code'] + [['goto' , p[0]['test']], [p[5]['label']] , [p[5]['scode'] , 'goto' , p[0]['next'] ]]
		for case in p[6]:
			p[0]['code'] = [[p[0]['code'] , case['label']], [case['scode'] , 'goto' , p[0]['next']]]
		if(len(p)==11):
			p[0]['else'] = self.xtras.getNewLabel()
			p[0]['code'] = p[0]['code'] + [[p[0]['else']]] + p[9]['code'] + [['goto' , p[0]['next']]]

		p[0]['code'] = p[0]['code'] + [[p[0]['test']]]
		p[0]['code'] = p[0]['code'] + p[5]['ecode'] + [['ifgoto', '=',  p[2]['place'] , p[5]['place'] , p[5]['label']]]
		for case in p[6]:
			p[0]['code'] = p[0]['code'] + case['ecode'] + [['ifgoto', '=',  p[2]['place'] , case['place'] , case['label']]]
		if(len(p)==11):
			p[0]['code'] = p[0]['code'] + [['goto' , p[0]['else'] ]]
		p[0]['code'] = p[0]['code'] + [[p[0]['next']]]

	def p_mswitch(self, p):
		'''
			mswitch : empty
		'''
		p[0]={}
		p[0]['var'] = p[-1]['place']

	def p_casess(self, p):
		'''
			casess : case casess
				   | empty
		'''
		p[0]=[]
		if(len(p)!=2):
			p[0] = [p[1]] + p[2]
		else:
			p[0]= []

	def p_case(self, p):
		'''
			case : KEY_CASE expression COLON statementSequence
		'''
		p[0]={}
		p[0]['label'] = self.xtras.getNewLabel()
		p[0]['ecode'] = p[2]['code']
		p[0]['scode'] = p[4]['code']
		p[0]['place'] = p[2]['place']

	def p_whileStatement(self, p):
		'''
			whileStatement : KEY_WHILE markerWhile expression KEY_BEGIN statementSequence KEY_END
		'''
		#if (p[4]['type']!='BOOLEAN'):
		#	raise TypeError("Error at line number %d, while condition must be a boolean expression \n" %(p.lexer.lineno,))
		#TODO uncomment the above type checking call when done
		whileCode = [[self.tunnelTab.currTable.loopLabs['loop']]]
		whileCode += p[3]['code']
		whileCode += [['ifgoto', '==', p[3]['place'] , 'false' ,  self.tunnelTab.currTable.loopLabs['suf'] ]]
		whileCode += p[5]['code']
		whileCode += [['goto' , self.tunnelTab.currTable.loopLabs['loop']]]
		whileCode += [[self.tunnelTab.currTable.loopLabs['suf']]]
		p[0] = {'code': whileCode}
		self.tunnelTab.endScope()

	def p_markerWhile(self,p):
		'''
			markerWhile :
		'''
		self.tunnelTab.startScope('bb', {'id': self.xtras.getNewId()})
		loopLabel = self.xtras.getNewLabel()
		preLabel = loopLabel
		sufLabel =self.xtras.getNewLabel()
		self.tunnelTab.currTable.loopLabs['pre'] = preLabel
		self.tunnelTab.currTable.loopLabs['loop'] = loopLabel
		self.tunnelTab.currTable.loopLabs['suf'] = sufLabel

	def p_forStatement(self, p):
		'''
			forStatement : KEY_FOR markerFor LRB assignment SCOLON expression SCOLON assignment RRB KEY_BEGIN statementSequence KEY_END
		'''
		#TODO type checking of boolean in p[6]
		p[0] = {}
		forCode = p[4]['code']
		forCode += [[self.tunnelTab.currTable.loopLabs['pre']]]
		forCode += p[6]['code']
		forCode += [["ifgoto", "==", p[6]['place'] , "false" , self.tunnelTab.currTable.loopLabs['suf']]]
		forCode += p[11]['code']
		forCode += [[self.tunnelTab.currTable.loopLabs['loop']]]
		forCode += p[8]['code']
		forCode += [["goto" , self.tunnelTab.currTable.loopLabs['pre']]]
		forCode += [[self.tunnelTab.currTable.loopLabs['suf']]]
		p[0]['code'] = forCode
		self.tunnelTab.endScope()

	def p_markerFor(self,p):
		'''
			markerFor :
		'''
		self.tunnelTab.startScope('bb', {'id': self.xtras.getNewId()})
		preLabel = self.xtras.getNewLabel()
		loopLabel = self.xtras.getNewLabel()
		sufLabel =self.xtras.getNewLabel()
		self.tunnelTab.currTable.loopLabs['pre'] = preLabel
		self.tunnelTab.currTable.loopLabs['loop'] = loopLabel
		self.tunnelTab.currTable.loopLabs['suf'] = sufLabel


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
						| KEY_READ LRB designator RRB
						| KEY_READINT LRB designator RRB
						| KEY_READREAL LRB designator RRB
						| KEY_READCHAR LRB designator RRB
						| KEY_READBOOL LRB designator RRB
		'''
		p[0] = {}
		if p.slice[1].type=='KEY_WRITE':
			p[0]['code'] = p[3]['code'] + [['print' , p[3]['place']]]
		elif p.slice[1].type == 'KEY_WRITEINT':

			p[0]['code'] = p[3]['code'] + [['printint' , p[3]['place']]]
		elif p.slice[1].type == 'KEY_WRITEREAL':
			p[0]['code'] = p[3]['code'] + [['printreal' , p[3]['place']]]
		elif p.slice[1].type == 'KEY_WRITECHAR':
			p[0]['code'] = p[3]['code'] + [['printchar' , p[3]['place']]]
		elif p.slice[1].type == 'KEY_WRITEBOOL':
			p[0]['code'] = p[3]['code'] + [['printbool' , p[3]['place']]]
		elif p.slice[1].type == 'KEY_WRITELN' and len(p)==5:
			p[0]['code'] = p[3]['code'] + [['println' , p[3]['place']]]
		elif p.slice[1].type =='KEY_WRITELN':
			p[0]['code'] = [['println']]
		elif p.slice[1].type == 'KEY_READ':
			p[0]['code'] = [['read' , p[3]['place']]]
		elif p.slice[1].type == 'KEY_READINT':
			if (p[3]['kind']=='simplevar'):
				p[0]['code'] = [['readint' , p[3]['place'] ]]
			elif (p[3]['kind']=='array'):
				recode = [['readarray' , p[3]['place'] , p[3]['offset'] ]]
				p[0]['code'] = p[3]['code'] + recode
		elif p.slice[1].type  == 'KEY_READREAL':
			p[0]['code'] = [['readreal' , p[3]['place']]]
		elif p.slice[1].type  == 'KEY_READCHAR':
			p[0]['code'] = [['readchar' , p[3]['place']]]
		elif p.slice[1] == 'KEY_READBOOL':
			p[0]['code'] = [['readbool' , p[3]['place']]]


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
		# print("$$$$$$$$$$$$$$$$$$")
		self.irrrcode = self.parserObj.irrcode
		return parse_ret

if __name__=="__main__":
	parser = Parserrr()
	filename = sys.argv[1]

	accepted_types = {
		  'MULTIPLY': ('INTEGER', 'REAL', None)
		, 'PLUS': ('INTEGER', 'REAL', None)
		, 'MINUS': ('INTEGER', 'REAL', None)
		, 'DIVIDE': ('INTEGER', 'REAL', None)
		, 'LT': ('INTEGER', 'BOOLEAN')
		, 'LTEQ': ('INTEGER', 'BOOLEAN')
		, 'GT': ('INTEGER', 'BOOLEAN')
		, 'GTEQ': ('INTEGER', 'BOOLEAN')
		, 'EQUAL': ('INTEGER', 'REAL', 'BOOLEAN')
		, 'NEQUAL': ('INTEGER', 'REAL', 'BOOLEAN')
		, 'AND': ('BOOLEAN', 'BOOLEAN')
		, 'OR': ('BOOLEAN', 'BOOLEAN')
		, 'NOT' : ('BOOLEAN', 'BOOLEAN')
		, 'IS' : ()
		, 'IN' : ()
	}

	result = parser.parse_file(filename, debug = True)
