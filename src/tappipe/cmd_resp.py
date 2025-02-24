import struct
from .enums import cmdtype
from .node_table import node_table

class cmd_resp:
	debug = False
	parent = None
	bytes = []
	decoded = {}
	processor = None
	def __init__(self, parent=None, bytes=[], debug=False):
		self.debug = debug
		self.parent = parent
		self.bytes = bytes
		self.decoded = {}
		self.processor = None
		keys = ['address','type']
		values = struct.unpack('>2s2s',self.bytes[0:4])
		self.decoded = dict(zip(keys, values))
		self.decoded['data'] = bytearray(self.bytes[4:])
		if (self.decoded['type'] == cmdtype.NODE_TABLE.value):
			self.processor = node_table(self, self.decoded['data'], self.debug)
