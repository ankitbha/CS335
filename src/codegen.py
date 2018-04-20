#!/usr/bin/env python3

import sys
import math
import copy
import inspect
import symtable
import random
import par

#class CodeGen:
# def reg_init():
ret = None
ex=False
vreg = {"$v0":None, "$v1":None}
areg = {"$a0":None, "$a1":None, "$a2":None, "$a3":None}
zreg = {"$zero":None}
treg = {}
sreg = {}
preg = { "$gp" : None, "$sp" : None, "$fp" : None, "ra" : None }
kreg = { "$k0" : None, "$k1" : None }
reg_float = dict()
for i in range(1,24):  reg_float.update({ '$f' + str(i) : [] })
reg_norm = {"$t0":None, "$t1":None, "$t2":None, "$t3":None, "$t4":None, "$t5":None, "$t6":None, "$t7":None, "$t8":None, "$t9":None, "$s0":None, "$s1":None, "$s2":None, "$s3":None, "$s4":None, "$s5":None, "$s6":None, "$s7":None}

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
	global reg_norm
	global used_reg_norm
	global unused_reg_norm
	if varObj.vtype == "REAL":
		for i in reg_float.keys():
			if (reg_float[i]==varObj):
				return i

		if len(unused_reg_float)!=0:
			reg = unused_reg_float[0]
			unused_reg_float.remove(reg)
			used_reg_float.append(reg)
			reg_float[reg] = varObj
			addrDesc[varObj] = reg
			return reg


		else:
			spillReg = random.choice(used_reg_float)
			# forNextUse=nextUseTable[numLine]
			# tempFarthest=None
			# for var in forNextUse.keys():
			# 	if (tempFarthest==None):
			# 		tempFarthest=var
			# 	elif (forNextUse[var]>forNextUse[tempFarthest]):
			# 		tempFarthest=var
			# 	else:
			# 		continue
			# for spillReg in reg_float.keys():
			# 	if reg_float[spillReg]==tempFarthest:
			# 		break

			#write something like
			#    assembly = assembly + "movl " + regspill + ", " + var + "\n"
			# acode = acode + "lw " + spillReg + ", " + addrDesc[reg_norm[spillReg]] + "\n"
			acode = acode + "\t" + "s.s " + spillReg + ", " + (reg_float[spillReg]).lex + "\n"
			acode = acode + "\t" + "l.s " + spillReg + ", " + varObj.lex + "\n"
			addrDesc[reg_float[spillReg]] = "MEM"
			reg_float[spillReg] = varObj
			addrDesc[varObj] = spillReg

	else:
		#regExist=False
		#emptyReg=None
		for i in reg_norm.keys():
			if (reg_norm[i]==varObj):
				#regExist = True
				return i
			#if(emptyReg==None and !regExist):


		if len(unused_reg_norm)!=0:
			reg = unused_reg_norm[0]
			unused_reg_norm.remove(reg)
			used_reg_norm.append(reg)
			reg_norm[reg] = varObj
			addrDesc[varObj] = reg
			return reg


		else:
			spillReg = random.choice(used_reg_norm)
			# forNextUse=nextUseTable[numLine]
			# tempFarthest=None
			#forNextUse should be a dictionary, so nextUseTable must also be a
			#dictionary with keys as line numbers and value as another dictionary
			#with key being variable names and values being nextUselineNo
			# for var in forNextUse.keys():
			# 	if (tempFarthest==None):
			# 		tempFarthest=var
			# 	elif (forNextUse[var]>forNextUse[tempFarthest]):
			# 		tempFarthest=var
			# 	else:
			# 		continue
			# for spillReg in reg_norm.keys():
			# 	if reg_norm[spillReg]==tempFarthest:
			# 		break

			acode = acode + "\t" + "sw " + spillReg + ", " + (reg_norm[spillReg]).lex + "\n"
			acode = acode + "\t" + "lw " + spillReg + ", " + varObj.lex + "\n"
			addrDesc[reg_norm[spillReg]] = "MEM"
			reg_norm[spillReg] = varObj
			addrDesc[varObj] = spillReg
	return spillReg

