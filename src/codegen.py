import sys

class SymTab:
    def __init__(self):
        self.symtab = dict()

    def lookup(self, lexeme):
        if lexeme in self.symtab:
            return copy.deepcopy(self.symtab[str(lexeme)])
        return None

    def lookupComplete(self, lexeme):
        scope = ScopeList[currentScope]
        while scope is not None:
            entry = scope["table"].lookup(lexeme)
            if entry != None:
                return copy.deepcopy(entry)
            scope = ScopeList[scope["parent"]]
        return None

    def insertID(self, lineno, name, id_type, types=None, specifiers=[], num=1, value=None, stars=0, order=[], parameters=[], defined=False, access="public", scope=""):
        currtable = ScopeList[currentScope]["table"]
        #print("[Symbol Table]", currtable.symtab)
        if currtable.lookup(str(name)):         # No need to check again
            #print("[Symbol Table] Entry already exists")
            pass
        else:
            currtable.symtab[str(name)] = {
                "name"      : str(name),
                "id_type"   : str(id_type),
                "type"      : list([] if types is None else types),        # List of data_types
                "specifier" : list([] if specifiers is None else specifiers),    # List of type specifiers
                "num"       : int(num),            # Number of such id
                "value"     : list(value) if type(value) is list else value,           # Mostly required for const type variable
                "star"      : int(stars),
                "order"     : list(order if order else []),          # order of array in case of array
                "parameters": copy.deepcopy(parameters if parameters else []),   # Used for functions only
                "is_defined": bool(defined),
                "access"    : str(access),   # Default 'public'
                "myscope"   : str(scope if scope != ""  else str(currentScope)),
                "inc"       : False,
                "dec"       : False,
                "tac_name"  : str(name) + "_" + str(scope if scope != ""  else str(currentScope)) ,
                "offset"    : 0
        #        "size"      : size
            }
            warning = ''
            if id_type not in ["namespace", "class", "struct", "union", "object", "temporary"]:
                check_datatype(lineno, currtable.symtab[str(name)]["type"], name, id_type)
                check_specifier(lineno, currtable.symtab[str(name)]["specifier"], name)
                if types is None:
                    warning = "(warning: Type is None)"
                #print("[Symbol Table] ", warning, " Inserting new identifier: ", name, " type: ", types, "specifier: ", specifiers)
            #ScopeList[-1]["table"].numVar += 1

    def insertTemp(self, name, id_type, scope_name, types):
        if simple_type_specifier[' '.join(types)]["equiv_type"] in ["bool"]:
            types = ["int"]
        currtable = ScopeList[scope_name]["table"]
        if currtable.lookup(str(name)):         # No need to check again
            #print("[Symbol Table] Entry already exists")
            pass
        else:
            size = 4
            if ScopeList[currentScope]["scope_type"] not in ["global", "namespace_scope", "class_scope"]:
                #ScopeList[scope_name]["offset"] += size
                #offset = ScopeList[scope_name]["offset"]
                ScopeList[currentScope]["offset"] += size
                offset = ScopeList[currentScope]["offset"]
            else:
                offset = 0

            if (types is None) or (len(types) == 0):
                print("Something is Wrong!!")
            currtable.symtab[str(name)] = {
                "name"      : str(name),
                "id_type"   : str(id_type),
                "type"      : list([] if types is None else types),        # List of data_types
                "specifier" : [],    # List of type specifiers
                "num"       : 1,            # Number of such id
                "value"     : None,           # Mostly required for const type variable
                "star"      : 0,
                "order"     : [],          # order of array in case of array
                "parameters": [],   # Used for functions only
                "is_defined": False,
                "access"    : "public",
                "myscope"   : scope_name,
                "inc"       : False,
                "dec"       : False,
                "tac_name"  : str(name),
                "offset"    : 0,
                "size"      : size,
                "offset"    : offset
            }

    @staticmethod
    def addIDAttr(name, attribute, value):
        currtable = ScopeList[currentScope]["table"]
        if attribute in currtable.symtab[str(name)].keys():
            if currtable.symtab[str(name)][str(attribute)] is not None:
                currtable.symtab[str(name)][str(attribute)] += list(value)
            else:
                currtable.symtab[str(name)][str(attribute)] = list(value) if value is list else value
        else:
            currtable.symtab[str(name)].update({attribute : value})
        if attribute not in AttrList:
            AttrList.append(attribute)
        #print("[Symbol Table] Adding attribute of identifier: ", name, " attribute: ", attribute, "value: ", value)

    @staticmethod
    def updateIDAttr(name, attribute, value):
        currtable = ScopeList[currentScope]["table"]
        currtable.symtab[str(name)].update({attribute : value})
        #print("[Symbol Table] Updating attribute of identifier: ", name, " attribute: ", attribute, "value: ", value)


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
    for spillReg in regDes.keys():
    	if regDes[spillReg]==tempFarthest:
    		break;

	#write something like
	#	assembly = assembly + "movl " + regspill + ", " + var + "\n"

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
    print("#########################################################")
    #print(basicblocks)

