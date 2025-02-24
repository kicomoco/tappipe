import argparse
import sys
import serial
import tappipe
import paho.mqtt.client as mqtt
import json
import pickle
import logging

parser = argparse.ArgumentParser(
    prog="tappipe",
	description="Tigo TAP->CCA RS485 Power Report Decoder",
)

parser.add_argument('-s', '--mqtt-server', help='MQTT Server IP Address', required=True)
parser.add_argument('-p', '--mqtt-port', help='MQTT Server Port', required=False)
parser.add_argument('-u', '--mqtt-username', help='MQTT Server Username', required=False)
parser.add_argument('-w', '--mqtt-password', help='MQTT Server Password', required=False)
parser.add_argument('-t', '--mqtt-prefix', help='MQTT Topic Prefix', required=True)
parser.add_argument('-c', '--serial-port', help='Serial Port', required=True)

args = parser.parse_args()

serialPort = serial.Serial(port=args.serial_port, baudrate=38400, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

mqttc = mqtt.Client("tappipe")

if (args.mqtt_username != None and args.mqtt_password != None):
	mqttc.username_pw_set(args.mqtt_username,args.mqtt_password)

mqttc.connect(args.mqtt_server,1883 if args.mqtt_port == None else args.mqtt_port,60)

mqttc.loop_start()

def getHex(bytes, sep=' '):
	return sep.join("{0:02x}".format(x) for x in bytes)

stream = tappipe.parser([], False, logging.NOTSET)
#stream.setDebug(True)

nodeTable = {}

def nodeTableAscii(nodeTable):
	str = "----------------------------------\n"
	str += "| NODE | ADDRESS                 |\n"
	for nodeId in nodeTable:
		str += f"| {nodeId:04} | " + getHex(nodeTable[nodeId],':') + " |\n"
	str += "----------------------------------\n"
	return str

def saveNodeTable(nodeTable):
	with open('/data/mqtt-tigo/nodeTable.pickle', 'wb') as handle:
		pickle.dump(nodeTable, handle, protocol=pickle.HIGHEST_PROTOCOL)

def loadNodeTable():
	with open('/data/mqtt-tigo/nodeTable.pickle', 'rb') as handle:
		nodeTable = pickle.load(handle)
	print("Loaded Node Table")
	print(nodeTableAscii(nodeTable))
	return nodeTable

nodeTable = loadNodeTable()

intLoops = 0
while (True):
	stream += serialPort.read(10)
	intLoops += 1
	fr = stream.fetchFrame()
	if (fr):
		intLoops = 0
		fr.process()
		if (fr.getType() == tappipe.frametype.RECV_RESP.value):
			numPackets = len(fr.processor.decoded['packets'])
			if (numPackets > 0):
				for i in range(numPackets):
					if (fr.processor.decoded['packets'][i].getType() == tappipe.pvtype.POWER_REPORT.value):
						nodeId = fr.processor.decoded['packets'][i].decoded['nodeid']
						if nodeId in nodeTable.keys():
							address = nodeTable[nodeId]
							mqttc.publish(
								args.mqtt_prefix+getHex(address,':'),
								json.dumps({
									"NodeID":nodeId,
									"Address":getHex(address,':'),
									"VIN":fr.processor.decoded['packets'][i].decoded['vin'],
									"VOUT":fr.processor.decoded['packets'][i].decoded['vout'],
									"DUTY":fr.processor.decoded['packets'][i].decoded['duty'],
									"AMPSIN":fr.processor.decoded['packets'][i].decoded['ampsin'],
									"TEMP":fr.processor.decoded['packets'][i].decoded['temp'],
									"RSSI":fr.processor.decoded['packets'][i].decoded['rssi'],
									"SLOT":fr.processor.decoded['packets'][i].decoded['slot']
								}),
								0,
								True
							)
					if (fr.processor.decoded['packets'][i].getType() == tappipe.pvtype.TOPOLOGY_REPORT.value):
						nodeId = fr.processor.decoded['packets'][i].decoded['nodeid']
						address = fr.processor.decoded['packets'][i].decoded['address']
						nodeTable[nodeId] = address
						print("Node Table Update")
						saveNodeTable(nodeTable)
						print(nodeTableAscii(nodeTable))
		if (fr.getType() == tappipe.frametype.CMD_RESP.value):
			if (fr.processor.decoded['type'] == tappipe.cmdtype.NODE_TABLE.value):
				for nodeId in fr.processor.processor.decoded['table']:
					nodeTable[nodeId] = fr.processor.processor.decoded['table'][nodeId]
				print("Node Table Update")
				saveNodeTable(nodeTable)
				print(nodeTableAscii(nodeTable))
	del fr
	if (intLoops > 50):
		print("No Frame in 50 loops, exiting...")
		quit()
