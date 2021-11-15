import logging

from pyats import aetest
from genie.testbed import load
from pyats.async_ import pcall

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
 
"""
9b1dfa        n0        0,1                 CE1                mpls.virl
9b1dfa        n1      0,1,2              SP1PE1                mpls.virl
9b1dfa       n10        0,1               SP3P1                mpls.virl
9b1dfa       n11        0,1               SP3P2                mpls.virl
9b1dfa       n12        0,1               SP3P3                mpls.virl
9b1dfa       n13        0,1               SP3P4                mpls.virl
9b1dfa       n14        0,1               SP3P5                mpls.virl
9b1dfa       n15        0,1               SP3P6                mpls.virl
9b1dfa       n16        0,1              SP3PE2                mpls.virl
9b1dfa       n17      0,1,2              SP3PE3                mpls.virl
9b1dfa       n18        0,1                 CE3                mpls.virl
9b1dfa       n19        0,1                 CE4                mpls.virl
9b1dfa        n2        0,1               SP1P1                mpls.virl
9b1dfa        n3        0,1               SP1P2                mpls.virl
9b1dfa        n4      0,1,2              SP1PE2                mpls.virl
9b1dfa        n5      0,1,2              SP2PE1                mpls.virl
9b1dfa        n6        0,1               SP2P1                mpls.virl
9b1dfa        n7      0,1,2              SP2PE2                mpls.virl
9b1dfa        n8        0,1                 CE2                mpls.virl
9b1dfa        n9        0,1              SP3PE1                mpls.virl
"""

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'
    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,SP1PE1,SP1P1,SP1P2,SP1PE2,CE2,SP2PE1,SP2P1,SP2PE2,SP3PE1,xr_uut_list,\
            SP3PE2,SP3PE3,CE3,CE4,SP3P1,SP3P2,SP3P3,SP3P4,SP3P5,SP3P6,sp1_uut_list,\
            core_uut_list_iosxe,xr_uut_list,xe_uut_list,core_uut_list,sp3_uut_list,sp2_uut_list
  
        CE1 = testbed.devices['CE1']
        CE2 = testbed.devices['CE2']
        CE3 = testbed.devices['CE3']
        SP1PE1 = testbed.devices['SP1PE1']
        SP1PE2 = testbed.devices['SP1PE2']
        SP2PE1 = testbed.devices['SP2PE1']
        SP2PE2 = testbed.devices['SP2PE2']
        SP3PE1 = testbed.devices['SP3PE1']
        SP3PE2 = testbed.devices['SP3PE2']
        SP3PE3 = testbed.devices['SP3PE3']
        SP1P1 = testbed.devices['SP1P1']
        SP1P2 = testbed.devices['SP1P2']
        SP2P1 = testbed.devices['SP2P1']
        SP3P1 = testbed.devices['SP3P1']
        SP3P2 = testbed.devices['SP3P2']
        SP3P3 = testbed.devices['SP3P3']
        SP3P4 = testbed.devices['SP3P4']
        SP3P5 = testbed.devices['SP3P5']
        SP3P6 = testbed.devices['SP3P6']
 
        uut_list1 =  list(testbed.devices.keys())            
        uut_list = [] 
        xe_uut_list = []
        core_uut_list = []
        sp3_uut_list = []
        sp2_uut_list = []
        sp1_uut_list = []
        xr_uut_list = []
        for uut in testbed.devices.keys():
            if not 'jumphost' in uut:
                dev = testbed.devices[uut]
                uut_list.append(dev)
                if not 'xr' in dev.os:
                    xe_uut_list.append(dev)
                elif  'xr' in dev.os:
                    xr_uut_list.append(dev)
        for uut in testbed.devices.keys():
            if not 'jumphost' in uut:
                dev = testbed.devices[uut]
                if not 'CE' in dev.name:
                    core_uut_list.append(dev)

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if '.virl' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    if uut.name == node_label:
                        uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)

        for uut in xr_uut_list:
            uut.connect()
 
       
    @aetest.subsection
    def basic_conf_devices(self, testbed):
        #pcall(unshut_intf,uut=tuple(uut_list))
        #pcall(add_mpls_config,uut=tuple(xr_uut_list))  

        #pcall(copy_run_start,uut=tuple(xe_uut_list))
        pass

class learn_bgp(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def bgp_test(self, testbed):
 
        nbr_info = []
        uut1_bgp_info = SP1PE1.learn('bgp')
        for bgp_instance in uut1_bgp_info.routes_per_peer['instance']:
            for vrf in uut1_bgp_info.routes_per_peer['instance'][bgp_instance]['vrf']:
                for nbr in uut1_bgp_info.routes_per_peer['instance'][bgp_instance]['vrf'][vrf]['neighbor']:
                    nbr_info.append((bgp_instance, vrf, nbr))

        if not nbr_info:
            self.failed('BGP neighbors are missing!')
        else:
            self.passed('We have %s neigbors' % len(nbr_info), 
                        data = {'neighbors': nbr_info})
   
        uut1_bgp_info = SP1PE1.learn('ospf')
        uut1_route_info = SP1PE1.learn('routing')





        
class mpls_consistency_check(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def test_mpls_cs_check(self, testbed):
        for uut in xr_uut_list:
            if not consistency_check(uut):
                print('MPLS CS failed @ UUT:',uut)
                self.failed()


class mpls_path_check(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def test_mpls_path_check(self, testbed):
        result_list = []  
        op = SP1PE1.execute('sh mpls forwarding')
        #import pdb ; pdb.set_trace()
        dict1 = {}
        for line in op.splitlines():
            if line:
                ip = line.split()[0]
                if 'MPLS' in line:
                    label_stack = line.split()[1].split()[2]
                    dict1[ip] = label_stack
                else:
                    dict1[ip] = 'no_label'
        print(dict1)
    	
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))