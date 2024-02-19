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
 
import logging
# get your logger for your script
log = logging.getLogger(__name__)

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
        global uut_list, XR1,XR2,XR3,XR4,XR5,XR6,XR7,XR8,PE11,PE12,PE2,CE1,CE2,uut_list_core,\
        igp_inst_a1,igp_inst_a2,igp_inst_c,conf_dict_list_core

  
        # connect to device
        CE1	=	testbed.devices["CE1"]
        CE2	=	testbed.devices["CE2"]
        PE11	=	testbed.devices["PE11"]
        PE12	=	testbed.devices["PE12"]
        PE2	=	testbed.devices["PE2"]
        XR1	=	testbed.devices["XR1"]
        XR2	=	testbed.devices["XR2"]
        XR3	=	testbed.devices["XR3"]
        XR4	=	testbed.devices["XR4"]
        XR5	=	testbed.devices["XR5"]
        XR6	=	testbed.devices["XR6"]
        XR7	=	testbed.devices["XR7"]
        XR8	=	testbed.devices["XR8"]

        igp_inst_a1=("AGG1","AGG1","AGG1","AGG1","AGG1" )
        igp_inst_c=("CORE","CORE","CORE","CORE" )
        igp_inst_a2=("AGG2","AGG2","AGG2","AGG2" )
 
        uut_list = [ XR1,XR2,XR3,XR4,XR5,XR6,XR7,XR8,PE11,PE12,PE2,CE1,CE2]
        uut_list_core = [ XR1,XR2,XR3,XR4,XR5,XR6,XR7,XR8,PE11,PE12,PE2]

        conf_dict=yaml.load(open('umpls_topo.yaml'))
        conf_dict_list_core = []
        for uut in uut_list_core:
            conf_dict_list_core.append(conf_dict)

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")

        for uut in uut_list:       
        #for uut in [CE2]:
        	uut.connect()
 

 
    @aetest.subsection
    def precleanup(self, testbed):
        try:
            log.info("cleanup all configs")
            pcall(unshut_intf,uut=tuple(uut_list))
            pcall(remove_intf_all,uut=tuple(uut_list))
            pcall(cleanup_igp,uut=tuple(uut_list)) 
        except:
            logger.info(f'Failed pre cleanup')

    @aetest.subsection
    def interFaceConf(self, testbed):
        log.info("add interface configs")
        try: 
            loopback_config(uut_list)
            bringUpL3Link(CE1,[PE11,PE12])
            bringUpL3Link(CE2,[PE2])
            bringUpL3Link(XR1,[PE11,PE12,XR2,XR3])
            bringUpL3Link(XR2,[PE11,PE12,XR3])

            bringUpL3Link(XR4,[XR3,XR5,XR6])
            bringUpL3Link(XR5,[XR3,XR6])

            bringUpL3Link(XR7,[XR6,XR8,PE2])
            bringUpL3Link(XR8,[XR6,PE2])
        except:
            logger.info(f'Failed')

    @aetest.subsection
    def igpMpls(self, testbed):
        log.info("add Igp mpls configs")
        try:
            pcall(configureIsis,uut=tuple(uut_list_core),conf_dict=tuple(conf_dict_list_core))
            pcall(mplsldpAutoconfig,uut=tuple(uut_list_core))
        except:
            logger.info(f'Failed')
  
    @aetest.subsection
    def bgpLu(self, testbed):
        log.info("add bgp Lu")
        try:
            addBgpUmplsxr(PE11,[XR3])
            addBgpUmplsxr(PE12,[XR3])
            addBgpUmplsxr(XR3,[PE11,PE12,XR6])
            addBgpUmplsxr(XR6,[PE2,XR3])
        except:
            logger.info(f'Failed')
  
    @aetest.subsection
    def bgpVpnV4(self, testbed):
        try:
            log.info("add bgp vpnv4")
            addBgpVpnv4xr(PE11,[PE2])
            addBgpVpnv4xr(PE12,[PE2])
            addBgpVpnv4xr(PE2,[PE11,PE12])
        except:
            logger.info(f'Failed')
  
    @aetest.subsection
    def l3VpnService(self, testbed):
        log.info("add bgp l3 vpn pe-ce")
        try 
            for uut in [CE1,CE2]:
                addOspfXr(uut)

            addL3VpnService(PE11,"BLUE","G0/0/0/1","65001:1")
            addL3VpnService(PE12,"BLUE","G0/0/0/0","65001:1")
            addL3VpnService(PE2,"BLUE","G0/0/0/2","65001:1")
        except:
            logger.info(f'Failed')
  


