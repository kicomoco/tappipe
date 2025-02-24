import struct
from .enums import pvtype
import logging

class topology_report:
	parent = None
	bytes = []
	decoded = {}
	def __init__(self, parent=None, bytes=[]):
		self.parent = parent
		self.bytes = bytes
		self.decoded = {}
		(self.decoded['nodeid'],self.decoded['shortaddress'],self.decoded['nexthop'],self.decoded['address']) = struct.unpack('>xH2sxx2s8s',self.bytes[0:17])
		self.decoded['dsn'] = self.bytes[5]
		self.decoded['data_len'] = self.bytes[6]
		logging.debug("Topology Report",self.decoded)
	def setDebug(self, debug):
		self.debug = debug
	def setLogLevel(self, logLevel):
		self.loglevel = logLevel
	def getType(self):
		return pvtype.TOPOLOGY_REPORT.value
