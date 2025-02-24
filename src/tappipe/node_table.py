import struct

class node_table:
	debug = False
	parent = None
	bytes = []
	decoded = {}
	def __init__(self, parent=None, bytes=[], debug=False):
		self.debug = debug
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
		if (self.debug):
			print("Node Table",self.decoded['records'])
			print("Table:",self.decoded['table'])
