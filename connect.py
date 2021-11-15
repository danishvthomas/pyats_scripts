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
 
name_list2 = ['CEL7','CEL6','SP1R5','SP2R5','CER7','CER6','SP1R2','SP1R3','SP1R1','SP1R4','SP2R3','SP2R2','SP2R4','SP2R1'] 
for servidor,name in zip(node_list,name_list2):
    subprocess.run(cmd.format(name=name,srv=servidor).split())
    #subprocess.run('list')
 