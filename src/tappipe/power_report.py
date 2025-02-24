import struct
from .enums import pvtype
import logging
from .stringhex import stringhex

class power_report:
	debug = False
	loglevel = logging.NOTSET
	parent = None
	bytes = []
	decoded = {'nodeid':None,'shortaddress':None,'vin':None,'vout':None,'duty':None,'ampsin':None,'temp':None,'slot':None,'rssi':None}
	def __init__(self, parent=None, bytes=[], debug=False, logging=logging.NOTSET):
		self.loglevel = logging
		self.debug = debug
		if (self.debug):
			self.loglevel = logging.DEBUG
		self.parent = parent
		self.bytes = bytes
		self.decoded = {'nodeid':None,'shortaddress':None,'vin':None,'vout':None,'duty':None,'ampsin':None,'temp':None,'slot':None,'rssi':None}
		
		if (len(self.bytes) < 17):
			logging.info("Power Report: Not enough bytes")
			return
		(self.decoded['nodeid'],self.decoded['shortaddress'],self.decoded['slot']) = struct.unpack('>xHHxxxxxxxxxxxxH',self.bytes[0:19])
		self.decoded['vin'] = ((self.bytes[7] << 4) + (self.bytes[8] >> 4)) * 0.05
		self.decoded['vout'] = (((self.bytes[8] & 0xf) << 8) + self.bytes[9]) * 0.1
		self.decoded['duty'] = self.bytes[10]
		self.decoded['ampsin'] = ((self.bytes[11] << 4) + (self.bytes[12] >> 4)) * 0.005
		self.decoded['temp'] = (((self.bytes[12] & 0xf) << 8) + self.bytes[13]) * 0.1
		(self.decoded['slot'],) = struct.unpack('>H',self.bytes[17:19])
		self.decoded['rssi'] = self.bytes[19]
		logging.info("Node",self.decoded['nodeid'],"Slot",self.decoded['slot'],"VIN",self.decoded['vin'],"VOUT",self.decoded['vout'],"AMPS",self.decoded['ampsin'],"Temp",self.decoded['temp'],"RSSI",self.decoded['rssi'])
		logging.debug("Power Report",self.decoded)
		logging.debug("Bytes:",stringhex(self.bytes))
	def setDebug(self, debug):
		self.debug = debug
	def setLogLevel(self, logLevel):
		self.loglevel = logLevel
	def getType(self):
		return pvtype.POWER_REPORT.value