# populating the next use table thing ----------------------- ankit

    
    for l, block in basicblocks.items():
        print(block)
        #block = line.split(', ')
        #print(block)
        for b in block[::-1]:
            b = b.split(', ')
            print(b[1],"\n")
            # nextUseTable[b[0]] = {var:symTable[var] for var in variables}
            if b[1] in mathop:
            	#print("b1 = ",b[1])
                symTable[b[2]].status = stat.DEAD
                if b[3] in variables:
                    symTable[b[3]].status = stat.LIVE
                if b[4] in variables:
                    symTable[b[4]].status = stat.LIVE

# After the implementation of symbol table, we may havev to change the code in this section.

            elif b[1] == '=':
                symTable[b[2]].status = stat.DEAD
                    if b[3] in variables: 
                        symTable[b[3]].status = stat.LIVE
            
            elif b[1] == 'ifgoto':
                continue
                # if b[3] in variables:
                #     symTable[b[3]].status = stat.LIVE
                # if b[4] in variables:
                #     symTable[b[4]].status = stat.LIVE 



nextUseTable[b[0]] = {var:symTable[var] for var in varlist}
            optr = b[1]

            # INSTRUCTION NUMBER NEEDED
            if optr == '=':
                symTable[b[2]].status = stat.DEAD
                if b[3] in varlist: 
                    symTable[b[3]].status = stat.LIVE

            elif optr in arithOp:
                symTable[b[2]].status = stat.DEAD
                if b[3] in varlist:
                    symTable[b[3]].status = stat.LIVE
                if b[4] in varlist:
                    symTable[b[4]].status = stat.LIVE

            elif optr == 'ifgoto':
                if b[3] in varlist:
                    symTable[b[3]].status = stat.LIVE
                if b[4] in varlist:
                    symTable[b[4]].status = stat.LIVE
            # TODO
            # print missing
# add other if else statements also


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
	


    vreg = {"$v0":None, "$v1":None}
    areg = {"$a0":None, "$a1":None, "$a2":None, "$a3":None}
    zreg = {"$zero":None}
    treg = {"$t0":None, "$t1":None, "$t2":None, "$t3":None, "$t4":None, "$t5":None, "$t6":None, "$t7":None, "$t8":None, "$t9":None}
    sreg = {"$s0":None, "$s1":None, "$s2":None, "$s3":None, "$s4":None, "$s5":None, "$s6":None, "$s7":None}
    preg = { "$gp" : None, "$sp" : None, "$fp" : None, "ra" : None }
    kreg = { "$k0" : None, "$k1" : None }

        # (temporaries) Caller saved if needed. Subroutines can use w/out saving (Not preserved across procedure calls)
        self.temp_regs = dict()
        for i in range(10):  self.temp_regs.update({ '$t' + str(i) : [] })

        # (saved values) - Callee saved (Preserved across procedure calls)
        self.saved_regs = dict()
        for i in range(8):  self.temp_regs.update({ '$s' + str(i) : [] })

        self.pointer_regs = { "$gp" : None, "$sp" : None, "$fp" : None, "ra" : None }

        self.general_regs = {**self.temp_regs, **self.saved_regs}

        # Floating point registers
        #self.float_regs = dict()
        #for i in range(1,24):  self.float_regs.update({ '$f' + str(i) : [] })

        # Used-Unused Regs
        #self.unused_gen_regs = list(self.general_regs.keys())
        #self.used_gen_regs = []

        #self.unused_float_regs = list(self.float_regs.keys())
		#self.used_float_regs = []




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
