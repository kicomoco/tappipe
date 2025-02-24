def stringhex(bytes):
	return ' '.join("{0:02x}".format(x) for x in bytes)