import requests
import json
import sys
import pdb
import time


"""
dvthomas@dvthomas-virtual-machine:~/pyats/pyats_scripts$ python3 nxapi1.py "conf " "interf loop0 ; no shut"
******************************************************************************** ['nxapi1.py', 'conf ', 'interf loop0 ; no shut']
command is: interf loop0 ; no shut
********************************************************************************
********************************************************************************
url is: http://192.168.0.55:8080/ins
********************************************************************************
Printing response
********************************************************************************

dvthomas@dvthomas-virtual-machine:~/pyats/pyats_scripts$ python3 nxapi1.py "show " "show run interf loopb0"
******************************************************************************** ['nxapi1.py', 'show ', 'show run interf loopb0']
command is: show run interf loopb0
********************************************************************************
********************************************************************************
url is: http://192.168.0.55:8080/ins
********************************************************************************
Printing response
********************************************************************************
{'ins_api': {'type': 'cli_show', 'version': '1.0', 'sid': 'eoc', 'outputs': {'output': {'input': 'show run interf loopb0', 'msg': 'Success', 'code': '200', 'body': {'nf:filter': {'m:configure': {'m:terminal': {'interface': {'__XML__PARAM__interface': {'__XML__value': 'loopback0'}}}}}, 'nf:source': {'nf:running': ''}}}}}}
dvthomas@dvthomas-virtual-machine:~/pyats/pyats_scripts$


"""
def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1

cli_type = sys.argv[1]
command = sys.argv[2]

print("**"*40,sys.argv)
print("command is:",command)
print("**"*40)



def nxapi_test(cli_type,command):
    if 'conf' in cli_type:
        type = "cli_conf"
    elif "show" in cli_type:
        type = "cli_show"
    client_cert_auth=False
    switchuser='cisco'
    switchpassword='cisco'


    url='http://192.168.0.55:8080/ins'
    print("**"*40)
    print("url is:",url)
    print("**"*40)
    myheaders={'content-type':'application/json'}
    payload={
      "ins_api": {
        "version": "1.0",
        "type": type,
        "chunk": "0",
        "sid": "sid",
        "input": command,
        "output_format": "json"
      }
    }

    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
    output = json.dumps(response, indent=4, sort_keys=True)
    return(output)

response = nxapi_test(cli_type,command)

countdown(3)
print("Printing response ")
print("**"*40)

print(response)
