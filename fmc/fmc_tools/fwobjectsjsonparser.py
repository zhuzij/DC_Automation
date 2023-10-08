import os
import sys
sys.path.append(os.getcwd())
import json
from common.utils import json_file_to_dict

class FWObjectsJsonParser():
    def __init__(self, env, json_file):
        self.json_file = json_file
        self.env = env
        self.fw_obj_dict = json_file_to_dict(self.json_file)
        self.output_fwobj_dict = {}

    def run(self):
        self.output_fwpol_list = []
        self.output_fwpol_dict = {}
        for rule in self.fw_obj_dict["AccessRules"]:
            # get rule name
            name = rule['name']
            # get status
            if rule['enabled'] == True:
                status = 'enable'
            else:
                status = 'disable'
            # get src int list of dict
            srcint_list = []
            for int in rule["sourceZones"][ "objects"]:
                srcint_dict = {}
                sintname = int["name"]
                srcint_dict["name"] = sintname
                srcint_list.append(srcint_dict)
            # get dst int list of dict
            dstint_list = []
            for int in rule["destinationZones"][ "objects"]:
                dstint_dict = {}
                dintname = int["name"]
                dstint_dict["name"] = dintname
                dstint_list.append(dstint_dict)
            # get action
            if rule['action'] == 'ALLOW':
                action = 'accept'
            else:
                action = 'deny'
            # get srcaddr list of dict
            srcaddr_list = []
            if isinstance(rule["sourceNetworks"], dict):
                for addr in rule["sourceNetworks"][ "objects"]:
                    srcaddr_dict = {}
                    saddrname = addr["name"]
                    srcaddr_dict["name"] = saddrname
                    srcaddr_list.append(srcaddr_dict)
            else:
                srcaddr_dict = {}
                srcaddr_dict["name"] = 'all'
                srcaddr_list.append(srcaddr_dict)
            # get dstaddr list of dict
            dstaddr_list = []
            if isinstance(rule["destinationNetworks"], dict):
                for addr in rule["destinationNetworks"][ "objects"]:
                    dstaddr_dict = {}
                    daddrname = addr["name"]
                    dstaddr_dict["name"] = daddrname
                    dstaddr_list.append(dstaddr_dict)
            else:
                dstaddr_dict = {}
                dstaddr_dict["name"] = 'all'
                dstaddr_list.append(dstaddr_dict)
            # get service list of dict
            service_list = []
            if isinstance(rule["destinationPorts"], dict):
                for svc in rule["destinationPorts"][ "objects"]:
                    service_dict = {}
                    svcname = svc["name"]
                    service_dict["name"] = svcname
                    service_list.append(service_dict)
            else:
                service_dict = {}
                service_dict["name"] = 'ALL'
                service_list.append(service_dict)
            # get comments
            comments = rule["newComments"]
            self.output_fwpol_dict = {
                'name': name,
                "status": status,
                "srcintf": srcint_list,
                "dstintf": dstint_list,
                "action": action,
                "srcaddr": srcaddr_list,
                "dstaddr": dstaddr_list,
                "service": service_list
                }
            self.output_fwpol_list.append(self.output_fwpol_dict)
        
        self.output_fwobj_dict = {
            'policies': self.output_fwpol_list
            }
        
        # Save to JSON
        json_file = f'fmc/output/{self.env}_parsed_firewall_obj_dict.json'
        with open(json_file, 'w') as f:
            json.dump(self.output_fwobj_dict, f, indent=4)
        print(f"File saved to {json_file}...")