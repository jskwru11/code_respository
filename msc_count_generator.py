######import statements######

from mimir import Mimir
import getpass
import re

def msc_count():
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




    #get dictionary of the following: {msc-9010 : device_count) for all msc's using the 9010s
    #API call to gather all devices
    devices = mimir_api.np.devices.get(cpyKey=cpykey, groupId=groupid)
    #dictionary to gather key:deviceName : value:deviceId
    devices_dict = dict()
    for device in devices:
        devices_dict[device.deviceName] = device.deviceId
    #API call to gather all bgp show command for all devices
    device_cli = mimir_api.np.cli.get(cpyKey=cpykey, groupId=groupid, command=show_command)
    #dictionary to gather key:deviceId : value:bgp_show_command
    devices_cli_dict = dict()
    for device in device_cli:
        devices_cli_dict[device.deviceId] = device.rawData
    #dictionary to combine deviceId from devices_dict and devices_cli_dict key:msc-9010 : value:bgp_show_command
    device_bgp_dict = dict()
    for name, device_id in devices_dict.items():
        for d_id, show_c in devices_cli_dict.items():
            if device_id in list(devices_cli_dict.keys()):
                device_bgp_dict[name] = devices_cli_dict[device_id]
    #iterate over the items in the device_bgp_dict and findall all /32 routes in show show_command
    #take a count of the routes and over device_bgp_dict value: key:msc-9010  : value:device_count
    for name, show_command in device_bgp_dict.items():
        findall_obj = re.findall(regex_pattern, show_command)
        device_bgp_dict[name] = len(findall_obj)
    #return device_bgp_dict key:msc-9010  : value:device_count
    return device_bgp_dict

#run function as a script, but not if imported***
if __name__ == "__main__":
    a = msc_count()
    print(a)
