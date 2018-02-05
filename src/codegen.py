import sys

def inputIR():
	pass

def getReg():
	pass

def setLoc():
	pass

def getLoc():
	pass

def main():
	if len(sys.argv) == 2:
	    filename = str(sys.argv[1])
	else:
	    print("Too many or too few arguements")
	    exit()

	incode = open(filename).read().splitlines()
	print(incode)


if __name__ == "__main__":
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
