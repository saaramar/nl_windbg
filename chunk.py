from memory import get_pte_addr, read_memory
from constants import GRANULARITY
import struct
import binascii

class Chunk(object):
	def __init__(self, chunk):
		header = read_memory(chunk - 0x10, 0x10)
		self._chunk        = chunk
		self._prevSize     = struct.unpack("<B", header[0])[0]
		self._poolIdx      = struct.unpack("<B", header[1])[0]
		self._currSize     = struct.unpack("<B", header[2])[0]
		self._type         = struct.unpack("<B", header[3])[0]
		self._tag          = header[4:8]
		self._eprocess     = header[8:]

	def printChunk(self):
		print("Chunk addr: 0x%x" % (self._chunk))
		print("\tPrevSize == 0x%x" % (self._prevSize * GRANULARITY))
		print("\tPoolIndex == 0x%x" % (self._poolIdx))
		print("\tCurrSize == 0x%x" % (self._currSize * GRANULARITY))
		print("\tType == %s" % (self.getChunkTypeString(self._type)))
		print("\tTag == %s" % repr(self._tag))

	def getPteOfPage(self):
		return get_pte_addr(self._chunk)

	# actually need to check if we are in lage page, and then
	# check PDE, but pasten, do it later
	# So remember - if we are in large page, this function is not reliable
	# Anyway, I get this from !pool, !pte, etc... - this just for fun
	def is_exe(self):
		pte_addr = self.getPteOfPage()
		pte = binascii.b2a_hex(read_memory(pte_addr + 0x7, 0x1))
		return int(pte, 0x10) & 0x80 == 0

	def getChunkTypeString(self, type):
		if type == 2:
			return "Allocated"
		elif type == 0 or type == 4:
			return "Free"
		return "Unknown"