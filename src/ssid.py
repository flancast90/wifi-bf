import subprocess

def start(code):
	r = subprocess.run(["nmcli", "-f", "SSID", "dev", "wifi"], capture_output=True, text=True).stdout
	grep = r.split("\n")

	networks = [k.strip() for k in grep if (k.strip() != "SSID") and (k.strip() != "--") and (k.strip() != "")]

	ssid = []

	filtered = [ssid.append(networks[i]) for i in range(len(networks)) if networks[i] not in ssid]
	
	if (code == 0):
		print(ssid)
	else:
		return ssid
		
if __name__ == "__main__":
	start(0)