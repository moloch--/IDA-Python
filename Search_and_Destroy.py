####################################################################
# Search & Destroy - v0.2
# About: Simple IDA Python script to find vulnerable C functions
# By Moloch
####################################################################

import idautils
import idc

from idaapi import *


### Setup code, feel free to add more!
dangerous_functions = [
    "sprintf", 
    "strcpy",
    "strcat",
    "memcpy",
    "gets",
    "printf",
    "scanf",
]

current_address = ScreenEA()
func_lib = {}
for function in Functions(SegStart(current_address), SegEnd(current_address)):
    func_lib[GetFunctionName(function)] = function

### Main Class
class SearchAndDestroy(Choose2):

    def __init__(self, title):
        Choose2.__init__(self, title, [ ["Address", 10 | Choose2.CHCOL_HEX], ["Name", 30 | Choose2.CHCOL_PLAIN] ])
        self.title = title
        self.n = 0
        self.icon = 41
        self.PopulateItems()

    def PopulateItems(self):
        self.items = []
        for func_name in dangerous_functions:
            print "[*] Searching for ", func_name
            address = LocByName(func_name)
            if address != BADADDR:
                function = func_lib[func_name]
                code_refs = CodeRefsTo(address, 0)
                count = 0
                for ref in code_refs:
                    count += 1
                    xref = "0x%08x" % ref
                    SetColor(ref, CIC_ITEM, 0x0000ff)
                    self.items.append([xref, GetFunctionName(function), ref])
                print "[+] Found %d ref(s) to %s" % (count, func_name)
        
    def OnClose(self):
        print "[*] Closed ", self.title

    def OnSelectLine(self, index):
        idc.Jump(self.items[index][2])
        print "[*] Jumping to 0x%08x" % self.items[index][2]

    def OnGetLine(self, index):
        return self.items[index]

    def OnGetSize(self):
        return len(self.items)

    def OnDeleteLine(self, index):
        ea = self.items[index][2]
        idc.Delfunc_name(ea)
        return index

    def OnRefresh(self, index):
        self.PopulateItems()
        return index

### Start GUI
gui = SearchAndDestroy("Search and Destroy - v0.2")
gui.Show()