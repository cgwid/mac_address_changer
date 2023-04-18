# Python MAC Address changer via CLI

There are 3 flags: -i, -m, and --help

-i is for the interface that you want to change the MAC address on
-m is the new mac address

There are checks to ensure that the both flags are supplied and checks for the format of the mac address. 
Feedback in the console for various errors/scenarios and upon successfully completing.

# To use

Example: python3 main.py -i eth0 -m 00:11:22:33:44:55
