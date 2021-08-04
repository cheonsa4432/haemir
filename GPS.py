#!/usr/bin/env python
import serial
import operator
import collections
import calcpoint

ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)	

def GPSparser(data):
	gps_data = data.split(",")
	idx_rmc = data.find('GNGGA')
	if data[idx_rmc:idx_rmc+5] == "GNGGA":
		data = data[idx_rmc:]	
		print(data)
		if checksum(data):
			parsed_data = data.split(",")
			return parsed_data
		else :
			print ("checksum error")

def checksum(sentence):
	sentence = sentence.strip('\n')
	nmeadata, cksum = sentence.split('*',1)
	calc_cksum = reduce(operator.xor, (ord(s) for s in nmeadata), 0)
	print (int(cksum,16), calc_cksum)
	if int(cksum,16) == calc_cksum:
		return True 
	else:
		return False 

while 1: 
	data = ser.readline()
	result = collections.defaultdict()
	res = GPSparser(data)
	if res == None:
		continue
	result['latitude'] = float(res[2])
	result['longitude'] = float(res[4])
	result['altitude'] = float(res[9])
	print (data)
	if(res == "checksum error"):
		print(res)
	print (result)
	
	print (calcpoint.grid(result['latitude']*100.0, result['longitude']*100.0))




	
