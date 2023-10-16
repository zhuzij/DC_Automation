"""
explore possiblities of fortigate_api by https://github.com/vladimirs-git/fortigate-api/tree/main
"""

from fortigate_api import FortigateAPI

fgt = FortigateAPI(host="192.168.3.1", username="joe", password="Iching12#", timeout = 30) #default ignored:vdom='root')


# Get address by name
addresses_by_name = fgt.address.get(uid="10.0.0.0/8")
print(addresses_by_name)

# Create address
data = {"name": "ADDRESS",
        "obj-type": "ip",
        "subnet": "127.0.0.100 255.255.255.252",
        "type": "ipmask"}
# response = fgt.address.create(data)
# print(f"{response=}")
# # # Get all addresses
# # addresses_all = fgt.address.get()

# # Get address by name
# addresses_by_name = fgt.address.get(uid="ADDRESS")
# print(f"{addresses_by_name=}")

# Get address by operator contains \"=@\"
# addresses_contains = fgt.address.get(filter="subnet=@10.0")
# print(f"{addresses_contains=}")

# # Get address by operator contains \"=@\"
# addresses_contains = fgt.address.get(filter="name=@net")
# print(f"{addresses_contains=}")

# # Get address by operator equals \"==\"
# addresses_contains = fgt.address.get(filter="name==net_10")
# print(f"{addresses_contains=}")

from collections import Counter

counter = Counter(('a', 'b', 'c', 'a', 'b', 'b')) # list/set does make sense for counting per element
# counter = Counter({'key_1': 38, 'key_2': 91, 'key_3': 53, 'key_4': 14, 'key_5': 31}) # pass dict doesn't make sense
# Output: Counter({'b': 3, 'a': 2, 'c': 1})
print(f"{counter['b']=}")
# print(f"{counter['key_5']=}") # pass dict doesn't make sense
from collections import namedtuple
# namedtuple vs class based:
# Class-based approach
class PersonClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# namedtuple-based approach
PersonData = namedtuple('PersonData', ['name', 'age'])
p = PersonData(name="Joe", age=58)
print(p.name, p.age)
# Both serve similar purposes but namedtuple is more concise

'''
    Username ("john doe"): The space between "john" and "doe" gets encoded as %20, resulting in 'john%20doe'.

    Email ("john@doe.com"): The "@" symbol gets encoded as %40, giving us 'john%40doe.com'.

    Special Characters ("?&=#"): Each special character is encoded, resulting in %3F%26%3D%23.'''
from fortigate_api import helpers as h

nameinurl = h.quote("john doe")
print(f"{nameinurl=}")
emailinurl = h.quote("john@doe.com")
print(f"{emailinurl=}")


from collections import ChainMap
# useful for getting the value of a key in the order you specify for the chaining of dicts
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
chainmap = ChainMap(dict1, dict2)
print(f"{chainmap['b']=}")

# print os environment variables:
import os, sys
import json
print(f'{os.environ["COMPUTERNAME"]=}')

