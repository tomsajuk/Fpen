import socket
import sys
import pyautogui as control


control.FAILSAFE = False
width, height = control.size()
print width, height
sep = ' '

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Socket Failed due ' + msg[1]
	sys.exit()

host = '192.168.137.4'
port = 8888

try:
	remote_ip = socket.gethostbyname(host)
except socekt.gaierror:
	print 'hostname not resovled'
	sys.exit()

print 'IP address ' + remote_ip

sock.connect((remote_ip, port))
print 'Socket Connected'

def receiveInt():
	buf = ''
	while sep not in buf:
	    buf += conn.recv(8)
	return int(buf)

reply = sock.recv(4096)
print reply

curx, cury = control.position()
reply = str(curx) + sep
sock.send(reply)
reply = str(cury) + sep
sock.send(reply)
y=0

try:
	while True:
		click = receiveInt()
		x = receiveInt()
		#y = receiveInt
		print x,' ',y
		curx, cury = control.position()

		if click:
			if (curx + x < 0 & cury + y < 0):
				control.dragTo(0,0,0.3)
				continue
			if (curx + x > width & cury + y > height):
				control.dragTo(width,height,0.3)
				continue
			if (curx + x < 0):
				control.dragTo(0,cury+y,0.3)
				continue
			if (cury + y < 0):
				control.dragTo(curx+x,0,0.3)
				continue
			if (curx + x > width):
				control.dragTo(width,cury+y,0.3)
				continue
			if (cury + y > height):
				control.dragTo(curx+x,height,0.3)
				continue
			control.dragRel(x,y,0.3)

		else:
			if (curx + x < 0 & cury + y < 0):
				control.moveTo(0,0,0.3)
				continue
			if (curx + x > width & cury + y > height):
				control.moveTo(width,height,0.3)
				continue
			if (curx + x < 0):
				control.moveTo(0,cury+y,0.3)
				continue
			if (cury + y < 0):
				control.moveTo(curx+x,0,0.3)
				continue
			if (curx + x > width):
				control.moveTo(width,cury+y,0.3)
				continue
			if (cury + y > height):
				control.moveTo(curx+x,height,0.3)
				continue
			control.moveRel(x,y,0.3)

		sock.send('OK')	
except KeyboardInterrupt:
	sock.close()

sock.close()