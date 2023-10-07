from fmcapi import *
import json

class FMCObjectManager:

    def __init__(self, cred, env):
        self.env = env
        self.cred = cred
        self.firewall_obj_dict = {}

    def fetch_objects(self, obj_class, key_name, additional_fields=[], dependency=''):
        obj_list = []
        if dependency:
            if obj_class.__name__ == "AccessRules":
                obj_instance = obj_class(fmc=self.fmc, acp_name=dependency)
                response = obj_instance.get()
                if 'items' in response:
                    for obj in response['items']:
                        obj_dict = {
                            'id': obj.get('id', 'N/A'),
                            'name': obj.get('name', 'N/A'),
                            'type': obj.get('type', 'N/A'),
                        }
                        for field in additional_fields:
                            obj_dict[field] = obj.get(field, 'N/A')
                            obj_dict["acp_name"] = dependency
                        obj_list.append(obj_dict)
                self.firewall_obj_dict[key_name] = obj_list

            elif obj_class.__name__ in ["ManualNatRules", "AutoNatRules"]:
                obj_instance = obj_class(fmc=self.fmc)
                obj_instance.nat_policy(name=dependency)
                response = obj_instance.get()
                if 'items' in response:
                    for obj in response['items']:
                        obj_dict = {
                            'id': obj.get('id', 'N/A'),
                            'name': obj.get('name', 'N/A'),
                            'type': obj.get('type', 'N/A'),
                        }
                        for field in additional_fields:
                            obj_dict[field] = obj.get(field, 'N/A')
                        obj_dict["natpolicy_name"] = dependency
                        obj_list.append(obj_dict)
                self.firewall_obj_dict[key_name] = obj_list       
        else:
            obj_instance = obj_class(fmc=self.fmc)
            response = obj_instance.get()
            if 'items' in response:
                for obj in response['items']:
                    obj_dict = {
                        'id': obj.get('id', 'N/A'),
                        'name': obj.get('name', 'N/A'),
                        'type': obj.get('type', 'N/A'),
                    }
                    for field in additional_fields:
                        obj_dict[field] = obj.get(field, 'N/A')
                    obj_list.append(obj_dict)
            self.firewall_obj_dict[key_name] = obj_list

    def run(self):
        with FMC(**self.cred, autodeploy=False) as self.fmc:
            # Fetch and populate various types of objects
            self.fetch_objects(Hosts, 'Addresses', ['id', 'name', 'type', 'value', 'description'])
            self.fetch_objects(Ranges, 'Ranges', ['id', 'name', 'value', 'description'])
            self.fetch_objects(NetworkGroups, 'AddressGroups', ['id', 'name', 'type', 'objects', 'literals', 'description'])
            self.fetch_objects(ProtocolPortObjects, 'Services', ['id', 'name', 'type', 'description', 'port', 'protocol'])
            self.fetch_objects(ICMPv4Objects, 'ICMPv4Objects', ['id', 'name', 'type', 'description', 'overrideTargetId', 'code', 'icmpType', 'overrides', 'overridable'])
            self.fetch_objects(PortObjectGroups, 'ServiceGroups', ['id', 'name', 'type', 'objects', 'literals', 'description'])
            self.fetch_objects(Applications, 'Applications', ['id', 'name', 'type'])
            self.fetch_objects(InterfaceGroups, 'InterfaceGroups', ['id', 'name', 'type', 'description', 'interfaceMode', 'interfaces'])
            self.fetch_objects(SecurityZones, 'SecurityZones', ['id', 'name', 'type', 'description', 'interfaceMode', 'interfaces'])
            self.fetch_objects(AccessPolicies, 'Policies', ['id', 'name', 'type', 'description', 'defaultAction', 'prefilterPolicySetting'])
            # print(f"{self.firewall_obj_dict['Policies']=}")
            for acp in self.firewall_obj_dict['Policies']:
                self.acp_name = acp.get('name', None)
                # print(f"{self.acp_name=}")
                self.fetch_objects(AccessRules, 'AccessRules', ['id', 'name', 'type', 'action', 'enabled', 'sendEventsToFMC', 'logFiles', 'logBegin', 'logEnd', 'variableSet', 'originalSourceNetworks', 'vlanTags', 'users', 'sourceNetworks', 'destinationNetworks', 'sourcePorts', 'destinationPorts', 'ipsPolicy', 'urls', 'sourceZones', 'destinationZones', 'applications', 'filePolicy', 'sourceSecurityGroupTags', 'destinationSecurityGroupTags', 'enableSyslog', 'newComments', 'commentHistoryList', 'acp_name'], dependency=self.acp_name)
            self.fetch_objects(PolicyAssignments, 'PolicyAssignments', ['id', 'name', 'type', 'targets', 'policy'])
            self.fetch_objects(FTDNatPolicies, 'FTDNatPolicies', ['id', 'name', 'type'])
            for natpolicy in self.firewall_obj_dict['FTDNatPolicies']:
                self.natpolicy_name = natpolicy.get('name', None)
                if self.natpolicy_name:
                    self.fetch_objects(AutoNatRules, 'AutoNatRules', ['id', 'name', 'type', 'originalNetwork', 'translatedNetwork', 'interfaceInTranslatedNetwork', 'natType', 'interfaceIpv6', 'fallThrough', 'dns', 'routeLookup', 'noProxyArp', 'netToNet', 'sourceInterface', 'destinationInterface', 'originalPort', 'translatedPort', 'serviceProtocol', 'patOptions', 'description', 'natpolicy_name'], dependency=self.natpolicy_name)
            for natpolicy in self.firewall_obj_dict['FTDNatPolicies']:
                self.natpolicy_name = natpolicy.get('name', None)
                if self.natpolicy_name:
                    self.fetch_objects(ManualNatRules, 'ManualNatRules', ['id', 'name', 'type', 'originalSource', 'originalDestination', 'translatedSource', 'translatedDestination', 'interfaceInTranslatedSource', 'interfaceInOriginalDestination', 'natType', 'interfaceIpv6', 'fallThrough', 'dns', 'routeLookup', 'noProxyArp', 'netToNet', 'sourceInterface', 'destinationInterface', 'originalSourcePort', 'translatedSourcePort', 'originalDestinationPort', 'translatedDestinationPort', 'patOptions', 'unidirectional', 'enabled', 'description', 'natpolicy_name'], dependency=self.natpolicy_name)
            # self.fetch_objects(NatRules, 'NatRules', ['id', 'name', 'type'])
            # self.fetch_objects(DeviceRecords, 'DeviceRecords', ['id', 'name', 'type', 'hostName', 'natID', 'regKey', 'license_caps', 'performanceTier', 'accessPolicy'])
            # self.fetch_objects(IPv4StaticRoutes, 'IPv4StaticRoutes', ['id', 'name', 'interfaceName', 'selectedNetworks', 'gateway', 'routeTracking', 'metricValue', 'isTunneled'])


            # Save to JSON
            json_file = 'fmc/output/firewall_obj_dict.json'  # Specify the actual path where you want to save the JSON file
            with open(json_file, 'w') as f:
                json.dump(self.firewall_obj_dict, f, indent=4)

# if __name__ == "__main__":
#     fmc_manager = FMCObjectManager(env, **cred)
#     fmc_manager.run()
