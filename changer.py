import subprocess
import re
import string
import random

#RANDOM MAC GENERATOR
def random_mac ():

    #uppercased hexdigits
    uppercase_hex = "".join(set(string.hexdigits.upper()))

    #2nd character must be "0,2,4,6,8,A,C,E"
    mac = ""
    for i in range (6) :
        for j in range (2) :
            if i == 0 :
                mac+=random.choice("02468ACE")
            else :
                mac += random.choice(uppercase_hex)
        mac+=":"
    return mac.strip(":")

#GET USR MAC ADRESS
def get_usr_mac_address (iface) :
    # use the ifconfig command to get the interface details, including the MAC address
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
    return re.search("ether (.+) ", output).group().split()[1].strip()

#CHANGING MAC ADRESS
def change_mac_address (iface,new_mac_address):
    #disable network
    subprocess.check_output(f"ifconfig {iface} down",shell=True)
    #changing mac adress
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac_address}", shell=True)
    #enable network
    subprocess.check_output(f"ifconfig {iface} up",shell=True)

if __name__ == "__main__" :
    import argparse
    parse = argparse.ArgumentParser(description="MAC Changer For Linux")
    parse.add_argument("-i","--interface",help="Network interface name")
    parse.add_argument("-r","--random", action="store_true",help="Whether to generate a random MAC address")
    parse.add_argument("-m","--macaddress",help="The new MAC you want to set")
    args = parse.parse_args()
    iface = args.interface
    if args.random :
        #if random parameter set
        new_mac_address = random_mac()
    elif args.mac :
        #if new mac is set
        new_mac_address = args.mac

    #Current MAC address
    old_mac_address = get_usr_mac_address(iface)
    print(f"[*]OLD MAC ADDRESS IS : {old_mac_address}")
    #Change mac address
    change_mac_address(iface,new_mac_address)
    #Check
    new_mac_address = get_usr_mac_address(iface)
    print(f"[+]NEW MAC ADDRESS IS : {new_mac_address}")