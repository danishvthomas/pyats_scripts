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
 

 

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    

    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        # convert a pyATS testbed to Genie testbed
        # genie testbed extends pyATS testbed and does more with it, eg, 
        # adding .learn() and .parse() functionality
        # this step will be harmonized and no longer required in near future
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut15,uut16,uut17,uut18,uut_list_iosxe,\
            core_uut_list,xr_uut_list
            
 

        # connect to device
        uut1 = testbed.devices['xrv-0']
        uut2 = testbed.devices['xrv-1']
        uut3 = testbed.devices['xrv-2']
        uut4 = testbed.devices['xrv-3']
        uut5 = testbed.devices['xrv-4']
        uut6 = testbed.devices['xrv-5']
        uut7 = testbed.devices['xrv-6']
        uut8 = testbed.devices['xrv-7']
        uut9 = testbed.devices['xrv-8']
        uut10 = testbed.devices['xrv-9']
        uut11 = testbed.devices['xrv-10']
        uut12 = testbed.devices['xrv-11']
        uut13 = testbed.devices['xrv-12']
        uut14 = testbed.devices['iosv-0']
        uut15 = testbed.devices['iosvl2-0']
        uut16 = testbed.devices['iosvl2-1']
        uut17 = testbed.devices['iosvl2-2']
        uut18 = testbed.devices['iosvl2-3']
        uut19 = testbed.devices['iosvl2-4']

        xr_uut_list = [uut15,uut16,uut17,uut18]
        #Genie.testbed = testbed = Testbed()
        #uut1 = Device(testbed=testbed, name='R1', os='iosxe')

        uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut15,uut16,uut17,uut18,uut19]
        #uut_list = [uut1,uut2,uut3,uut4]
        uut_list_iosxe = [uut14]    

        core_uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14]    
         
 

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'evpn' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                	if uut.name == node_label:
                		uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)

        
        #uut1.connections['cli']["command"]='open /'+lab_id+'/n0/0'
        
        for uut in core_uut_list:
        	uut.connect()
 

 
        # compute our neighbors
        #original_stdout = sys.stdout # Save a reference to the original standard output
        #with open('show_logg.txt', 'w') as f:
        #    sys.stdout = f # Change the standard output to the file we created.
        #    for uut in [uut8,uut16]:
        #        uut.execute("show logg")

        #    sys.stdout = original_stdout # Reset the standard output to its original value

        #result = pcall(connect_device,uut=tuple(uut_list))
 
        #remove_subintf(uut1," Gi0/2",'12')

 
    @aetest.subsection
    def basic_conf_devices(self, testbed):
         
        #R10----R1--R2--R3-------R12
        #       | X | X | 
        #       R4--R5--R6 ----R14
        #       | X | X | 
        #R11---R7--R8---R9------R13

        # uut5 is RR
        
        '''
        
        #loopback_config(core_uut_list)
 
        #pcall(unshut_intf,uut=tuple(uut_list))
       
        pcall(remove_subintf,uut=tuple(core_uut_list))
        bring_up_subif2(uut1,[uut3,uut4,uut5,uut10])
        bring_up_subif2(uut2,[uut3,uut4,uut5,uut6])
        bring_up_subif2(uut3,[uut12,uut5,uut6])
        bring_up_subif2(uut4,[uut5,uut7,uut8])

        bring_up_subif2(uut5,[uut6,uut7,uut8,uut9])
  
        #import pdb ; pdb.set_trace()
        #add_mpls_interface_config(uut6)
        bring_up_subif2(uut6,[uut14,uut8,uut9])
        bring_up_subif2(uut7,[uut11,uut8])
        bring_up_subif2(uut8,[uut9])
        bring_up_subif2(uut9,[uut13])

        '''

        #add_ospf_config(uut,os=None):
        pcall(add_ospf_config,uut=tuple(core_uut_list)) 
        #pcall(add_mpls_conf,uut=tuple(core_uut_list)) 
        '''
        bring_up_subif(uut0,[uut1,uut4,uut5,uut9])
        bring_up_subif(uut2,[uut5,uut6,uut7,uut3])
        bring_up_subif(uut3,[uut6,uut7,uut8,uut4])
        bring_up_subif(uut4,[uut7,uut8,uut12])
        bring_up_subif(uut5,[uut6,uut15,uut16])
        bring_up_subif(uut6,[uut7,uut15,uut16,uut17])
        bring_up_subif(uut7,[uut8,uut16,uut17,uut18])
        bring_up_subif(uut8,[uut17,uut18])
        bring_up_subif(uut15,[uut11,uut16])
        bring_up_subif(uut16,[uut17])
        bring_up_subif(uut17,[uut18])
        bring_up_subif(uut18,[uut13])

 
        pcall(add_mpls_interface_config,uut=tuple(xr_uut_list))
        pcall(copy_run_start,uut=tuple(xr_uut_list)) 
 


class Test_BGP(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        #pdb.set_trace()
        # do our learning
        uut16.execute("show ver")
        self.bgp = testbed.devices['uut1'].learn('bgp')

    @aetest.test
    def test_bgp_has_neighbors(self):
        # compute our neighbors
        
        uut16.execute("show ver")       
        nbr_info = []
        for bgp_instance in self.bgp.routes_per_peer['instance']:
            for vrf in self.bgp.routes_per_peer['instance'][bgp_instance]['vrf']:
                for nbr in self.bgp.routes_per_peer['instance'][bgp_instance]['vrf'][vrf]['neighbor']:
                    nbr_info.append((bgp_instance, vrf, nbr))

        # decide whether this testcase is pass or fail
        if not nbr_info:
            self.failed('BGP neighbors are missing!')
        else:
            # on pass - save the neighbor data for future analysis
            # in the final report
            self.passed('We have %s neigbors' % len(nbr_info), 
                        data = {'neighbors': nbr_info})

class log_analyse(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        # do our learning
        pass

    @aetest.test
    def log_analyse_uut(self):
        # compute our neighbors
        file = open('show_logg.txt', mode = 'r', encoding = 'utf-8-sig')
        lines = file.readlines()
        file.close()
        for line in lines:
        	print(line)

'''        	
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))