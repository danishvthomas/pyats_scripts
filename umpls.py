import logging
import yaml
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
        global uut_list,core1xe, abr2xr, ce1, ce2, ce3, abr1xr, abr3xe, agg2xe, agg1xr, agg3xe, pe2xr, pe1xr, pe3xe,\
               xe_uut_list,xr_uut_list,uut_list_core

  

        # connect to device
        ce1	=	testbed.devices["ce1"]
        ce2	=	testbed.devices["ce2"]
        ce3	=	testbed.devices["ce3"]

        abr2xr	=	testbed.devices["abr2xr"]
        abr1xr	=	testbed.devices["abr1xr"]
        abr3xe	=	testbed.devices["abr3xe"]

        core1xe	=	testbed.devices["core1xe"]

        agg2xe	=	testbed.devices["agg2xe"]
        agg1xr	=	testbed.devices["agg1xr"]
        agg3xe	=	testbed.devices["agg3xe"]

        pe2xr	=	testbed.devices["pe2xr"]
        pe1xr	=	testbed.devices["pe1xr"]
        pe3xe	=	testbed.devices["pe3xe"]


        uut_list = [core1xe, abr2xr, ce1, ce2, ce3, abr1xr, abr3xe, agg2xe, agg1xr, agg3xe, pe2xr, pe1xr, pe3xe]
        xe_uut_list = [core1xe, abr3xe, agg2xe, agg3xe, pe3xe,ce1, ce2, ce3]
        xr_uut_list = [abr2xr, abr1xr, agg1xr, pe2xr, pe1xr]
        uut_list_core = [core1xe, abr2xr, abr1xr, abr3xe, agg2xe, agg1xr, agg3xe, pe2xr, pe1xr, pe3xe]




        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'unifiedMPLS' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    if uut.name == node_label:
                        uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'
   
                logger.info('lab_id is : %s' % lab_id)

        
 
        
        for uut in uut_list:
        #for uut in [abr2xr,p1xe]:    
        	uut.connect()
 

 
    @aetest.subsection
    def basic_conf_devices(self, testbed):
         
        #      ce1---pe1--
        #        |  X   |   X  |  X   |   X    |
        #iosv7 xrv0xrv1xrv2xrv6xrv7xrv8
        #        |  X   |   X  |  X   |   X    |   
        #     xrv3iosv3xrv4iosv4iosv6
        #       l20         l21 
 
        #    area1    ABR   ASBR     
        uut_list1 = [core1xe,abr1xr]  

        conf_dict=yaml.load(open('umpls_topo.yaml'))
       
     
        conf_dict_list = []
        for uut in uut_list:
            conf_dict_list.append(conf_dict)
       
        pcall(unshut_intf,uut=tuple(uut_list))
        pcall(remove_intf_all,uut=tuple(uut_list))
        pcall(cleanup_igp,uut=tuple(uut_list)) 
        pcall(configure_interfaces,uut=tuple(uut_list),conf_dict=tuple(conf_dict_list))
        pcall(configure_isis,uut=tuple(uut_list),conf_dict=tuple(conf_dict_list))
        pcall(mplsldpAutoconfig,uut=tuple(uut_list_core))
       
        pcall(copy_run_start,uut=tuple(xe_uut_list))
           

        #import pdb ; pdb.set_trace()
   
 
if __name__ == "__main__":
    # if this script is run standalone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshoptestbed.yaml')))
