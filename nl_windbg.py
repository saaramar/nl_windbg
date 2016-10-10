from constants import *
from basic_funcs import *
from memory import *

import struct

'''##############################################################################################################
						parsed pool internals structs - freelists, pending frees, etc.

#################################################################################################################'''

def getFreelist(size):
	ret = exeCmdParsed("dq poi(nt!NonPagedPoolDescriptor+%x)+%x"%(FREELIST_OFFSET, size))
	head = ret[1].replace("`", "")
	tail = ret[2][:0x11]

	lst = []
	while head != tail:
		head = getNextChunk(head)
		lst.append(head)

	return lst

def getFreelistLength(size):
	return len(getFreelist(size))

'''
Pending free are single-list, marked as free but not inserted to freelists yet
(only on call to nt!ExDefferedFreePool, when pendingfree are full).
Really important for exploits of UAF, refcounts issues, etc.
Read them from the NonPagedPoolDescriptor symbol in ntos
'''
def getPendingFree():
	lst = []
	curr = exeCmdParsed("dq poi(nt!NonPagedPoolDescriptor+%x)"%(PENDING_OFFSET))[1]
	for i in xrange(PENDING_SIZE):
		if not validPtr(curr):
			break
		lst.append(curr)
		curr = getNextChunk(curr)

	return lst

def getNonPagedBitmap(offset = 0, length = 0x100):
	bitmap_addr = deref("nt!MiNonPagedPoolBitMap+8")
	bitmap = read_memory(bitmap_addr + offset, length / 8)

	return bitmap

'''
allocate memory (NonPaged), copy the shellcode into it, jump
	or
set NX bit in the addr's PTE to 0, copy shellcode and jump to it
'''
def execute_shellcode(shellcode, addr = 0):
	shellcode += chr(0xcc)	# set breakpoint at the end
	if addr == 0:
		err("not supported yet on allocation")
		return STATUS_NOT_IMPLEMENTED
	else:
		set_x_pte(addr)
		write_memory(addr, shellcode)

	# now addr is +X and contains our shellcode, just jump to it
	jump(addr)
	return STATUS_SUCCESS

def execute_shellcode_shared_page(shellcode):
	set_x_pte(KERNEL_SHARED_PAGE)
	return execute_shellcode(shellcode, addr = KERNEL_SHARED_PAGE+0x50)


'''##############################################################################################################
													tracing

#################################################################################################################'''

def add_enter_func_trace(addr, argc = 4):
	cmd = '".printf \\"enter func %y'
	for i in xrange(4):
		cmd += '\\\\r\\\\n\\\\targ%d == ' % i + '0x%x'
	cmd += '\\\\r\\\\n\\",' + '%x, ' % addr + '@rcx, @rdx, @r8, @r9;g"'
	set_bp(addr, cmd)

def add_leave_func_trace(symbol):
	# ugly, for now
	func_code = exeCmd("uf %s" % symbol)
	ret_idx = func_code.index("ret")
	c3_addr = func_code[ret_idx-0x22:ret_idx-0x11].replace("`", "")
	c3_addr = int(c3_addr, 0x10)

	cmd = '".printf \\"leave func %s, retval == 0x%%p\\\\r\\\\n\\", @rax;g"' % symbol
	set_bp(c3_addr, cmd)

def trace_func(symbol):
	func_addr = get_symbol_addr(symbol)

	try:
		add_enter_func_trace(func_addr)
		add_leave_func_trace(symbol)
	except Exception, exp:
		err("exp occured - %s" % str(exp))
		return STATUS_ERROR

	trace("set enter/leave traces on the function %s" % symbol)
	return STATUS_SUCCESS