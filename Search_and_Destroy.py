####################################################################
# Search & Destroy - v0.1
# Simple IDA Python script to find vulnerable C functions
# By Moloch
####################################################################

from idaapi import *

dangerousFunctions = [
		"sprintf", 
		"strcpy",
		"strcat",
		"memcpy",
		"gets",
		"printf",
		"scanf",
	]
dangerousRefs = {}

print "\n\n\n *** Search & Destroy - v0.1 *** "

# Find functions and refs
for function in dangerousFunctions:
	address = LocByName(function)
	print "[*] Searching for calls to %s" % function
	if address != BADADDR:
		crossRefs = CodeRefsTo(address, 0)
		dangerousRefs[function] = []
		for ref in crossRefs:
			crossRef = "0x%08x" % ref
			SetColor(ref, CIC_ITEM, 0x0000ff)
			dangerousRefs[function].append(crossRef)
		print "[+] Found %d ref(s) to %s" % (len(dangerousRefs[function]), function)

# Display cross refs 
for entry in dangerousRefs.keys():
	title = " Cross Refrences to %s " % entry
	print "\n", "=" * len(title)
	print title
	print "=" * len(title)
	for ref in dangerousRefs[entry]:
		print ref
