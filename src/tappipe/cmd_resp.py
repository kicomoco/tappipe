import struct
from .enums import cmdtype
from .node_table import node_table
import logging

class cmd_resp:
	parent = None
	bytes = []
	decoded = {}
	processor = None
	def __init__(self, parent=None, bytes=[]):
		self.parent = parent
		self.bytes = bytes
		self.decoded = {}
		self.processor = None
		keys = ['address','type']
		values = struct.unpack('>2s2s',self.bytes[0:4])
		self.decoded = dict(zip(keys, values))
		self.decoded['data'] = bytearray(self.bytes[4:])
		if (self.decoded['type'] == cmdtype.NODE_TABLE.value):
			logging.info("CMD Type is NODE_TABLE")
			self.processor = node_table(self, self.decoded['data'])
	def setDebug(self, debug):
		self.debug = debug
	def setLogLevel(self, logLevel):
		self.loglevel = logLevel