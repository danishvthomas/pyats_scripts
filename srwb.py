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
        global uut_list,xrv0, xrv1, xrv2, xrv3, xrv4, xrv5, xrv6, xrv7, xrv8,xr9k1,xr9k2,xr9k4,xr9kpe1,xr9kpe2,uut_list_core,\
        igp_inst_a1,igp_inst_a2,igp_inst_c,conf_dict_list_core,test_uut_list,igp_inst_c1,igp_inst_c2,igp_inst_c3,c1_uut_list,c2_uut_list,c3_uut_list,conf_dict

  
        # connect to device
        xrv0	=	testbed.devices["xrv0"]
        xrv1	=	testbed.devices["xrv1"]
        xrv2 	=	testbed.devices["xrv2"]
        xrv3	=	testbed.devices["xrv3"]
        xrv4	=	testbed.devices["xrv4"]
        xrv5	=	testbed.devices["xrv5"]
        xrv6	=	testbed.devices["xrv6"]
        xrv7	=	testbed.devices["xrv7"]
        xr9k1	=	testbed.devices["xr9k1"]
        xr9k2	=	testbed.devices["xr9k2"]
        xr9k4	=	testbed.devices["xr9k4"]
        xr9kpe1	=	testbed.devices["xr9kpe1"]
        xr9kpe2	=	testbed.devices["xr9kpe2"]
                
        c1_uut_list = [xr9kpe1,xrv0,xrv1,xrv2,xrv3,xr9k2]
        c2_uut_list = [xr9k2,xrv4,xrv5,xr9k4]
        c3_uut_list = [xr9k4,xrv6,xrv7,xr9kpe2]

        igp_inst_c1=("CORE1","CORE1","CORE1","CORE1","CORE1","CORE1")
        igp_inst_c2=("CORE2","CORE2","CORE2","CORE2")
        igp_inst_c3=("CORE3","CORE3","CORE3","CORE3")
 
        #uut_list_c = [xrv1,xrv2,xrv3,xrv4,PE1,PE2,C1,C2,C3,C4,C5,C6,C7,C8]
        uut_list = [xrv0, xrv1, xrv2, xrv3, xrv4, xrv5, xrv6, xrv7,xr9k1,xr9k2,xr9k4,xr9kpe1,xr9kpe2]
        #test_uut_list = [CE2,CE1,PE11,PE12,PE2]
        uut_list_core = [xrv0, xrv1, xrv2, xrv3, xrv4, xrv5, xrv6, xrv7,xr9k1,xr9k2,xr9k4,xr9kpe1,xr9kpe2]

        conf_dict=yaml.load(open('srwb_topo.yaml'))
        conf_dict_list_core = []
        for i in range(len(uut_list_core)+1):
            conf_dict_list_core.append(conf_dict)

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")

        #for uut in [xr9k4,xrv6,xrv7,xr9k2,xr9k1,xrv2,xrv3,xrv4,xrv5]:       
        for uut in uut_list:
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
        time.sleep(30)   
 
    @aetest.subsection
    def interFaceConf(self, testbed):
        log.info("add interface configs")
 
        try: 
            loopback_config(uut_list)
            bringUpL3Link(xrv0,[xr9kpe1,xrv2,xrv3])
            bringUpL3Link(xrv1,[xr9kpe1,xrv2,xrv3])
            bringUpL3Link(xr9k2,[xr9k1,xrv2,xrv3,xrv4,xrv5])
            bringUpL3Link(xr9k4,[xr9k1,xrv6,xrv7,xrv4,xrv5])            
            bringUpL3Link(xrv6,[xr9kpe2,xrv7])  
            bringUpL3Link(xrv7,[xr9kpe2])  
            bringUpL3Link(xrv4,[xrv5])  

        except:
            logger.info(f'Failed')
 
 
    @aetest.subsection
    def igpMpls(self, testbed):
        log.info("add Igp mpls configs")
        try:
             #pcall(removeSRxrv,uut=(xrv6,xrv7,xrv8,PE2),igp_inst=igp_inst_a2,index=(40,22,33,13))
            #pcall(configureIsis,uut=tuple(uut_list_core),conf_dict=tuple(conf_dict_list_core))
            for uut in uut_list_core:
                #import pdb;pdb.set_trace()
                configureIsis(uut,conf_dict)

        except:
            logger.info(f'Failed')
        time.sleep(3)  
 
    
    @aetest.subsection
    def srMpls(self, testbed):
        log.info("add Igp mpls configs")
        try:
            pcall(configureSRxr,uut=tuple(c1_uut_list),igp_inst=igp_inst_c1,index=(1,2,3,4,5,6))
            pcall(configureSRxr,uut=tuple(c2_uut_list),igp_inst=igp_inst_c2,index=(21,22,23,24))
            pcall(configureSRxr,uut=tuple(c3_uut_list),igp_inst=igp_inst_c3,index=(31,32,33,34))            

        except:
            logger.info(f'Failed')
        time.sleep(3)  

