import sys
import math
import copy
import inspect
#import symtable

class SymClass(object):
	def __init__(self, lexeme, typ):
		self.lexeme = lexeme
		self. typ = typ

#class CodeGen:
# def reg_init():
ex=False
vreg = {"$v0":None, "$v1":None}
areg = {"$a0":None, "$a1":None, "$a2":None, "$a3":None}
zreg = {"$zero":None}
treg = {"$t0":None, "$t1":None, "$t2":None, "$t3":None, "$t4":None, "$t5":None, "$t6":None, "$t7":None, "$t8":None, "$t9":None}
sreg = {"$s0":None, "$s1":None, "$s2":None, "$s3":None, "$s4":None, "$s5":None, "$s6":None, "$s7":None}
preg = { "$gp" : None, "$sp" : None, "$fp" : None, "ra" : None }
kreg = { "$k0" : None, "$k1" : None }
reg_float = dict()
for i in range(1,24):  reg_float.update({ '$f' + str(i) : [] })
reg_norm = {**treg, **sreg}

unused_reg_norm = list(reg_norm.keys())
used_reg_norm = []
unused_reg_float = list(reg_float.keys())
used_reg_float = []


	#regTuple = ()
	#regDes = {}
	#regDes = regDes.fromkeys(list(regTuple))

def check_reg(self, varName):
	pass
# basically check the register holding the given variable "var" and return it as string form. It will need symbol table implementation.
def getReg(varObj, numLine):
	global acode
	print("called getreg")
	if varObj.typ in ["float", "double"]:
		for i in reg_float.keys():
			if (reg_float[i]==varObj):
				return i

		if unused_reg_float:
			reg = unused_reg_float[0]
			unused_reg_float.remove(reg)
			used_reg_float.append(reg)
			reg_float[reg] = [varObj]
			addrDesc[varObj] = reg
			return reg


		else:
			forNextUse=nextUseTable[numLine]
			tempFarthest=None
			#forNextUse should be a dictionary, so nextUseTable must also be a
			#dictionary with keys as line numbers and value as another dictionary
			#with key being variable names and values being nextUselineNo
			for var in forNextUse.keys():
				if (tempFarthest==None):
					tempFarthest=var
				elif (forNextUse[var]>forNextUse[tempFarthest]):
					tempFarthest=var
				else:
					continue
			for spillReg in reg_float.keys():
				if reg_float[spillReg]==tempFarthest:
					break

			#write something like
			#    assembly = assembly + "movl " + regspill + ", " + var + "\n"
			# acode = acode + "lw " + spillReg + ", " + addrDesc[reg_norm[spillReg]] + "\n"
			addrDesc[reg_float[spillReg]] = "MEM"
			reg_float[spillReg] = [varObj]
			addrDesc[varObj] = spillReg
			return spillReg

	else:
		#regExist=False
		#emptyReg=None
		for i in reg_norm.keys():
			if (reg_norm[i]==varObj):
				#regExist = True
				return i
			#if(emptyReg==None and !regExist):


		if unused_reg_norm:
			reg = unused_reg_norm[0]
			unused_reg_norm.remove(reg)
			used_reg_norm.append(reg)
			reg_norm[reg] = varObj
			addrDesc[varObj] = reg
			return reg


		else:
			forNextUse=nextUseTable[numLine]
			tempFarthest=None
			#forNextUse should be a dictionary, so nextUseTable must also be a
			#dictionary with keys as line numbers and value as another dictionary
			#with key being variable names and values being nextUselineNo
			for var in forNextUse.keys():
				if (tempFarthest==None):
					tempFarthest=var
				elif (forNextUse[var]>forNextUse[tempFarthest]):
					tempFarthest=var
				else:
					continue
			for spillReg in reg_norm.keys():
				if reg_norm[spillReg]==tempFarthest:
					break

			#write something like
			acode = acode + "lw " + spillReg + ", " + addrDesc[reg_norm[spillReg]] + "\n"
			addrDesc[reg_norm[spillReg]] = "MEM"
			reg_norm[spillReg] = [varObj]
			addrDesc[varObj] = spillReg
	return spillReg

def isInt(s):
	if (isinstance(s, SymClass)):
		return False
	else:
		return True

def RepresentsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


acode="# Generated Code \n"
def translate(line):
	global acode
	global labels
	global ex
	#print(acode)
	#acode = acode + "# Generated Code \n"
	lineno = int(line[0])
	op = line[1]
	# Generating assembly code if the tac is a mathematical operation
	#print(op)
	
	if op in mathop:
		#print(op)
		ans = line[2]
		#print(ans)
		num1 = line[3]
		num2 = line[4]
		# Addition
		if op == '+':
			#print("yes")
			if isInt(num1) and isInt(num2):
				#print("yes")
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)+int(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2)
				
				acode = acode + "\tadd " + reg + ", " + addr2 +", $zero" + "\n"
				
				acode = acode + "\taddi " + reg + ", " + reg + ", " +num1 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1, lineno)
				acode = acode + "\tadd " + reg + ", " + addr1 +", $zero" + "\n"
				
				acode = acode + "\taddi " + reg + ", " + reg + ", " + num2 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1, lineno)
				if(addr2 == "MEM"):
					addr1 = getReg(num1, lineno)
				
				acode = acode + "\tadd " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register


		elif op == '-':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)-int(num2)) + "\n"
				addrDesc[ans] = reg

				#update register
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				
				acode = acode + "\tsub " + reg  +", $zero, " + addr2 + "\n"
				
				acode = acode + "\taddi " + reg + ", " + reg + ", " + num1 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tsub " + reg + ", $zero, " + num2 + "\n"
				acode = acode + "\tadd " + reg + ", " + reg + ", " + addr1 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr1 = getReg(num1,lineno)
				
				acode = acode + "\tsub " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register
		elif op == '*':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)*int(num2)) + "\n"
				addrDesc[ans] = reg

				#update register
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				
				acode = acode + "\tmul " + reg + ", " + reg + ", " + addr2 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tmul " + reg + ", " + reg + ", " + addr1 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr1 = getReg(num1,lineno)
				
				acode = acode + "\tmul " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register

		# Division
		elif op == '/':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)/int(num2)) + "\n"
				addrDesc[ans] = reg
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				
				acode = acode + "\tdiv " + reg + ", " + reg + ", " + addr2 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tdiv " + reg + ", " + addr1 + ", " + reg  + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr1 = getReg(num1,lineno,lineno)
				
				acode = acode + "\tdiv " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register

		# Modulus
		elif op == '%':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)%int(num2)) + "\n"
				addrDesc[ans] = reg

				#update register
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				
				acode = acode + "\trem " + reg + ", " + reg + ", " + addr2 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\trem " + reg + ", " + addr1 + ", " + reg  + "\n"
				addrDesc[ans] = reg


			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr1 = getReg(num1,lineno)
				
				acode = acode + "\trem " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

	elif op == "goto":
	# 	# Add code to write all the variables to the memory
	 	l = line[2]
	 	acode = acode + "\tj " + label[int(l)] +"\n"
	
	elif op == "ifgoto":
		#4, ifgoto, <=, a, 50, 2
		rel = line[2]
		num1 = line[3]
		num2 = line[4]
		l = line[5]

		if isInt(num1) and isInt(num2):
			if(rel == "<="):
				if(int(num1) <= int(num2)):
					acode = acode + "\tj " + labels[int(l)] +"\n"

			if(rel == ">="):
				if(int(num1) >= int(num2)):
					acode = acode + "\tj " + labels[int(l)] +"\n"
				
			if(rel == "=="):
				if(int(num1) == int(num2)):
					acode = acode + "\tj " + labels[int(l)] +"\n"
				
			if(rel == ">"):
				if(int(num1) > int(num2)):
					acode = acode + "\tj " + labels[int(l)] +"\n"
				
			if(rel == "<"):
				if(int(num1) < int(num2)):
					acode = acode + "\tj " + labels[int(l)] +"\n"
				
			if(rel == "!="):
				if(int(num1) != int(num2)):
					acode = acode + "\tj " + labels[int(l)] +"\n"

		elif isInt(num1) and not isInt(num2):
			print("yes2")
			addr2 = addrDesc[num2]
			if(addr2 == "MEM"):
				addr2 = getReg(num2,lineno)
				
			if(rel == "<="):
				acode = acode + "\tbge " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"
				
			if(rel == ">="):
				acode = acode + "\tble " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"

				
			if(rel == "=="):
				acode = acode + "\tbeq " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"
				
			if(rel == ">"):
				acode = acode + "\tblt " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"
				
			if(rel == "<"):
				acode = acode + "\tbgt " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"
				
			if(rel == "!="):
				acode = acode + "\tbne " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"
		
		elif not isInt(num1) and isInt(num2):
			#bge Rsrc1, Src2, label
			print("yes3")
			addr1 = addrDesc[num1]
			if(addr1 == "MEM"):
				addr1 = getReg(num1,lineno)
				
			if(rel == "<="):
				acode = acode + "\tble " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"
				
			if(rel == ">="):
				acode = acode + "\tbge " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

			if(rel == "=="):
				acode = acode + "\tbeq " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"
				
			if(rel == ">"):
				acode = acode + "\tbgt " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"
				
			if(rel == "<"):
				acode = acode + "\tblt " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"
				
			if(rel == "!="):
				acode = acode + "\tbne " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

		elif not isInt(num1) and not isInt(num2):
			#bge Rsrc1, Src2, label
			print("yes4")
			addr1 = addrDesc[num1]
			if(addr1 == "MEM"):
				addr1 = getReg(num1,lineno)
			
			addr2 = addrDesc[num2]
			if(addr2 == "MEM"):
				addr2 = getReg(num2,lineno)
				
			if(rel == "<="):
				acode = acode + "\tble " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"
				
			if(rel == ">="):
				acode = acode + "\tbge " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"

			if(rel == "=="):
				acode = acode + "\tbeq " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"
				
			if(rel == ">"):
				acode = acode + "\tbgt " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"
				
			if(rel == "<"):
				acode = acode + "\tblt " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"
				
			if(rel == "!="):
				acode = acode + "\tbne " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"
	if op=="=":
		#move Rdest, Rsrc
		#=, a, 2
		num1=line[2]
		addr1 = addrDesc[num1]
		if(addr1 == "MEM"):
			addr1 = getReg(num1,lineno)
		num2=line[3]
		if isInt(num2):
			acode=acode+"\tli "+ addr1 + ", " + num2 + "\n"
		else:
			addr2 = addrDesc[num2]
			if(addr2 == "MEM"):
				addr2 = getReg(num2,lineno)
			acode = acode + "\tmove" + addr1 + ", " + addr2 + "\n" 
	if op=="printint":
		#8, print, a
		ans=line[2];
		addr1 = addrDesc[ans]
		if(addr1 == "MEM"):
			addr1 = getReg(ans,lineno)
		acode = acode +"\tli $v0, 0\n"
		acode = acode +"\tmove, $v0, " + addr1 + "\n"
		acode = acode +"\tsyscall\n"

	if op=="scanint":
		#8, scanint, a
		ans=line[2];
		addr1 = addrDesc[ans]
		if(addr1 == "MEM"):
			addr1 = getReg(ans,lineno)
		acode = acode +"\tli $v0, 5\n"
		acode = acode +"\tsyscall\n"
		acode = acode +"\tmove, "+ addr1 + " ,$v0" + "\n"
	if op=="call":
		l=line[2]
		acode = acode + "\tjal " + l.lexeme +"\n"
	if op=="return":
		if(ex==False):
			acode = acode + "\tj exit\n"
			ex=True
		else:
			acode = acode + "\tjal $ra\n"



