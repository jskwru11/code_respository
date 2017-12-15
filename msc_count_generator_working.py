######import statements######

from mimir import Mimir
import getpass
import re

######global variables#####
# username = getpass.getuser()
username = input("Username: ")
password = getpass.getpass()
mimir_api = Mimir()
mimir_api.authenticate(username=username, password=password)
cpykey = 94617
groupid = 235688
show_command = 'show bgp vpnv4 unicast vrf CELL_MGMT'
regex_pattern = r'(\*[>\s]?i10\.\d{1,3}\.\d{1,3}\.\d{1,3}\/32\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+)(\d+\s+)(\d+\s+)(\d+\s+)(.*)'




#get tuple of the following: (msc, count) for all msc's using the 9010s
devices = mimir_api.np.devices.get(cpyKey=cpykey, groupId=groupid)

devices_dict = dict()

for device in devices:
    devices_dict[device.deviceName] = device.deviceId


device_cli = mimir_api.np.cli.get(cpyKey=cpykey, groupId=groupid, command=show_command)
devices_cli_dict = dict()
for device in device_cli:
    devices_cli_dict[device.deviceId] = device.rawData

device_bgp_dict = dict()
# devices_list = list(devices_cli_dict.keys())

# for name, device_id in devices_dict.items():
#     try:
#         device_bgp_dict[name] = devices_cli_dict[device_id]
#     except KeyError:
#         print("{} ooops!!!".format(device_id))
for name, device_id in devices_dict.items():
    for d_id, show_c in devices_cli_dict.items():
        if device_id in list(devices_cli_dict.keys()):
            device_bgp_dict[name] = devices_cli_dict[device_id]

sample_sample = open("sample_sample.txt", "w")
print(device_bgp_dict['AKROOH2093A-P-CI-9010-03'], file=sample_sample)
sample_sample.close()

new_text = open("new_text.txt", "a")
for key, value in device_bgp_dict.items():
    findall_obj = re.findall(regex_pattern, value)
    print((key,len(findall_obj)), file=new_text)
    device_bgp_dict[key] = len(findall_obj)


new_text.close()
dict_text = open("dict_text.txt", 'w')
print(device_bgp_dict, file=dict_text)
dict_text.close()


# outfile = open("bgp.txt", "w")
# outfile2 = open("bgp1.txt", "w")
# outfile3 = open("bgp2.txt", "w")
# print(device_bgp_dict, file=outfile)
# print(devices_cli_dict.keys(), file=outfile2)
# print(devices_dict.values(), file=outfile3)
# # print(len(devices_cli_dict.keys()))
# # print(len(devices_dict.values()))
# # print(len(device_bgp_dict.values()))
# # print(len(device_bgp_dict.keys()))
# outfile.close()