if __name__ == "__main__":
    # if this script is run standalone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshoptestbed.yaml')))


''' 
##################

class test1CEtoCEREach(aetest.Testcase):
    @aetest.setup
    def setup(self, section):
        pass
        time.sleep(3)   
    @aetest.test
    def test_1(self, section):
        dest_ip_list = []
        op1 = CE1.execute("show route ipv4 ospf")
        if '/32' in op1:
            for line in op1.splitlines():
                if '/32' in line:
                    ip_add = line.split()[2]
                    ip1 = ip_add.split("/")[0]
                    dest_ip_list.append(ip1)
        else:
            self.failed()    

 
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
            pcall(configureSRxrv,uut=(PE11,PE12,xrv1,xrv2,xrv3),igp_inst=igp_inst_a1,index=(1,2,3,4,5))
            pcall(configureSRxrv,uut=(xrv3,xrv4,xrv5,xrv6),igp_inst=igp_inst_c,index=(1,20,30,40))
            pcall(configureSRxrv,uut=(xrv6,xrv7,xrv8,PE2),igp_inst=igp_inst_a2,index=(40,22,33,13))
        except:
            logger.info(f'Failed no OSPF route in CE')
            self.failed()  
  
        time.sleep(30)   
    @aetest.test
    def test_1_ping(self, section):
        dest_ip_list = []
        op1 = CE1.execute("show route ipv4 ospf")
        if '/32' in op1:
            for line in op1.splitlines():
                if '/32' in line:
                    ip_add = line.split()[2]
                    ip1 = ip_add.split("/")[0]
                    dest_ip_list.append(ip1)
        else:
            self.failed()    
  

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
            pcall(removeLdp,uut=(PE11,PE12,xrv1,xrv2,xrv3),igp_inst=igp_inst_a1)
            pcall(removeLdp,uut=(xrv3,xrv4,xrv5,xrv6),igp_inst=igp_inst_c)
            pcall(removeLdp,uut=(xrv6,xrv7,xrv8,PE2),igp_inst=igp_inst_a2)
        except:
            logger.info(f'Failed')
 
        time.sleep(30)   
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


    @aetest.test
    def removeSR(self, section):
        try:
            pcall(removeSRxrv,uut=(PE11,PE12,xrv1,xrv2,xrv3),igp_inst=igp_inst_a1,index=(1,2,3,4,5))
            pcall(removeSRxrv,uut=(xrv3,xrv4,xrv5,xrv6),igp_inst=igp_inst_c,index=(1,20,30,40))
            pcall(removeSRxrv,uut=(xrv6,xrv7,xrv8,PE2),igp_inst=igp_inst_a2,index=(40,22,33,13))
            pcall(mplsldpAutoconfig,uut=tuple(uut_list_core))
        except:
            logger.info(f'Failed')
 
        time.sleep(30)   
    @aetest.test
    def test_3_ping(self, section):
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
 
''' 