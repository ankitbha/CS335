###########################################
# Oberon Compiler Project
# CS 335: Principles Of Compiler Design
# Group - 5
# Ankit Kumar, Rahul Varma, Raghubansh Mani
# Suralkar Vijay Suresh, Vikas Wasiya
###########################################
import lex

# reserved keywords
reserved = {
	'ABS' : 'ABS',
	'AND' : 'AND',
	'ARRAY' : 'ARRAY',
	'BEGIN' : 'BEGIN',
	'BOOLEAN' : 'BOOLEAN',
	'CASE' : 'CASE',
	'CAP' : 'CAP',
	'CHAR' : 'CHAR',
	'CHR' : 'CHR',
	'CONST' : 'CONST',
	'DIV' : 'DIV',
	'DO' : 'DO',
	'ELSE' : 'ELSE',
	'ELSIF' : 'ELSIF',
	'END' : 'END',
	'EXIT' : 'EXIT',
	'FCLOSE' : 'FCLOSE',
	'FOPEN' : 'FOPEN',
	'FOR' : 'FOR',
	'FPRINTF' : 'FPRINTF',
	'FREAD' : 'FREAD',
	'IF' : 'IF',
	'IN' : 'IN',
	'INTEGER' : 'INTEGER',	
	'IS' : 'IS',
	'LEN' : 'LEN',
	'LOOP' : 'LOOP',
	'MOD' : 'MOD',
	'MODULE' : 'MODULE',
	'NEW' : 'NEW',
	'NIL' : 'NIL',
	'NOT' : 'NOT',
	'ODD' : 'ODD',
	'OF' : 'OF',
	'OR' : 'OR',
	'ORD' : 'ORD',	
	'POINTER' : 'POINTER',
	'PROCEDURE' : 'PROCEDURE',
	'READ' : 'READ',	
	'REAL' : 'REAL',
	'RECORD' : 'RECORD',
	'REPEAT' : 'REPEAT',
	'RETURN' : 'RETURN',
	'SET' : 'SET',
	'THEN' : 'THEN',
	'TO' : 'TO',
	'TYPE' : 'TYPE',
	'UNTIL' : 'UNTIL',
	'VAR' : 'VAR',
	'WHILE' : 'WHILE',
	'WRITE' : 'WRITE',
	'WRITELN' : 'WRITELN'
}

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULUS = r'%'
t_DOT = r'\.'

# Relation
t_ASSIGN = r':='
t_EQUAL = r'='
t_NEQUAL = r'!='
t_LT = r'<'
t_GT = r'>'
t_LTEQ = r'<='
t_GTEQ = r'>='



#t_ignore = ' \t'
# BOOLEAN
t_OR = r'\|'
t_AND = r'&'
t_IN = r'IN'
t_IS = r'IS'

# Delimiters
t_COMMA = r','
t_SCOLON = r';'
t_LSB = r'\['
t_RSB = r'\]'
t_LRB = r'\('
t_RRB = r'\)'
t_LCB = r'{'
t_RCB = r'}'


t_VAL_INTEGER = r'[0-9]+'
t_VAL_REAL = r'[0-9]+\.[0-9]+'
t_VAL_BOOLEAN = r'TRUE|FALSE'
#t_DOT_DOT = r'\.\.'
t_VAL_STRING = r'\".*?\"'

#literals = "+-*/~&.,;|([{}]):><#=^"
#t_VAL_CHAR = r'(L)?\'(.|\n)\''
   
tokens = ['ASSIGN', 'LT' , 'GT' , 'PLUS' , 'MINUS' , 'MUULTIPLY' , 'DIVIDE' , 'MODULUS' , 'OR' , 'AND' , 'EQUAL' , 'IN' , 'IS' , 'NEQUAL' , 'DOT' , 'COMMA' , 'SCOLON' , 'LSB' , 'RSB' , 'LRB' , 'RRB' , 'LCB' , 'RCB' , 'LTEQ', 'GTEQ', 'IDENT', 'VAL_INTEGER', 'VAL_REAL', 'VAL_STRING', 'VAL_BOOLEAN', 'VAL_CHAR', 'DOT_DOT' ] + list(reserved.values())

def t_IDENT(t):
	r'[a-zA-Z]([a-zA-Z0-9])*'
	t.type = reserved.get(t.value,'IDENT')
	#if t.value == 'TRUE' or t.value == 'FALSE':
		#t.type = 'VAL_BOOLEAN'
	return t

#t_ignore_comment = r'(\(\*(.|\n)*?\*\))'
def t_comment(t):
	r'(\(\*(.|\n)*?\*\))'
	t.lexer.lineno += t.value.count('\n')
	pass #ignore a comment line

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# error handling : skip unwanted charater after printing a message
def t_error(t):
	last_cr = t.lexer.lexdata.rfind('\n',0,t.lexpos)
	if (last_cr < 0) :
		last_cr = -1		
	else :
		last_cr = last_cr 
	columnNo = (t.lexpos - last_cr)
	print "Illegal character",t.value[0],"at line : ",t.lexer.lineno,"column",columnNo,": Skipping"
	t.lexer.skip(1)

lexer = lex.lex()

# if called from main check the working of this lexer
if __name__ == '__main__' :
	lex.runmain()
