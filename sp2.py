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

#smtp.host = mail.google.com
#smtp.port = 25
#default_domain = gmail.com
"""
Lab ID   Node ID      Lines          Node Label                Lab Title
------------------------------------------------------------------------
f67dac        n0        0,1                ios1                 sp2.virl
f67dac        n1        0,1                ios2                 sp2.virl
f67dac       n10      0,1,2                xrv1                 sp2.virl
f67dac       n11      0,1,2                xrv2                 sp2.virl
f67dac       n12      0,1,2                xrv3                 sp2.virl
f67dac       n13      0,1,2                xrv4                 sp2.virl
f67dac        n2        0,1                ios3                 sp2.virl
f67dac        n3        0,1                ios4                 sp2.virl
f67dac        n4        0,1                ios5                 sp2.virl
f67dac        n5        0,1                ios6                 sp2.virl
f67dac        n6        0,1                ios7                 sp2.virl
f67dac        n7        0,1                ios8                 sp2.virl
f67dac        n8        0,1                ios9                 sp2.virl
f67dac        n9        0,1               ios10                 sp2.virl

"""

 
 
 
class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    

    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,ios1,ios2,ios3,ios4,ios5,ios6,ios7,ios8,ios9,ios10,xrv1,xrv2,xrv3,xrv4,uut_list_iosxe,\
            core_uut_list_iosxe,xr_uut_list
  
        # connect to device
        ios1 = testbed.devices['ios1']
        ios2 = testbed.devices['ios2']
        ios3 = testbed.devices['ios3']
        ios4 = testbed.devices['ios4']
        ios5 = testbed.devices['ios5']
        ios6 = testbed.devices['ios6']
        ios7 = testbed.devices['ios7']
        ios8 = testbed.devices['ios8']
        ios9 = testbed.devices['ios9']
        ios10 = testbed.devices['ios10']
        xrv1 = testbed.devices['xrv1']
        xrv2 = testbed.devices['xrv2']
        xrv3 = testbed.devices['xrv3']
        xrv4 = testbed.devices['xrv4']
                       
 

        uut_list = [ios1,ios2,ios3,ios4,ios5,ios6,ios7,ios8,ios9,ios10,xrv1,xrv2,xrv3,xrv4]
        #uut_list = [r1,ios2,ios3,ios4]
        uut_list_iosxe = [ios1,ios2,ios3,ios4,ios5,ios6,ios7,ios8,ios9,ios10]    

        core_uut_list_iosxe = [ios1,ios2,ios3,ios4,ios5,ios6,ios7,ios8]    
         
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13

        for uut in uut_list:
            print(uut.name)
        
        

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

        
        #r1.connections['cli']["command"]='open /'+lab_id+'/n0/0'
        
        for r in uut_list:
            r.connect()
 
       
    @aetest.subsection
    def basic_conf_devices(self, testbed):
         
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13


        pcall(unshut_intf,uut=tuple(uut_list))
        pcall(copy_run_start,uut=tuple(uut_list_iosxe))

    	
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))