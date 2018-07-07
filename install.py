#!/usr/bin/python3

import os, sys

##variables

#error messages
#invalid input
invInpMsg = "Ungueltige Eingabe\n"

#module to be installed
moduls = {1:"Kontrollstation", 2:"Drohne", 3:"Repeater"}
module = "none"

#autorun on or off
autorun = False

#path for installation
pathname = "/opt"

##check directory, must be *pathname*
path = os.path.dirname(os.path.abspath(sys.argv[0]))
if (path != "%s/droneMesh"%pathname):
	while True:
		#get user input
		print("Sie befinden sich nicht im Ordner '%s/droneMesh'. Sollen alle Dateien dorthin verschoben werden? (j/n)"%pathname)
		inp = input()
		if(inp == 'j'): 
			print("Dateien werden verschoben...")
			os.system("sudo cp -r ../droneMesh %s"%pathname)
			break
		elif(inp == 'n'): 
			print("Verschieben sie die Dateien bitte manuell und starten sie die Installation neu.")
			sys.exit()
			break
		print(invInpMsg)
		
#configuration file
conf = open("%s/droneMesh/configs/conf.dat"%pathname,"w")


##choose module
while True:
	#get user input
	print("Waehlen sie das zu installierende Modul:\n1: %s\n2: %s\n3: %s"%(moduls[1],moduls[2],moduls[3]))
	inp = input()
	#parse uer input
	try: module  = int(inp)
	except ValueError:
		print(invInpMsg)
		continue
		
	#check if user input is valid
	if(not((module-1) in range(3))):
		print(invInpMsg)
		continue
	else: break
print("%s wurde ausgewaehlt"%moduls[module])	


##choose autorun
while True:
	#get user input
	print("Soll das Modul im Autostart geladen werden? (j/n)")
	inp = input()
	if(inp == 'j'): 
		autorun = True
		break
	elif(inp == 'n'): 
		autorun = False
		break
	print(invInpMsg)
	
#write config file
conf.write("module:%i\nautorun:%i"%(module, int(autorun)))

#set "autorun.py" to autostart via /etc/rc.local
insertLine = "%s/droneMesh/autorun.py &\n"%pathname
f = open("/etc/rc.local", "r")
cont = f.readlines()
f.close()
#check if entry already exists
entryFound = 0
for line in cont:
	if (line == insertLine):
		entryFound = 1
		break
#if not found, insert entry
if (entryFound == 0):
	newFileCont = []
	entryWritten = 0
	for line in cont:
		#skip comment lines
		if (not(entryWritten) and (line[0] != "#")):
			newFileCont.append(insertLine)
			entryWritten = 1
			
		newFileCont.append(line)
	#write to file
	f = open("/etc/rc.local", "w")
	newFileCont = "".join(newFileCont)
	f.write(newFileCont)
	f.close()
	 

#install batctl for controlling batman
os.system("sudo apt-get install batctl")

##run module dependent processes

#install isc-dhcpd and vlc if module is control station
if(module == 1):
	#install DHCP-Server
	print("\nInstall DHCP-Server...")
	os.system("sudo apt-get install isc-dhcp-server")
	#copy configuration files for DHCP-Server
	print("\nCopy Configuration Files...")
	os.system("sudo cp configs/dhcpd.conf /etc/dhcp/")
	os.system("sudo cp configs/isc-dhcp-server /etc/default/")
	
	#install vlc
	print("\nInstall VLC-Media-Player...")
	os.system("sudo apt-get install vlc")
	
#install vlc if module is drone
elif(module == 2):
	#install vlc
	print("\nInstall VLC-Media-Player...")
	os.system("sudo apt-get install vlc")
	#copy configuration files for DHCP-Server
	print("\nCopy Configuration Files...")
	#os.system("sudo cp configs/vlcrc /home/pi/.config/vlc/") #not working, because vlc-direction doesn't exist
	
	
#create ignoredInterfaces-file if doesn't exist:
try: 
	f = open("ignoredInterfaces", "r")
	f.close()
except FileNotFoundError:
	f = open("ignoredInterfaces", "w")
	f.write("#The following network interface hw-adresses will be ignored when running the module")
	f.close()
