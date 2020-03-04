from nornir.plugins.tasks import commands
from nornir import InitNornir
from sys import argv

show_mac = "sho mac address-table | i DYNAMIC"
show_trunk = "sho int trunk | i trunking"
show_intf_mac = "sho inter | i line protocol is|Hardware"

mac = None
if len(argv) != 2:
    mac = "0c25.0522.800a"
else:
    mac = str(argv[1])

nr = InitNornir(config_file="config/config.yaml")

switches = nr.filter(filter_func=lambda x: "switch" in x.groups)

mac_addresses_result = switches.run(task=commands.remote_command, command=show_mac)
nr.close_connections()

sw_trunks_result = switches.run(task=commands.remote_command, command=show_trunk)
nr.close_connections()

'''
Example of show interfaces trunk

Gi0/1       on               802.1q         trunking      1

'''
trunks = {}
for x in sw_trunks_result:
    tmp = str(sw_trunks_result[x].result).lstrip(" ").rstrip(" ").splitlines()
    trunks[x] = [(s.split())[0] for s in tmp]

result = None
'''
Example of show mac address-table output:

  10    0c25.0522.800a    DYNAMIC     Gi0/3

'''
for x in mac_addresses_result:
    for s in str(mac_addresses_result[x].result).lstrip(" ").rstrip(" ").splitlines():
        if s.find(mac) != -1:
            intf = (s.split())[3]
            if intf not in trunks[x]:
                result = [x, intf]
                break
    if result is not None:
        break

if result is None:
    sw_interfaces = switches.run(task=commands.remote_command, command=show_intf_mac)
    nr.close_connections()

    '''
    Example output of show interfaces:
    
    Vlan10 is up, line protocol is up 
      Hardware is Ethernet SVI, address is 0c25.056b.800a (bia 0c25.056b.800a)
    
    '''
    for x in sw_interfaces:
        intf = ""
        for strings in str(sw_interfaces[x].result).lstrip(" ").rstrip(" ").splitlines():
            if strings.find(mac) != -1:
                result = [x, intf]
                break
            else:
                intf = (strings.rstrip(" ").lstrip(" ").split())[0]

        if result is not None:
            break

if result is not None:
    print(result[0])
    print(result[1])
else:
    print("not found")

