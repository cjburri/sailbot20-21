#!/usr/bin/python3
import time
import serial

BUFFER_LENGTH = 25
CHANNELS = 18
MAX_READ_ATTEMPTS = 32

buffer = []
bufferOffset = 0

print("Recieve and decode X6R Inverted SBUS Signal")

JetsonSerial = serial.Serial(
    port="/dev/ttyTHS1", # RX terminal THS1 (Port 10 on J41 Header)
    baudrate=100000,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_TWO,
)
# Wait a second to let the port initialize
time.sleep(1)


class SerialChannels:
	def __init__(self):
		self.channels = []
		self.numChannels = CHANNELS - 1

		self.frame_error = 0
		self.failsafe = 0

SerialChannels = SerialChannels()


try:

	while True:
		recieve()
		print('\t'.join("%i: %s" % (index, value) for index, value in enumerate(SerialChannels.channels)))

except KeyboardInterrupt:
    print("Exiting Program")

def recieve():
	data = None
	counter = 0

	while ((JetsonSerial.in_waiting) and (offset < BUFFER_LENGTH) and (counter < MAX_READ_ATTEMPTS)):
		data = JetsonSerial.read()

		if (offset == 0 and data != 0x0f):
			continue

		buffer[offset] = (data & 0xff)
		offset += 1

	if (offset == BUFFER_LENGTH):
		if decodeSBUS():
			if SerialChannels.failsafe:
				print("Idk this wasn't in the manual")
			if SerialChannels.frame_error:
				print("Idk this wasn't in the manual")

			if SerialChannels.failsafe or SerialChannels.frame_error:
				print("Successful decode")



	buffer = []
	offset = 0

def decodeSBUS():

	if (buffer[0] != 0x0f):
		return false
		print("Incorrect start bit")
	if (buffer[BUFFER_LENGTH - 1] != 0x00):
		return false
		print("Incorrect stop bit")

	SerialChannels.channels = []
	dataChannels = SerialChannels.channels

	dataChannels.append((buffer[1] | buffer[2] << 8) & 0x07FF) # Channel 0
	dataChannels.append((buffer[2] >> 3 | buffer[3] << 5) & 0x07FF) # Channel 1
	dataChannels.append((buffer[3] >> 6 | buffer[4] << 2 | buffer[5] << 10) & 0x07FF) # Channel 2
	dataChannels.append((buffer[5] >> 1 | buffer[6] << 7) & 0x07FF) # Channel 3
	dataChannels.append((buffer[6] >> 4 | buffer[7] << 4) & 0x07FF) # Channel 4
	dataChannels.append((buffer[7] >> 7 | buffer[8] << 1 | buffer[9] << 9) & 0x07FF) # Channel 5
	dataChannels.append((buffer[9] >> 2 | buffer[10] << 6) & 0x07FF) # Channel 6
	dataChannels.append((buffer[10] >> 5 | buffer[11] << 3) & 0x07FF) # Channel 7
	dataChannels.append((buffer[12] | buffer[13] << 8) & 0x07FF) # Channel 8
	dataChannels.append((buffer[13] >> 3 | buffer[14] << 5) & 0x07FF) # Channel 9
	dataChannels.append((buffer[14] >> 6 | buffer[15] << 2 | buffer[16] << 10) & 0x07FF) # Channel 10
	dataChannels.append((buffer[16] >> 1 | buffer[17] << 7) & 0x07FF) # Channel 11
	dataChannels.append((buffer[17] >> 4 | buffer[18] << 4) & 0x07FF) # Channel 12
	dataChannels.append((buffer[18] >> 7 | buffer[19] << 1 | buffer[20] << 9) & 0x07FF) # Channel 13
	dataChannels.append((buffer[20] >> 2 | buffer[21] << 6) & 0x07FF) # Channel 14
	dataChannels.append((buffer[21] >> 5 | buffer[22] << 3) & 0x07FF) # Channel 15

	SerialChannels.frame_error = (buffer[23] & (1 << 2)) != 0
	SerialChannels.failsafe = (buffer[23] & (1 << 3)) != 0

	return true