def flushRegDesc():
	global acode
	global reg_norm
	global used_reg_norm
	global unused_reg_norm
	used_reg_norm = []
	unused_reg_norm = list(reg_norm.keys())
	# for reg in used_reg_norm:
	# 	used_reg_norm.remove(reg)
		# addrDesc[reg_norm[reg]] = 'MEM'
		# acode = acode + "\t" + "sw " + reg + ", " + (reg_norm[reg]).lex + "\n"
		# unused_reg_norm.append(reg)




	for reg in used_reg_float:
		used_reg_float.remove(reg)
		# addrDesc[reg_float[reg]] = 'MEM'
		# acode = acode + "\t" + "sw " + reg + ", " + (reg_float[reg]).lex + "\n"
		unused_reg_float.append(reg)

def flushAddrDesc():
	global acode
	global reg_norm
	global used_reg_norm
	global unused_reg_norm
	for reg in used_reg_norm:
		# used_reg_norm.remove(reg)
		addrDesc[reg_norm[reg]] = 'MEM'
		if((reg_norm[reg]).lex not in ['_temp','_temp1']):
			acode = acode + "\t" + "sw " + reg + ", " + (reg_norm[reg]).addr + "\n"
		# unused_reg_norm.append(reg)
	for reg in used_reg_float:
		# used_reg_float.remove(reg)
		addrDesc[reg_float[reg]] = 'MEM'
		acode = acode + "\t" + "sw " + reg + ", " + (reg_float[reg]).addr + "\n"
		# unused_reg_float.append(reg)


