import logging

from pyats import aetest
from genie.testbed import load
from pyats.async_ import pcall
import yaml
from pexpect import pxssh
import getpass
import pdb
import pyats_lib
import sys
import random
import genie
from genie.libs.conf.ospf import Ospf
from igp_lib import *
import requests
import json
import sys

import time

from genie.conf.base import Testbed, Device, Link, Interface

# Python
import unittest
from unittest.mock import Mock

# Genie package#
#from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie Conf
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface import Interface
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.ospf.gracefulrestart import GracefulRestart
from genie.libs.conf.ospf.stubrouter import StubRouter
from genie.libs.conf.ospf.areanetwork import AreaNetwork
from genie.libs.conf.ospf.arearange import AreaRange
from genie.libs.conf.ospf.interfacestaticneighbor import InterfaceStaticNeighbor

logger = logging.getLogger(__name__)
from unicon.eal.dialogs import Statement, Dialog


import pdb



def nxapi_test(cli_type,command):
    if 'conf' in cli_type:
        type = "cli_conf"
    elif "show" in cli_type:
        type = "cli_show"
    client_cert_auth=False
    switchuser='cisco'
    switchpassword='cisco'
    url='http://192.168.0.52:8080/ins'
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

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'



    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,leaf1,leaf3,bgw1,bgw2,spine2,R1,R2,spine1,uut_list_l3,uut_list_leaf

        #import pdb ; pdb.set_trace()

        R1 = testbed.devices['R1']
        R2 = testbed.devices['R2']
        leaf1 = testbed.devices['leaf1']
        leaf3 = testbed.devices['leaf3']
        spine1 = testbed.devices['spine1']
        bgw1 =  testbed.devices['bgw1']
        spine2 = testbed.devices['spine2']
        bgw2 =  testbed.devices['bgw2']

        #uut_list_bgw = [uut3,uut4]
        uut_list = [leaf1,leaf3,bgw1,R1,R2,spine1,spine2,bgw2]
        uut_list_l3 = [leaf1,leaf3,bgw1,R1,R2,spine1,spine2,bgw2]
        uut_list_leaf = [leaf1,leaf3,bgw1,bgw2]
        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'vxlan' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    if uut.name == node_label:
                        uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)
        for uut in uut_list:
            uut.connect()

    @aetest.subsection
    def basic_conf_devices(self, testbed):

        conf_dict=yaml.load(open('vxlan_topo.yaml'))
        #pcall(remove_intf_all,uut=tuple(uut_list))
        #pcall(cleanup_igp,uut=tuple(uut_list))
        #pcall(unshut_intf,uut=tuple(uut_list))
        #loopback_config(uut_list_l3)


        #uut_list1 = uut_list_l3
        #for uut1 in uut_list1:
        #    uut_list2 = uut_list
        #    uut_list2.remove(uut1)
        #    for uut2 in uut_list2:
        #        bring_up_l3_link_xr_nx(uut1,[uut2])



        pdb.set_trace()


        area_l1_1 = '49.0001'
        area_l1_2 = '49.0002'

        for uut in [leaf1,spine1,bgw1]:
            configure_isis_new(uut,area_l1_1,[leaf1,spine1,bgw1])

        for uut in [leaf3,spine2,bgw2]:
            configure_isis_new(uut,area_l1_2,[leaf3,spine2,bgw2])

        for uut in uut_list_leaf:
            uut.configure("feature ospf")
        conf_list = []
        for uut in uut_list_l3:
            conf_list.append(conf_dict)

        pcall(add_interface_config,uut=tuple(uut_list),conf_dict=tuple(conf_list))
        #add_ospf_conf(uut_list,conf_dict)
        pcall(add_vxlan_common_conf,uut=tuple(uut_list))


        #pcall(add_bgp_vxlan,uut=tuple([leaf1,leaf2]),conf_dict=tuple([conf_dict,conf_dict]))
        #pcall(add_ebgp_ms_vxlan,uut=tuple(uut_list_bgw),conf_dict=tuple([conf_dict,conf_dict]))

        '''
         #for uut in uut_list_leaf:
        #    add_bgp_vxlan(uut)
        #for uut in uut_list_l3:
        #    add_ospf_config_all(uut)

        for uut in uut_list:
            add_subintf_all(uut,conf_dict)

        add_ospf_config_all(uut,conf_dict)
        add_ospf_conf(uut_list,conf_dict)

        add_ebgp_conf(uut9,uut13,conf_dict)
        '''
        #pcall(add_pim_config_all,uut=tuple(uut_list_l3),conf_dict=tuple([conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict]))
        #add_pim_config_all(uut,os=None):

        #pcall(copy_run_start,uut=tuple(uut_list))

        pass

class test1(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def test1_1(self, testbed):
        result_list = []
        op = nxapi_test("show","show nve vni")
        if op:
            print(op)
        else:
            self.failed()

class test12(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def test2_1(self, testbed):
        result_list = []
        op = nxapi_test("show","show nve peers")
        for uut in [leaf1,leaf2]:
            leaf_spine_l3_conf(uut,spine)
        #leaf_spine_l3_conf(uut,spine)
        pdb.set_trace()
        if op:
            print(op)
        else:
            self.failed()

if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))
