#!/usr/bin/python3

import os, sys

#variables

#invalid string
invalid = "Ungueltige Eingabe\n"

#modul
moduls = {1:"Kontrollstation", 2:"Drohne", 3:"Repeater"}
modul = "none"

#autorun on or off
autorun = False

#pathname
pathname = "/opt"

#check directory, must be *pathname*
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
		print(invalid)
		
#configuration file
conf = open("%s/droneMesh/conf.dat"%pathname,"w")


#choose modul
while True:
	#get user input
	print("Waehlen sie das zu installierende Modul:\n1: %s\n2: %s\n3: %s"%(moduls[1],moduls[2],moduls[3]))
	inp = input()
	#parse uer input
	try: modul = int(inp)
	except ValueError:
		print(invalid)
		continue
		
	#check if user input is valid
	if((modul<1) or (modul>3)):
		print(invalid)
		continue
	else: break
print("%s wurde ausgewaehlt"%moduls[modul])	


#choose autorun
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
	print(invalid)
	
#write config file
conf.write("module:%i\nautorun:%i"%(modul, int(autorun)))

#copy autostart file to /etc/init
os.system("sudo cp autorun.conf /etc/init/droneMeshAuto.conf")

#install batctl for controlling batman
os.system("sudo apt-get install batctl")

#install isc-dhcpd and vlc if modul is 1
if(modul == 1):
	#install DHCP-Server
	print("\nInstall DHCP-Server...")
	os.system("sudo apt-get install isc-dhcp-server")
	#copy configuration files for DHCP-Server
	print("\nCopy Configuration Files...")
	os.system("sudo cp dhcpd.conf /etc/dhcp/")
	
	#install vlc
	print("\nInstall VLC-Media-Player...")
	os.system("sudo apt-get install vlc")
	
#install vlc if nodul is 2
elif(modul == 2):
	#install vlc
	print("\nInstall VLC-Media-Player...")
	os.system("sudo apt-get install vlc")
	

#p = subprocess.run(["sudo", "apt-get", "install", "isc-dhcpd"])
