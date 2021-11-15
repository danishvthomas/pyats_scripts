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
consoles> list
Lab ID   Node ID      Lines          Node Label                Lab Title
------------------------------------------------------------------------
c2ccff        n0        0,1                CEL7     SP.ZTH.v1.0.w10.virl
c2ccff        n1        0,1                CEL6     SP.ZTH.v1.0.w10.virl
c2ccff        n2        0,1               SP1R5     SP.ZTH.v1.0.w10.virl
c2ccff        n3        0,1               SP2R5     SP.ZTH.v1.0.w10.virl
c2ccff        n4        0,1                CER7     SP.ZTH.v1.0.w10.virl
c2ccff        n5        0,1                CER6     SP.ZTH.v1.0.w10.virl
c2ccff        n6      0,1,2               SP1R2     SP.ZTH.v1.0.w10.virl
c2ccff        n7      0,1,2               SP1R3     SP.ZTH.v1.0.w10.virl
c2ccff        n8      0,1,2               SP1R1     SP.ZTH.v1.0.w10.virl
c2ccff        n9      0,1,2               SP1R4     SP.ZTH.v1.0.w10.virl
c2ccff       n10      0,1,2               SP2R3     SP.ZTH.v1.0.w10.virl
c2ccff       n11      0,1,2               SP2R2     SP.ZTH.v1.0.w10.virl
c2ccff       n12      0,1,2               SP2R4     SP.ZTH.v1.0.w10.virl
c2ccff       n13      0,1,2               SP2R1     SP.ZTH.v1.0.w10.virl

"""

 

def unshut_intf(uut):
    intf_list =[]
    op1 = uut.execute("show ip int brief")
    for line in op1.splitlines():
        if 'NVRAM' in line:
            intf = line.split()[0]
            intf_list.append(intf)
        elif 'default' in line:
            intf = line.split()[0]
            intf_list.append(intf)

    cfg = \
    """
    interface {intf}
    no shut
    cdp en
    """
    if 'iosxr' in uut.os:
        cfg = \
        """
        cdp
        interface {intf}
        no shut
        cdp
        """
    for intf in intf_list:
        uut.configure(cfg.format(intf=intf))
 
 
class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    

    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut_list_iosxe,\
            core_uut_list_iosxe,xr_uut_list
            
            


        # connect to device
        uut1 = testbed.devices['uut1']
        uut2 = testbed.devices['uut2']
        uut3 = testbed.devices['uut3']
        uut4 = testbed.devices['uut4']
        uut5 = testbed.devices['uut5']
        uut6 = testbed.devices['uut6']
        uut7 = testbed.devices['uut7']
        uut8 = testbed.devices['uut8']
        uut9 = testbed.devices['uut9']
        uut10 = testbed.devices['uut10']
        uut11 = testbed.devices['uut11']
        uut12 = testbed.devices['uut12']
        uut13 = testbed.devices['uut13']
        uut14 = testbed.devices['uut14']
                       
 

        uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14]
        #uut_list = [uut1,uut2,uut3,uut4]
        uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14]    

        core_uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8]    
         
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13


        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if '.virl' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    if node_label in uut.name.replace("-",""):
                    #if uut.name == node_label:
                        uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)

        
        #uut1.connections['cli']["command"]='open /'+lab_id+'/n0/0'
        
        for uut in uut_list:
        	uut.connect()
 
       
    @aetest.subsection
    def basic_conf_devices(self, testbed):
         
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13

 
 
        pcall(unshut_intf,uut=tuple(uut_list))
 

    	
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))