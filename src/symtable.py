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
        self.children = {}

	def addEntry(self, lex, vtype, kind):
        if vtype in typeSizeAllocation.keys():
            size = typeSizeAllocation[ltype]
        else:
            size = None
        self.varsHere[lex] = SymTabEntry(lex, kind, vtype, size)
        return self.varsHere[lex]

    def queryEnt(self, lex):
        if lex in self.varsHere:
            return self.varsHere[lexeme]
        return None

class tunnelTable(object):
    def __init__(self):
        self.rootTable = SymTab("program", None, {})
		self.currTable = self.rootTable
        self.labelCount = 1

    def newLabel(self):
        self.labelCount += 1
        return "L" + str(self.labelCount - 1)

    def queryEnt(self, lex):
        iterTable = self.currTable
        queryRes = iterTable.queryEnt(lex)
        if queryRes == None:
			parTable = iterTable.parent
        	if (table.parent == None):
            	return None
			else:
				return self.queryEnt(lexeme, table.parent)
		else:
			return queryRes

    def addEntry(self, lex, vtype, kind):
        return self.currTable.addEntry(lex, vtype, kind)

    def startScope(self, div, addOns):
        freshTable = SymTab(div, self.currentTable, addOns)
        self.currentTable.children[addOns['id']] = freshTable
        self.currentTable = freshTable
        return self.currentTable

    def endScope(self):
        self.currentTable = self.currentTable.parent
