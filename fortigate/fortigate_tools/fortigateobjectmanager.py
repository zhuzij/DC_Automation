#*****************************************************
#     Filename: fortigateobjectmanager.py
#     Purpose: Generate FGT Object Dictionary
#     Date of creation: 9-01-2023
#     Author-Joe Zhu
#*****************************************************
#  C:\Users\jacki\Downloads\Homelab\DC_Automation\fortigate\fortigate_tools\fortigateobjectmanager.py
import json
from fortigate_api import FortigateAPI

class FortigateObjectManager:
    def __init__(self, env, cred):
        self.selected_env = env
        self.cred = cred
        self.vdom = cred['vdom']
        self.fgt_obj_output = f"fortigate/output/{self.selected_env}_{self.vdom}_objects.json"
        self.fgt = FortigateAPI(**self.cred)
        self.firewall_obj_dict = {}
        
    def fetch_objects(self):
        # Fetch various object types
        self.firewall_obj_dict = {
            'interfaces': self.fgt.interface.get(),
            'addresses': self.fgt.address.get(),
            'addrgroups': self.fgt.address_group.get(),
            'services': self.fgt.service.get(),
            'servicegrps': self.fgt.service_group.get(),
            'policies': self.fgt.policy.get(),
            'ippools': self.fgt.ip_pool.get(),
            'routes': self.fgt.static_route.get(),
            'zones': self.fgt.zone.get(),
        }
        
    def write_to_file(self):
        with open(self.fgt_obj_output, "w") as output_file:
            json.dump(self.firewall_obj_dict, output_file, indent=4)
                
    def run(self):
        self.fetch_objects()
        self.write_to_file()
