#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='new MAC address. MAC address should be 6 '
                                                          'groups of 2 hexadecimal values separated by colons '
                                                          'and the first group must be an even value '
                                                          'Ex: 00:11:22:33:44:55')

    # parse_args returns a pair of values. A dict of the options and their values.
    # Any further values input after the arguments ex. -i value -m value other_arguments_here
    # in this specific case what is returned to variable args will not be used

    (options, args) = parser.parse_args()

    if not options.interface and not options.new_mac:
        parser.error('[-] Please specify an interface and new mac address, use --help for more info')
    elif not options.interface:
        parser.error('[-] Please specify an interface, use --help for more info')
    elif not options.new_mac:
        parser.error('[-] Please specify an interface, use --help for more info')

    # check mac address input to make sure it is a properly formatted mac address
    regex_result = mac_format_check(options.new_mac)
    if regex_result is None:
        parser.error('[-] The entered MAC address value is NOT formatted correctly. Use --help for more info')

    # check mac address input to see if first byte / group is even number per Unicast mac address rules.
    # Due to the format check above I don't believe a check needs to be made to see if pattern.match is None
    pattern = re.compile(r'^[a-f0-9][a-f0-9]')
    match = pattern.match(options.new_mac)
    first_byte = int(match.group(), 16)
    if first_byte % 2 != 0:
        parser.error('[-] The first byte of the MAC address needs to be an even number. The hexadecimal value '
                     f'"{match.group()}" = {first_byte} in decimal')

    return options


def change_mac_address(interface, new_mac):
    print(f'[+] Changing MAC address for {interface} to {new_mac}')

    # Second way of using subprocess. More secure as anything within the variable "interface
    # will be used in context of ifconfig so if it is not a flag for ifconfig then will run
    # into an error

    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(['ifconfig', interface])
    ifconfig_output_string = ifconfig_output.decode('utf-8')

    mac_pattern = re.compile(r'[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:'
                             r'[a-f0-9][a-f0-9]')

    mac_pattern_search = mac_pattern.search(ifconfig_output_string)

    if mac_pattern_search is not None:
        return mac_pattern_search.group(0)
    else:
        print(f'[-] Could not find MAC address for {options.interface} interface')


def mac_format_check(message):
    mac_pattern = re.compile(r'[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:'
                             r'[a-f0-9][a-f0-9]')
    return mac_pattern.search(message)


options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f'Current MAC = {str(current_mac)}')

if current_mac is not None:
    change_mac_address(options.interface, options.new_mac)

    current_mac = get_current_mac(options.interface)

    if current_mac == options.new_mac:
        print(f'[+] The MAC address was successfully changed to {current_mac}')
    else:
        print(f'[-] The MAC address was NOT changed successfully. The value is {current_mac}')

# Note
# First way of using subprocess below however this allows for hijacking of the script when
# also using input from the user. The user can use a semicolon to signal the end of the
# command and then run additional commands.

# subprocess.call(f'ifconfig {interface} down', shell=True)
# subprocess.call(f'ifconfig {interface} hw ether {new_mac}', shell=True)
# subprocess.call(f'ifconfig {interface} up', shell=True)