osenv = {'ALLUSERSPROFILE': 'C:\\ProgramData', 'APPDATA': 'C:\\Users\\jacki\\AppData\\Roaming', 'APPDIR_PATH': 'C:\\Users\\jacki\\AppData\\Roaming\\Free Snipping Tool\\', 'ARYA': 'C:\\Users\\jacki\\Downloads\\Homelab\\Python\\arya\\arya\\', 'ASL.LOG': 'Destination=file', 'CHOCOLATEYINSTALL': 'C:\\ProgramData\\chocolatey', 'CHOCOLATEYLASTPATHUPDATE': '133415561497464466', 'CHROME_CRASHPAD_PIPE_NAME': '\\\\.\\pipe\\crashpad_28820_RZENNTMPZQBCWBAI', 'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 'COMPUTERNAME': 'JACK-LABPC', 'COMSPEC': 'C:\\Windows\\system32\\cmd.exe', 'DRIVERDATA': 'C:\\Windows\\System32\\Drivers\\DriverData', 'EFC_3900': '1', 'HOMEDRIVE': 'C:', 'HOMEPATH': '\\Users\\jacki', 'LOCALAPPDATA': 'C:\\Users\\jacki\\AppData\\Local', 'LOGONSERVER': '\\\\JACK-LABPC', 'NUMBER_OF_PROCESSORS': '16', 'ONEDRIVE': 'C:\\Users\\jacki\\OneDrive', 'ONLINESERVICES': 'Online Services', 'ORIGINAL_XDG_CURRENT_DESKTOP': 'undefined', 'OS': 'Windows_NT', 'PATH': 'C:\\Python312\\Scripts\\;C:\\Python312\\;C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Windows\\System32\\OpenSSH\\;C:\\Program Files\\PuTTY\\;C:\\Program Files\\dotnet\\;C:\\Program Files\\Microsoft SQL Server\\Client SDK\\ODBC\\130\\Tools\\Binn\\;C:\\Program Files (x86)\\Microsoft SQL Server\\130\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\130\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\130\\DTS\\Binn\\;C:\\Program Files (x86)\\Common Files\\Acronis\\SnapAPI\\;C:\\Program Files (x86)\\Common Files\\Acronis\\VirtualFile\\;C:\\Program Files (x86)\\Common Files\\Acronis\\VirtualFile64\\;C:\\Program Files (x86)\\Common Files\\Acronis\\FileProtector\\;C:\\Program Files (x86)\\Common Files\\Acronis\\FileProtector64\\;C:\\Program Files (x86)\\Windows Kits\\10\\Windows Performance Toolkit\\;C:\\Program Files\\Git\\cmd;C:\\Program Files\\VanDyke Software\\SecureCRT\\;C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Tools\\MSVC\\14.37.32822\\bin\\Hostx64\\x64;C:\\Program Files\\nodejs\\;C:\\ProgramData\\chocolatey\\bin;C:\\Users\\jacki\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\;C:\\Users\\jacki\\AppData\\Local\\Programs\\Python\\Python311\\;C:\\Users\\jacki\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Program Files\\JetBrains\\PyCharm Community Edition 2022.2.1\\bin;C:\\Users\\jacki\\AppData\\Local\\atom\\bin;C:\\Users\\jacki\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\jacki\\AppData\\Local\\GitHubDesktop\\bin;C:\\Users\\jacki\\AppData\\Local\\Programs\\Microsoft VS Code\\bin;C:\\Program Files (x86)\\Sennheiser\\HeadSetup Pro\\Plugins;C:\\Program Files (x86)\\Sennheiser\\HeadSetup Pro\\Open Source;C:\\Program Files (x86)\\Sennheiser\\HeadSetup Pro\\External;C:\\Users\\jacki\\Downloads\\Homelab\\Python\\arya\\arya\\;C:\\Users\\jacki\\AppData\\Roaming\\npm', 'PATHEXT': '.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW;.CPL', 'PLATFORMCODE': 'M8', 'PROCESSOR_ARCHITECTURE': 'AMD64', 'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 154 Stepping 3, GenuineIntel', 'PROCESSOR_LEVEL': '6', 'PROCESSOR_REVISION': '9a03', 'PROGF81DEF27053': '1', 'PROGRAMDATA': 'C:\\ProgramData', 'PROGRAMFILES': 'C:\\Program Files', 'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 'PROGRAMW6432': 'C:\\Program Files', 'PSMODULEPATH': 'C:\\Users\\jacki\\OneDrive\\Documents\\WindowsPowerShell\\Modules;C:\\Program Files\\WindowsPowerShell\\Modules;C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\Modules;C:\\Program Files (x86)\\Microsoft SQL Server\\130\\Tools\\PowerShell\\Modules\\', 'PUBLIC': 'C:\\Users\\Public', 'PYCHARM COMMUNITY EDITION': 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2022.2.1\\bin;', 'REGIONCODE': 'NA', 'SESSIONNAME': 'Console', 'SYSTEMDRIVE': 'C:', 'SYSTEMROOT': 'C:\\Windows', 'TEMP': 'C:\\Users\\jacki\\AppData\\Local\\Temp', 'TMP': 'C:\\Users\\jacki\\AppData\\Local\\Temp', 'USERDOMAIN': 'JACK-LABPC', 'USERDOMAIN_ROAMINGPROFILE': 'JACK-LABPC', 'USERNAME': 'jacki', 'USERPROFILE': 'C:\\Users\\jacki', 'WINDIR': 'C:\\Windows', 'ZES_ENABLE_SYSMAN': '1', '__PSLOCKDOWNPOLICY': '0', 'TERM_PROGRAM': 'vscode', 'TERM_PROGRAM_VERSION': '1.83.1', 'LANG': 'en_US.UTF-8', 'COLORTERM': 'truecolor', 'GIT_ASKPASS': 'c:\\Users\\jacki\\AppData\\Local\\Programs\\Microsoft VS Code\\resources\\app\\extensions\\git\\dist\\askpass.sh', 'VSCODE_GIT_ASKPASS_NODE': 'C:\\Users\\jacki\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe', 'VSCODE_GIT_ASKPASS_EXTRA_ARGS': '--ms-enable-electron-run-as-node', 'VSCODE_GIT_ASKPASS_MAIN': 'c:\\Users\\jacki\\AppData\\Local\\Programs\\Microsoft VS Code\\resources\\app\\extensions\\git\\dist\\askpass-main.js', 'VSCODE_GIT_IPC_HANDLE': '\\\\.\\pipe\\vscode-git-680b67b555-sock', 'VSCODE_INJECTION': '1'}
# print(f"{type(osenv)=}")
osenv_json = json.dumps(osenv, indent=4)
# print(osenv_json)
# tempf = f"{os.environ['TEMP']}/OS_Environment_Variables.txt"
tempf = f"{os.getcwd()}/fortigate/output/OS_Environment_Variables.txt"
print(f"{os.getcwd()=}")
# sys.path.append(os.getcwd())
with open(tempf, 'w') as jfile:
    json.dump(osenv, jfile, indent=4)

urls = r"""Object  GUI and REST API URL to the object (FortiOS v6.4)
Address
https://192.168.3.1/ng/firewall/address

https://192.168.3.1/api/v2/cmdb/firewall/address/

AddressGroup
https://192.168.3.1/ng/firewall/address

https://192.168.3.1/api/v2/cmdb/firewall/addrgrp/

Antivirus
https://192.168.3.1/ng/utm/antivirus/profile

https://192.168.3.1/api/v2/cmdb/antivirus/profile/

Application
https://192.168.3.1/ng/utm/appctrl/sensor

https://192.168.3.1/api/v2/cmdb/application/list/

DhcpServer
https://192.168.3.1/ng/interface/edit/{name}

https://192.168.3.1/api/v2/cmdb/system.dhcp/server/

ExternalResource
https://192.168.3.1/ng/external-connector

https://192.168.3.1/api/v2/cmdb/system/external-resource/

Interface
https://192.168.3.1/ng/interface

https://192.168.3.1/api/v2/cmdb/system/interface/

InternetService
https://192.168.3.1/ng/firewall/internet_service

https://192.168.3.1/api/v2/cmdb/firewall/internet-service/

IpPool
https://192.168.3.1/ng/firewall/ip-pool

https://192.168.3.1/api/v2/cmdb/firewall/ippool/

Policy
https://192.168.3.1/ng/firewall/policy/policy/standard

https://192.168.3.1/api/v2/cmdb/firewall/policy/

Schedule
https://192.168.3.1/ng/firewall/schedule

https://192.168.3.1/api/v2/cmdb/firewall.schedule/onetime/

Service
https://192.168.3.1/ng/firewall/service

https://192.168.3.1/api/v2/cmdb/firewall.service/custom/

ServiceCategory
https://192.168.3.1/ng/firewall/service

https://192.168.3.1/api/v2/cmdb/firewall.service/category/

ServiceGroup
https://192.168.3.1/ng/firewall/service

https://192.168.3.1/api/v2/cmdb/firewall.service/group/

SnmpCommunity
https://192.168.3.1/ng/system/snmp

https://192.168.3.1/api/v2/cmdb/system.snmp/community/

VirtualIp
https://192.168.3.1/ng/firewall/virtual-ip

https://192.168.3.1/api/v2/cmdb/firewall/vip/

Zone
https://192.168.3.1/ng/interface

https://192.168.3.1/api/v2/cmdb/system/zone/"""

# new_urls = urls.replace("hostname", "192.168.3.1")

# print(new_urls)