class test1CEtoCEREach(aetest.Testcase):
    @aetest.setup
    def setup(self, section):
        pass

    @aetest.test
    def test_1(self, section):
        dest_ip_list = []
        op1 = CE1.execute("show route ipv4 ospf")
        for line in op1.splitlines():
            if '/32' in line:
                ip_add = line.split()[2]
                ip1 = ip_add.split("/")[0]
                dest_ip_list.append(ip1)

 
        for ip1 in dest_ip_list:
            CE1.execute(f"ping {ip1} sou loop0 repe 10")
            res1 = CE1.execute(f"ping {ip1} sou loop0 repe 10")
            if not 'Success rate is 100 percent' in res1:
                log.info(f"FAILED PING FOR {ip1}")
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        pass 
        log.info("%s testcase cleanup/teardown" % self.uid)           
 


class test2LdpToSRMigration(aetest.Testcase):
    @aetest.setup
    def setup(self, section):
        try:
            pcall(configureSRxr,uut=(PE11,PE12,XR1,XR2,XR3),igp_inst=igp_inst_a1,index=(1,2,3,4,5))
            pcall(configureSRxr,uut=(XR3,XR4,XR5,XR6),igp_inst=igp_inst_c,index=(1,20,30,40))
            pcall(configureSRxr,uut=(XR6,XR7,XR8,PE2),igp_inst=igp_inst_a2,index=(40,22,33,13))
        except:
            logger.info(f'Failed')
  

    @aetest.test
    def test_1_ping(self, section):
        dest_ip_list = []
        op1 = CE1.execute("show route ipv4 ospf")
        for line in op1.splitlines():
            if '/32' in line:
                ip_add = line.split()[2]
                ip1 = ip_add.split("/")[0]
                dest_ip_list.append(ip1)
 
        for ip1 in dest_ip_list:
            CE1.execute(f"ping {ip1} sou loop0 repe 10")
            res1 = CE1.execute(f"ping {ip1} sou loop0 repe 10")
            log.info(f" ping respons is {res1}")
            if not 'Success rate is 100 percent' in res1:
                log.info(f"FAILED PING FOR {ip1}")
                self.failed()


    @aetest.test
    def removeLDP(self, section):
        try:
            pcall(removeLdp,uut=(PE11,PE12,XR1,XR2,XR3),igp_inst=igp_inst_a1)
            pcall(removeLdp,uut=(XR3,XR4,XR5,XR6),igp_inst=igp_inst_c)
            pcall(removeLdp,uut=(XR6,XR7,XR8,PE2),igp_inst=igp_inst_a2)
        except:
            logger.info(f'Failed')
  
        import time
        time.sleep(10)

    @aetest.test
    def test_2_ping(self, section):
        dest_ip_list = []
        op1 = CE1.execute("show route ipv4 ospf")
        for line in op1.splitlines():
            if '/32' in line:
                ip_add = line.split()[2]
                ip1 = ip_add.split("/")[0]
                dest_ip_list.append(ip1)
 
        for ip1 in dest_ip_list:
            CE1.execute(f"ping {ip1} sou loop0 repe 10")
            res1 = CE1.execute(f"ping {ip1} sou loop0 repe 10")
            log.info(f" ping respons is {res1}")
            if not 'Success rate is 100 percent' in res1:
                log.info(f"FAILED PING FOR {ip1}")
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass 
        log.info("%s testcase cleanup/teardown" % self.uid)           
 
  
 
if __name__ == "__main__":
    # if this script is run standalone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshoptestbed.yaml')))
