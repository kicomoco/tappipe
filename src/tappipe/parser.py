from .frame import frame

class parser:
	debug = False
	bytes = []
	startFrame = bytearray([0xff,0x7e,0x07])                                                                                                                                    
	endFrame = bytearray([0x7e,0x08])
	def __init__(self, bytes=[], debug=False):
		self.debug = debug
		self.bytes = bytearray(bytes)
	def __add__(self, other):
		self.bytes += other
		return self
	def setDebug(self, debug):
		self.debug = debug
	def fetchFrame(self):
		frameStarted = self.bytes.find(self.startFrame)
		frameEnded = self.bytes.find(self.endFrame, frameStarted)
		if (frameStarted != -1 and frameEnded != -1):
			fr = frame(self.bytes[frameStarted:frameEnded+len(self.endFrame)], self.debug)
			self.bytes = self.bytes[frameEnded+len(self.endFrame):]
			if (fr.checkCRC()):
				return fr
		return False	

