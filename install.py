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
conf = open("%s/droneMesh/conf.dat"%pathname,"w")


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

#copy autostart file to /etc/init
os.system("sudo cp autorun.conf /etc/init/droneMeshAuto.conf")

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
	os.system("sudo cp dhcpd.conf /etc/dhcp/")
	
	#install vlc
	print("\nInstall VLC-Media-Player...")
	os.system("sudo apt-get install vlc")
	
#install vlc if module is drone
elif(module == 2):
	#install vlc
	print("\nInstall VLC-Media-Player...")
	os.system("sudo apt-get install vlc")
	

#p = subprocess.run(["sudo", "apt-get", "install", "isc-dhcpd"])
