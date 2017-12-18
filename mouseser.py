#Server program running on pi

#importing modules
import socket
import sys
import RPi.GPIO as gpio
import time

#pin definitions
echoPin = 24
trigPin = 23
butPin = 17
host = '192.168.137.4'
port = 8888
sep = ' '

#setting up RPi.GPIO
gpio.setmode(gpio.BCM)
gpio.setup(echoPin, gpio.IN)
gpio.setup(trigPin, gpio.OUT)
gpio.setup(butPin, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.output(trigPin, False)

print ("Waiting for sensor to settle")
time.sleep(1)

#calculating distance from sensor
def distance():
	gpio.output(trigPin, True)
	time.sleep(0.00001)
	gpio.output(trigPin, False)

	while gpio.input(echoPin) == 0:
		start = time.time()

	while gpio.input(echoPin) == 1:
		stop = time.time()

	duration = stop - start
	curDis = duration * 17150
	curDis = round(curDis, 0)
	#print ("DIstance = ", curDis, "cm")
	return curDis


#creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket Created'

#binding 
try:
	s.bind((host, port))
except socket.error, msg:
	print 'Socket Creation failed due to ' + msg[1]
	sys.exit()

print 'Socket Created'

#listening on the port
s.listen(1)
print 'Listening'

#accepting connection
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])
conn.send('Welcome to the mouse')

#receiving 
def receiveInt():
	buf = ''
	while sep not in buf:
	    buf += conn.recv(8)
	return int(buf)

def sendInt(x):
	reply = str(x) + sep
	return reply

prex = receiveInt()
prey = receiveInt()

print prex, prey
#y = prey
#prex = 0.00
try:
	while True:
		gpio.output(trigPin, False)
		#time.sleep(0.1)
		if gpio.input(butPin):
			conn.send(sendInt(0))
		else:
			conn.send(sendInt(1))
		x = distance()
		chax = int(x - prex) * 10
		#chay = int(y - prey) * 10
		conn.send(sendInt(chax))
		#conn.send(sendInt(chay))
		prex = x
		#prey =  y
		conn.recv(100)
except KeyboardInterrupt:
	conn.close()
	s.close()
	gpio.cleanup()


conn.close()
s.close()