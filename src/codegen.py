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
	print("*************************************")
	print(labels)
	print("*************************************")
	#print(acode)
	#acode = acode + "# Generated Code \n"
	lineno = int(line[0])
	op = line[1]
	# Generating assembly code if the tac is a mathematical operation
	#print(op)

	if op in mathop:
		print(op)
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
				acode = acode + "addi " + reg + ", $zero, " + str(int(num1)+int(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2)

				acode = acode + "add " + reg + ", " + addr2 +", $zero" + "\n"

				acode = acode + "addi " + reg + ", " + reg + ", " +num1 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1, lineno)
				acode = acode + "add " + reg + ", " + addr1 +", $zero" + "\n"

				acode = acode + "addi " + reg + ", " + reg + ", " + num2 + "\n"
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

				acode = acode + "add " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register


		elif op == '-':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "addi " + reg + ", $zero, " + str(int(num1)-int(num2)) + "\n"
				addrDesc[ans] = reg

				#update register
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "sub " + reg  +", $zero, " + addr2 + "\n"

				acode = acode + "addi " + reg + ", " + reg + ", " + num1 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "sub " + reg + ", $zero, " + num2 + "\n"
				acode = acode + "add " + reg + ", " + reg + ", " + addr1 + "\n"
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

				acode = acode + "sub " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register
		elif op == '*':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "addi " + reg + ", $zero, " + str(int(num1)*int(num2)) + "\n"
				addrDesc[ans] = reg

				#update register
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "li " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "mul " + reg + ", " + reg + ", " + addr2 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "li " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "mul " + reg + ", " + reg + ", " + addr1 + "\n"
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

				acode = acode + "mul " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register

		# Division
		elif op == '/':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "addi " + reg + ", $zero, " + str(int(num1)/int(num2)) + "\n"
				addrDesc[ans] = reg
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "li " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "div " + reg + ", " + reg + ", " + addr2 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "li " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "div " + reg + ", " + addr1 + ", " + reg  + "\n"
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

				acode = acode + "div " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

				#update register

		# Modulus
		elif op == '%':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "addi " + reg + ", $zero, " + str(int(num1)%int(num2)) + "\n"
				addrDesc[ans] = reg

				#update register
			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "li " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "rem " + reg + ", " + reg + ", " + addr2 + "\n"
				addrDesc[ans] = reg

				#update register

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "li " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "rem " + reg + ", " + addr1 + ", " + reg  + "\n"
				addrDesc[ans] = reg


			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr1 = getReg(num1,lineno)

				acode = acode + "rem " + reg + ", " + addr1 +", "+ addr2 + "\n"
				addrDesc[ans] = reg

	elif op == "goto":
	# 	# Add code to write all the variables to the memory
	 	l = line[2]
	 	acode = acode + "j " + label[int(l)] +"\n"

	elif op == "ifgoto":
		#4, ifgoto, <=, a, 50, 2
		rel = line[2]
		num1 = line[3]
		num2 = line[4]
		l = line[5]

		if isInt(num1) and isInt(num2):
			if(rel == "<="):
				if(int(num1) <= int(num2)):
					acode = acode + "j " + labels[int(l)] +"\n"

			if(rel == ">="):
				if(int(num1) >= int(num2)):
					acode = acode + "j " + labels[int(l)] +"\n"

			if(rel == "=="):
				if(int(num1) == int(num2)):
					acode = acode + "j " + labels[int(l)] +"\n"

			if(rel == ">"):
				if(int(num1) > int(num2)):
					acode = acode + "j " + labels[int(l)] +"\n"

			if(rel == "<"):
				if(int(num1) < int(num2)):
					acode = acode + "j " + labels[int(l)] +"\n"

			if(rel == "!="):
				if(int(num1) != int(num2)):
					acode = acode + "j " + labels[int(l)] +"\n"

		elif isInt(num1) and not isInt(num2):
			print("yes2")
			addr2 = addrDesc[num2]
			if(addr2 == "MEM"):
				addr2 = getReg(num2,lineno)

			if(rel == "<="):
				acode = acode + "bgt " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"

			if(rel == ">="):
				acode = acode + "blt " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"


			if(rel == "=="):
				acode = acode + "beq " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"

			if(rel == ">"):
				acode = acode + "ble " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"

			if(rel == "<"):
				acode = acode + "bge " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"

			if(rel == "!="):
				acode = acode + "bne " + addr2 + ", " + num1 + ", " + labels[int(l)] +"\n"

		elif not isInt(num1) and isInt(num2):
			#bge Rsrc1, Src2, label
			print("yes3")
			addr1 = addrDesc[num1]
			if(addr1 == "MEM"):
				addr1 = getReg(num1,lineno)

			if(rel == "<="):
				acode = acode + "ble " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

			if(rel == ">="):
				acode = acode + "bge " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

			if(rel == "=="):
				acode = acode + "beq " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

			if(rel == ">"):
				acode = acode + "bgt " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

			if(rel == "<"):
				acode = acode + "blt " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

			if(rel == "!="):
				acode = acode + "bne " + addr1 + ", " + num2 + ", " + labels[int(l)] +"\n"

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
				acode = acode + "ble " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"

			if(rel == ">="):
				acode = acode + "bge " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"

			if(rel == "=="):
				acode = acode + "beq " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"

			if(rel == ">"):
				acode = acode + "bgt " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"

			if(rel == "<"):
				acode = acode + "blt " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"

			if(rel == "!="):
				acode = acode + "bne " + addr1 + ", " + addr2 + ", " + labels[int(l)] +"\n"

		# if(rel == "=="):
		# 	if()
	 # 	for var in varlist:
	 # 		loc = getlocation(var)
	 # 		if loc != "mem":
	 # 			assembly = assembly + "movl " + loc + ", " + var + "\n"
	 # 			setlocation(var, "mem")

	# 	label = instruction[2]
	# 	if isnumber(label):
	# 		assembly = assembly + "jmp L" + label + "\n"
	# 	else:
	# 		assembly = assembly + "jmp " + label + "\n"

	# elif operator == "param":
	# 	#LineNo, param, val
	# 	val = instruction[2]
	# 	if isnumber(val):
	# 		val = "$" + val
	# 	else:
	# 		loc2 = getlocation(val)
	# 		if loc2 != "mem":
	# 			val = addressDescriptor[val]
	# 	assembly = assembly + "pushl " + val + "\n"


	# # Generating assembly code if the tac is a function call
	# elif operator == "call":
	# 	#Lno., call, func_name, arg_num, ret
	# 	# Add code to write all the variables to the memory
	# 	arg_num = instruction[3]
	# 	for var in varlist:
	# 		loc = getlocation(var)
	# 		if loc != "mem":
	# 			assembly = assembly + "movl " + loc + ", " + var + "\n"
	# 			setlocation(var, "mem")
	# 	label = instruction[2]
	# 	assembly = assembly + "call " + label + "\n"

	# # Generating assembly code if the tac is a label for a new leader
	# elif operator == "label":
	# 	label = instruction[2]
	# 	assembly = assembly + label + ": \n"

	# # Generating assembly code if the tac is an ifgoto statement
	# elif operator == "ifgoto":
	# 	# Add code to write all the variables to the memory
	# 	for var in varlist:
	# 		loc = getlocation(var)
	# 		if loc != "mem":
	# 			assembly = assembly + "movl " + loc + ", " + var + "\n"
	# 			setlocation(var, "mem")
	# 	operator = instruction[2]
	# 	operand1 = instruction[3]
	# 	operand2 = instruction[4]
	# 	label = instruction[5]
	# 	#check whether the operands are variables or constants
	# 	if not isnumber(operand1) and not isnumber(operand2): #both the operands are variables
	# 		#Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		#Get the register for comparing the operands
	# 		reg1 = getReg(operand1, line)
	# 		#generating assembly instructions
	# 		if loc1 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + reg1 + "\n"
	# 		else:
	# 			assembly = assembly + "movl " + operand1 + ", " + reg1 + "\n"
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmp " + loc2 + ", " + reg1 + "\n"
	# 		else:
	# 			assembly = assembly + "cmp " + operand2 + ", " + reg1 + "\n"
	# 		#updating the registor & address descriptors
	# 		setregister(reg1, operand1)
	# 		setlocation(operand1, reg1)

	# 	elif not isnumber(operand1) and isnumber(operand2): #only operand1 is variables
	# 		#Get the location of the 1st operand
	# 		loc1 = getlocation(operand1)
	# 		if loc1 != "mem":
	# 			assembly = assembly + "cmp $" + operand2 + ", " + loc1 + "\n"
	# 		else:
	# 			assembly = assembly + "cmp $" + operand2 + ", " + operand1 + "\n"
	# 	elif isnumber(operand1) and not isnumber(operand2): #only operand2 is variables
	# 		#Get the location of the 1st operand
	# 		loc2 = getlocation(operand2)
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmp " + loc2 + ", $" + operand1 + "\n"
	# 		else:
	# 			assembly = assembly + "cmp " + operand2 + ", $" + operand1 + "\n"
	# 	elif isnumber(operand1) and isnumber(operand2): #none of the operandsare variables
	# 		#generate assembly instructions
	# 		assembly = assembly + "cmp $" + operand2 + ", $" + operand1 + "\n"

	# 	# Add code to write all the variables to the memory
	# 	for var in varlist:
	# 		loc = getlocation(var)
	# 		if loc != "mem":
	# 			assembly = assembly + "movl " + loc + ", " + var + "\n"
	# 			setlocation(var, "mem")
	# 	if isnumber(label):
	# 		label = "L" + label
	# 	if operator == "<=":
	# 		assembly = assembly + "jle " + label + "\n"
	# 	elif operator == ">=":
	# 		assembly = assembly + "jge " + label + "\n"
	# 	elif operator == "==":
	# 		assembly = assembly + "je " + label + "\n"
	# 	elif operator == "<":
	# 		assembly = assembly + "jl " + label + "\n"
	# 	elif operator == ">":
	# 		assembly = assembly + "jg " + label + "\n"
	# 	elif operator == "!=":
	# 		assembly = assembly + "jne " + label + "\n"

	# # Generating assembly code if the tac is a goto statement
	# elif operator == "goto":
	# 	# Add code to write all the variables to the memory
	# 	for var in varlist:
	# 		loc = getlocation(var)
	# 		if loc != "mem":
	# 			assembly = assembly + "movl " + loc + ", " + var + "\n"
	# 			setlocation(var, "mem")

	# 	label = instruction[2]
	# 	if isnumber(label):
	# 		assembly = assembly + "jmp L" + label + "\n"
	# 	else:
	# 		assembly = assembly + "jmp " + label + "\n"

	# # Generating assembly code if the tac is a return statement
	# elif operator == "exit":
	# 	assembly = assembly + "call exit\n"

	# # Generating assembly code if the tac is a print
	# elif operator == "print":
	# 	operand = instruction[2]
	# 	if not isnumber(operand):
	# 		loc = getlocation(operand)
	# 		if not loc == "mem":
	# 			assembly = assembly + "pushl " + loc + "\n"
	# 			assembly = assembly + "pushl $str\n"
	# 			assembly = assembly + "call printf\n"
	# 		else:
	# 			assembly = assembly + "pushl " + operand + "\n"
	# 			assembly = assembly + "pushl $str\n"
	# 			assembly = assembly + "call printf\n"
	# 	else:
	# 		assembly = assembly + "pushl $" + operand + "\n"
	# 		assembly = assembly + "pushl $str\n"
	# 		assembly = assembly + "call printf\n"

	# # Generating code for assignment operations
	# elif operator == '=':
	# 	destination = instruction[2]
	# 	source = instruction[3]
	# 	loc1 = getlocation(destination)
	# 	# If the source is a literal then we can just move it to the destination
	# 	if isnumber(source):
	# 		if loc1 == "mem":
	# 			assembly = assembly + "movl $" + source + ", " + destination + "\n"
	# 		else:
	# 			assembly = assembly + "movl $" + source + ", " + loc1 + "\n"
	# 	else:
	# 		# If both the source and the destination reside in the memory
	# 		loc2 = getlocation(source)
	# 		if loc1 == "mem" and loc2 == "mem":
	# 			regdest = getReg(destination, line)
	# 			assembly = assembly + "movl " + source + ", " + regdest + "\n"
	# 			# Update the address descriptor entry for result variable to say where it is stored no
	# 			setregister(regdest, destination)
	# 			setlocation(destination, regdest)
	# 		# If the source is in a register
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			regdest = getReg(destination, line)
	# 			assembly = assembly + "movl " + loc2 + ", " + regdest + "\n"
	# 			# Update the address descriptor entry for result variable to say where it is stored no
	# 			setregister(regdest, destination)
	# 			setlocation(destination, regdest)
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + source + ", " + loc1 + "\n"
	# 		elif loc1 != "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc2 + ", " + loc1 + "\n"


	# # Generating the prelude for a function definition
	# elif operator == "function":
	# 	function_name = instruction[2]
	# 	assembly = assembly + ".globl " + function_name + "\n"
	# 	assembly = assembly + ".type "  + function_name + ", @function\n"
	# 	assembly = assembly + function_name + ":\n"
	# 	assembly = assembly + "pushl %ebp\n"
	# 	assembly = assembly + "movl %esp, %ebp\n"


	# elif operator == "arg":
	# 	#Lno, arg, i, a_i -----> Move parameter i to var a_i
	# 	i = instruction[2]
	# 	a = instruction[3]
	# 	displacement = 4*i + 4
	# 	assembly = assembly + "movl " + str(displacement) + "(%ebp), " + a + "\n"

	# elif operator == "pop":
	# 	#LNo, pop, n
	# 	n = instruction[2]
	# 	assembly = assembly + "addl $4, $esp\n"

	# # Generating the conclude of the function
	# elif operator == "return":
	# 	#LNo, return, val
	# 	val = instruction[2]
	# 	for var in varlist:
	# 		loc = getlocation(var)
	# 		if loc == "%eax":
	# 			assembly = assembly + "movl " + loc + ", " + var + "\n"
	# 			setlocation(var, "mem")
	# 			break
	# 	if isnumber(val):
	# 		val = "$" + val
	# 	assembly = assembly + "movl " + val + ", %eax\n"
	# 	assembly = assembly + "movl %ebp, %esp\n"
	# 	assembly = assembly + "popl %ebp\n"
	# 	assembly = assembly + "ret\n"

	# #Logical Left Shift : TAC Syntax ---> Line No, <<, result, num, count
	# #corres to result = num << count
	# elif operator == "<<":
	# 	result = instruction[2]
	# 	operand1 = instruction[3]		#num
	# 	operand2 = instruction[4]		#count
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(operand1)<<int(operand2)) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case result = 5 << x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move 5 to result, result = 5
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		#perform left shift, result = result << x
	# 		if loc2 != "mem":
	# 			assembly = assembly + "shl " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "shl " + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		#case result = a << 2
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move a to regdest, result = a
	# 		if loc1 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 		# Perform Left shift result = result << 2
	# 		assembly = assembly + "shl $" + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		#case result = a << b
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			#result = a and result = result << b
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shl " + operand2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shl " + operand2 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)


	# #Logical Right Shift : TAC Syntax ---> Line No, >>, result, num, count
	# #corres to result = num >> count
	# elif operator == ">>":
	# 	result = instruction[2]
	# 	operand1 = instruction[3]		#num
	# 	operand2 = instruction[4]		#count
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(operand1)>>int(operand2)) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case result = 5 >> x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move 5 to result, result = 5
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		#perform right shift, result = result >> x
	# 		if loc2 != "mem":
	# 			assembly = assembly + "shr " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "shr " + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		#case result = a << 2
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move a to regdest, result = a
	# 		if loc1 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 		# Perform Right shift result = result >> 2
	# 		assembly = assembly + "shr $" + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		#case result = a >> b
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			#result = a and result = result >> b
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shr " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shr " + operand2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shr " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "shr " + operand2 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)

	# elif operator == "&&":
	# 	#Line, &&, result, op1, op2
	# 	result = instruction[2]
	# 	operand1 = instruction[3]		#num
	# 	operand2 = instruction[4]		#count
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(operand1) and int(operand2)) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case result = 0 && x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move 5 to result, result = 5
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		#perform logical and, result = result >> x
	# 		if loc2 != "mem":
	# 			assembly = assembly + "and " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "and " + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		#case result = a && 2
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move a to regdest, result = a
	# 		if loc1 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 		# Perform Logical and result = result && 2
	# 		assembly = assembly + "and $" + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		#case result = a && b
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			#result = a and result = result && b
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "and " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "and " + operand2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "and " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "and " + operand2 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)

	# elif operator == "||":
	# 	#Line, ||, result, op1, op2
	# 	result = instruction[2]
	# 	operand1 = instruction[3]		#op1
	# 	operand2 = instruction[4]		#op2
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(operand1) or int(operand2)) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case result = 0 || x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move 5 to result, result = 5
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		#perform logical and, result = result || x
	# 		if loc2 != "mem":
	# 			assembly = assembly + "or " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "or " + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		#case result = a || 2
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move a to regdest, result = a
	# 		if loc1 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 		# Perform Logical and result = result || 2
	# 		assembly = assembly + "or $" + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		#case result = a || b
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			#result = a and result = result || b
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "or " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "or " + operand2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "or " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "or " + operand2 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)

	# elif operator == "~":
	# 	#Line, not, result, op1
	# 	result = instruction[2]
	# 	operand1 = instruction[3]		#num
	# 	if isnumber(operand1):
	# 		#Case : result = !(1)
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(not(int(operand1))) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1):
	# 		#case result = !(a)
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move a to regdest, result = a
	# 		if loc1 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 		# Perform Logical and result = !(result)
	# 		assembly = assembly + "not $" + operand2 + ", " + regdest + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# # Return the assembly code

	# elif operator == '<=':
	# 	result = instruction[2]
	# 	operand1 = instruction[3]
	# 	operand2 = instruction[4]
	# 	LT = "LT"+str(relcount)
	# 	NLT = "NLT"+str(relcount)
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		#case: result = 4 < 5
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(int(operand1)<=int(operand2))) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case: result = 5 < x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand2 + ", " + regdest + "\n"
	# 		assembly = assembly + "jle " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand2 + ", " + regdest + "\n"
	# 		# Add the other operand to the register content
	# 		if loc1 != "mem":
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		assembly = assembly + "jle " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		assembly = assembly + "jle " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)
	# 	relcount = relcount + 1

	# elif operator == '>=':
	# 	result = instruction[2]
	# 	operand1 = instruction[3]
	# 	operand2 = instruction[4]
	# 	LT = "LT"+str(relcount)
	# 	NLT = "NLT"+str(relcount)
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		#case: result = 4 < 5
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(int(operand1)>=int(operand2))) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case: result = 5 < x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand2 + ", " + regdest + "\n"
	# 		assembly = assembly + "jge " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand2 + ", " + regdest + "\n"
	# 		# Add the other operand to the register content
	# 		if loc1 != "mem":
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		assembly = assembly + "jge " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		assembly = assembly + "jge " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)
	# 	relcount = relcount + 1

	# elif operator == '==':
	# 	result = instruction[2]
	# 	operand1 = instruction[3]
	# 	operand2 = instruction[4]
	# 	LT = "LT"+str(relcount)
	# 	NLT = "NLT"+str(relcount)
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		#case: result = 4 < 5
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(int(operand1)==int(operand2))) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case: result = 5 < x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand2 + ", " + regdest + "\n"
	# 		assembly = assembly + "je " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand2 + ", " + regdest + "\n"
	# 		# Add the other operand to the register content
	# 		if loc1 != "mem":
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		assembly = assembly + "je " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		assembly = assembly + "je " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)
	# 	relcount = relcount + 1

	# elif operator == '!=':
	# 	result = instruction[2]
	# 	operand1 = instruction[3]
	# 	operand2 = instruction[4]
	# 	LT = "LT"+str(relcount)
	# 	NLT = "NLT"+str(relcount)
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		#case: result = 4 < 5
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(int(operand1)!=int(operand2))) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case: result = 5 < x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand2 + ", " + regdest + "\n"
	# 		assembly = assembly + "jne " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand2 + ", " + regdest + "\n"
	# 		# Add the other operand to the register content
	# 		if loc1 != "mem":
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		assembly = assembly + "jne " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		assembly = assembly + "jne " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)
	# 	relcount = relcount + 1

	# elif operator == '<':
	# 	result = instruction[2]
	# 	operand1 = instruction[3]
	# 	operand2 = instruction[4]
	# 	LT = "LT"+str(relcount)
	# 	NLT = "NLT"+str(relcount)
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		#case: result = 4 < 5
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(int(operand1)<int(operand2))) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case: result = 5 < x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand2 + ", " + regdest + "\n"
	# 		assembly = assembly + "jl " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand2 + ", " + regdest + "\n"
	# 		# Add the other operand to the register content
	# 		if loc1 != "mem":
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		assembly = assembly + "jl " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		assembly = assembly + "jl " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)
	# 	relcount = relcount + 1

	# elif operator == '>':
	# 	result = instruction[2]
	# 	operand1 = instruction[3]
	# 	operand2 = instruction[4]
	# 	LT = "LT"+str(relcount)
	# 	NLT = "NLT"+str(relcount)
	# 	if isnumber(operand1) and isnumber(operand2):
	# 		#case: result = 4 < 5
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		assembly = assembly + "movl $" + str(int(int(operand1)>int(operand2))) + ", " + regdest + "\n"
	# 		# Update the address descriptor entry for result variable to say where it is stored no
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif isnumber(operand1) and not isnumber(operand2):
	# 		#case: result = 5 < x
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc2 = getlocation(operand2)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
	# 		if loc2 != "mem":
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand2 + ", " + regdest + "\n"
	# 		assembly = assembly + "jg " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		loc1 = getlocation(operand1)
	# 		# Move the first operand to the destination register
	# 		assembly = assembly + "movl $" + operand2 + ", " + regdest + "\n"
	# 		# Add the other operand to the register content
	# 		if loc1 != "mem":
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		else:
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		assembly = assembly + "jg " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		setlocation(result, regdest)
	# 	elif not isnumber(operand1) and not isnumber(operand2):
	# 		# Get the register to store the result
	# 		regdest = getReg(result, line)
	# 		# Get the locations of the operands
	# 		loc1 = getlocation(operand1)
	# 		loc2 = getlocation(operand2)
	# 		if loc1 != "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 != "mem":
	# 			assembly = assembly + "movl " + operand1 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc2 + ", " + regdest + "\n"
	# 		elif loc1 != "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + loc1 + ", " + regdest + "\n"
	# 		elif loc1 == "mem" and loc2 == "mem":
	# 			assembly = assembly + "movl " + operand2 + ", " + regdest + "\n"
	# 			assembly = assembly + "cmpl " + operand1 + ", " + regdest + "\n"
	# 		# Update the register descriptor entry for regdest to say that it contains the result
	# 		assembly = assembly + "jg " + LT + "\n"
	# 		assembly = assembly + "movl $0, " + regdest + "\n"
	# 		assembly = assembly + "jmp NLT" + "\n"
	# 		assembly = assembly + LT + ":" + "\n"
	# 		assembly = assembly + "movl $1, " + regdest + "\n"
	# 		assembly = assembly + NLT + ":" + "\n"
	# 		setregister(regdest, result)
	# 		# Update the address descriptor entry for result variable to say where it is stored now
	# 		setlocation(result, regdest)
	# 	relcount = relcount + 1

mathop = ['+', '-', '*', '/', '%']
addrDesc = {}
nextUseTable = {}
incode = []
variables = []
symList = []
symTable = {}
leaders = [1,]
labels = {}
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

	keyword = ['ifgoto', 'goto', 'return', 'call', 'print', 'label', 'function', 'exit', 'return']
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

		elif 'goto' in line:
			leaders.append(int(line[-1]))
			leaders.append(int(line[0])+1)

		elif 'function' in line:
			leaders.append(int(line[0]))

		elif 'label' in line:
			leaders.append(int(line[0]))
	leaders = list(set(leaders))
	leaders.sort()
	print(leaders)
	labels = {i:"L"+str(i) for i in leaders}
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
	print(basicblocks)

# populate the nextUseTable
	print(nextUseTable)
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
			elif ins[1] == 'print':
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
