from .frame import frame
from .stringhex import stringhex
import logging

class parser:
	bytes = []
	startFrame = bytearray([0xff,0x7e,0x07])                                                                                                                                    
	endFrame = bytearray([0x7e,0x08])
	def __init__(self, bytes=[]):
		self.bytes = bytearray(bytes)
	def __add__(self, other):
		self.bytes += other
		return self
	def setDebug(self, debug):
		self.debug = debug
	def setLogLevel(self, logLevel):
		self.loglevel = logLevel
	def fetchFrame(self):
		frameStarted = self.bytes.find(self.startFrame)
		if (frameStarted):
			logging.info("Frame Start Pattern found at %d", frameStarted)
		else:
			logging.info("Frame Start Pattern not found")
		frameEnded = self.bytes.find(self.endFrame, frameStarted)
		if (frameEnded):
			logging.info("Frame End Pattern found at %d", frameEnded)
		else:
			logging.info("Frame End Pattern not found")
		if (frameStarted != -1 and frameEnded != -1):
			fr = frame(self.bytes[frameStarted:frameEnded+len(self.endFrame)])
			self.bytes = self.bytes[frameEnded+len(self.endFrame):]
			logging.debug("Frame found with bytes %s", stringhex(fr.bytes))
			if (fr.failedCRC):
				logging.info("Frame CRC Failed")
			else:
				logging.info("Frame CRC Passed")
				return fr
		return False	

