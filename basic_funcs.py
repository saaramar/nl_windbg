import pykd

def exeCmd(cmd):
	s = pykd.dbgCommand(cmd)
	return s

def exeCmdParsed(cmd):
	s = pykd.dbgCommand(cmd).replace("\n", " ").split(" ")
	s.remove("")
	lst = [parse_windbg_syntax(e) for e in s if e != ""]
	return lst

def parse_windbg_syntax(trace):
	return trace.replace("`", "").replace("-", "")

def get_register(reg):
	ret = exeCmdParsed("r%s" %(reg))
	ret = ret[0].split("=")[1]
	return int(ret, 0x10)

def deref(symbol):
	ret = exeCmdParsed("dq %s" % symbol)
	return int(ret[1], 0x10)

def get_symbol_addr(symbol):
	if isinstance(symbol, long):
		return symbol
	ret = exeCmdParsed("x %s" % symbol)
	return int(ret[0], 0x10)

def jump(addr):
	exeCmd("rrip = %x" % addr)

def set_bp(addr, cmd):
	exeCmd("bp %x %s" % (addr, cmd))

def err(trace):
	print("[*ERR*] %s" % trace)

def trace(trace):
	print("[*INF*] %s" % trace)