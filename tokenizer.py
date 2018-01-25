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

# some rules
t_ignore = ' \t'
t_ASSIGN = r':='
t_LTEQ = r'<='
t_GTEQ = r'>='

#t_VAL_INTEGER = r'[0-9]+'
#t_VAL_REAL = r'[0-9]+\.[0-9]+'
t_VAL_INTEGER = r'[0-9][0-9A-F]*H|[0-9]+'
t_VAL_REAL = r'[0-9]+\.[0-9]+(E|D)[+]?[0-9]+|[0-9]+\.[0-9]+(E|D)[-]?[0-9]+|[0-9]+\.[0-9]+'

#t_VAL_BOOLEAN = r'TRUE|FALSE'
t_DOT_DOT = r'\.\.'
t_VAL_STRING = r'\".*?\"'

literals = "+-*/~&.,;|([{}]):><#=^"
#t_VAL_CHAR = r'(L)?\'(.|\n)\''
   
tokens = ['ASSIGN', 'LTEQ', 'GTEQ', 'IDENT', 'VAL_INTEGER', 'VAL_REAL',
 'VAL_STRING', 'VAL_BOOLEAN', 'VAL_CHAR', 'DOT_DOT' ] + list(reserved.values())

def t_IDENT(t):
	r'[a-zA-Z]([a-zA-Z0-9])*'
	t.type = reserved.get(t.value,'IDENT')
	if t.value == 'TRUE' or t.value == 'FALSE':
		t.type = 'VAL_BOOLEAN'
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
