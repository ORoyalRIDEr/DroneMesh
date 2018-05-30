#!/usr/bin/python3

import os

#stop dhcpcd to configure network interfaces
#os.system("service dhcpcd stop")

#run batman module
os.system("modprobe batman-adv")

#find wifi interfaces

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
    

#set up network:
for interface in wlInt:
    print("\nsetting up %s\n"%interface)
    process = os.popen('ip link set mtu 1560 dev %s'%interface)
    process = os.popen('iwconfig %s mode ad-hoc essid droneMesh channel 1'%interface)
    process = os.popen('batctl if add %s'%interface)
    process = os.popen('ip link set up dev %s'%interface)
    
