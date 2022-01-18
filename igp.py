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
        global uut_list,Router_A,Router_B,Router_C,Router_D,Router_E,Router_F,Router_G,Router_H,core1xe, abr2xr, xrv_0,xrv_1,xrv_10,xrv_11,nxos9000_0,\
            xrv_2,xrv_3,xrv_4,xrv_5,xrv_6,xrv_7,xrv_8,xrv_9,\
               xe_uut_list,xr_uut_list,uut_list_core,l1_uut_list,\
            CE1,PE1AS1,P1AS1,PE2AS1,CSCPE1,CSCP1,CSCPE2,PE1AS2,P1AS2,PE2AS2,CE2

        CE1 = testbed.devices['CE1']
        PE1AS1 = testbed.devices['PE1AS1']
        P1AS1 = testbed.devices['P1AS1']
        PE2AS1 = testbed.devices['PE2AS1']
        CSCPE1 = testbed.devices['CSCPE1']
        CSCP1 = testbed.devices['CSCP1']
        CSCPE2 = testbed.devices['CSCPE2']
        PE1AS2 = testbed.devices['PE1AS2']
        P1AS2 = testbed.devices['P1AS2']
        PE2AS2 = testbed.devices['PE2AS2']
        CE2 = testbed.devices['CE2']


        uut_list1 =  list(testbed.devices.keys())
        uut_list = [CE1,PE1AS1,P1AS1,PE2AS1,CSCPE1,CSCP1,CSCPE2,PE1AS2,P1AS2,PE2AS2,CE2]


        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'isis' in line:
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


        #conf_dict=yaml.load(open('umpls_topo.yaml'))
        """
        Topology 1--- connectivity
        A----B----C    D
        |    |     \  /
        |    |      X
        |    |     /  \
        E----F----G    H


        Topology 1--- ISIS
        A----B----C    D
        |    |     \  /
        |    |      X
        |    |     /  \
        E----F----G    H



        """

        #conf_dict_list = []
        #for uut in uut_list:
        #    conf_dict_list.append(conf_dict)


        pcall(remove_intf_all,uut=tuple(uut_list))
        pcall(cleanup_igp,uut=tuple(uut_list))
        pcall(unshut_intf,uut=tuple(uut_list))

        loopback_config(uut_list)

        bring_up_subif4(Router_A,[Router_B,Router_E])
        bring_up_subif4(Router_B,[Router_C,Router_F])
        bring_up_subif4(Router_E,[Router_F])
        bring_up_subif4(Router_F,[Router_G])
 
        import pdb; pdb.set_trace()
        bring_up_lan([Router_C,Router_D,Router_G,Router_H],['Gi0/0','Gi0/0','Gi0/0','Gi0/0'],100)
        """
        area_l1_1 = '49.0001'
        area_l2 = '49.0000'
        area_l1_2 = '49.0002'
        area_l1_3 = '49.0003'

        for uut in [xrv_0,xrv_1,xrv_2]:
            configure_isis_new(uut,area_l1_1,l1_uut_list)
        for uut in [xrv_9,xrv_7,xrv_8]:
            configure_isis_new(uut,area_l1_2,l1_uut_list)
        for uut in [xrv_11,xrv_10]:
            configure_isis_new(uut,area_l1_3,l1_uut_list)
        for uut in [xrv_4,xrv_3,xrv_5,xrv_6]:
            configure_isis_new(uut,area_l2,l1_uut_list)

        #pcall(configure_interfaces,uut=tuple(uut_list),conf_dict=tuple(conf_dict_list))
        #pcall(configure_isis,uut=tuple(uut_list),conf_dict=tuple(conf_dict_list))
        pcall(mplsldpAutoconfig,uut=tuple(uut_list))

        #pcall(copy_run_start,uut=tuple(xe_uut_list))

        from netmiko import ConnectHandler

        cisco = {
            'device_type': 'cisco_ios',
            'host': 'cisco.domain.com',
            'username': 'admin',
            'password': 'cisco123',
            }

        """
if __name__ == "__main__":
    # if this script is run standalone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshoptestbed.yaml')))
