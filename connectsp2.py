#!/usr/bin/env python3

import subprocess
cmd = 'gnome-terminal --tab --title {name} -- sshpass -p nbv12345 ssh admin@{srv}  '
cmd1 = 'gnome-terminal '
cmd2 = '--tab --title {name} -- sshpass -p nbv12345 ssh admin@{srv}'
cmd3 = cmd1
node_list = []
name_list = []
server = '192.168.0.105'
for i in range(14):
    node_list.append(server)
    tab_name = 'R'+str(i+1)
    name_list.append(tab_name)
 
name_list2 = ['CE1','XR1','XR2','R3','XR4','CE3','R5','R6','R7','R8','CE4','CE2','R9','R10'] 
for servidor,name in zip(node_list,name_list2):
    subprocess.run(cmd.format(name=name,srv=servidor).split())
    #subprocess.run('list')
 