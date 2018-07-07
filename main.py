import RPi.GPIO as GPIO
from time import sleep
import os
import subprocess
import socket
import sys

def Shutdown(channel):
	print("Shudown!!!")
	os.system("sudo shutdown -h now")

def Restart(channel):
	print("Restart!!!")
	os.system("sudo shutdown -r now")

def led_blue():
        GPIO.output(R, GPIO.LOW)
        GPIO.output(G, GPIO.LOW)
        GPIO.output(B, GPIO.HIGH)

def led_red():
        GPIO.output(R, GPIO.HIGH)
        GPIO.output(G, GPIO.LOW)
        GPIO.output(B, GPIO.LOW)

def led_green():
        GPIO.output(R, GPIO.LOW)
        GPIO.output(G, GPIO.HIGH)
        GPIO.output(B, GPIO.LOW)

def led_off():
        GPIO.output(R, GPIO.LOW)
        GPIO.output(G, GPIO.LOW)
        GPIO.output(B, GPIO.LOW)


# Setup GPIO pins
R, G, B = 14, 15, 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)
led_off()

# Add power buttons events
GPIO.add_event_detect(20, GPIO.FALLING, callback = Shutdown, bouncetime = 200)
GPIO.add_event_detect(21, GPIO.FALLING, callback = Restart, bouncetime = 200)

# Wait connection from Android
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 1234)
sock.bind(server_address)
sock.listen(1)
led_blue()
print("Waiting for connection.")
connection, (client_ip, client_port) = sock.accept()
print("Connection accepted from %s." %client_ip)

# Scanning QR code
while True:
    led_red()
    # Take a photo
    os.system("raspistill -w 320 -h 240 -o camera.jpg --timeout 1")
    # Read QR code
    zbar = subprocess.Popen("zbarimg -q --raw /home/pi/camera.jpg", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    qrresult = zbar.stdout.readline()
    # Check scan result
    if (qrresult != ""):
        # An item was scanned
        led_green()
        print("\nQR code scan result: " + qrresult)
        connection.sendall(qrresult)
        sleep(0.5)
    else:
        sys.stdout.write('.')
        sys.stdout.flush()


