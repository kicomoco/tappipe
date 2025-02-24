import struct
from .crc import crc
from .enums import frametype
from .recv_resp import recv_resp
from .cmd_resp import cmd_resp

class frame:
	debug = False
	bytes = []
	decoded = {'address':None,'type':None}
	escapeItems = [
		([0x7e, 0x0], [0x7e]),
		([0x7e, 0x1], [0x24]),
		([0x7e, 0x2], [0x23]),
		([0x7e, 0x3], [0x25]),
		([0x7e, 0x4], [0xa4]),
		([0x7e, 0x5], [0xa3]),
		([0x7e, 0x6], [0xa5])
	]
	processor = None
	def __init__(self, bytes=[], debug=False):
		self.debug = debug
		self.bytes = bytearray(bytes)
		self.decoded = {'address':None,'type':None}
		self.processor = None
		self.escape()
		if (len(self.bytes)<12):
			return
		if (self.checkCRC() == False):
			return
		keys = ['address','type']
		values = struct.unpack('>xxx2s2s',self.bytes[0:7])
		self.decoded = dict(zip(keys, values))
		self.decoded['data'] = bytearray(self.bytes[7:-4])
	def checkCRC(self):
		if (self.debug):
			print(" ".join("{0:02x}".format(x) for x in self.bytes))
		crc = (self.bytes[-4] << 8) + self.bytes[-3]
		if (self.debug):
			print("CRC"," ".join("{0:04x}".format(crc)))
		test = crc(self.bytes[3:-4],self.debug)
		if (self.debug):
			print("Res"," ".join("{0:04x}".format(test.check())))
		if (test.check() == crc):
			if (self.debug):
				print("CRC PASSED")
			return True
		else:
			#if (self.debug):
			print("CRC FAILED")
			return False
	def escape(self):
		for y in self.escapeItems:
			self.bytes = self.bytes.replace(bytearray(y[0]), bytearray(y[1]))
	def getAddress(self):
		return self.decoded['address']
	def getType(self):
		return self.decoded['type']
	def process(self):
		if (self.getType() == frametype.RECV_RESP.value):
			self.processor = recv_resp(self, self.decoded['data'], self.debug)
			
		if (self.getType() == frametype.CMD_RESP.value):
			self.processor = cmd_resp(self, self.decoded['data'], self.debug)
