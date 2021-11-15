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



class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    

    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut15,uut16,uut17,uut18,uut_list_iosxe,\
            core_uut_list_iosxe,xr_uut_list,uut_list_l3,uut_list_leaf,uut_list_bgw
        
        #import pdb ; pdb.set_trace()
 
        uut1 = testbed.devices['uut1']
        uut2 = testbed.devices['uut2']
        uut3 = testbed.devices['uut3']
        uut4 = testbed.devices['uut4']
        uut5 = testbed.devices['uut5']
        uut6 = testbed.devices['uut6']
        uut7 = testbed.devices['uut7']
        uut8 = testbed.devices['uut8']
 
        #xr_uut_list = [uut15,uut16,uut17,uut18]
        #Genie.testbed = testbed = Testbed()
        #uut1 = Device(testbed=testbed, name='R1', os='iosxe')

        uut_list_bgw = [uut3,uut4]
        uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8]
        uut_list_l3 = [uut2,uut3,uut4,uut5,uut7,uut8]        
        uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6]    
        uut_list_leaf = [uut2,uut3,uut4,uut5]     
        core_uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8]    

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if '     Lab at ' in line:
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

        conf_dict=yaml.load(open('nxos_topo.yaml'))
        #pcall(remove_intf_all,uut=tuple(uut_list))
        #pcall(cleanup_igp,uut=tuple(uut_list))
        #pcall(unshut_intf,uut=tuple(uut_list))
        #loopback_config(uut_list_l3)
        
        conf_list = []
        for uut in uut_list_l3:
            conf_list.append(conf_dict)
        #for uut in uut_list:  
        #    add_interface_config(uut,conf_dict)
        
        #pcall(add_interface_config,uut=tuple(uut_list),conf_dict=tuple(conf_list))
        #add_ospf_conf(uut_list,conf_dict)
        
        cfg_vxlan = \
                """
                no vlan 1001-1002
                nv overlay evpn
                feature ospf
                feature bgp
                feature pim
                feature interface-vlan
                feature vn-segment-vlan-based
                feature nv overlay
                fabric forwarding anycast-gateway-mac 0000.2222.3333
                
                evpn
                  vni 2001001 l2
                  vni 2001002 l2
                rd auto
                    route-target import auto
                    route-target export auto
                
                vlan 10
                  vn-segment 900001
                
                interface Vlan10
                  no shutdown
                  vrf member vxlan-900001
                  ip forward
                
                vlan 10
                vlan 101
                  vn-segment 2001001
                vlan 102
                  vn-segment 2001002
                
                vrf context vxlan-900001
                  vni 900001
                  rd auto
                  address-family ipv4 unicast
                    route-target both auto
                    route-target both auto evpn
                  address-family ipv6 unicast
                    route-target both auto
                    route-target both auto evpn
                
                
                interface Vlan101
                  no shutdown
                  vrf member vxlan-900001
                  ip address 101.1.1.1/24
                  ipv6 address 101:1:0:1::1/64
                  fabric forwarding mode anycast-gateway
                
                interface Vlan102
                  no shutdown
                  vrf member vxlan-900001
                  ip address 102.1.1.1/24
                  ipv6 address 102:1:0:1::1/64
                  fabric forwarding mode anycast-gateway
                
                interface nve1
                  no shutdown
                  source-interface loopback0
                  host-reachability protocol bgp
                  member vni 900001 associate-vrf
                  member vni 2001001
                  ingress-replication protocol bgp
                  member vni 2001002
                  ingress-replication protocol bgp

                
                
                """
        #for uut in uut_list_leaf:
        #    uut.configure(cfg_vxlan)

        #pcall(add_bgp_vxlan,uut=tuple(uut_list_leaf),conf_dict=tuple([conf_dict,conf_dict,conf_dict,conf_dict]))
        #pcall(add_ebgp_ms_vxlan,uut=tuple(uut_list_bgw),conf_dict=tuple([conf_dict,conf_dict]))

         #for uut in uut_list_leaf:
        #    add_bgp_vxlan(uut)
        #for uut in uut_list_l3:
        #    add_ospf_config_all(uut)         
        '''
        for uut in uut_list:  
            add_subintf_all(uut,conf_dict)

        add_ospf_config_all(uut,conf_dict)
        add_ospf_conf(uut_list,conf_dict)
 
        add_ebgp_conf(uut9,uut13,conf_dict)
        '''
        #pcall(add_pim_config_all,uut=tuple(uut_list_l3),conf_dict=tuple([conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict]))
        #add_pim_config_all(uut,os=None):

        pcall(copy_run_start,uut=tuple(uut_list))
     
        pass
        
class test1(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def test1_1(self, testbed):
        result_list = []  
        pass
  


if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))