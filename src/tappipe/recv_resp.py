import struct
from .enums import pvtype
from .power_report import power_report
from .topology_report import topology_report

def getHex(bytes):
	return " ".join("{0:02x}".format(x) for x in bytes)

class recv_resp:
	debug = False
	parent = None
	bytes = []
	decoded = {'rxBuffers':None,'txBuffers':None,'packet_number':None,'slot_number':None,'packets':[]}
	processor = None
	def __init__(self, parent=None, bytes=[], debug=False):
		self.debug = debug
		self.parent = parent
		self.bytes = bytes
		self.decoded = {'rxBuffers':None,'txBuffers':None,'packet_number':None,'slot_number':None,'packets':[]}
		self.processor = None


		if (len(self.bytes) < 2):
			return

		(status,) = struct.unpack('>H',self.bytes[0:2])
		expected_length = 2 \
			+ (1 if status & 0x1 == 0 else 0) \
			+ (1 if status & 0x2 == 0 else 0) \
			+ (2 if status & 0x4 == 0 else 0) \
			+ (2 if status & 0x8 == 0 else 0) \
			+ (2 if status & 0x10 == 0 else 1)
		actual_length = len(self.bytes) - 2
		if (actual_length < expected_length):
			return

		position = 2

		# RX Buffers
		if (status & 0x1 == 0):
			self.decoded['rxBuffers'] = self.bytes[position]
			position += 1
		# TX Buffers
		if (status & 0x2 == 0):
			self.decoded['txBuffers'] = self.bytes[position]
			position += 1
		# Unknown A
		if (status & 0x4 == 0): 
			position += 2
		# Unknown B
		if (status & 0x8 == 0):
			position += 2
		# Packet
		if (status & 0x10 == 0):
			(self.decoded['packet_number'],) = struct.unpack('>H',self.bytes[position:position+2])
			position += 2
		else:
			self.decoded['packet_number'] = self.bytes[position]
			position += 1
		# Slot Counter
		(self.decoded['slot_number'],) = struct.unpack('>H',self.bytes[position:position+2])
		position += 2
	
		datalen = len(self.bytes) - position
		packets = 1
		if (self.decoded['rxBuffers'] != None and self.decoded['rxBuffers'] != 0):
			packets = self.decoded['rxBuffers']
			packetLength = int(datalen / packets)
		else:
			packetLength = datalen


		for i in range(packets):
			if (position >= len(self.bytes)):
				return
			if (self.bytes[position] == pvtype.POWER_REPORT.value):
				self.decoded['packets'].append(power_report(self, self.bytes[position:position+packetLength]))
			if (self.bytes[position] == pvtype.TOPOLOGY_REPORT.value):
				self.decoded['packets'].append(topology_report(self, self.bytes[position:position+packetLength]))
			position += packetLength


