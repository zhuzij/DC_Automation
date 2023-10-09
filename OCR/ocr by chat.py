

for node in top_system_data['imdata']:
	dn = node['topSystem']['attributes']['dn']
	name = node['topSystem']['attributes']['name']
	oobMgmtAddr = node['topSystem']['attributes']['oobMgmtAddr']
	oobMgmtAddrMask = node['topSystem']['attributes']['oobMgmtAddrMask']
	role = node['topSystem']['attributes']['role']

	node_data.append({
	"dn": dn,
	"name": name,
	"oobMgmtAddr": oobMgmtAddr,
	"oobMgmtAddrMask": oobMgmtAddrMask,
	"role": role
	})

	with open('apic_top_system_output.json', 'w') as f:
	json.dump(node_data, f, indent=4)
	print("Data successfully written to apic_top_system_output.json")

	log_out = APIC_URL + "/api/aaaLogout.json"
	session.post(log_out, json={"aaaUser": {"attributes": {"name": "admin", "pwd": "cisco"}}}, verify=False)
