#*****************************************************
#     Filename: fortigate_api_get_objects_json_v1.py
#     Purpose: Generate FGT Object Dictionary
#     Date of creation: 9-01-2023
#     Author-Joe Zhu
#*****************************************************
 
import yaml
from fortigate_api import FortigateAPI
from common.utils import Environment_Task_Manager
# print(os.getcwd())
""" List of class objects straight from fortigate_api.py
        self.address = Address(self.rest)
        self.address_group = AddressGroup(self.rest)
        self.antivirus = Antivirus(self.rest)
        self.application = Application(self.rest)
        self.dhcp_server = DhcpServer(self.rest)
        self.external_resource = ExternalResource(self.rest)
        self.interface = Interface(self.rest)
        self.internet_service = InternetService(self.rest)
        self.ip_pool = IpPool(self.rest)
        self.policy = Policy(self.rest)
        self.schedule = Schedule(self.rest)
        self.service = Service(self.rest)
        self.service_category = ServiceCategory(self.rest)
        self.service_group = ServiceGroup(self.rest)
        self.snmp_community = SnmpCommunity(self.rest)
        self.virtual_ip = VirtualIP(self.rest)
        self.zone = Zone(self.rest)
        >> I added self.static_routes, see docstring below for details
        """
 
def load_config(config_file, env):
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    # print(config.get(env, {}))
    return config.get(env, {})

env_file = f"config/config.yaml"
environ = input('Please enter environment: (Options: lab_fortigate):\n')
config_data = load_config(config_file, environ)
fgt_obj_output = f"{fpath}/output/{environ}_{config_data.get('vdom')}_objects_json.txt"
 
# create FortigateAPI object with IP, username, password and vdom
fgt = FortigateAPI(**config_data)
 
# get to know each of the object type's dictionary structure for the purpose of parsing their useful data
# Interfaces
interfaces = fgt.interface.get()
# print(interfaces)
# Addresses
addresses = fgt.address.get()
# print(addresses)
 
# Address Groups
addrgroups = fgt.address_group.get()
# print(addrgroups)
 
# Service
services = fgt.service.get()
# print(services)
 
# Service groups
servicegrps = fgt.service_group.get()
# print(servicegrps)
 
# Firewall Policy
policies = fgt.policy.get()
# print(policies)
 
# IP Pool
ippools = fgt.ip_pool.get()
# print(ippools)
 
# VIP
vips = fgt.virtual_ip.get()
# print(vips)
 
# static routes
'''
need to modify fortigate_api.py
1. import the class:
    from fortigate_api.staticroute import StaticRoute
2. under the class builder add:
    self.static_route = StaticRoute(self.rest)
3. paste the code below to staticroute.py
"""Static Route Object."""
 
from fortigate_api.base import Base
 
class StaticRoute(Base):
    """Static Route Object."""
 
    def __init__(self, rest):
        """Static Route Object.
 
        ::
            :param rest: Fortigate REST API connector
            :type rest: Fortigate
        """
        super().__init__(rest=rest, url_obj="api/v2/cmdb/router/static")
 
'''
routes = fgt.static_route.get()
# print(routes)
zones = fgt.zone.get()
# print(zones)
 
# Write to the output file
with open(fgt_obj_output, "w") as output_file:
    # Write the objects to the file with section notes
    output_file.write("#! Interfaces:\n" + str(interfaces) + "\n\n")
    output_file.write("#! Addresses:\n" + str(addresses) + "\n\n")
    output_file.write("#! Address Groups:\n" + str(addrgroups) + "\n\n")
    output_file.write("#! Services:\n" + str(services) + "\n\n")
    output_file.write("#! Service Groups:\n" + str(servicegrps) + "\n\n")
    output_file.write("#! Policies:\n" + str(policies) + "\n\n")
    output_file.write("#! IP Pools:\n" + str(ippools) + "\n\n")
    output_file.write("#! VIPs:\n" + str(vips) + "\n\n")
    output_file.write("#! Static Routes:\n" + str(routes) + "\n\n")
    output_file.write("#! Zones:\n" + str(zones) + "\n\n")
 
# Building object Dicts:
firewall_obj_dict = {}
firewall_obj_dict['interfaces'] = interfaces
firewall_obj_dict['addresses'] = addresses
firewall_obj_dict['addrgroups'] = addrgroups
firewall_obj_dict['services'] = services
firewall_obj_dict['servicegrps'] = servicegrps
firewall_obj_dict['policies'] = policies
firewall_obj_dict['ippools'] = ippools
firewall_obj_dict['routes'] = routes
firewall_obj_dict['zones'] = zones
 
if __name__ == '__main__':
    print(firewall_obj_dict)