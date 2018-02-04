
reserved = {
	'ABS' : 'KEY_ABS',
	'ARRAY' : 'KEY_ARRAY',
	'BEGIN' : 'KEY_BEGIN',
	'BOOLEAN' : 'KEY_BOOLEAN',
	'CASE' : 'KEY_CASE',
	'CAP' : 'KEY_CAP',
	'CHAR' : 'KEY_CHAR',
	'CHR' : 'KEY_CHR',
	'CONST' : 'KEY_CONST',
	'DIV' : 'KEY_DIV',
	'DO' : 'KEY_DO',
	'ELSE' : 'KEY_ELSE',
	'ELSIF' : 'KEY_ELSIF',
	'END' : 'KEY_END',
	'EXIT' : 'KEY_EXIT',
	'FCLOSE' : 'KEY_FCLOSE',
	'FOPEN' : 'KEY_FOPEN',
	'FOR' : 'KEY_FOR',
	'FPRINTF' : 'KEY_FPRINTF',
	'FREAD' : 'KEY_FREAD',
	'IF' : 'KEY_IF',
	'IN' : 'KEY_IN',
	'INTEGER' : 'KEY_INTEGER',
	'IS' : 'KEY_IS',
	'LEN' : 'KEY_LEN',
	'LOOP' : 'KEY_LOOP',
	'MOD' : 'KEY_MOD',
	'MODULE' : 'KEY_MODULE',
	'NEW' : 'KEY_NEW',
	'NIL' : 'KEY_NIL',
	'NOT' : 'KEY_NOT',
	'ODD' : 'KEY_ODD',
	'OF' : 'KEY_OF',
	'ORD' : 'KEY_ORD',
	'POINTER' : 'KEY_POINTER',
	'PROCEDURE' : 'KEY_PROCEDURE',
	'READ' : 'KEY_READ',
	'REAL' : 'KEY_REAL',
	'RECORD' : 'KEY_RECORD',
	'REPEAT' : 'KEY_REPEAT',
	'RETURN' : 'KEY_RETURN',
	'SET' : 'KEY_SET',
	'THEN' : 'KEY_THEN',
	'TO' : 'KEY_TO',
	'TYPE' : 'KEY_TYPE',
	'UNTIL' : 'KEY_UNTIL',
	'VAR' : 'KEY_VAR',
	'WHILE' : 'KEY_WHILE',
	'WRITE' : 'KEY_WRITE',
	'WRITELN' : 'KEY_WRITELN'
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
        t_VSTRING = r'\"([^\\]|(\\.))*?\"'
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

        def t_newline2(self, t):
                r'(\r\n)+'
                t.lexer.lineno += len(t.value) / 2

        def t_error(self, t):
                print ("Illegal character",t.value[0],"at line : ",t.lexer.lineno,": Skipping")
                t.lexer.skip(1)
