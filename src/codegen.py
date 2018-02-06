import sys

def getReg(varName, numLine):
    
    #regExist=False
    emptyReg=None
    for i in regDes.keys():
    	if (regDes[i]==varName):    		
    		#regExist = True
    		return i;
    	#if(emptyReg==None and !regExist):
    	if(emptyReg==None):
    		if (regDes[i] == None):
    			emptyReg=i;
    
    if (emptyReg!=None):
    	return emptyReg;

    forNextUse=nextUseTable[numLine]
	"""
    forNextUse should be a dictionary, so nextUseTable must also be a
	dictionary with keys as line numbers and value as another dictionary
	with key being variable names and values being nextUselineNo
	"""	
    tempFarthest=None
    for var in forNextUse.keys():
        if (tempFarthest==None):
        	tempFarthest=var
        elif (forNextUse[var]>forNextUse[tempFarthest]):
        	tempFarthest=var
        else:
        	continue
    for spillReg in regDes.keys():
    	if regDes[spillReg]==tempFarthest:
    		break;

    """ write something like
		assembly = assembly + "movl " + regspill + ", " + var + "\n"
    """
    return spillReg

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
    nextuseTable = [None for i in range(len(incode))]

    leaders = [1,]
    variables = []
    
    for line in incode:
        l = line.split(', ')
        for var in l:
            if(var not in reserved and not isInt(var)):
                variables.append(var)
                #add var to variable list
                #add in addressdisp ans symbl table
    variables = list(set(variables))
    print(variables)
    for line in incode:
        l = line.split(', ')
        if 'ifgoto' in l:
            leaders.append(int(l[-1]))
            leaders.append(int(l[0])+1)
        
        elif 'goto' in l:
            leaders.append(int(l[-1]))
            leaders.append(int(l[0])+1)
        
        elif 'function' in l:
            leaders.append(int(l[0]))
        
        elif 'label' in l:
            leaders.append(int(l[0]))
    leaders = list(set(leaders))
    leaders.sort()
    print(leaders)

# generating blocks here -------------------------- ankit 

    basicblocks = {}
    num_instr = len(incode)
    for i in range(len(leaders)):
        instruction1 = leaders[i]
        if i+1<len(leaders):
            instruction2 = leaders[i+1]-1
        else:
            instruction2 = num_instr
        basicblocks[instruction1] = incode[instruction1-1:instruction2]  


# populating the next use table thing ----------------------- ankit

    
    for l, block in basicblocks.items():
        for b in block[::-1]:
            # nextUseTable[b[0]] = {var:symTable[var] for var in variables}
            if b[1] in mathop:
                # symTable[b[2]].status = stat.DEAD
             #    if b[3] in variables:
             #        symTable[b[3]].status = stat.LIVE
             #    if b[4] in variables:
             #        symTable[b[4]].status = stat.LIVE

# After the implementation of symbol table, we may havev to change the code in this section.

                continue

            elif b[1] == '=':
                continue
                # symTable[b[2]].status = stat.DEAD
                #    if b[3] in variables: 
            
                #        symTable[b[3]].status = stat.LIVE
            elif b[1] == 'ifgoto':
                continue
                # if b[3] in variables:
                #     symTable[b[3]].status = stat.LIVE
                # if b[4] in variables:
                #     symTable[b[4]].status = stat.LIVE 






#   for instr in instrlist:
#   templist = instr.split(', ')
#   if templist[1] not in ['label', 'call', 'function']:
#       varlist = varlist + templist 
# varlist = list(set(varlist))
# varlist = [x for x in varlist if not isnumber(x)]
# for word in tackeywords:
#   if word in varlist:
#       varlist.remove(word)
# addressDescriptor = addressDescriptor.fromkeys(varlist, "mem")
# symbolTable = addressDescriptor.fromkeys(varlist, ["live", None])



if __name__ == "__main__":
    keyword = ['ifgoto', 'goto', 'return', 'call', 'print', 'label', 'function', 'exit', 'return']
    relation = ['<=', '>=', '==', '>', '<', '!=', '=']
    mathop = ['+', '-', '*', '/', '%']
    boolop = ['&', '|', '!']
    reserved = keyword + relation + mathop + boolop
    
    regTuple = ()
    regDes = {}
    regDes = regDes.fromkeys(list(regTuple))

    main()


    

# if len(sys.argv) == 2:
#   filename = str(sys.argv[1])
# else:
#   print("usage: python codegen.py irfile")
#   exit()

# irfile = open(filename, 'r')
# ircode = irfile.read()
# ircode = ircode.strip('\n')

# # Consruct the instruction list
# instrlist = []
# instrlist = ircode.split('\n')

# nextuseTable = [None for i in range(len(instrlist))]

# # Construct the variable list and the address discriptor table
# for instr in instrlist:
#   templist = instr.split(', ')
#   if templist[1] not in ['label', 'call', 'function']:
#       varlist = varlist + templist 
# varlist = list(set(varlist))
# varlist = [x for x in varlist if not isnumber(x)]
# for word in tackeywords:
#   if word in varlist:
#       varlist.remove(word)
# addressDescriptor = addressDescriptor.fromkeys(varlist, "mem")
# symbolTable = addressDescriptor.fromkeys(varlist, ["live", None])
