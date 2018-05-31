#!/usr/bin/python3

import os, sys

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
try: f = open("%s/droneMesh/conf.dat"%pathname, "r")
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
#os.system("service dhcpcd stop") ###  debug

#run batman module
os.system("modprobe batman-adv")

##find wifi interfaces

#contains wireless interfaces
wlInt = []
#table with all network interfaces
netInt = open('/proc/net/dev', 'r') 

#skip file header
for a in range(2): 
    netInt.readline()
    
#read interface that should be ignored
f = open("ignoredInterfaces","r")
ignInt = f.readlines()
#remove new line charackters:
for i in range(len(ignInt)):
	ignInt[i] = ignInt[i].split("\n")[0]
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
    process = os.popen('ip link set mtu 1560 dev %s'%interface)
    process = os.popen('iwconfig %s mode ad-hoc essid droneMesh channel 1'%interface)
    process = os.popen('batctl if add %s'%interface)
    process = os.popen('ip link set up dev %s'%interface)
    
    
##run module dependent processes

#control station
if (module == 1):
	#set ip address
	for interface in wlInt:
		os.system("sudo ip addr add 169.254.255.1 dev %s"%interface)
	
	#start DHCP-Server
	p = subprocess.run([]) ### run DHCP Server
	
	#start VLC-Media-Player
	os.system("")
	
#drone
if (module == 2):
	#set ip address
	for interface in wlInt:
		os.system("sudo ip addr add 169.254.255.2 dev %s"%interface) ### validate ip address
		
	#start VLC-Media-Player
	os.system("")
	
#repeater
if (module == 3):
	#ping DHCP Server:
	p = subprocess.run(["ping"], ["169.254.255.1"], ["-c"], ["2"])
	### evaluate response
	### request ip address



    
