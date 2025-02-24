from enum import Enum

class frametype(Enum):
	RECV_RESP = bytearray([0x1, 0x49])
	CMD_RESP = bytearray([0xb, 0x10])

class cmdtype(Enum):
	NODE_TABLE = bytearray([0x0, 0x27])

class pvtype(Enum):
	POWER_REPORT = 0x31
	TOPOLOGY_REPORT = 0x9
