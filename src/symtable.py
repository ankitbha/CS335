class SymTab:
#     def __init__(self):
#         self.symtab = dict()

#     def lookup(self, lexeme):
#         if lexeme in self.symtab:
#             return copy.deepcopy(self.symtab[str(lexeme)])
#         return None

#     def lookupComplete(self, lexeme):
#         scope = ScopeList[currentScope]
#         while scope is not None:
#             entry = scope["table"].lookup(lexeme)
#             if entry != None:
#                 return copy.deepcopy(entry)
#             scope = ScopeList[scope["parent"]]
#         return None

#     def insertID(self, lineno, name, id_type, types=None, specifiers=[], num=1, value=None, stars=0, order=[], parameters=[], defined=False, access="public", scope=""):
#         currtable = ScopeList[currentScope]["table"]
#         #print("[Symbol Table]", currtable.symtab)
#         if currtable.lookup(str(name)):         # No need to check again
#             #print("[Symbol Table] Entry already exists")
#             pass
#         else:
#             currtable.symtab[str(name)] = {
#                 "name"      : str(name),
#                 "id_type"   : str(id_type),
#                 "type"      : list([] if types is None else types),        # List of data_types
#                 "specifier" : list([] if specifiers is None else specifiers),    # List of type specifiers
#                 "num"       : int(num),            # Number of such id
#                 "value"     : list(value) if type(value) is list else value,           # Mostly required for const type variable
#                 "star"      : int(stars),
#                 "order"     : list(order if order else []),          # order of array in case of array
#                 "parameters": copy.deepcopy(parameters if parameters else []),   # Used for functions only
#                 "is_defined": bool(defined),
#                 "access"    : str(access),   # Default 'public'
#                 "myscope"   : str(scope if scope != ""  else str(currentScope)),
#                 "inc"       : False,
#                 "dec"       : False,
#                 "tac_name"  : str(name) + "_" + str(scope if scope != ""  else str(currentScope)) ,
#                 "offset"    : 0
#         #        "size"      : size
#             }
#             warning = ''
#             if id_type not in ["namespace", "class", "struct", "union", "object", "temporary"]:
#                 check_datatype(lineno, currtable.symtab[str(name)]["type"], name, id_type)
#                 check_specifier(lineno, currtable.symtab[str(name)]["specifier"], name)
#                 if types is None:
#                     warning = "(warning: Type is None)"
#                 #print("[Symbol Table] ", warning, " Inserting new identifier: ", name, " type: ", types, "specifier: ", specifiers)
#             #ScopeList[-1]["table"].numVar += 1

#     def insertTemp(self, name, id_type, scope_name, types):
#         if simple_type_specifier[' '.join(types)]["equiv_type"] in ["bool"]:
#             types = ["int"]
#         currtable = ScopeList[scope_name]["table"]
#         if currtable.lookup(str(name)):         # No need to check again
#             #print("[Symbol Table] Entry already exists")
#             pass
#         else:
#             size = 4
#             if ScopeList[currentScope]["scope_type"] not in ["global", "namespace_scope", "class_scope"]:
#                 #ScopeList[scope_name]["offset"] += size
#                 #offset = ScopeList[scope_name]["offset"]
#                 ScopeList[currentScope]["offset"] += size
#                 offset = ScopeList[currentScope]["offset"]
#             else:
#                 offset = 0

#             if (types is None) or (len(types) == 0):
#                 print("Something is Wrong!!")
#             currtable.symtab[str(name)] = {
#                 "name"      : str(name),
#                 "id_type"   : str(id_type),
#                 "type"      : list([] if types is None else types),        # List of data_types
#                 "specifier" : [],    # List of type specifiers
#                 "num"       : 1,            # Number of such id
#                 "value"     : None,           # Mostly required for const type variable
#                 "star"      : 0,
#                 "order"     : [],          # order of array in case of array
#                 "parameters": [],   # Used for functions only
#                 "is_defined": False,
#                 "access"    : "public",
#                 "myscope"   : scope_name,
#                 "inc"       : False,
#                 "dec"       : False,
#                 "tac_name"  : str(name),
#                 "offset"    : 0,
#                 "size"      : size,
#                 "offset"    : offset
#             }

#     @staticmethod
#     def addIDAttr(name, attribute, value):
#         currtable = ScopeList[currentScope]["table"]
#         if attribute in currtable.symtab[str(name)].keys():
#             if currtable.symtab[str(name)][str(attribute)] is not None:
#                 currtable.symtab[str(name)][str(attribute)] += list(value)
#             else:
#                 currtable.symtab[str(name)][str(attribute)] = list(value) if value is list else value
#         else:
#             currtable.symtab[str(name)].update({attribute : value})
#         if attribute not in AttrList:
#             AttrList.append(attribute)
#         #print("[Symbol Table] Adding attribute of identifier: ", name, " attribute: ", attribute, "value: ", value)

#     @staticmethod
#     def updateIDAttr(name, attribute, value):
#         currtable = ScopeList[currentScope]["table"]
#         currtable.symtab[str(name)].update({attribute : value})
#         #print("[Symbol Table] Updating attribute of identifier: ", name, " attribute: ", attribute, "value: ", value)

