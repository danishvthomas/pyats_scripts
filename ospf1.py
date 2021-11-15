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
            core_uut_list_iosxe,xr_uut_list
            
            
 
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
        uut15 = testbed.devices['uut15']
        #xr_uut_list = [uut15,uut16,uut17,uut18]
        #Genie.testbed = testbed = Testbed()
        #uut1 = Device(testbed=testbed, name='R1', os='iosxe')

        #uut_list = [uut4,uut5]
        uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut15]
        uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6]    

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

        conf_dict=yaml.load(open('ospf_topo.yaml'))
        '''  
        for uut in [uut9,uut13]:
            uut.configure('no router static')
 
        pcall(remove_intf_all,uut=tuple(uut_list))
        pcall(cleanup_igp,uut=tuple(uut_list))
        pcall(unshut_intf,uut=tuple(uut_list))
        loopback_config(uut_list)
        for uut in uut_list:  
            add_subintf_all(uut,conf_dict)
        add_isis_conf(uut_list,conf_dict)
        add_ospf_conf(uut_list,conf_dict)
 
        add_ebgp_conf(uut9,uut13,conf_dict)
        '''
        import pdb ; pdb.set_trace()

        pcall(add_mpls_interface_config,uut=tuple(uut_list))
        pcall(copy_run_start,uut=tuple(uut_list_iosxe))
   
        pass
        
class test_ospf_route_filter_distrib_list1(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def test_ospf_route_filter_distrib_list1(self, testbed):
        result_list = []  
        uut = uut4
        #import  pdb;pdb.set_trace()
        #  1.1.1.1--- uut3=====uut4===uut5/6
        cmd = \
            """
            no ip prefix-list deny-1-1-1-1 deny 1.1.1.1/32
            router ospf 100
            no distribute-list prefix deny-1-1-1-1 in
            """
        uut.configure(cmd)
        if not 'via' in uut4.execute('show ip route 1.1.1.1')  :
            result_list.append('fail')
        #rt1 = uut.parse('show ip route')
        rt2 = uut.parse('show ip route 1.1.1.1') 
        #rt3 = uut.parse('show ip ospf database') 
        #routes = uut.learn('routing')
        uut.configure('ip prefix-list deny-1-1-1-1 deny 1.1.1.1/32')
        cmd = \
            """
            router ospf 100
            distribute-list prefix deny-1-1-1-1 in
            """
        uut.configure(cmd)   
        #rt22 = uut.parse('show ip route 1.1.1.1') 

        if 'via' in uut.execute('show ip route 1.1.1.1'):
            result_list.append('fail')
        elif not 'via' in uut5.execute('show ip route 1.1.1.1')  :
            result_list.append('fail')
        cmd = \
            """
            router ospf 100
            no distribute-list prefix deny-1-1-1-1 in
            """
        uut.configure(cmd)
        if not 'via' in uut4.execute('show ip route 1.1.1.1')  :
            result_list.append('fail')
        elif not 'via' in uut5.execute('show ip route 1.1.1.1')  :
            result_list.append('fail')
        if 'fail' in result_list:
            self.failed()
 
class test_ospf_route_filter_distrib_listv6(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def test_ospf_route_filter_distrib_listv6(self, testbed):
        result_list = []  
        uut = uut4
 
        cmd = \
            """
            no ipv6 prefix-list deny-2001:1:187:1:1::8C05 deny 2001:1:187:1:1::8C05/128
            router ospfv3 100
            address-family ipv6 unicast 
            #no distribute-list prefix deny-2001:1:187:1:1::8C05 in
            """
        uut.configure(cmd)
        if not 'via' in uut4.execute('show ipv6 route 2001:1:187:1:1::8C05'):
            result_list.append('fail')
 
        cmd = \
            """
            ipv6 prefix-list deny-2001:1:187:1:1::8C05 deny 2001:1:187:1:1::8C05/128
            router ospfv3 100
            address-family ipv6 unicast 
            distribute-list prefix deny-2001:1:187:1:1::8C05 in
            """
 
        uut.configure(cmd)   
 

        if 'via' in uut4.execute('show ipv6 route 2001:1:187:1:1::8C05'):
            result_list.append('fail')
        elif not 'via' in uut5.execute('show ipv6 route 2001:1:187:1:1::8C05'):
            result_list.append('fail')
        cmd = \
            """
            router ospfv3 100
            address-family ipv6 unicast 
            no distribute-list prefix deny-2001:1:187:1:1::8C05 in
            """
        uut.configure(cmd)
        if not 'via' in uut4.execute('show ipv6 route 2001:1:187:1:1::8C05'):
            result_list.append('fail')
        elif not 'via' in uut5.execute('show ipv6 route 2001:1:187:1:1::8C05'):
            result_list.append('fail')
        if 'fail' in result_list:
            self.failed()




if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))