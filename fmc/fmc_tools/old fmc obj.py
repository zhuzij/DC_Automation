from fmcapi import *
import json

'''
https://www.youtube.com/watch?v=4NIe3T-HjDwAuthorship and gratitude for contributors.

This python module was created by Dax Mickelson along with LOTs of help from Ryan Malloy and Neil Patel.
Thank you to the github community members who have also pitched in, especially Mark Sullivan and his team.  Feel
free to send comments/suggestions/improvements.  Either by email: dmickels@cisco.com or more importantly via a pull
request from the github repository: https://github.com/daxm/fmcapi.
'''
# Initialize FMC object
<<<<<<< HEAD:fmc/fmc_tools/test.py
fmc_host = "fmcrestapisandbox.cisco.com"  # Add 'https://' before the host name
username = "ZijianZhu3"
password = "uCdLzGMt"
=======
fmc_host = "192.168.3.37"
username = "admin"
password = "Buguan372!"
>>>>>>> c87a643d619854914e2d7f376b331a97ce85d721:fmc/fmc_tools/old fmc obj.py

# Initialize empty lists to hold dictionaries for each object type
host_list = []
address_group_list = []
service_list = []
service_group_list = []
policy_list = []

with FMC(host=fmc_host, username=username, password=password, autodeploy=False) as fmc:
    # Initialize dictionaries to hold various objects
    all_objects = {}

    # Fetch and populate Hosts (Addresses)
    hosts_obj = Hosts(fmc=fmc)
    response = hosts_obj.get()
    if 'items' in response:
        for host in response['items']:
            host_list.append({
                'id': host.get('id', 'N/A'),
                'name': host.get('name', 'N/A'),
                'type': host.get('type', 'N/A'),
                'value': host.get('value', 'N/A'),
                'description': host.get('description', 'N/A')
            })
    all_objects['Addresses'] = host_list

    # Initialize an empty list for IP Ranges
    range_list = []

    # Fetch and populate Ranges
    ranges_obj = Ranges(fmc=fmc)
    response = ranges_obj.get()
    if 'items' in response:
        for ip_range in response['items']:
            range_list.append({
                'id': ip_range.get('id', 'N/A'),
                'name': ip_range.get('name', 'N/A'),
                'value': ip_range.get('value', 'N/A'),
                'description': ip_range.get('description', 'N/A')
            })

    # Add the Range list to the all_objects dictionary
    all_objects['Ranges'] = range_list

    # Fetch and populate Address Groups
    address_groups_obj = NetworkGroups(fmc=fmc)
    response = address_groups_obj.get()
    if 'items' in response:
        for group in response['items']:
            address_group_list.append({
                'id': group.get('id', 'N/A'),
                'name': group.get('name', 'N/A'),
                'type': group.get('type', 'N/A'),
                'objects': group.get('objects', 'N/A'),
                'literals': group.get('literals', 'N/A'),
                'description': group.get('description', 'N/A')
            })
    all_objects['AddressGroups'] = address_group_list

    # Fetch and populate Services

    services_obj = ProtocolPortObjects(fmc=fmc)
    response = services_obj.get()
    if 'items' in response:
        for service in response['items']:
            service_list.append({
            'id': service.get('id', 'N/A'),
            'name': service.get('name', 'N/A'),
            'description': service.get('description', 'N/A'),
            'port': service.get('port', 'N/A'),
            'protocol': service.get('protocol', 'N/A'),
            'type': service.get('type', 'N/A')
            })

    all_objects['Services'] = service_list

    # Initialize an empty list for ICMPv4 objects
    icmpv4_list = []

    # Fetch and populate ICMPv4Objects
    icmpv4_obj = ICMPv4Objects(fmc=fmc)
    response = icmpv4_obj.get()
    if 'items' in response:
        for icmpv4 in response['items']:
            icmpv4_list.append({
                'id': icmpv4.get('id', 'N/A'),
                'name': icmpv4.get('name', 'N/A'),
                'description': icmpv4.get('description', 'N/A'),
                'type': icmpv4.get('type', 'N/A'),
                'overrideTargetId': icmpv4.get('overrideTargetId', 'N/A'),
                'code': icmpv4.get('code', 'N/A'),
                'icmpType': icmpv4.get('icmpType', 'N/A'),
                'overrides': icmpv4.get('overrides', 'N/A'),
                'overridable': icmpv4.get('overridable', 'N/A')
            })

    # Add the ICMPv4 list to the all_objects dictionary
    all_objects['ICMPv4Objects'] = icmpv4_list

    # Fetch and populate Service Groups
    service_groups_obj = PortObjectGroups(fmc=fmc)  
    response = service_groups_obj.get()
    if 'items' in response:
        for service_group in response['items']:
            service_group_list.append({
                'id': service_group.get('id', 'N/A'),
                'name': service_group.get('name', 'N/A'),
                'type': service_group.get('type', 'N/A'),
                'objects': service_group.get('objects', 'N/A'),
                'literals': service_group.get('literals', 'N/A'),
                'description': service_group.get('description', 'N/A')
            })
    all_objects['ServiceGroups'] = service_group_list

    # Initialize an empty list for applications
    application_list = []

    # Fetch and populate Applications
    applications_obj = Applications(fmc=fmc)
    response = applications_obj.get()
    if 'items' in response:
        for application in response['items']:
            application_list.append({
                'id': application.get('id', 'N/A'),
                'name': application.get('name', 'N/A'),
                'type': application.get('type', 'N/A')
            })

    # Add the application list to the all_objects dictionary
    all_objects['Applications'] = application_list

    # Initialize an empty list for Interface Groups
    interface_group_list = []

    # Fetch and populate InterfaceGroups
    interface_groups_obj = InterfaceGroups(fmc=fmc)
    response = interface_groups_obj.get()
    if 'items' in response:
        for intf_group in response['items']:
            interface_group_list.append({
                'id': intf_group.get('id', 'N/A'),
                'name': intf_group.get('name', 'N/A'),
                'description': intf_group.get('description', 'N/A'),
                'interfaceMode': intf_group.get('interfaceMode', 'N/A'),
                'interfaces': intf_group.get('interfaces', 'N/A')
            })

    # Add the Interface Group list to the all_objects dictionary
    all_objects['InterfaceGroups'] = interface_group_list

    # Initialize an empty list for Security Zones
    security_zone_list = []

    # Fetch and populate SecurityZones
    security_zones_obj = SecurityZones(fmc=fmc)
    response = security_zones_obj.get()
    if 'items' in response:
        for sec_zone in response['items']:
            security_zone_list.append({
                'id': sec_zone.get('id', 'N/A'),
                'name': sec_zone.get('name', 'N/A'),
                'type': sec_zone.get('type', 'N/A'),
                'description': sec_zone.get('description', 'N/A'),
                'interfaceMode': sec_zone.get('interfaceMode', 'N/A'),
                'interfaces': sec_zone.get('interfaces', 'N/A')
            })

    # Add the Security Zone list to the all_objects dictionary
    all_objects['SecurityZones'] = security_zone_list

    # Initialize an empty list for policies
    policy_list = []

    # Fetch and populate Policies
    policies_obj = AccessPolicies(fmc=fmc)
    response = policies_obj.get()
    if 'items' in response:
