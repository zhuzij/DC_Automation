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
fmc_host = "fmcrestapisandbox.cisco.com"  # Add 'https://' before the host name
username = "ZijianZhu3"
password = "zWbWbe6u"

# Initialize empty lists to hold dictionaries for each object type
host_list = []
address_group_list = []
service_list = []
service_group_list = []
policy_list = []

with FMC(host=fmc_host, username=username, password=password, autodeploy=False) as fmc:
    # Initialize dictionaries to hold various objects
    all_objects = {}
     # Initialize an empty list for policies
    policy_list = []

    # Fetch and populate Policies
    policies_obj = AccessPolicies(fmc=fmc)
    response = policies_obj.get()
    print(f"acp {response=}")
    if 'items' in response:
        for policy in response[:3]['items']:
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
        # print(f"accessrule {response=}")
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
                    'commentHistoryList': rule.get('commentHistoryList', 'N/A')
                })

    # Add the Access Rule list to the all_objects dictionary
    all_objects['AccessRules'] = access_rule_list