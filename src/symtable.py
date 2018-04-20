import sys

typeSizeAllocation = {}
typeSizeAllocation.update({'INTEGER': 4, 'CHAR': 1, 'BOOLEAN': 1, 'REAL': 8})
typeSizeAllocation.update({'FILE': None, 'STRING': None})

divList = ['bb', 'func']
kindList = ['simplevar', 'array', 'pointer', 'record', 'func', 'const']

class SymTabEntry(object):
	def __init__(self, lex, vtype, kind, offset=None, addr=None, size=None, placist=None):
		self.lex = lex
		self.kind = kind
		self.vtype = vtype
		self.size = size
		self.placist = placist
		self.offset = offset
		self.addr = addr

	#TODO write correct following function
	#def updEntry(self, addOns, updAddOns):
		#self.addOns = updAddOns
		#TODO remove the following two functions

	def __repr__(self):
		return "{}".format(self.lex)
		# return "lex: {}, kind: {}, type: {}, placist: {}, offset: {}, addr: {}".format(self.lex, self.kind, self.vtype, self.placist, self.offset, self.addr)

	def __str__(self):
		return self.lex

class SymTab(object):

	def __init__(self, div, addOns, parent):
		self.parent = parent
		self.addOns = addOns
		self.div = div
		self.varsHere = {}
		self.children = {}
		self.temps = {}
		self.loopLabs = {'pre': None, 'loop': None, 'suf': None}
		self.offsTab = 0

	def addEntry(self, lex, vtype, kind, offset=None, placist=None):
		if kind=='simplevar':
			if vtype in typeSizeAllocation.keys():
				size = typeSizeAllocation[vtype]
			else:
				size = None
		elif (kind=='pointer' or kind=='const'):
			size = 4
		else:
			size = None
		if (offset!=None):
			addr = str(offset)+'($fp)'
		else:
			addr = lex
		self.varsHere[lex] = SymTabEntry(lex, vtype, kind, offset, addr, size, placist)
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
		# print(self.addOns)
		# print(self.addOns['id'])
		if len(self.addOns) > 0:
			print("## Attributes ##")
			for k,v in self.addOns.items():
				print(k + " -> " + str(v))
	## print vars
		if len(self.varsHere) > 0:
			print("## Variables ##")
			for k,v in self.varsHere.items():
				print(k + " -> " + repr(v))
			# print("########")

class tunnelTable(object):
	def __init__(self):
		self.rootTable = SymTab("program", {'id': "main"}, None)
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

	def getVariables(self,Table=None):
		if(Table==None):
			Table=self.rootTable
		var = list(Table.varsHere.values())
		var = var + list(Table.temps.values())
		for child in list(Table.children.values()):
			var = var + self.getVariables(child)
		return var

	def printfull(self, Table):
		if(Table == None):
			iterTable = self.currTable
		else:
			iterTable = Table
		queryRes = iterTable.printMe()
		if (iterTable.parent == None):
			return
		else:
			parTable = iterTable.parent
			self.printfull(parTable)
			return

	def queryProc(self,lex):
		# print("###############")
		# print(lex)
		# print("###############")
		try:
			proc = self.rootTable.children[lex].addOns
			return proc
		except KeyError:
			return None

	def addEntry(self, lex, vtype, kind, offset=0, placist=None):
		return self.currTable.addEntry(lex, vtype, kind, offset, placist)

	def startScope(self, div, addOns):
		freshTable = SymTab(div, addOns, self.currTable)
		# print("#######")
		# print(addOns)
		# print("#######")
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

	def getNewTemp(self, vtype, kind, tunnelTab):
		self.tempCount += 1
		if kind=='simplevar':
			if vtype in typeSizeAllocation.keys():
				size = typeSizeAllocation[vtype]
			else:
				size = None
		elif (kind=='pointer' or kind=='const'):
			size = 4
		else:
			size = None
		tempObj = SymTabEntry("_t"+str(self.tempCount-1), vtype, kind, None, "_t"+str(self.tempCount-1), size, None)
		if(vtype == 'STRING'):
			tunnelTab.rootTable.temps["_t"+str(self.tempCount-1)] = tempObj
		else:
			tunnelTab.currTable.temps["_t"+str(self.tempCount-1)] = tempObj
		# print(self.tempCount-1)
		# print(tunnelTab.currTable.temps)
		return tempObj

	def getNewLabel(self):
		self.labelCount += 1
		return "_L" + str(self.labelCount-1)

	def getNewId(self):
		self.idCount += 1
		return "_id" + str(self.idCount-1)