mathop = ['+', '-', '*', '/', '%']
addrDesc = {}
nextUseTable = {}
incode = []
variables = []
symList = []
symTable = {}
leaders = [1,]
labels = {1:"L1"}
basicblocks = {}

def main():

	global mathop
	global addrDesc
	global nextUseTable
	global incode
	global variables
	global symList
	global symTable
	global leaders
	global basicblocks
	global labels

	if len(sys.argv) == 2:
		filename = str(sys.argv[1])
	else:
		print("Too many or too few arguements")
		exit()

	keyword = ['ifgoto', 'goto', 'return', 'call', 'printint', 'label', 'call', 'exit', 'return', 'scanint']
	relation = ['<=', '>=', '==', '>', '<', '!=', '=']

	boolop = ['&', '|', '!']
	reserved = keyword + relation + mathop + boolop
	acode="# Generated Code \n"
	incodestr = open(filename).read().splitlines()

	for line in incodestr:
		incode.append(line.strip().split(', '))

# populate variables list

	for line in incode:
		#l = line.split(', ')
		for var in line:
			if(var not in reserved and not RepresentsInt(var)):
				variables.append(var)

	variables = list(set(variables))
	print(variables)

# populate symbol table

	for v in variables:
		symTable[v] = SymClass(v,'int')
		symList.append(symTable[v])
		print("------------------------------------------")
		print(symTable[v].lexeme)
		print("------------------------------------------")

