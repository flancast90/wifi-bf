import subprocess
import re

def start(code):
    try:
        # Run the macOS airport command to get a list of Wi-Fi networks
        r = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport", "-s"], capture_output=True, text=True, check=True).stdout
        lines = r.split('\n')

        ssids = []
        security_types = []

        # Skip the header line
        for line in lines[1:]:
            if line.strip():
                # Split the line by spaces, but handle spaces within SSIDs
                # The security column is usually the second to last or third to last
                parts = line.split()

                # Find the index of the security field using a regex for common security types
                security_match = re.search(r'(WPA|WPA2|WEP|OPEN)', line, re.IGNORECASE)
                if security_match:
                    # The SSID is everything before the security field
                    security = security_match.group(0)

                    # Get the part of the string before the security info
                    ssid_and_bss_part = line[:security_match.start()].strip()

                    # Split this part to isolate the SSID
                    ssid_parts = ssid_and_bss_part.split()

                    # The SSID is usually the first part
                    ssid = ssid_parts[0]

                    if ssid not in ssids:
                        ssids.append(ssid)
                        security_types.append(security)

    except FileNotFoundError:
        print("The 'airport' utility was not found. This script is for macOS.")
        return [[], []]
    except subprocess.CalledProcessError as e:
        print(f"Error running airport command: {e}")
        return [[], []]

    if code == 0:
        print(ssids)
        print(security_types)
    else:
        return [ssids, security_types]

if __name__ == "__main__":
    start(0)
