import struct
from .crc import crc
from .enums import frametype
from .recv_resp import recv_resp
from .cmd_resp import cmd_resp
import logging
from .stringhex import stringhex

class frame:
	debug = False
	loglevel = logging.NOTSET
	bytes = []
	failedCRC = False
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
	def __init__(self, bytes=[], debug=False, logging=logging.NOTSET):
		self.loglevel = logging
		self.debug = debug
		if (self.debug):
			self.loglevel = logging.DEBUG
		self.bytes = bytearray(bytes)
		self.decoded = {'address':None,'type':None}
		self.processor = None
		self.escape()
		if (len(self.bytes)<12):
			logging.debug("Frame too short")
			return
		if (self.checkCRC() == False):
			logging.debug("CRC Failed")
			return
		keys = ['address','type']
		values = struct.unpack('>xxx2s2s',self.bytes[0:7])
		self.decoded = dict(zip(keys, values))
		self.decoded['data'] = bytearray(self.bytes[7:-4])
	def setDebug(self, debug):
		self.debug = debug
	def setLogLevel(self, logLevel):
		self.loglevel = logLevel
	def checkCRC(self):
		logging.debug("Frame Bytes %s", stringhex(self.bytes))
		crc = (self.bytes[-4] << 8) + self.bytes[-3]
		test = crc(self.bytes[3:-4],self.debug)
		logging.debug("CRC From Frame is %04x", test)
		if (test.check() == crc):
			logging.info("CRC PASSED")
			self.failedCRC = False
			return True
		else:
			logging.info("CRC FAILED")
			self.failedCRC = True
			return False
	def escape(self):
		for y in self.escapeItems:
			self.bytes = self.bytes.replace(bytearray(y[0]), bytearray(y[1]))
		logging.debug("Escaped Frame Bytes %s", stringhex(self.bytes))
	def getAddress(self):
		return self.decoded['address']
	def getType(self):
		return self.decoded['type']
	def process(self):
		if (self.getType() == frametype.RECV_RESP.value):
			logging.info("Frame Type is RECV_RESP")
			self.processor = recv_resp(self, self.decoded['data'], self.debug, self.loglevel)
			
		if (self.getType() == frametype.CMD_RESP.value):
			logging.info("Frame Type is CMD_RESP")
			self.processor = cmd_resp(self, self.decoded['data'], self.debug, self.loglevel)
