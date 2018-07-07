#!/usr/bin/python3

import os, sys
import subprocess

##variables

autorun = 0

#path for installation
pathname = "/opt"

#open and read configuration file
try: f = open("%s/droneMesh/configs/conf.dat"%pathname, "r")
except FileNotFoundError:
	print(fileErrorMsg)
	sys.exit()
conf = f.readlines()
f.close()

#find "autorun" entry
for line in conf:
	setting,value = line.split(":", 1)
	print(setting,value)
	if (setting == "autorun"):
		try: autorun = int(value)
		except ValueError:
			sys.exit()
		break
		
#run run.py if autorun is not 0
if (autorun != 0):
	subprocess.run(["sudo", "%s/droneMesh/run.py"%pathname])
	
