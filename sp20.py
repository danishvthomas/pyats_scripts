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
 

def changeName(uut):
    uut_name = uut.name.replace("","")
    uut.configure('hostname {uut_name}'.format(uut_name=uut_name)) 

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    

    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        # convert a pyATS testbed to Genie testbed
        # genie testbed extends pyATS testbed and does more with it, eg, 
        # adding .learn() and .parse() functionality
        # this step will be harmonized and no longer required in near future
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,iosv0,iosv1,iosv2,iosv3,iosv4,iosv5,iosv6,iosv7,iosvl20,iosvl21,xrv0,xrv1,xrv2,xrv3,xrv4,xrv5,xrv6,xrv7,xrv8,\
               ios_uut_list,xr_uut_list  

  

        # connect to device
        iosv0 = testbed.devices['iosv0']
        iosv1 = testbed.devices['iosv1']
        iosv2 = testbed.devices['iosv2']
        iosv3 = testbed.devices['iosv3']
        iosv4 = testbed.devices['iosv4']
        iosv5 = testbed.devices['iosv5']
        iosv6 = testbed.devices['iosv6']
        iosv7 = testbed.devices['iosv7']
        iosvl20 = testbed.devices['iosvl20']
        iosvl21 = testbed.devices['iosvl21']  
        xrv0 = testbed.devices['xrv0']
        xrv1 = testbed.devices['xrv1']
        xrv2 = testbed.devices['xrv2']
        xrv3 = testbed.devices['xrv3']
        xrv4 = testbed.devices['xrv4']
        xrv5 = testbed.devices['xrv5']
        xrv6 = testbed.devices['xrv6']
        xrv7 = testbed.devices['xrv7']
        xrv8 = testbed.devices['xrv8'] 

        uut_list = [core1xe, abr2xr, ce1, ce2, ce3, abr1xr, abr3xe, agg2pxe, agg1pxr, agg3pxe, pe2xr, pe1xr, pe3xe]
        xe_uut_list = [core1xe, abr3xe, agg2pxe, agg3pxe, pe3xe,ce1, ce2, ce3]
        xr_uut_list = [abr2xr, abr1xr, agg1pxr, pe2xr, pe1xr]

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'ospf' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                	if uut.name == node_label:
                		uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'
                	elif uut.name == node_label.replace("-",""):
                		uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'
   
                logger.info('lab_id is : %s' % lab_id)

        
        #uut1.connections['cli']["command"]='open /'+lab_id+'/n0/0'
        
        for uut in ios_uut_list:
        	uut.connect()
 
        #pcall(changeName,uut=tuple(uut_list))
        # 
        #  
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
         
        #      iosv0iosv1iosv2xrv5iosv5
        #        |  X   |   X  |  X   |   X    |
        #iosv7 xrv0xrv1xrv2xrv6xrv7xrv8
        #        |  X   |   X  |  X   |   X    |   
        #     xrv3iosv3xrv4iosv4iosv6
        #       l20         l21 
 
        #    area1    ABR   ASBR     


        #pcall(unshut_intf,uut=tuple(uut_list))
        ''' 
        pcall(remove_subintf,uut=tuple(uut_list))
        
        bring_up_subif3(iosv0,[iosv1,xrv1,xrv0])
        bring_up_subif3(xrv0,[iosv1,xrv1,iosv3,xrv3,iosv7])
        bring_up_subif3(xrv3,[xrv1,iosv3])
 
        bring_up_subif3(iosv1,[iosv2,xrv1,xrv2])
        bring_up_subif3(xrv1,[iosv3,xrv4,xrv2])
        bring_up_subif3(iosv3,[xrv2,xrv4])

        bring_up_subif3(iosv2,[xrv2,xrv5,xrv6])
        bring_up_subif3(xrv2,[iosv4,xrv6,xrv4])
        bring_up_subif3(xrv4,[iosv4,xrv6])

        bring_up_subif3(xrv5,[iosv5,xrv6,xrv7])
        bring_up_subif3(xrv6,[iosv6,xrv7,iosv4])
        bring_up_subif3(iosv4,[iosv6,xrv7])


        bring_up_subif3(iosv5,[xrv7])
        bring_up_subif3(xrv7,[iosv6,xrv8])
        
        #loopback_config(uut_list)

        pcall(cleanup_igp,uut=tuple(uut_list)) 

        for uut in [iosv0,xrv0,xrv3,iosv1,xrv1,iosv3]:
            add_ospf_config(uut,instance = '100')
        for uut in [iosv2,xrv2,xrv4,xrv5,xrv6,iosv4,iosv5,xrv7,iosv6]:
            add_ospf_config(uut,instance = '200')
        '''
        pcall(add_mpls_conf,uut=tuple(ios_uut_list))
        #pcall(copy_run_start,uut=tuple(ios_uut_list))
           
        #import pdb ; pdb.set_trace()
   
        #pcall(add_ospf_config,uut=tuple(core_uut_list)) 
        #pcall(add_mpls_conf,uut=tuple(core_uut_list)) 

        import pdb ; pdb.set_trace()
        
        
        # pcall(copy_run_start,uut=tuple(xr_uut_list)) 
 
 
if __name__ == "__main__":
    # if this script is run standalone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshoptestbed.yaml')))