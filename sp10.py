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
        global uut_list,CEL7,CEL6,SP2R3,SP2R2,SP2R4,SP2R1,SP1R5,SP2R5,CER7,CER6,SP1R2,SP1R3,SP1R1,SP1R4  
  

        # connect to device
        CEL7 = testbed.devices['CEL7']
        CEL6 = testbed.devices['CEL6']
        CER7 = testbed.devices['CER7']
        CER6 = testbed.devices['CER6']
        SP1R1 = testbed.devices['SP1R1']
        SP1R2 = testbed.devices['SP1R2']
        SP1R3 = testbed.devices['SP1R3']
        SP1R4 = testbed.devices['SP1R4']
        SP1R5 = testbed.devices['SP1R5']
        SP2R1 = testbed.devices['SP2R1']
        SP2R2 = testbed.devices['SP2R2']
        SP2R3 = testbed.devices['SP2R3']
        SP2R4 = testbed.devices['SP2R4']
        SP2R5 = testbed.devices['SP2R5']
 

 

        uut_list = [CEL7,CEL6,SP2R3,SP2R2,SP2R4,SP2R1,SP1R5,SP2R5,CER7,CER6,SP1R2,SP1R3,SP1R1,SP1R4] 

 
 

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'SP.ZTH' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                	if uut.name == node_label:
                		uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)

        
        #uut1.connections['cli']["command"]='open /'+lab_id+'/n0/0'
        
        for uut in uut_list:
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
        
 
        pcall(unshut_intf,uut=tuple(uut_list))
       
        #pcall(remove_subintf,uut=tuple(core_uut_list))
        #bring_up_subif2(uut1,[uut3,uut4,uut5,uut10])
 
        #import pdb ; pdb.set_trace()
        #add_mpls_interface_config(uut6)
  
        #pcall(add_ospf_config,uut=tuple(core_uut_list)) 
        #pcall(add_mpls_conf,uut=tuple(core_uut_list)) 
 
        #pcall(add_mpls_interface_config,uut=tuple(xr_uut_list))
        # pcall(copy_run_start,uut=tuple(xr_uut_list)) 
 
 
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))