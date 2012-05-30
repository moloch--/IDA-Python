###################################################
# Stack Variable Calculator
# By Moloch - v0.1
###################################################
from idaapi import *

# Min buffer size to display
BUFFER_SIZE  = 16

def stack_calc(function):
	''' Calculates stack variable sizes for a given function '''
	stack_frame = GetFrame(function) 
	frame_size = GetStrucSize(stack_frame)
	display_title = True
	frame_counter = 0
	flag = -1
	
	while frame_counter < frame_size:
		stack_var = GetMemberName(stack_frame, frame_counter)
		if stack_var != None:
			if flag != -1:
				size = frame_counter - flag
				if stack_var == " s":
					size -= 8
					frame_counter = frame_size
				if BUFFER_SIZE < size:
					if display_title:
						display_title = False
						print "\n[*] Function:", GetFunctionName(function)
					print "\t%s (%d bytes)" % (current_member, size)
				flag = frame_counter
				current_member = stack_var
				try:
					frame_counter += GetMemberSize(stack_frame, frame_counter)
				except:
					frame_counter += 1
			else:
				flag = frame_counter
				current_member = stack_var
				try:
					frame_counter += GetMemberSize(stack_frame, frame_counter)
				except:
					frame_counter += 1
		else:
			frame_counter += 1
###################################################
# > Start	
###################################################
current_address = ScreenEA()
print "\n\n\n*** Stack Variable Calculator - v0.1 ***"
for function in Functions(SegStart(current_address), SegEnd(current_address)):
	stack_calc(function)
		

