#!/usr/bin/python3

import os, sys
import subprocess
import time

##variables

#error messages
#error with conf.dat
fileErrorMsg = "Die Installation ist fehlerhaft. Bitte installieren Sie das gewünschte Modul erneut."

#module to be run
moduls = {1:"Kontrollstation", 2:"Drohne", 3:"Repeater"}
module = "none"

#path for installation
pathname = "/opt"

##set module

#read settings.dat
try: f = open("%s/droneMesh/configs/conf.dat"%pathname, "r")
except FileNotFoundError:
	print(fileErrorMsg)
	sys.exit()

settings = f.readlines()
f.close()

#find and validate module setting
for line in settings:
	pair = line.split(":")
	if (pair[0] == "module"):
		value = pair[1]
		try: 
			module = int(value)
		except ValueError:
			print(fileErrorMsg)
			sys.exit()
		if(not((module-1) in range(3))):
			print(fileErrorMsg)
			sys.exit()

print("Starte Modul '%s'..."%moduls[module])


#stop dhcpcd to configure network interfaces
subprocess.run(["sudo", "service", "dhcpcd", "stop"])
#load module batman
subprocess.run(["sudo", "modprobe", "batman-adv"])

##find wifi interfaces

#contains wireless interfaces
wlInt = []
#table with all network interfaces
netInt = open('/proc/net/dev', 'r') 

#skip file header
for a in range(2): 
    netInt.readline()
    
#read interface that should be ignored
ignInt = []
try: 
	f = open("%s/droneMesh/configs/ignoredInterfaces"%pathname,"r")
	ignInt = f.readlines()
	#remove new line charackters:
	for i in range(len(ignInt)):
		ignInt[i] = ignInt[i].split("\n")[0]
	f.close()
except FileNotFoundError:
	#create ignoredInterfaces-file
	f = open("%s/droneMesh/configs/ignoredInterfaces"%pathname,"w")
	f.write("#The following network interface hw-adresses will be ignored when running the module")
	f.close()

lines = netInt.readlines()
for line in lines:
	#extract interface name
    interface = line.split(':')[0].split(' ')[-1] 
    #add interface if it's a wireless interface if shouldn't be ignored
    if ((interface.find("wl") != -1) and not(interface in ignInt)): wlInt.append(interface) 
    

##set up network:
for interface in wlInt:
    print("\nsetting up %s\n"%interface)
    subprocess.run(["ip", "link", "set", "mtu", "1560", "dev", interface])
    subprocess.run(["iwconfig", interface, "mode", "ad-hoc", "essid", "droneMesh", "channel", "1"])
    subprocess.run(["batctl", "if", "add", interface])
    subprocess.run(["ip", "link", "set", "up", "dev", interface])
subprocess.run(["ip", "link", "set", "up", "dev", "bat0"])
    
    
##run module dependent processes

#control station
if (module == 1):
	#set ip address
	for interface in wlInt:
		subprocess.run(["sudo", "ip", "addr", "add", "10.254.239.1/24", "dev", "bat0"])
	
	#start DHCP-Server
	subprocess.run(["sudo", "service", "isc-dhcp-server", "start"])
	
	#start VLC-Media-Player
	print("\nGeben sie ein Nicht-Administratorkonto an, mit dem der VLC-Player gestartet werden soll:")
	nonsudousr = input()
	os.system("su -c \"vlc rtp://@:5004\" %s"%nonsudousr)
	
#drone
if (module == 2):
	#set ip address
	for interface in wlInt:
		subprocess.run(["sudo", "ip", "addr", "add", "10.254.239.2/24", "dev", "bat0"])
		
	#run VLC-Media-Player
	subprocess.run(["su", "-c", "cvlc -vvv v4l2:///dev/video0 --sout '#transcode{vcodec=h264,vb=800,acodec=mpga,ab=128,channels=2,samplerate=44100}:rtp{dst=10.254.239.1,port=5004,mux=ts,sap,name=test}' --sout-keep", "pi"])
	
#repeater
if (module == 3):
	#ping DHCP Server until it's reachable:
	while True:
		p = subprocess.run(["sudo", "dhclient", "bat0", "-cf", "configs/dhclient.conf"])
		if (p != 0): break
		time.sleep(2)



    
