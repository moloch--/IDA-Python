###################################################
# Stack Variable Calculator - v0.2
# About: Automatically finds stack variables and 
#        calculates their size in bytes
# By Moloch
###################################################
from idaapi import *

# Min buffer size to display
BUFFER_SIZE  = 0

def stack_calc(function):
	''' Calculates stack variable sizes for a given function '''
	stack_frame = GetFrame(function) 
	frame_size = GetStrucSize(stack_frame)
	frame_counter = 0
	flag = -1
	
	print "\n[*] Stack variables of %s:" % GetFunctionName(function)
	while frame_counter < frame_size:
		stack_var = GetMemberName(stack_frame, frame_counter)
		if stack_var != None:
			if flag != -1:
				size = frame_counter - flag
				if stack_var == " s":
					size -= 8
				if BUFFER_SIZE < size:
					print "    %s (%d bytes)" % (current_member, size)
				flag = frame_counter
				current_member = stack_var
			else:
				flag = frame_counter
				current_member = stack_var
			try:
				frame_counter += GetMemberSize(stack_frame, frame_counter)
			except:
				frame_counter += 1
		else:
			frame_counter += 1

### GUI Class
class StackCalculator(Choose2):

    def __init__(self, title):
        Choose2.__init__(self, title, [ ["Address", 10 | Choose2.CHCOL_HEX], ["Name", 30 | Choose2.CHCOL_PLAIN] ])
        self.title = title
        self.n = 0
        self.icon = 41
        self.PopulateItems()

    def PopulateItems(self):
        self.items = [ [hex(x), GetFunctionName(x), x] for x in idautils.Functions() ]
        
    def OnClose(self):
        print "[*] Closed ", self.title

    def OnSelectLine(self, index):
        stack_calc(self.items[index][2])

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
gui = StackCalculator("Stack Calculator - v0.2")
gui.Show()
