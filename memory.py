from basic_funcs import exeCmd, exeCmdParsed, parse_windbg_syntax

import binascii
import struct

def read_memory(addr, length):
	mem_lines = exeCmd("db %x L%x" %(addr, length)).split("\n")
	mem = ""
	for line in mem_lines:
		if line.find("  ") == -1:
			break
		mem += parse_windbg_syntax(line.split("  ")[1])
	mem = mem.replace(" ", "")
	return binascii.a2b_hex(mem)

def write_memory(addr, data):
	cmdline = binascii.b2a_hex(data)
	cmdline = ' '.join(cmdline[i:i+2] for i in range(0, len(cmdline), 2))
	exeCmd(("eb %x " + cmdline) % addr)
	return 0

def get_pte_addr(addr):
	pte_addr = addr>>9;
	pte_addr = pte_addr | 0xFFFFF68000000000;
	pte_addr = pte_addr & 0xFFFFF6FFFFFFFFF8;
	return pte_addr;

def set_x_pte(addr):
	pte_addr = get_pte_addr(addr)
	val = binascii.a2b_hex(read_memory(pte_addr, 1))
	val = struct.unpack("<B", val)[0]
	val = struct.pack("<B", val & 0x7f)
	write_memory(pte_addr, val)

'''
   +0x000 Flink            : Ptr64 _LIST_ENTRY
   +0x008 Blink            : Ptr64 _LIST_ENTRY
'''
def getNextChunk(chunk):
	ret = exeCmdParsed("dq %s" % chunk)
	return ret[1]

def getPrevChunk(chunk):
	ret = exeCmdParsed("dq %s" % chunk)
	return ret[2]

def validPtr(ptr):
	return ptr not in ["0000000000000000", "????????????????"]