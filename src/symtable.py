import sys

typeSizeAllocation = {}
typeSizeAllocation.update({'INTEGER': 4, 'CHAR': 1, 'BOOLEAN': 1, 'REAL': 8})
typeSizeAllocation.update({'FILE': None, 'STRING': None})

divList = ['bb', 'func']
kindList = ['simplevar', 'array', 'pointer', 'record']

class SymTabEntry(object):
	def __init__(self, lex, vtype, kind, size=None, placist=None):
		self.lex = lex
		self.kind = kind
		self.vtype = vtype
		self.size = size
		self.placist = placist

	#TODO write correct following function
	#def updEntry(self, addOns, updAddOns):
		#self.addOns = updAddOns
		#TODO remove the following two functions

	def __repr__(self):
		return "{}".format(self.lex)
		# return "lex: {}, kind: {}, type: {}, size: {}".format(self.lex, self.kind, self.vtype, self.size)

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

	def addEntry(self, lex, vtype, kind, placist=None):
		if vtype in typeSizeAllocation.keys():
			size = typeSizeAllocation[vtype]
		else:
			size = None
		self.varsHere[lex] = SymTabEntry(lex, vtype, kind, size, placist)
		return self.varsHere[lex]

	def queryEnt(self, lex):
		if lex in self.varsHere:
			return self.varsHere[lex]
		return None

	# def queryProc(self,lex):
	# 	for child in self.children:
	# 		self.currTable.children[addOns['id']] = freshTable
	# 	if lex

#TODO remove the following function
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
	def queryProc(self,lex):
		# print("###############")
		# print(lex)
		# print("###############")
		try:
			proc = self.rootTable.children[lex].addOns
			return proc
		except KeyError:
			return None

	def addEntry(self, lex, vtype, kind, placist=None):
		return self.currTable.addEntry(lex, vtype, kind, placist)

	def startScope(self, div, addOns):
		freshTable = SymTab(div, addOns, self.currTable)
		self.currTable.children[addOns['id']] = freshTable
		self.currTable = freshTable
		return self.currTable

	def endScope(self):
		self.currTable = self.currTable.parent

	def queryLabs(self, labName, tab):
		if(tab == None):
			iterTable = self.currTable
		else:
			iterTable = tab
		lab = iterTable.loopLabs[labName]
		if lab == None:
			if (iterTable.parent == None):
				return None
			else:
				parTable = iterTable.parent
				return self.queryLabs(labName, parTable)
		else:
			return lab

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
		return "_L" + str(self.labelCount-1)

	def getNewId(self):
		self.idCount += 1
		return "_id" + str(self.idCount-1)
