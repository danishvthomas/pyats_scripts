#!/bin/bash

 

gnome-terminal --maximize --tab --title='R1'  --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R2' --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R3'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R4'  --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R5'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R6'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R7'  --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R8' --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R9'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R10'  --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R11'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          --tab --title='R12'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105'
                          #--tab --title='R13'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          #--tab --title='R14'  --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          #--tab --title='XR1'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          #--tab --title='XR2'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          #--tab --title='XR3'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105' \
                          #--tab --title='XR4'   --command 'sshpass -p "nbv12345"  ssh admin@192.168.0.105'