
reserved = {
	'ABS' : 'KEY_ABS',                                 # Absolute
	'ARRAY' : 'KEY_ARRAY',                             # declare array
	'BEGIN' : 'KEY_BEGIN',                             # start block
	'BOOLEAN' : 'KEY_BOOLEAN',                         # var type
    'BREAK' : 'KEY_BREAK',                             # break loop
	'CASE' : 'KEY_CASE',                               # switch case
	'CHAR' : 'KEY_CHAR',                               # declare array
	'CHR' : 'KEY_CHR',                                 # ascii to char
	'CONST' : 'KEY_CONST',                             # define constant
    'CONTINUE' : 'KEY_CONTINUE',                       # continue loop
	'DO' : 'KEY_DO',                                   # do while
	'ELSE' : 'KEY_ELSE',                               # if else
	'ELSEIF' : 'KEY_ELSEIF',                             # if else
	'END' : 'KEY_END',                                 # end block
	'EXIT' : 'KEY_EXIT',                               # end program
	'FCLOSE' : 'KEY_FCLOSE',                           # close file
	'FOPEN' : 'KEY_FOPEN',                             # open file
	'FOR' : 'KEY_FOR',                                 # for loop
	'FPRINTF' : 'KEY_FPRINTF',                         # file write
	'FREAD' : 'KEY_FREAD',                             # file read
	'IF' : 'KEY_IF',                                   # if else
	'IN' : 'KEY_IN',                                   # set 
	'INTEGER' : 'KEY_INTEGER',                         # data type
	'IS' : 'KEY_IS',                                   # check type
	'MODULE' : 'KEY_MODULE',                           # start keyword
	'NEW' : 'KEY_NEW',                                 # new object/record
	'NIL' : 'KEY_NIL',                                 # nil set
	'OF' : 'KEY_OF',                                   # array declare keyword
	'ORD' : 'KEY_ORD',                                 # num to char
	'POINTER' : 'KEY_POINTER',                         # pointer
	'PROCEDURE' : 'KEY_PROCEDURE',                     # function
	'READ' : 'KEY_READ',                               # get input
	'REAL' : 'KEY_REAL',                               # data type
	'RECORD' : 'KEY_RECORD',                           # data structure
	'RETURN' : 'KEY_RETURN',                           # return value
	'SET' : 'KEY_SET',                                 # data type
    'STRING' : 'KEY_STRING',
    'SWITCH' : 'KEY_SWITCH',                           # switch case
	'THEN' : 'KEY_THEN',                               # if else
	'TO' : 'KEY_TO',                                   # pointer to
	'TYPE' : 'KEY_TYPE',                               # data type
	'VAR' : 'KEY_VAR',                                 # declare variable
	'WHILE' : 'KEY_WHILE',                             # while/do while loop
	'WRITE' : 'KEY_WRITE',                             # write output
	'WRITELN' : 'KEY_WRITELN'                          # outuput in new line
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
        t_NOT = r'!'

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
        tokens = ['ASSIGN', 'LT' , 'GT' , 'PLUS' , 'MINUS' , 'MULTIPLY' , 'DIVIDE' , 'MODULUS' , 'OR' , 'NOT', 'AND' , 'EQUAL' ,  'NEQUAL' , 'DOT' , 'COMMA' , 'SCOLON' , 'LSB' , 'RSB' , 'LRB' , 'RRB' , 'LCB' , 'RCB' , 'LTEQ', 'GTEQ', 'IDENT', 'VINTEGER', 'VREAL', 'VSTRING', 'VBOOLEAN', 'VCHAR' , 'COLON' ] + list(reserved.values())
        
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
