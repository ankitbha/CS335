import sys

def inputIR():
	pass

def getReg():
	pass

def setLoc():
	pass

def getLoc():
	pass

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():
	if len(sys.argv) == 2:
	    filename = str(sys.argv[1])
	else:
	    print("Too many or too few arguements")
	    exit()

	incode = open(filename).read().splitlines()
	print(incode)

	for line in incode:
		line = line.split(', ')
		for var in line:
			if(var not in reserved and var not isInt(var)):
				#add var to variable list
				#add in addressdisp ans symbl table


# 	for instr in instrlist:
# 	templist = instr.split(', ')
# 	if templist[1] not in ['label', 'call', 'function']:
# 		varlist = varlist + templist 
# varlist = list(set(varlist))
# varlist = [x for x in varlist if not isnumber(x)]
# for word in tackeywords:
# 	if word in varlist:
# 		varlist.remove(word)
# addressDescriptor = addressDescriptor.fromkeys(varlist, "mem")
# symbolTable = addressDescriptor.fromkeys(varlist, ["live", None])



if __name__ == "__main__":
	keyword = ['ifgoto', 'goto', 'return', 'call', 'print', 'label', 'function', 'exit']
	relation = ['<=', '>=', '==', '>', '<', '!=', '=']
	mathop = ['+', '-', '*', '/', '%']
    boolop = ['&', '|', '!']
    reserved = keyword + relation + mathop + boolop
    
    main()


	

# if len(sys.argv) == 2:
# 	filename = str(sys.argv[1])
# else:
# 	print("usage: python codegen.py irfile")
# 	exit()

# irfile = open(filename, 'r')
# ircode = irfile.read()
# ircode = ircode.strip('\n')

# # Consruct the instruction list
# instrlist = []
# instrlist = ircode.split('\n')

# nextuseTable = [None for i in range(len(instrlist))]

# # Construct the variable list and the address discriptor table
# for instr in instrlist:
# 	templist = instr.split(', ')
# 	if templist[1] not in ['label', 'call', 'function']:
# 		varlist = varlist + templist 
# varlist = list(set(varlist))
# varlist = [x for x in varlist if not isnumber(x)]
# for word in tackeywords:
# 	if word in varlist:
# 		varlist.remove(word)
# addressDescriptor = addressDescriptor.fromkeys(varlist, "mem")
# symbolTable = addressDescriptor.fromkeys(varlist, ["live", None])
