import struct
import logging

class node_table:
	parent = None
	bytes = []
	decoded = {}
	def __init__(self, parent=None, bytes=[]):
		self.parent = parent
		self.bytes = bytes
		self.decoded = {}
		keys = ['start','records']
		values = struct.unpack('>xHH',self.bytes[0:5])
		self.decoded = dict(zip(keys, values))
		self.decoded['data'] = self.bytes[5:]
		self.decoded['table']= {}
		start = 5
		for i in range(self.decoded['records']):
			(address, nodeid) = struct.unpack('>8sH',self.bytes[start:start+10])
			self.decoded['table'][nodeid] = address
			start += 10
		logging.info("Node Table",self.decoded['records'])
		logging.info("Table:",self.decoded['table'])
	def setDebug(self, debug):
		self.debug = debug
	def setLogLevel(self, logLevel):
		self.loglevel = logLevel