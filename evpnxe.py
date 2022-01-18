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
import pdb

igp = 'ospf'

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'
    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,core_uut_list,CE1,CE2,PE1,PE2,PE3,P1,CE1AS1,CE1AS2,CE1AS3,CE2AS3,PE1AS1,PE1AS2,PE1AS3,PE2AS1,PE2AS2,PE2AS3,ASBR1AS1,ASBR1AS2,ASBR1AS3,\
        P1AS1,P1AS2,P2AS2,P1AS3,P2AS3,P3AS3,P4AS3,as1_uut_list,as2_uut_list,as3_uut_list,xe_uut_list,xr_uut_list,igp


        CE1 = testbed.devices['CE1']
        CE2 = testbed.devices['CE2']

        PE1 = testbed.devices['PE1']
        PE2 = testbed.devices['PE2']
        PE3 = testbed.devices['PE3']


        P1 = testbed.devices['P1']

        uut_list = [ CE1,CE2,PE1,PE2,PE3,P1]

        core_uut_list =[PE1,PE2,PE3,P1]

        as1_uut_list = []
        as2_uut_list = []
        as3_uut_list = []
        xe_uut_list = []
        xr_uut_list = []

        for uut in uut_list:
            if "iosxr" in uut.os:
                xr_uut_list.append(uut)
            elif "iosxe" in uut.os:
                xe_uut_list.append(uut)


        jumphost = testbed.devices['jumphost']
        jumphost.connections['cli']['ip']=ipaddress.IPv4Address('192.168.234.148')

        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'evpn' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    if uut.name == node_label:
                        uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

        for uut in core_uut_list:
            uut.connect()



    @aetest.subsection
    def basic_conf_devices(self, testbed):

        #pcall(clean1,uut=tuple([PE1,PE2,PE3]))
        import pdb;pdb.set_trace()

        pcall(remove_intf_all,uut=tuple(core_uut_list))
        pcall(cleanup_igp,uut=tuple(core_uut_list))
        pcall(unshut_intf,uut=tuple(core_uut_list))
        pcall(add_lldp,uut=tuple(core_uut_list))
        loopback_config(core_uut_list)
        uut_list2 = core_uut_list
        for uut in core_uut_list:
            for uut2 in uut_list2:
                if not uut == uut2:
                    print("UUT1 is %r,UUT2 is %r",uut.name,uut2.name)
                    add_l3_link(uut,[uut2])

        if 'ospf' in igp:
            pcall(add_ospf_configs,uut=tuple(core_uut_list))
        elif 'isis' in igp:
            pcall(add_isis_configs,uut=tuple(core_uut_list))

        pcall(add_mpls_conf,uut=tuple(core_uut_list))

        rr1 = get_ipv4(P1,'Loopb0')

        pe1 = get_ipv4(PE1,'Loopb0')
        pe2 = get_ipv4(PE2,'Loopb0')
        pe3 = get_ipv4(PE3,'Loopb0')
        #evpn_pe_conf_bgp_xe(PE1,rr1,pe1,'1')
        #evpn_pe_conf_bgp_xe(PE2,rr1,pe2,'1')
        #evpn_pe_conf_bgp_xe(PE3,rr1,pe2,'1')

        bgp_l2vpn_evpn_xr(P1,[pe1,pe2,pe3])

        pcall(add_l2vpn_evpn_mh,uut=tuple([PE1,PE2]))
        pcall(add_l2vpn_evpn_sa,uut=tuple([PE3]))


        pcall(copy_run_start,uut=tuple(core_uut_list))

        #pcall(rsvp_isis,uut=tuple(core_uut_list))
        #pcall(mpls_te_isis,uut=tuple(core_uut_list))

class bring_up_te(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        """
        Te Tunnel from PE1AS3(xr) to ASBR1AS3(xe)
        """
        cfg =\
        """
        interface tunnel-te1010
        ipv4 unnumbered Loopback0
        priority 0 0
        signalled-bandwidth 4444
        destination 13.13.13.1
        path-option 10 dynamic
        """
        #PE1AS3.configure(cfg)
        #time.sleep(5)
    @aetest.test
    def te_test(self, testbed):
        pass
        #for uut in [PE1AS3]:
        #    op = uut.execute("sh mpls traffic-eng tunnels")
        #    if not "Admin:    up Oper:   up   Path:  valid   Signalling: connected" in op:
        #        self.failed()


if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HExrv_E = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HExrv_E, '..', 'files', 'workshop-testbed.yaml')))
