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
