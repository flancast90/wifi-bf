import subprocess

def start(code):
	r = subprocess.run(["nmcli", "-f", "SSID", "dev", "wifi"], capture_output=True, text=True).stdout
	grep = r.split("\n")
	
	s = subprocess.run(["nmcli", "-f", "SECURITY", "dev", "wifi"], capture_output=True, text=True).stdout
	grep_s = s.split("\n")

	networks = [k.strip() for k in grep if (k.strip() != "SSID") and (k.strip() != "--") and (k.strip() != "")]
	net_type = [k.strip() for k in grep_s if (k.strip() != "SECURITY") and (k.strip() != "")]
	

	ssid = []
	security = []

	for i in range(len(networks)):
		if networks[i] not in ssid:
			ssid.append(networks[i])
			security.append(net_type[i])
	
	if (code == 0):
		print(ssid)
		print(security)
	else:
		return [ssid, security]
		
if __name__ == "__main__":
	start(0)
