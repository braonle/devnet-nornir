from nornir.plugins.tasks import commands
from nornir import InitNornir
from sys import argv

mac = None
if len(argv) != 2:
    mac = "ca03.15d6.0008"
else:
    mac = str(argv[1])

nr = InitNornir(config_file="config/config.yaml")

switches = nr.filter(filter_func=lambda x: "switch" in x.groups)

mac_addresses_result = switches.run(task=commands.remote_command, command="sho mac address-table | i DYNAMIC")
nr.close_connections()

sw_trunks_result = switches.run(task=commands.remote_command, command="sho int trunk | i trunking")
nr.close_connections()

trunks = {}
for x in sw_trunks_result:
    tmp = str(sw_trunks_result[x].result).lstrip(" ").rstrip(" ").splitlines()
    lst = []
    for s in tmp:
        lst.append((s.split())[0])
    trunks[x] = lst

result = None
for x in mac_addresses_result:
    tmp = str(mac_addresses_result[x].result).lstrip(" ").rstrip(" ").splitlines()
    for s in tmp:
        words = s.split()
        if words[1] == mac:
            intf = words[3]
            if intf not in trunks[x]:
                result = [x, intf]
                break
    if result is not None:
        break
if result is None:
    sw_interfaces = switches.run(task=commands.remote_command, command="sho inter | i line protocol is|Hardware")
    nr.close_connections()

    for x in sw_interfaces:
        tmp = str(sw_interfaces[x].result).lstrip(" ").rstrip(" ").splitlines()
        intf = ""
        for strings in tmp:
            strings = strings.rstrip(" ").lstrip(" ").split()
            if strings[0] != "Hardware":
                intf = strings[0]
            else:
                if strings[6] == mac:
                    result = [x, intf]
                    break
        if result is not None:
            break

if result is not None:
    print(result[0])
    print(result[1])
else:
    print("not found")