def isInt(s):
	if (isinstance(s, symtable.SymTabEntry)):
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
	global ret
	#print(acode)
	#acode = acode + "# Generated Code \n"
	lineno = int(line[0])
	op = line[1]
	# Generating assembly code if the tac is a mathematical operation
	#print(op)


	if op in floatop:
		#print(op)
		ans = line[2]
		#print(ans)
		num1 = line[3]
		num2 = line[4]
		# Addition
		if op == '+f':
			#print("yes")
			if isInt(num1) and isInt(num2):
				#print("yes")
				reg = getReg(ans,lineno)
				acode = acode + "\tli.s " + reg + str(float(num1)+float(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tli.s " + reg + ", " + num1 + "\n"
				acode = acode + "\tadd.s " + reg + ", " + reg + ", " +addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1, lineno)
				acode = acode + "\tli.s " + reg + ", " + num2 + "\n"

				acode = acode + "\tadd.s " + reg + ", " + reg + ", " +addr1 + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1, lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2, lineno)

				acode = acode + "\tadd.s " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '-f':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli.s " + reg + str(float(num1)-float(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tli.s " + reg + ", " + num1 + "\n"

				acode = acode + "\tsub.s " + reg + ", " + reg + ", " +addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tli.s " + reg + ", " + num2 + "\n"

				acode = acode + "\tsub.s " + reg + ", " + addr1 + ", " + reg + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tsub.s " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '*f':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli.s " + reg + str(float(num1)*float(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tli.s " + reg + ", " + num1 + "\n"
				acode = acode + "\tmul.s " + reg + ", " + reg + ", " + addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli.s " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tmul.s " + reg + ", " + reg + ", " + addr1 + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tmul.s " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '/f':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli.s " + reg + str(float(num1)/float(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli.s " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tdiv.s " + reg + ", " + reg + ", " + addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tdiv.s " + reg + ", " + addr1 + ", " + reg  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tdiv.s " + reg + ", " + addr1 +", "+ addr2 + "\n"

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
					addr2 = getReg(num2,lineno)

				acode = acode + "\tadd " + reg + ", " + addr2 +", $zero" + "\n"

				acode = acode + "\taddi " + reg + ", " + reg + ", " +num1 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1, lineno)
				acode = acode + "\tadd " + reg + ", " + addr1 +", $zero" + "\n"

				acode = acode + "\taddi " + reg + ", " + reg + ", " + num2 + "\n"


			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1, lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2, lineno)

				acode = acode + "\tadd " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '-':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)-int(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tsub " + reg  +", $zero, " + addr2 + "\n"

				acode = acode + "\taddi " + reg + ", " + reg + ", " + num1 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tsub " + reg + ", $zero, " + num2 + "\n"
				acode = acode + "\tadd " + reg + ", " + reg + ", " + addr1 + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tsub " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '*':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)*int(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tmul " + reg + ", " + reg + ", " + addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tmul " + reg + ", " + reg + ", " + addr1 + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tmul " + reg + ", " + addr1 +", "+ addr2 + "\n"

		# Division
		elif op == '/':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)/int(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tdiv " + reg + ", " + reg + ", " + addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tdiv " + reg + ", " + addr1 + ", " + reg  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\tdiv " + reg + ", " + addr1 +", "+ addr2 + "\n"

		# Modulus
		elif op == '%':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\taddi " + reg + ", $zero, " + str(int(num1)%int(num2)) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\trem " + reg + ", " + reg + ", " + addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\trem " + reg + ", " + addr1 + ", " + reg  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)

				acode = acode + "\trem " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '<=':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				if(num1<=num2):
					result = 1
				else:
					result = 0
				acode = acode + "\taddi " + reg + ", $zero, " + str(result) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr1 + ", " + num1 + "\n"
				# acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tsle " + reg + ", " + addr1 + ", " + addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr2 + ", " + num2 + "\n"
				# acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tsle " + reg + ", " + addr1 + ", " + addr2  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tsle " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '<':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				if(num1<num2):
					result = 1
				else:
					result = 0
				acode = acode + "\taddi " + reg + ", $zero, " + str(result) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr1 + ", " + num1 + "\n"
				# acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tslt " + reg + ", " + addr1 + ", " + addr2 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr2 + ", " + num2 + "\n"
				# acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tslt " + reg + ", " + addr1 + ", " + addr2  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tslt " + reg + ", " + addr1 +", "+ addr2 + "\n"

		elif op == '>':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				if(num1>num2):
					result = 1
				else:
					result = 0
				acode = acode + "\taddi " + reg + ", $zero, " + str(result) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr1 + ", " + num1 + "\n"
				# acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tslt " + reg + ", " + addr2 + ", " + addr1 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr2 + ", " + num2 + "\n"
				# acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tslt " + reg + ", " + addr2 + ", " + addr1  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tslt " + reg + ", " + addr2 +", "+ addr1 + "\n"

		elif op == '>=':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				if(num1>=num2):
					result = 1
				else:
					result = 0
				acode = acode + "\taddi " + reg + ", $zero, " + str(result) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr1 + ", " + num1 + "\n"
				# acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tsle " + reg + ", " + addr2 + ", " + addr1 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr2 + ", " + num2 + "\n"
				# acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tsle " + reg + ", " + addr2 + ", " + addr1  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tsle " + reg + ", " + addr2 +", "+ addr1 + "\n"

		elif op == '!=':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				if(num1!=num2):
					result = 1
				else:
					result = 0
				acode = acode + "\taddi " + reg + ", $zero, " + str(result) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr1 + ", " + num1 + "\n"
				# acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tsne " + reg + ", " + addr2 + ", " + addr1 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr2 + ", " + num2 + "\n"
				# acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tsne " + reg + ", " + addr2 + ", " + addr1  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tsne " + reg + ", " + addr2 +", "+ addr1 + "\n"

		elif op == '==':
			if isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				if(num1==num2):
					result = 1
				else:
					result = 0
				acode = acode + "\taddi " + reg + ", $zero, " + str(result) + "\n"

			elif isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr1 + ", " + num1 + "\n"
				# acode = acode + "\tli " + reg + ", " + num1 + "\n"
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tseq " + reg + ", " + addr2 + ", " + addr1 + "\n"

			elif not isInt(num1) and isInt(num2):
				reg = getReg(ans,lineno)
				addr2 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
				acode = acode + "\tli " + addr2 + ", " + num2 + "\n"
				# acode = acode + "\tli " + reg + ", " + num2 + "\n"
				addr1 = addrDesc[num1]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				acode = acode + "\tseq " + reg + ", " + addr2 + ", " + addr1  + "\n"

			elif not isInt(num1) and not isInt(num2):
				reg = getReg(ans,lineno)
				addr1 = addrDesc[num1]
				addr2 = addrDesc[num2]
				if(addr1 == "MEM"):
					addr1 = getReg(num1,lineno)
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tseq " + reg + ", " + addr2 +", "+ addr1 + "\n"


	elif op == "goto":
	# 	# Add code to write all the variables to the memory
		l = line[2]
		acode = acode + "\tj " + labels[int(l)] +"\n"

	elif op == "ifgoto":
		#4, ifgoto, <=, a, 50, 2
		rel = line[2]
		num1 = line[3]
		num2 = line[4]
		l = line[5]
		print(line[0], line[1],line[2],line[3],line[4],line[5])

		if (num1.vtype=='INTEGER'):
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
				# bge Rsrc1, Src2, label

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
		if (num1.vtype=='INTEGER'):
			if isInt(num2):
				acode=acode+"\tli "+ addr1 + ", " + num2 + "\n"
			else:
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tmove " + addr1 + ", " + addr2 + "\n"
		elif (num1.vtype=='REAL'):
			if isInt(num2):
				acode = acode+"\tli.s "+ addr1 + ", " + num2 + "\n"
			else:
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tmov.s " + addr1 + ", " + addr2 + "\n"
		elif (num1.vtype=='CHAR'):
			if isInt(num2):
				acode=acode+"\tli "+ addr1 + ", '" + num2 + "'\n"
			else:
				addr2 = addrDesc[num2]
				if(addr2 == "MEM"):
					addr2 = getReg(num2,lineno)
				acode = acode + "\tmove " + addr1 + ", " + addr2 + "\n"

	if op=="printint":
		#8, print, a
		ans=line[2];
		addr1 = addrDesc[ans]
		if(addr1 == "MEM"):
			addr1 = getReg(ans,lineno)
		acode = acode +"\tli $v0, 1\n"
		acode = acode +"\tmove, $a0, " + addr1 + "\n"
		acode = acode +"\tsyscall\n"

	if op=="readint":
		#8, scanint, a
		ans=line[2];
		addr1 = addrDesc[ans]
		if(addr1 == "MEM"):
			addr1 = getReg(ans,lineno)
		acode = acode +"\tli $v0, 5\n"
		acode = acode +"\tsyscall\n"
		acode = acode +"\tmove, "+ addr1 + " ,$v0" + "\n"

	if op=="call":
		# num, call, func
		# acode =
		l=line[2]
		if(len(line)==4):
			ret = line[3].vtype
			acode = acode + "\taddi $sp, $sp, -12\n"
			acode = acode + "\tsw $fp, -8($sp)\n"
			acode = acode + "\tsw $ra, -4($sp)\n"
			acode = acode + "\tmove $fp, $sp\n"
			# acode = acode + "\taddi $fp, $fp, -4\n"
			acode = acode + "\taddi $sp, $sp, " + str(-l.offset) + "\n"
			acode = acode + "\tjal " + l.lex +"\n"
			acode = acode + "\tmove $sp, $fp\n"
			acode = acode + "\tlw $fp, -8($sp)\n"
			acode = acode + "\tlw $ra, -4($sp)\n"
		else:
			ret = None
			acode = acode + "\taddi $sp, $sp, -8\n"
			acode = acode + "\tsw $fp, -4($sp)\n"
			acode = acode + "\tsw $ra, 0($sp)\n"
			acode = acode + "\tmove $fp, $sp\n"
			# acode = acode + "\taddi $fp, $fp, -4\n"
			acode = acode + "\tjal " + l.lex +"\n"
			acode = acode + "\tmove $sp, $fp\n"
			acode = acode + "\tlw $fp, -8($sp)\n"
			acode = acode + "\tlw $ra, -4($sp)\n"

	if op == "param":
		# param, exp
		ans = line[2]
		if(isInt(ans)):
			addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
			acode = acode + "\tli " + addr1 + ", " + ans + "\n"
		else:
			addr1 = addrDesc[ans]
			if(addr1 == "MEM"):
				addr1 = getReg(ans,lineno)

		acode = acode + "\tsub $sp, $sp, 4\n"
		acode = acode + "\tsw " + addr1 +", 0($sp)\n"

	if op == "gparam":
		# param, exp
		ans = line[2]
		addr1 = addrDesc[ans]
		if(addr1 == "MEM"):
			addr1 = getReg(ans,lineno)
		acode = acode + "\tlw " + addr1 + ", " + str((-ans.offset-12)) +"($fp)\n"

	if op == "declarray":
		arr = line[2]
		size = line[3]
		addr = addrDesc[arr]
		if(addr == "MEM"):
			addr = getReg(arr,lineno)
		if(isInt(size)):
			acode = acode + "\tli $a0, " + size + "\n"
		else:
			addr1 = addrDesc[size]
			if(addr1 == "MEM"):
				addr1 = getReg(size,lineno)
			acode = acode + "\tmove $a0, " + addr1 + "\n"
		acode = acode + "\tli $v0, 9\n"
		acode = acode + "\tsyscall\n"
		acode = acode + "\tmove " + addr + ", $v0\n"

	if op=="return":
		if(ex==False):
			acode = acode + "\tj exit\n"
			ex=True
		else:
			if(len(line)==2):
				acode = acode + "jr $ra\n"
			if(len(line)==3):
				if(ret==None):
					print("Error")
				ans=line[2]
				if(isInt(ans)):
					addr1 = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
					acode = acode + "\tli " + addr1 + ", " + ans + "\n"
				else:
					addr1 = addrDesc[ans]
					if(addr1 == "MEM"):
						addr1 = getReg(ans,lineno)
				acode = acode + "\tsw " + addr1 + ", 0($fp)\n"
				acode = acode + "\tjr $ra\n"


# ------------------------------------------------------------------------------------------------------------


	if op=="readarray":
		#3, readarray, a, var, var
		#4, la, reg, label
		array = line[2]
		index = line[3]
		res = line[4]
		addr = addrDesc[res]
		arr = getReg(array,lineno)
		acode = acode + "\tla " + arr + ", " + array.lex + "\n"
		if(addr=="MEM"):
			addr=getReg(res,lineno)
		if(isInt(index)):
			acode = acode + "\tlw " + addr + ", " + str(4*int(index)) + "(" + arr + ")\n"

		else:
			addri = addrDesc[index]
			if(addri=="MEM"):
				addri=getReg(index,lineno)
			acode = acode + "\tadd " + addri + ", " + addri + ", " + addri + "\n"
			acode = acode + "\tadd " + addri + ", " + addri + ", " + addri + "\n"
			acode = acode + "\tadd " + addri + ", " + arr + "," + addri + "\n"
			acode = acode + "\tlw " + addr + ", 0(" + addri + ")\n"

	if op=="writearray":
		#3, write, a, var, var
		#4, la, reg, label
		array = line[2]
		index = line[3]
		res = line[4]
		arr = getReg(array,lineno)
		acode = acode + "\tla " + arr + ", " + array.lex + "\n"
		temparr = getReg(tunnelTab.rootTable.queryEnt("_temp"),lineno)
		acode = acode + "\tla " + temparr + ", " + array.lex + "\n"
		if (not isInt(res)):
			rres = getReg(res,lineno)
			if(isInt(index)):
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				# rres = getReg("number",lineno)
				acode = acode + "\tsw " + rres + ", 0(" + temparr + ")\n"
			else:
				rindex = getReg(index,lineno)
				acode = acode + "\tmul " + rindex + ", " + rindex + ", 4" + "\n"
				acode = acode + "\tadd " + temparr + ", " + temparr + ", " + rindex + "\n"
				acode = acode + "\tsw " + rres + ", 0(" + temparr + ")\n"
		else:
			tempr = getReg(tunnelTab.rootTable.queryEnt("_temp1"),lineno)
			if(isInt(index)):
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				acode = acode + "\taddi " + temparr + ", " +  temparr + ", " + index + "\n"
				acode = acode + "\tli" + tempr + ", " + res + "\n"
				acode = acode + "\tsw " + tempr + ", 0(" + temparr + ")\n"
			else:
				rindex = getReg(index,lineno)
				acode = acode + "\tmul " + rindex + ", " + rindex + ", 4" + "\n"
				acode = acode + "\tadd " + temparr + ", " + temparr + ", " + rindex + "\n"
				acode = acode + "\tli " + tempr + ", " + res + "\n"
				acode = acode + "\tsw " +  tempr +  ", 0(" + temparr + ")\n"

	if op == "println":
		# writeln("string")
		arg = line[2]
		addr1 = arg.lex
		acode = acode +"\tli $v0, 4\n"
		acode = acode +"\tmove, $a0, " + addr1 + "\n"
		acode = acode +"\tsyscall\n"
		acode = acode +"\tli $v0, 4\n"
		acode = acode +"\tmove, $a0, " + "nl" + "\n"
		acode = acode +"\tsyscall\n"



mathop = ['+', '-', '*', '/', '%', '<=', '>=', '==', '<', '>', '!=']
floatop = ['+f', '-f', '*f', '/f']
addrDesc = {}
nextUseTable = {}
incode = []
variables = []
arrayz = []
stringz = []
#funcs=[]
leaders = [1,]
labels = {1:"main"}
basicblocks = {}

def mipsgen():
	global acode
	global mathop
	global floatop
	global addrDesc
	global nextUseTable
	global incode
	global glvar
	# global arrayz
	global symList
	global symTable
	global leaders
	global basicblocks
	global labels
	# global glvar

	# if len(sys.argv) == 2:
	# 	filename = str(sys.argv[1])
	# else:
	# 	print("Too many or too few arguements")
	# 	exit()

	keyword = ['ifgoto', 'goto', 'return', 'call', 'printint', 'label', 'call', 'function' , 'exit', 'return', 'readint', 'readarray', 'writearray']
	relation = ['<=', '>=', '==', '>', '<', '!=', '=']

	boolop = ['&', '|', '!']
	reserved = keyword + relation + mathop + boolop + floatop
	acode="# Generated Code \n"
	# incodestr = open(filename).read().splitlines()

	# for line in incodestr:
	# 	incode.append(line.strip().split(', '))

# populate variables list

	# for line in incode:
	# 	if line[1] in ['label', 'return']:
	# 		pass
	# 	elif line[1] in ['function', 'call']:
	# 		pass
	# 	elif line[1] in ['readarray', 'writearray']:
	# 		arrayz.append(line[2])
	# 		for var in line[3:]:
	# 			if(var not in reserved and not RepresentsInt(var)):
	# 				variables.append(var)
	# 	else:
	# 		for var in line:
	# 			if(var not in reserved and not RepresentsInt(var)):
	# 				variables.append(var)
	#
	# variables = list(set(variables))
	# arrayz = list(set(arrayz))

# populate symbol table

	# for v in variables:
	# 	symTable[v] = SymClass(v,'int')
	# 	symList.append(symTable[v])
	# for v in arrayz:
	# 	symTable[v] = SymClass(v,'array_int')
	# 	symList.append(symTable[v])
	#
	# symTable["_temp"] = SymClass("_temp", 'int')
	# symList.append(symTable["_temp"])

# set the variables in IR to point to symTable dictionary's entries

	# for line in incode:
	# 	for ind, var in enumerate(line):
	# 		if(var in variables):
	# 			line[ind] = symTable[var]
	# 		if(var in arrayz):
	# 			line[ind] = symTable[var]

# address descriptors
	# glvar = list(tunnelTab.rootTable.varsHere.values())
	# gltemp = list(tunnelTab.rootTable.temps.values())
	# glvar = glvar + gltemp
	# procs = tunnelTab.rootTable.children
	glvar = tunnelTab.getVariables()
	# print(procs)
	# print(procs['bigger'].temps)
	# for proc in procs:
	# 	glvar = glvar + list(procs[proc].varsHere.values())
	# 	glvar = glvar + list(procs[proc].temps.values())
	# print(glvar)
	for s in glvar:
		if(s.kind=='func'):
			glvar.remove(s)
	for s in glvar:
		addrDesc[s]='MEM'

	for s in tunnelTab.rootTable.temps.values():
		if(s.vtype == 'STRING'):
			stringz.append(s)

	# print(addrDesc)
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
			#line[2] = line[2].lex
			leaders.append(int(line[0]))
			labels[int(line[0])] = line[2]
	leaders = list(set(leaders))
	leaders.sort()

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

# fill the nextUseTable
	#print(nextUseTable)
	for l, block in basicblocks.items():
		tempTab = {}
		for sym in glvar:
			tempTab[sym] = (0,math.inf)
		for ins in block[::-1]:
			nextUseTable[int(ins[0])] = {}
			for sym in glvar:
				nextUseTable[int(ins[0])][sym] = copy.deepcopy(tempTab[sym])

			if (ins[1] in mathop) or (ins[1] in floatop):
				tempTab[ins[2]] = (0,math.inf)
				if ins[3] in glvar:
					tempTab[ins[3]] = (1,int(ins[0]))
				if ins[4] in glvar:
					tempTab[ins[4]] = (1,int(ins[0]))
			elif ins[1] == '=':
				tempTab[ins[2]] = (0,math.inf)
				if ins[3] in glvar:
					tempTab[ins[3]] = (1,int(ins[0]))
			elif ins[1] == 'ifgoto':
				if ins[3] in glvar:
					tempTab[ins[3]] = (1,int(ins[0]))
				if ins[4] in glvar:
					tempTab[ins[4]] = (1,int(ins[0]))
			elif ins[1] == 'printint':
				if ins[2] in glvar:
					tempTab[ins[2]] = (1,int(ins[0]))
			elif ins[1] == 'readint':
				if ins[2] in glvar:
					tempTab[ins[2]] = (0,math.inf)
			elif ins[1] == 'readarray':
				if ins[2] in glvar:
					tempTab[ins[2]] = (1,int(ins[0]))
				if ins[3] in glvar:
					tempTab[ins[3]] = (1,int(ins[0]))
				if ins[4] in glvar:
					tempTab[ins[4]] = (1,int(ins[0]))
			elif ins[1] == 'writearray':
				if ins[2] in glvar:
					tempTab[ins[2]] = (1,int(ins[0]))
				if ins[3] in glvar:
					tempTab[ins[3]] = (1,int(ins[0]))
				if ins[4] in glvar:
					tempTab[ins[4]] = (1,int(ins[0]))
			#addMore

#	acode = ""
	acode += ".data\n"

	varlist = list(tunnelTab.rootTable.varsHere.values())
	varlist2 = []
	for var in varlist:
		if(var.kind!='func' and var.vtype!='STRING' and var.lex!="_temp" and var.lex!="_temp1"):
			varlist2.append(var)
	# print(varlist2['bigger'])

	for var in varlist2:
		acode += var.lex +":  "+".space " + str(var.size) +"\n"
	for s in stringz:
		acode += s.addr + ":   .asciiz  "+ s.kind +'\n'
	acode += "nl" + ':   .asciiz  "\\n"' + '\n\n'

	acode += ".text\n"
	acode += ".globl main\n\n"
	acode += ".ent main\n"

	# print(addrDesc)

	for line in incode:

		if(int(line[0]) in leaders):
			flushRegDesc()
			acode = acode + labels[int(line[0])] + ":\n"
		if str(line[1]) in ['goto','ifgoto','call']:
			flushAddrDesc()
		translate(line)

	acode = acode + "exit:\n\tli $v0, 10\n\tsyscall"
	# with open("/home/rohit/Desktop/1.s","w") as file:
	# 	file.write(acode)

	return acode

if __name__ == "__main__":
	parser = par.Parserrr()
	filename = sys.argv[1]
	result = parser.parse_file(filename, debug = True)
	incode = parser.irrrcode
	tunnelTab = parser.parserObj.tunnelTab
	tunnelTab.rootTable.addEntry("_temp", "INTEGER", "simplevar")
	tunnelTab.rootTable.addEntry("_temp1", "INTEGER", "simplevar")
	xtras = parser.parserObj.xtras
	global incode
	global tunnelTab
	global xtras
	print(mipsgen())
	# mipsgen()

# .data
# fin: .asciiz "maze1.dat"      # filename for input
# buffer: .asciiz ""

# .text
# #open a file for writing
# li   $v0, 13       # system call for open file
# la   $a0, fin      # board file name
# li   $a1, 0        # Open for reading
# li   $a2, 0
# syscall            # open a file (file descriptor returned in $v0)
# move $s6, $v0      # save the file descriptor

# #read from file
# li   $v0, 14       # system call for read from file
# move $a0, $s6      # file descriptor
# la   $a1, buffer   # address of buffer to which to read
# li   $a2, 1024     # hardcoded buffer length
# syscall            # read from file

# # Close the file
# li   $v0, 16       # system call for close file
# move $a0, $s6      # file descriptor to close
# syscall            # close file
