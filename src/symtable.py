import sys

typeSizeAllocation = {}
typeSizeAllocation({'int': 4, 'char': 1, 'bool': 1, 'real': 8})
typeSizeAllocation({'file': None, 'str': None})

class SymTabEntry(object):
    def __init__(self, lex, kind, vtype, size=None):
        self.lex = lex
        self.kind = kind
        self.vtype = vtype
        self.size = size

    def updEntry(self, attr, newAttr):
        self.attr = newAttr

class SymTab(object):

	def __init__(self, div, parent=None, addOns):
        self.parent = parent
        self.addOns = addOns
		self.div = div
        self.varsHere = {}
        self.children = []

	def insert(self, lex, vtype, kind):
        if vtype in typeSizeAllocation.keys():
            size = typeSizeAllocation[ltype]
        else:
            size = None
        self.varsHere[lex] = SymTabEntry(lex, kind, vtype, size)
        return self.varsHere[lex]

    def lookup(self, lex):
        if lex in self.varsHere:
            return self.varsHere[lexeme]
        return None
