#!/usr/bin/env python3
#title {name} -- sshpass -p nbv12345 ssh admin@192.168.0.105
import subprocess
import paramiko

cmd = 'gnome-terminal --tab --title {name} -- sshpass -p nbv12345 ssh admin@{srv}  '
cmd1 = 'gnome-terminal '
cmd2 = '--tab --title {name} -- sshpass -p nbv12345 ssh admin@{srv}'
cmd3 = cmd1
node_list = []
name_list = []
server = '192.168.0.104'
#server = '192.168.43.142'router_ip = "192.168.0.105"
router_username = "admin"
router_password = "nbv12345"

ssh = paramiko.SSHClient()

cmd4 = 'ssh.connect(router_ip, username=router_username, password=router_password,look_for_keys=False )'

for i in range(11):
    node_list.append(server)
    tab_name = 'R'+str(i+1)
    name_list.append(tab_name)
 
name_list2 = ['nx1','nx2','sw1','sw2','nxo0','nx3','xr0','xr1','xr2','xr3','nxo1']

for servidor,name in zip(node_list,name_list2):
    subprocess.run(cmd.format(name=name,srv=servidor).split())
 






