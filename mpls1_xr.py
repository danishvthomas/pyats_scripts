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

"""
9b1dfa        n0        0,1                 CE1                mpls.virl
9b1dfa        n1      0,1,2              SP1PE1                mpls.virl
9b1dfa       n10        0,1               SP3P1                mpls.virl
9b1dfa       n11        0,1               SP3P2                mpls.virl
9b1dfa       n12        0,1               SP3P3                mpls.virl
9b1dfa       n13        0,1               SP3P4                mpls.virl
9b1dfa       n14        0,1               SP3P5                mpls.virl
9b1dfa       n15        0,1               SP3P6                mpls.virl
9b1dfa       n16        0,1              SP3PE2                mpls.virl
9b1dfa       n17      0,1,2              SP3PE3                mpls.virl
9b1dfa       n18        0,1                 CE3                mpls.virl
9b1dfa       n19        0,1                 CE4                mpls.virl
9b1dfa        n2        0,1               SP1P1                mpls.virl
9b1dfa        n3        0,1               SP1P2                mpls.virl
9b1dfa        n4      0,1,2              SP1PE2                mpls.virl
9b1dfa        n5      0,1,2              SP2PE1                mpls.virl
9b1dfa        n6        0,1               SP2P1                mpls.virl
9b1dfa        n7      0,1,2              SP2PE2                mpls.virl
9b1dfa        n8        0,1                 CE2                mpls.virl
9b1dfa        n9        0,1              SP3PE1                mpls.virl
"""

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'
    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,xrv_1,xrv_2,xrv_3,xrv_4,xrv_5,xrv_6,xrv_7,xrv_8,xr_uut_list,\
            SP3PE2,SP3PE3,CE3,CE4,SP3P1,SP3P2,SP3P3,SP3P4,SP3P5,SP3P6,sp1_uut_list,\
            core_uut_list_iosxe,xr_uut_list,xe_uut_list,core_uut_list,sp3_uut_list,sp2_uut_list

        xrv_1 = testbed.devices['xrv_1']
        xrv_2 = testbed.devices['xrv_2']
        xrv_3 = testbed.devices['xrv_3']
        xrv_4 = testbed.devices['xrv_4']
        xrv_5 = testbed.devices['xrv_5']
        xrv_6 = testbed.devices['xrv_6']
        xrv_7 = testbed.devices['xrv_7']


        uut_list1 =  list(testbed.devices.keys())
        uut_list = [xrv_1,xrv_2,xrv_3,xrv_4,xrv_5,xrv_6,xrv_7]
        xe_uut_list = []
        core_uut_list = []
        sp3_uut_list = []
        sp2_uut_list = []
        sp1_uut_list = []
        xr_uut_list = []
        """
        for uut in testbed.devices.keys():
            if not 'jumphost' in uut:
                dev = testbed.devices[uut]
                uut_list.append(dev)
                if not 'xr' in dev.os:
                    xe_uut_list.append(dev)
                elif  'xr' in dev.os:
                    xr_uut_list.append(dev)
        for uut in testbed.devices.keys():
            if not 'jumphost' in uut:
                dev = testbed.devices[uut]
                if not 'CE' in dev.name:
                    core_uut_list.append(dev)
        """
        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'MPLS' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    if uut.name == node_label:
                        uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)
        #for uut in [xrv_1]:
        for uut in uut_list:
            uut.connect()


    @aetest.subsection
    def basic_conf_devices(self, testbed):
        area_l1_1 = '49.0001'

        logger.info('Configuring ISIS' )
        #configure_sr_isis_xe
        logger.info('Configuring Sxrv_' )
        for uut in uut_list:
            configure_isis_new(uut,area_l1_1,uut_list.remove(uut))

        sr_isis_cfg = \
        """
        segment-routing mpls
         !
        connected-prefix-sid-map
        address-family ipv4
        {ip}/32 index {index} range 1
        exit-address-family

        !
        router isis 100

        metric-style wide
        no hello padding
        log-adjacency-changes all
        segment-routing mpls
        segment-routing prefix-sid-map advertise-local
        passive-interface Loopback0
        !
        """

        cmd = \
        """
        router isis 100
        is-type level-1


        mpls traffic-eng router-id Loopback0
        mpls traffic-eng level-1

        """
        #for uut in uut_list:
        #    uut.configure(cmd)
        #pcall(configure_sr_isis_xe,uut=tuple(uut_list))
        #for uut in uut_list:
        #    uut.execute("clear isis *")
        #pcall(configure_sr_isis_x

class check_sr_isis(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        pass

    @aetest.test
    def sr_isis_test(self, testbed):
         pass
         #for uut in [xrv_1]:
         #for uut in uut_list:
         #    if not check_isis_sr(uut):
         #         self.failed()



if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HExrv_E = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HExrv_E, '..', 'files', 'workshop-testbed.yaml')))
