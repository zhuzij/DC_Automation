#*****************************************************
#     Filename: fortigate_policy_manager.py
#     Purpose: Dedup FGT FW policies using Resolved
#     Objects and write to excel for reference  
#     Date of creation: 9-27-2023
#     Author-Joe Zhu
#*****************************************************
 
import pandas as pd
from typing import List, Dict
import datetime
 
"""
Purpose of the code is to identify Fortigate policies that are identical/duplicated. All nested groups would be broken down to their member components which
are replaced with their actual values before the policy comparison.
The following policy Dict keys have been used for the comparison:
srcint
dstint
srcaddr
dstaddr
service
 
uncomment get_fgt_objects_via_api.py if anything changed at the FGT FW
To do:
need to deal with zone based if need be
need to deal with all type of protocol for service, currently only TCP/UDP/SCTP
"""


class FortigatePolicyManager:
    def __init__(self, firewall_obj_dict, selected_env_name):
        self.interfaces = firewall_obj_dict['interfaces']
        self.addresses = firewall_obj_dict['addresses']
        self.addrgroups = firewall_obj_dict['addrgroups']
        self.services = firewall_obj_dict['services']
        self.servicegrps = firewall_obj_dict['servicegrps']
        self.policies = firewall_obj_dict['policies']
        self.ippools = firewall_obj_dict['ippools']
        self.routes = firewall_obj_dict['routes']
        self.zones = firewall_obj_dict['zones']
        self.environ = selected_env_name
        self.fpath = 'fortigate/output'
        self.resolved_policies_output = f"{self.fpath}/{self.environ}_resolved_policies.txt"
        self.script_to_get_polid_disabled = f"{self.fpath}/{self.environ}_script_to_get_polid_disabled.txt"
        self.output_excel_file_for_validation = f'{self.fpath}/{self.environ}_FGT_policy_dedupd.xlsx'

    def resolve_intf_to_zone(self, name: str,
                         zones: List[Dict]) -> List[str]:
        # Initialize an empty list to store the resolved values
        resolved_zones = []
        # Check if the name exists in zones objects
        for zone in zones:
            if zone['name'] == name:
                resolved_zones.append(zone['name'])
        return resolved_zones

    def resolve_addr_to_value(self, name: str,
                     address_objects: List[Dict],
                     address_groups: List[Dict[str, List[Dict[str, str]]]]) -> List[str]:
        # Initialize an empty list to store the resolved values
        values = []
    
        # Check if the name exists in address_objects
        for obj in address_objects:
            if obj['name'] == name:
                # Handle different types of addresses
                if obj.get('type') == 'ipmask':
                    subnet = obj.get('subnet', '')
                    # Split subnet mask into octets
                    prefix = subnet.split()[0]
                    subnet_mask_octets = subnet.split()[1].split('.')
                    # Calculate the CIDR prefix length based on the subnet mask
                    prefix_length = sum(bin(int(octet)).count('1') for octet in subnet_mask_octets)
                    values.append(f"{prefix}/{prefix_length}")
                elif obj.get('type') == 'iprange':
                    values.append(f"{obj.get('start-ip', '')}-{obj.get('end-ip', '')}")
                elif obj.get('type') in ['fqdn', 'dynamic']:
                    values.append(obj.get('name', ''))
                return values
            # Check if the name exists in address_groups
        for group in address_groups:
            if group['name'] == name:
                # For each member, recursively resolve it to its value
                for member in group['member']:
                    values += self.resolve_addr_to_value(member['name'], address_objects, address_groups)
                return values
    
        # If the name does not exist in either, return an empty list
        return values
    

    def resolve_service_to_ports(self, name: str,
                             service_objects: List[Dict],
                             service_groups: List[Dict[str, List[Dict[str, str]]]]) -> List[str]:
        # Initialize an empty list to store the resolved port ranges
        port_ranges = []
    
        # Check if the name exists in service_objects
        for service in service_objects:
            if service['name'] == name:
                protocol = service.get('protocol', '')
                tcp_range = service.get('tcp-portrange', '')
                udp_range = service.get('udp-portrange', '')
                sctp_range = service.get('sctp-portrange', '')
                icmptype = str(service.get('icmptype', ''))
                icmpcode = str(service.get('icmpcode', ''))
                if protocol == 'TCP/UDP/SCTP' and tcp_range:
                    port_ranges.append(f"TCP/{tcp_range}")
                    if int(service['session-ttl']) > 0:
                        print(f"TCP/{service['name']=} {service['session-ttl']=}")
                        port_ranges.pop()
                        port_ranges.append(f"TCP/{tcp_range}_{service['session-ttl']}")
                if protocol == 'TCP/UDP/SCTP' and udp_range:
                    port_ranges.append(f"UDP/{udp_range}")
                if protocol == 'TCP/UDP/SCTP' and sctp_range:  
                    port_ranges.append(f"SCTP/{sctp_range}")
                if protocol == 'ICMP':
                    port_ranges.append(f"ICMP_{icmptype}/{icmpcode}")
                if protocol == 'IP':
                    port_ranges.append(f"IP_{service['name']}_{service['protocol-number']}")
                    # print(f"IP service: IP_{service['name']}_{service['protocol-number']}")
                if protocol == 'ALL':
                    port_ranges.append(f"ALL_{service['name']}")
                    print(f"ALL {service=}")
                # else:
                #     port_ranges.append(f"{service['name']}")
                #     print(f"WHAT {service=}")
                return port_ranges
    
        # Check if the name exists in service_groups
        for group in service_groups:
            if group['name'] == name:
                # For each member, recursively resolve it to its port ranges
                for member in group['member']:
                    port_ranges += self.resolve_service_to_ports(member['name'], service_objects, service_groups)
                return port_ranges
    
        # If the name does not exist in either, return an empty list
        return port_ranges

    def resolve_policy(self, policies: List[Dict],
                   address_objects: List[Dict],
                   address_groups: List[Dict],
                   service_objects: List[Dict],
                   service_groups: List[Dict],
                   intf_objects: List[Dict]) -> List[Dict]:
        # Initialize an empty list to store the updated policies
        updated_policies = []
    
        # Loop through each policy
        for policy in policies:
            updated_policy = policy.copy()  # Copy existing policy to avoid modifying the original
            resolved_src_addresses = []
            resolved_dst_addresses = []
            resolved_services = []
            resolved_srcintf = []
            resolved_dstintf = []
    
            # Loop through each source address in the policy
            for address in policy.get('srcaddr', []):
                # Resolve each source address to its values
                values = self.resolve_addr_to_value(address['name'], address_objects, address_groups)
                resolved_src_addresses.extend(values)
        
            # Loop through each destination address in the policy
            for address in policy.get('dstaddr', []):
                # Resolve each destination address to its values
                values = self.resolve_addr_to_value(address['name'], address_objects, address_groups)
                resolved_dst_addresses.extend(values)
    
            # Loop through each service in the policy
            for service in policy.get('service', []):
                # Resolve each service to its port ranges
                port_ranges = self.resolve_service_to_ports(service['name'], service_objects, service_groups)
                resolved_services.extend(port_ranges)
        
            # Loop through each source interfaces in the policy
            for srcintf in policy.get('srcintf', []):
                # Resolve each source interface to zone name
                srczone = self.resolve_intf_to_zone(srcintf['name'], self.zones)
                resolved_srcintf.extend(srczone)
            for dstintf in policy.get('dstintf', []):
                # Resolve each dst interface to zone name
                dstzone = self.resolve_intf_to_zone(dstintf['name'], self.zones)
                resolved_dstintf.extend(dstzone)
    
            # Update the 'srcint','srcaddr', 'dstaddr', and 'service' fields in the policy
            updated_policy['resolved_srcaddr'] = list(set(resolved_src_addresses))
            updated_policy['resolved_dstaddr'] = list(set(resolved_dst_addresses))
            updated_policy['resolved_service'] = list(set(resolved_services))
            updated_policy['resolved_srcintf'] = list(set(resolved_srcintf))
            updated_policy['resolved_dstintf'] = list(set(resolved_dstintf))
            updated_policies.append(updated_policy)
    
        return updated_policies
    
    def write_to_excel(self, duplicates, filename):    
        # Get the current date and time
        current_datetime = datetime.datetime.now()
    
        # Format the date and time as a string in the desired format
        suffix = current_datetime.strftime("%Y_%m_%d_%H_%M")
    
        # Add the suffix to the filename
        excel_file_name = filename.replace('.', f'_{suffix}.')
    
        all_duplicate_policies = []
        all_to_remove_policies = []
    
        # Loop through each tuple in the list and accumulate all policies
        for duplicate_policies, to_remove_policies in duplicates:
            all_duplicate_policies.append(duplicate_policies)
            all_to_remove_policies.append(to_remove_policies)
    
        # Convert lists of dictionaries to DataFrames
        duplicate_df = pd.DataFrame(all_duplicate_policies)
        to_remove_df = pd.DataFrame(all_to_remove_policies)
    
        # Keep only the columns that we are interested in
        columns_to_keep = ['policyid', 'srcintf', 'dstintf', 'srcaddr', 'dstaddr', 'service', 'action', 'comments',
                        'resolved_srcintf', 'resolved_dstintf', 'resolved_srcaddr', 'resolved_dstaddr', 'resolved_service']
    
        # Add a reference column next to 'policyid' referencing the policyid of the other tuple element
        duplicate_df['reference_policyid'] = to_remove_df['policyid'].values
        to_remove_df['reference_policyid'] = duplicate_df['policyid'].values
    
        # Reorder columns to have 'policyid' and 'reference_policyid' at the beginning
        columns_order = ['policyid', 'reference_policyid'] + columns_to_keep[1:]
        duplicate_df = duplicate_df[columns_order]
        to_remove_df = to_remove_df[columns_order]
    
        # Create a Pandas Excel writer using XlsxWriter as the engine
        with pd.ExcelWriter(excel_file_name, engine='openpyxl') as writer:
            # Write DataFrames to Excel sheets
            duplicate_df.to_excel(writer, sheet_name='Duplicate', index=False)
            to_remove_df.to_excel(writer, sheet_name='2bRemoved', index=False)
    
    # This function should take two policies as input and return True if they are identical
    # (ignoring names and considering the flattened address and service groups), and False otherwise.
    def policies_are_identical(self, policy1, policy2):
        """
        Checks whether two policies are identical.
    
        Arguments:
        policy1, policy2 -- dictionaries representing the policies to compare.
        Returns True if the policies are identical, and False otherwise.
        """
        return (
            set(policy1["resolved_srcaddr"]) == set(policy2["resolved_srcaddr"])
            and set(policy1["resolved_dstaddr"]) == set(policy2["resolved_dstaddr"])
            and set(policy1["resolved_service"]) == set(policy2["resolved_service"])
            and set(policy1["resolved_srcintf"]) == set(policy2["resolved_srcintf"])
            and set(policy1["resolved_dstintf"]) == set(policy2["resolved_dstintf"])
        )
    
    # Use these functions to deduplicate your list of policies. You can do this with a simple nested loop: for each policy, check if it is identical to any of
    # the policies that come after it in the list.
    # If it is, remove the duplicate. To avoid modifying the list while you're iterating over it, you can create a new list to hold the deduplicated policies.
    
    def get_duplicate_policies(self, policies):
        """Removes duplicate policies from a list of policies.
    
        Args:
            policies (list): List of policies to deduplicate.
    
        Returns:
            tuple: Tuple containing a list of deduplicated policies and a list of duplicates.
    
        """
        deduplicated_policies = []
        duplicates = []
    
        for i in range(len(policies)):
            is_duplicate = False
            for j in range(i+1, len(policies)): # avoid recursive comparison
                if self.policies_are_identical(policies[i], policies[j]):
                    duplicates.append((policies[i], policies[j]))  # Save removed/duplicated policy and survived policy
                    is_duplicate = True
                    break
            if not is_duplicate:
                deduplicated_policies.append(policies[i])
    
        return deduplicated_policies, duplicates
 

    def run(self):
        resolved_policies = self.resolve_policy(self.policies, self.addresses, self.addrgroups, self.services, self.servicegrps, self.interfaces)
        with open(self.resolved_policies_output,'w') as f:
            f.write(f"Resolved Policies:\n{str(resolved_policies)}")
        deduplicated_policies, duplicated_policies = self.get_duplicate_policies(resolved_policies)
        self.write_to_excel(duplicated_policies, self.output_excel_file_for_validation)

if __name__ == "__main__":
    manager = FortigatePolicyManager()
    manager.run()


   