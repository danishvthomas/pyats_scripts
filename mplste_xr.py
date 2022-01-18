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
        global uut_list,xrv_0,xrv_1,xrv_2,xrv_3,xrv_4,xrv_5,xrv_6,xrv_7,xrv_8,xrv_9,xrv_10,xrv_11,xrv_12,xr_uut_list,\
            SP3PE2,SP3PE3,CE3,CE4,SP3P1,SP3P2,SP3P3,SP3P4,SP3P5,SP3P6,sp1_uut_list,\
            core_uut_list_iosxe,xr_uut_list,xe_uut_list,core_uut_list,sp3_uut_list,sp2_uut_list
        xrv_0 = testbed.devices['xrv-0']
        xrv_1 = testbed.devices['xrv-1']
        xrv_2 = testbed.devices['xrv-2']
        xrv_3 = testbed.devices['xrv-3']
        xrv_4 = testbed.devices['xrv-4']
        xrv_5 = testbed.devices['xrv-5']
        xrv_6 = testbed.devices['xrv-6']
        xrv_7 = testbed.devices['xrv-7']
        xrv_8 = testbed.devices['xrv-8']
        xrv_9 = testbed.devices['xrv-9']
        xrv_10 = testbed.devices['xrv-10']
        xrv_11 = testbed.devices['xrv-11']
        xrv_12 = testbed.devices['xrv-12']


        uut_list1 =  list(testbed.devices.keys())
        uut_list = [xrv_0,xrv_1,xrv_2,xrv_3,xrv_4,xrv_5,xrv_6,xrv_7,xrv_8,xrv_9,xrv_10,xrv_11,xrv_12]
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
            if 'mpls' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    if uut.name == node_label:
                        uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)
        for uut in [xrv_0,xrv_11,xrv_7,xrv_3,xrv_12]:
        #for uut in uut_list:
            uut.connect()


    @aetest.subsection
    def basic_conf_devices(self, testbed):


        pcall(remove_intf_all,uut=tuple(uut_list))
        #pcall(cleanup_igp,uut=tuple(uut_list))
        #pcall(unshut_intf,uut=tuple(uut_list))

        #loopback_config(uut_list)
        #uut_list1 = uut_list
        #for uut1 in uut_list1:
        #    uut_list2 = uut_list
        #    uut_list2.remove(uut1)
        #    for uut2 in uut_list2 :end
        #        bring_up_l3_link(uut1,[uut2])
        area_l1_1 = '49.0001'


        #for uut in uut_list:
        #    configure_isis_new(uut,area_l1_1,uut_list)

        #pcall(add_mpls_config,uut=tuple(uut_list))




        #import pdb;pdb.set_trace()
        #pcall(mpls_te_xr_isis,uut=tuple(uut_list))
        #pcall(rsvp_xr_isis,uut=tuple(uut_list))
        #pcall(te_xr_isis,uut=tuple(uut_list))


class bring_up_te(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        cfg =\
        """
        interface tunnel-te1010
        ipv4 unnumbered Loopback0
        priority 0 0
        signalled-bandwidth 10
        destination 11.11.11.1
        path-option 10 dynamic
        """
        #xrv_0.configure(cfg)
        #time.sleep(5)
    @aetest.test
    def te_test(self, testbed):
         #pass
         for uut in [xrv_0]:
             op = uut.execute("sh mpls traffic-eng tunnels")
             if not "Admin:    up Oper:   up   Path:  valid   Signalling: connected" in op:
                 self.failed()

class bring_up_vpls(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        #
        #    xrv_11--0/0/0/2-----------0/0/0/4--xrv_7------mpls-----xrv_3-------0/0/0/1--------xrv12
        #
        #import pdb;pdb.set_trace()
        cfg1=\
        """

        interface BVI100
         ipv4 address 100.1.1.10 255.255.255.0
        interface GigabitEthernet0/0/0/4
          l2transport
          exit
          no ipv4 address
          no ipv4 directed-broadcast
          negotiation auto
          no cdp

        l2vpn
         bridge group DT
          bridge-domain DT1
           interface GigabitEthernet0/0/0/4

           vfi vfidt1
            neighbor 4.4.4.1 pw-id 100

           routed interface BVI100

        """
        cfg2=\
        """

        interface BVI100
         ipv4 address 100.1.1.20 255.255.255.0

        interface GigabitEthernet0/0/0/1
          l2transport

          no ipv4 address
          no ipv4 directed-broadcast
          negotiation auto
          no cdp

        l2vpn
         bridge group DT
          bridge-domain DT1
           interface GigabitEthernet0/0/0/1

           vfi vfidt1
            neighbor 8.8.8.1 pw-id 100

           routed interface BVI100


        """
        xrv_7.configure(cfg1)
        xrv_3.configure(cfg2)

        cfgce1=\
        """

        interface GigabitEthernet0/0/0/2
         ip address 100.1.1.1/24
        """
        cfgce2=\
        """

        interface GigabitEthernet0/0/0/1
         ip address 100.1.1.2/24
        """
        xrv_11.configure(cfgce1)
        xrv_12.configure(cfgce2)

        #time.sleep(5)
    @aetest.test
    def vpls_test(self, testbed):
        import pdb;pdb.set_trace()
        """
        RP/0/0/CPU0:xrv-3#sh l2vpn bridge-domain brief
        Mon Jan 10 15:02:23.706 UTC
        Legend: pp = Partially Programmed.
        Bridge Group:Bridge-Domain Name  ID    State          Num ACs/up   Num PWs/up    Num PBBs/up Num VNIs/up
        -------------------------------- ----- -------------- ------------ ------------- ----------- -----------
        DT:DT1                           0     up             1/1          1/0           0/0         0/0

        RP/0/0/CPU0:xrv-3#sh l2vpn bridge-domain
        Mon Jan 10 15:02:28.716 UTC
        Legend: pp = Partially Programmed.
        Bridge group: DT, bridge-domain: DT1, id: 0, state: up, ShgId: 0, MSTi: 0
          Aging: 300 s, MAC limit: 4000, Action: none, Notification: syslog
          Filter MAC addresses: 0
          ACs: 1 (1 up), VFIs: 1, PWs: 1 (0 up), PBBs: 0 (0 up), VNIs: 0 (0 up)
          List of ACs:
            Gi0/0/0/3.100, state: up, Static MAC addresses: 0
          List of Access PWs:
          List of VFIs:
            VFI vfidt1 (up)
              Neighbor 1.1.1.1 pw-id 100, state: down, Static MAC addresses: 0
          List of Access VFIs:
        RP/0/0/CPU0:xrv-3#

        """
         #pass
        for uut in [xrv_7,xrv_3]:
            op = uut.execute("sh l2vpn bridge-domain")
            if not "VFI vfidt1 (up)" in op:
                self.failed()
        import pdb;pdb.set_trace()

if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HExrv_E = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HExrv_E, '..', 'files', 'workshop-testbed.yaml')))
