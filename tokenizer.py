
reserved = {
	'ABS' : 'ABS',
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

class tokenizer(object):
        # Operators
        t_ignore = ' \t'
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

        # BOOLEAN
        t_OR = r'\|'
        t_AND = r'&'

        # Delimiters
        t_COMMA = r','
        t_SCOLON = r';'
        t_COLON = r':'
        t_LSB = r'\['
        t_RSB = r'\]'
        t_LRB = r'\('
        t_RRB = r'\)'
        t_LCB = r'{'
        t_RCB = r'}'


        t_VINTEGER = r'[0-9]+'
        t_VREAL = r'[0-9]+\.[0-9]+'
        t_VBOOLEAN = r'TRUE|FALSE'
        t_VSTRING = r'\".*?\"'
        t_VCHAR = r'(L)?\'(.|\n)\''
        tokens = ['ASSIGN', 'LT' , 'GT' , 'PLUS' , 'MINUS' , 'MULTIPLY' , 'DIVIDE' , 'MODULUS' , 'OR' , 'AND' , 'EQUAL' ,  'NEQUAL' , 'DOT' , 'COMMA' , 'SCOLON' , 'LSB' , 'RSB' , 'LRB' , 'RRB' , 'LCB' , 'RCB' , 'LTEQ', 'GTEQ', 'IDENT', 'VINTEGER', 'VREAL', 'VSTRING', 'VBOOLEAN', 'VCHAR', 'DOT_DOT' , 'COLON' ] + list(reserved.values())
        def t_IDENT(self, t):
                r'[a-zA-Z]([a-zA-Z0-9])*'
                t.type = reserved.get(t.value,'IDENT')
                return t

        def t_comment(self, t):
                r'(\(\*(.|\n)*?\*\))'
                t.lexer.lineno += t.value.count('\n')
                pass
        
        def t_newline(self, t):
                r'\n+'
                t.lexer.lineno += len(t.value)

        def t_error(self, t):
                last_cr = t.lexer.lexdata.rfind('\n',0,t.lexpos)
                if (last_cr < 0) :
                        last_cr = -1		
                else :
                        last_cr = last_cr 
                columnNo = (t.lexpos - last_cr)
                print ("Illegal character",t.value[0],"at line : ",t.lexer.lineno,"column",columnNo,": Skipping")
                t.lexer.skip(1)
