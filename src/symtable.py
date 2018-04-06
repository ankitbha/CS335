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

	def __repr__(self):
		return "kind: {}, type: {}".format(self.kind, self.vtype)

	def __str__(self):
		return self.lex

class SymTab(object):

	def __init__(self, div, addOns, parent):
		self.parent = parent
		self.addOns = addOns
		self.div = div
		self.varsHere = {}
		self.children = {}
		self.loopLabs = {'pre': None, 'loop': None, 'suf': None}

	def addEntry(self, lex, vtype, kind):
		if vtype in typeSizeAllocation.keys():
			size = typeSizeAllocation[ltype]
		else:
			size = None
		self.varsHere[lex] = SymTabEntry(lex, vtype, kind, size)
		return self.varsHere[lex]

	def queryEnt(self, lex):
		if lex in self.varsHere:
			return self.varsHere[lex]
		return None

	def printMe(self):
	## print attributes
		if len(self.addOns) > 0:
			print("## Attributes ##")
			for k,v in self.addOns.items():
				print(k + " -> " + str(v))
	## print vars
		if len(self.varsHere) > 0:
			print("## Variables ##")
			for k,v in self.varsHere.items():
				print(k + " -> " + repr(v))


class tunnelTable(object):
	def __init__(self):
		self.rootTable = SymTab("program", {}, None)
		self.currTable = self.rootTable

	def queryEnt(self, lex, Table):
		if(Table == None):
			iterTable = self.currTable
		else:
			iterTable = Table	
		queryRes = iterTable.queryEnt(lex)
		if queryRes == None:
			
			if (iterTable.parent == None):
				return None
			else:
				parTable = iterTable.parent
				return self.queryEnt(lex, parTable)
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
