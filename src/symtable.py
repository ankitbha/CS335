import sys

typeSizeAllocation = {}
typeSizeAllocation.update({'INTEGER': 4, 'CHAR': 1, 'BOOLEAN': 1, 'REAL': 8})
typeSizeAllocation.update({'FILE': None, 'STRING': None})

divList = ['bb', 'func']

class SymTabEntry(object):
	def __init__(self, lex, vtype, kind, size=None):
		self.lex = lex
		self.kind = kind
		self.vtype = vtype
		self.size = size

	def updEntry(self, addOns, updAddOns):
		self.addOns = updAddOns

class SymTab(object):

	def __init__(self, div, addOns, parent):
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
		self.varsHere[lex] = SymTabEntry(lex, vtype, kind, size)
		return self.varsHere[lex]

	def queryEnt(self, lex):
		if lex in self.varsHere:
			return self.varsHere[lexeme]
		return None

class tunnelTable(object):
	def __init__(self):
		self.rootTable = SymTab("program", {}, None)
		self.currTable = self.rootTable

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
		freshTable = SymTab(div, addOns, self.currTable)
		self.currTable.children[addOns['id']] = freshTable
		self.currTable = freshTable
		return self.currTable

	def endScope(self):
		self.currTable = self.currTable.parent

class xtraNeeds(object):
	def __init__(self):
		self.tempCount = 0
		self.labelCount = 1
		self.idCount = 1

	def getNewTemp(self, vtype, kind):
		self.tempCount += 1
		return SymTabEntry("_t"+str(self.tempCount-1), vtype, kind)

	def getNewLabel(self):
		self.labelCount += 1
		return "L" + str(self.labelCount-1)

	def getNewId(self):
		self.idCount += 1
		return "_id" + str(self.idCount-1)