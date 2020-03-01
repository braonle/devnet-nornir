from nornir.plugins.tasks import commands
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netconf_get, netconf_get_config
import nornir
import xml.dom.minidom

nr = nornir.InitNornir(config_file="config.yaml")

res = nr.run(task=netconf_get, filter_type="subtree", path="<interfaces xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'/>")

for x in res:
    dom = xml.dom.minidom.parseString(res[x].result)
    print(dom.toprettyxml())