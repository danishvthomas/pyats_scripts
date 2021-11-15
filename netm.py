from netmiko import ConnectHandler
#from getpass import getpass
from jumpssh import SSHSession
device = {
    'device_type': 'terminal_server',
    'host': '192.168.43.45',
    'username': 'admin',
    'password': 'nbv12345',
    'ssh_config_file': './ssh_config',
}
ESW1 = {
    'device_type': 'cisco_ios',
    'host': '/be4df9/n11/0',
    'username': 'cisco',
    'password': 'nbv12345',
    'ssh_config_file': './ssh_config',
}
net_connect = ConnectHandler(**device)
remote_connect = net_connect(**ESW1).open()
output = remote_connect.send_command("show ip int brief | in up")
print(output)

from netmiko import ConnectHandler
from jumpssh import SSHSession

targetnode = {
'device_type': 'alcatel_sros',
'ip': 'targed_node',
'username': 'admin',
'password': 'admin',
'port': 22,
}

jh_session = SSHSession('jumpserver_ip','jumpserver_user',password='jumpserver_passwd').open()
remote_connect = ConnectHandler(**targetnode)
output = remote_connect.send_command("show router interface")
print(output)