# set the variables in IR to point to symTable dictionary's entries

	for line in incode:
		for ind, var in enumerate(line):
			if(var not in reserved and not RepresentsInt(var)):
				line[ind] = symTable[var]
	print("&&&&&&&&&&&&&&&&&&&&&")
	print(incode)

#address descriptors

	for s in symList:
		addrDesc[s]='MEM'

# set up leaders and basic blocks

	for line in incode:
		#l = line.split(', ')
		if 'ifgoto' in line:
			leaders.append(int(line[-1]))
			leaders.append(int(line[0])+1)
			labels[int(line[-1])] = "L"+line[-1]
			labels[int(line[0])+1] = "L"+str(int(line[0])+1)

		elif 'goto' in line:
			leaders.append(int(line[-1]))
			leaders.append(int(line[0])+1)
			labels[int(line[-1])] = "L"+line[-1]
			labels[int(line[0])+1] = "L"+str(int(line[0])+1)

		#elif 'function' in line:
		#	leaders.append(int(line[0]))
		#	labels[int(line[0])] = "L"+str(line[0])

		elif 'label' in line:
			line[2] = line[2].lexeme
			leaders.append(int(line[0]))
			labels[int(line[0])] = line[2]
	leaders = list(set(leaders))
	leaders.sort()
	print(leaders)
	#labels = {i:"L"+str(i) for i in leaders and not i in labels}
	print(labels)
# generating blocks here

	num_instr = len(incode)
	for i in range(len(leaders)):
		instruction1 = leaders[i]
		if i+1<len(leaders):
			instruction2 = leaders[i+1]-1
		else:
			instruction2 = num_instr
		basicblocks[instruction1] = incode[instruction1-1:instruction2]
	#print(basicblocks)

# populate the nextUseTable
	#print(nextUseTable)
	for l, block in basicblocks.items():
		tempTab = {}
		for sym in symList:
			tempTab[sym] = (0,math.inf)
		for ins in block[::-1]:
			nextUseTable[int(ins[0])] = {}
			for sym in symList:
				nextUseTable[int(ins[0])][sym] = copy.deepcopy(tempTab[sym])
				# print(nextUseTable)

			if ins[1] in mathop:
				tempTab[ins[2]] = (0,math.inf)
				if ins[3] in symList:
					tempTab[ins[3]] = (1,int(ins[0]))
				if ins[4] in symList:
					tempTab[ins[4]] = (1,int(ins[0]))
			elif ins[1] == '=':
				tempTab[ins[2]] = (0,math.inf)
				if ins[3] in symList:
					tempTab[ins[3]] = (1,int(ins[0]))
			elif ins[1] == 'ifgoto':
				if ins[3] in symList:
					tempTab[ins[3]] = (1,int(ins[0]))
				if ins[4] in symList:
					tempTab[ins[4]] = (1,int(ins[0]))
			elif ins[1] == 'printint':
				if ins[2] in symList:
					tempTab[ins[2]] = (1,int(ins[0]))
			#addMore
	#print(nextUseTable)

	print("####################################################")
	#print(incode)

#print sections
	global acode
	acode = ""
	acode += ".data\n"
	for var in variables:
		acode += var+":  "+".space 4\n"

	for line in incode:
		if(int(line[0]) in leaders):
			acode = acode + labels[int(line[0])] + ": "
		translate(line)

	acode = acode + "exit:\n\tli $v0, 10\n\tsyscall"
	print(acode)

if __name__ == "__main__":
	main()