<<<<<<< HEAD:fmc/fmc_tools/test.py
        for policy in response['items']:
=======
        for policy in response['items'][:3]:
>>>>>>> c87a643d619854914e2d7f376b331a97ce85d721:fmc/fmc_tools/old fmc obj.py
            policy_list.append({
                'id': policy.get('id', 'N/A'),
                'name': policy.get('name', 'N/A'),
                'type': policy.get('type', 'N/A'),
                'description': policy.get('description', 'N/A'),
                'defaultAction': policy.get('defaultAction', 'N/A'),
                'prefilterPolicySetting': policy.get('prefilterPolicySetting', 'N/A')
            })

    # Add the policy list to the all_objects dictionary
    all_objects['Policies'] = policy_list

    # Initialize an empty list for Access Rules
    access_rule_list = []

    # Fetch and populate AccessRules for each ACP:
    for acp in  all_objects['Policies']:
        acp_name = acp['name']
        access_rules_obj = AccessRules(fmc=fmc, acp_name=acp_name)
        response = access_rules_obj.get()
        if 'items' in response:
            for rule in response['items']:
                access_rule_list.append({
                    'id': rule.get('id', 'N/A'),
                    'name': rule.get('name', 'N/A'),
                    'type': rule.get('type', 'N/A'),
                    'action': rule.get('action', 'N/A'),
                    'enabled': rule.get('enabled', 'N/A'),
                    'sendEventsToFMC': rule.get('sendEventsToFMC', 'N/A'),
                    'logFiles': rule.get('logFiles', 'N/A'),
                    'logBegin': rule.get('logBegin', 'N/A'),
                    'logEnd': rule.get('logEnd', 'N/A'),
                    'variableSet': rule.get('variableSet', 'N/A'),
                    'originalSourceNetworks': rule.get('originalSourceNetworks', 'N/A'),
                    'vlanTags': rule.get('vlanTags', 'N/A'),
                    'users': rule.get('users', 'N/A'),
                    'sourceNetworks': rule.get('sourceNetworks', 'N/A'),
                    'destinationNetworks': rule.get('destinationNetworks', 'N/A'),
                    'sourcePorts': rule.get('sourcePorts', 'N/A'),
                    'destinationPorts': rule.get('destinationPorts', 'N/A'),
                    'ipsPolicy': rule.get('ipsPolicy', 'N/A'),
                    'urls': rule.get('urls', 'N/A'),
                    'sourceZones': rule.get('sourceZones', 'N/A'),
                    'destinationZones': rule.get('destinationZones', 'N/A'),
                    'applications': rule.get('applications', 'N/A'),
                    'filePolicy': rule.get('filePolicy', 'N/A'),
                    'sourceSecurityGroupTags': rule.get('sourceSecurityGroupTags', 'N/A'),
                    'destinationSecurityGroupTags': rule.get('destinationSecurityGroupTags', 'N/A'),
                    'enableSyslog': rule.get('enableSyslog', 'N/A'),
                    'newComments': rule.get('newComments', 'N/A'),
<<<<<<< HEAD:fmc/fmc_tools/test.py
                    'commentHistoryList': rule.get('commentHistoryList', 'N/A')
=======
                    'commentHistoryList': rule.get('commentHistoryList', 'N/A'),
                    'acp_name': acp_name
>>>>>>> c87a643d619854914e2d7f376b331a97ce85d721:fmc/fmc_tools/old fmc obj.py
                })

    # Add the Access Rule list to the all_objects dictionary
    all_objects['AccessRules'] = access_rule_list

    # Initialize an empty list for Policy Assignments
    policy_assignment_list = []

    # Fetch and populate PolicyAssignments
    policy_assignments_obj = PolicyAssignments(fmc=fmc)
    response = policy_assignments_obj.get()
    if 'items' in response:
        for assignment in response['items']:
            policy_assignment_list.append({
                'id': assignment.get('id', 'N/A'),
                'name': assignment.get('name', 'N/A'),
                'type': assignment.get('type', 'N/A'),
                'targets': assignment.get('targets', 'N/A'),
                'policy': assignment.get('policy', 'N/A')
            })

    # Add the Policy Assignment list to the all_objects dictionary
    all_objects['PolicyAssignments'] = policy_assignment_list

 # Initialize an empty list for FTD NAT Policies
    ftd_nat_policy_list = []

    # Fetch and populate FTDNatPolicies
    ftd_nat_policies_obj = FTDNatPolicies(fmc=fmc)
    response = ftd_nat_policies_obj.get()
    # print(f'Response {ftd_nat_policies_obj=}')
    # for key in response:
    #     print(f'response {ftd_nat_policies_obj} {key=}')
    if 'items' in response:
        for policy in response['items']:
            ftd_nat_policy_list.append({
                'id': policy.get('id', 'N/A'),
                'name': policy.get('name', 'N/A'),
                'type': policy.get('type', 'N/A')
            })

    # Add the FTD NAT Policy list to the all_objects dictionary
    all_objects['FTDNatPolicies'] = ftd_nat_policy_list

    # Initialize an empty list for Auto NAT Rules
    auto_nat_rule_list = []

    # Fetch AutoNatRules based on FTDNatPolicies
    for natpolicy in all_objects['FTDNatPolicies']:
        natpolicy_name = natpolicy.get('name', None)
        if natpolicy_name:
            # Fetch and populate AutoNatRules
            auto_nat_rules_obj = AutoNatRules(fmc=fmc)
            auto_nat_rules_obj.nat_policy(name=natpolicy_name)
            response = auto_nat_rules_obj.get()
            print(f"auto_nat_rules_obj {response=}")
            if response and 'items' in response:
                for rule in response['items']:
                    auto_nat_rule_list.append({
                        'id': rule.get('id', 'N/A'),
                        'name': rule.get('name', 'N/A'),
                        'type': rule.get('type', 'N/A'),
                        'originalNetwork': rule.get('originalNetwork', 'N/A'),
                        'translatedNetwork': rule.get('translatedNetwork', 'N/A'),
                        'interfaceInTranslatedNetwork': rule.get('interfaceInTranslatedNetwork', 'N/A'),
                        'natType': rule.get('natType', 'N/A'),
                        'interfaceIpv6': rule.get('interfaceIpv6', 'N/A'),
                        'fallThrough': rule.get('fallThrough', 'N/A'),
                        'dns': rule.get('dns', 'N/A'),
                        'routeLookup': rule.get('routeLookup', 'N/A'),
                        'noProxyArp': rule.get('noProxyArp', 'N/A'),
                        'netToNet': rule.get('netToNet', 'N/A'),
                        'sourceInterface': rule.get('sourceInterface', 'N/A'),
                        'destinationInterface': rule.get('destinationInterface', 'N/A'),
                        'originalPort': rule.get('originalPort', 'N/A'),
                        'translatedPort': rule.get('translatedPort', 'N/A'),
                        'serviceProtocol': rule.get('serviceProtocol', 'N/A'),
                        'patOptions': rule.get('patOptions', 'N/A'),
                        'description': rule.get('description', 'N/A'),
                        'natpolicy_name': natpolicy_name
                    })

    # Add the Auto NAT Rule list to the all_objects dictionary
    all_objects['AutoNatRules'] = auto_nat_rule_list

   
    # Initialize an empty list for Manual NAT Rules
    manual_nat_rule_list = []

    # Fetch ManualNatRules based on FTDNatPolicies
    for natpolicy in all_objects['FTDNatPolicies']:
        natpolicy_name = natpolicy.get('name', None)
        if natpolicy_name:
            # Fetch and populate ManualNatRules
            manual_nat_rules_obj = ManualNatRules(fmc=fmc)
            manual_nat_rules_obj.nat_policy(name=natpolicy_name)
            response = manual_nat_rules_obj.get()
            if 'items' in response:
                for rule in response['items']:
                    manual_nat_rule_list.append({
                        'id': rule.get('id', 'N/A'),
                        'name': rule.get('name', 'N/A'),
                        'type': rule.get('type', 'N/A'),
                        'originalSource': rule.get('originalSource', 'N/A'),
                        'originalDestination': rule.get('originalDestination', 'N/A'),
                        'translatedSource': rule.get('translatedSource', 'N/A'),
                        'translatedDestination': rule.get('translatedDestination', 'N/A'),
                        'interfaceInTranslatedSource': rule.get('interfaceInTranslatedSource', 'N/A'),
                        'interfaceInOriginalDestination': rule.get('interfaceInOriginalDestination', 'N/A'),
                        'natType': rule.get('natType', 'N/A'),
                        'interfaceIpv6': rule.get('interfaceIpv6', 'N/A'),
                        'fallThrough': rule.get('fallThrough', 'N/A'),
                        'dns': rule.get('dns', 'N/A'),
                        'routeLookup': rule.get('routeLookup', 'N/A'),
                        'noProxyArp': rule.get('noProxyArp', 'N/A'),
                        'netToNet': rule.get('netToNet', 'N/A'),
                        'sourceInterface': rule.get('sourceInterface', 'N/A'),
                        'destinationInterface': rule.get('destinationInterface', 'N/A'),
                        'originalSourcePort': rule.get('originalSourcePort', 'N/A'),
                        'translatedSourcePort': rule.get('translatedSourcePort', 'N/A'),
                        'originalDestinationPort': rule.get('originalDestinationPort', 'N/A'),
                        'translatedDestinationPort': rule.get('translatedDestinationPort', 'N/A'),
                        'patOptions': rule.get('patOptions', 'N/A'),
                        'unidirectional': rule.get('unidirectional', 'N/A'),
                        'enabled': rule.get('enabled', 'N/A'),
                        'description': rule.get('description', 'N/A'),
                        'natpolicy_name': natpolicy_name
                    })

    # Add the Manual NAT Rule list to the all_objects dictionary
    all_objects['ManualNatRules'] = manual_nat_rule_list

    # NatRules class provides a way to fetch [id,name,type] of any type of nat rules - ManualNatRules or AutoNatRules
    # Initialize an empty list for NAT Rules
    nat_rule_list = []

    for natpolicy in all_objects['FTDNatPolicies']:
        natpolicy_name = natpolicy.get('name', None)
        if natpolicy_name:
            # Fetch and populate NatRules
            nat_rules_obj = NatRules(fmc=fmc)
            nat_rules_obj.nat_policy(name=natpolicy_name)
            response = nat_rules_obj.get()
            if 'items' in response:
                for rule in response['items']:
                    nat_rule_list.append({
                        'id': rule.get('id', 'N/A'),
                        'name': rule.get('name', 'N/A'),
                        'type': rule.get('type', 'N/A')
                    })

    # Add the NAT Rule list to the all_objects dictionary
    all_objects['NatRules'] = nat_rule_list

    # Initialize an empty list for Device Records
    device_record_list = []

    # Fetch and populate DeviceRecords
    device_records_obj = DeviceRecords(fmc=fmc)
    response = device_records_obj.get()
    print(f"device_records_obj {response=}")

    if response and 'items' in response:
        for record in response['items']:
            device_record_list.append({
                'id': record.get('id', 'N/A'),
                'name': record.get('name', 'N/A'),
                'type': record.get('type', 'N/A'),
                'hostName': record.get('hostName', 'N/A'),
                'natID': record.get('natID', 'N/A'),
                'regKey': record.get('regKey', 'N/A'),
                'license_caps': record.get('license_caps', 'N/A'),
                'performanceTier': record.get('performanceTier', 'N/A'),
                'accessPolicy': record.get('accessPolicy', 'N/A')
            })

    # Add the Device Record list to the all_objects dictionary
    all_objects['DeviceRecords'] = device_record_list


    # # Initialize an empty list for IPv4 Static Routes
    # ipv4_static_route_list = []

    # # Fetch and populate IPv4StaticRoutes
    # ipv4_static_routes_obj = IPv4StaticRoutes(fmc=fmc)
    # ipv4_static_routes_obj.device(device_name='')
    # response = ipv4_static_routes_obj.get()
    # print(f"ipv4_static_routes_obj {response=}")

    # if response and 'items' in response:
    #     for route in response['items']:
    #         ipv4_static_route_list.append({
    #             'id': route.get('id', 'N/A'),
    #             'name': route.get('name', 'N/A'),
    #             'interfaceName': route.get('interfaceName', 'N/A'),
    #             'selectedNetworks': route.get('selectedNetworks', 'N/A'),
    #             'gateway': route.get('gateway', 'N/A'),
    #             'routeTracking': route.get('routeTracking', 'N/A'),
    #             'metricValue': route.get('metricValue', 'N/A'),
    #             'isTunneled': route.get('isTunneled', 'N/A')
    #         })

    # # Add the IPv4 Static Route list to the all_objects dictionary
    # all_objects['IPv4StaticRoutes'] = ipv4_static_route_list



# Save to JSON
json_file = 'fmc/output/all_objects.json'  # Specify the actual path where you want to save the JSON file
with open(json_file, 'w') as f:
    json.dump(all_objects, f, indent=4)


# staticroutes:
r'''
Traceback (most recent call last):
File "c:\Users\jacki\Downloads\Homelab\DC_Automation\fmc\fmc_tools\test.py", line 378, in <module>
    response = static_routes_obj.get()
            ^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\jacki\AppData\Local\Programs\Python\Python311\Lib\site-packages\fmcapi\api_objects\apiclasstemplate.py", line 214, in get   
    if "items" not in response:
    ^^^^^^^^^^^^^^^^^^^^^^^
TypeError: argument of type 'NoneType' is not iterable
'''