import struct
from .enums import pvtype

class topology_report:
	debug = False
	parent = None
	bytes = []
	decoded = {}
	def __init__(self, parent=None, bytes=[], debug=False):
		self.debug = debug
		self.parent = parent
		self.bytes = bytes
		self.decoded = {}
		(self.decoded['nodeid'],self.decoded['shortaddress'],self.decoded['nexthop'],self.decoded['address']) = struct.unpack('>xH2sxx2s8s',self.bytes[0:17])
		self.decoded['dsn'] = self.bytes[5]
		self.decoded['data_len'] = self.bytes[6]
		if (self.debug):
			print("Topology Report",self.decoded)
	def getType(self):
		return pvtype.TOPOLOGY_REPORT.value
