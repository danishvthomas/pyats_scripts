#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock
import logging
import secrets
from genie.libs.conf.isis import Isis
# Genie package
#from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
import random
# Genie Conf
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface import Interface
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.ospf.gracefulrestart import GracefulRestart
from genie.libs.conf.ospf.stubrouter import StubRouter
from genie.libs.conf.ospf.areanetwork import AreaNetwork
from genie.libs.conf.ospf.arearange import AreaRange
from genie.libs.conf.ospf.interfacestaticneighbor import InterfaceStaticNeighbor
import pdb
import time
from genie.libs.conf.ldp import Ldp
from unicon.eal.dialogs import Statement, Dialog
import random
from netaddr.ip import IPNetwork, IPAddress
from randmac import RandMac

logger = logging.getLogger(__name__)
from unicon.eal.dialogs import Statement, Dialog
from genie.libs.conf.lldp import Lldp



from genie.libs.conf.bgp import Bgp
import ipaddress
import random

MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1
MAX_IPV6 = ipaddress.IPv6Address._ALL_ONES  # 2 ** 128 - 1



def parseCDPNei(uut):
    pass
    """
    RP/0/0/CPU0:P1#show cdp nei detail
    Mon Jan 17 04:34:52.910 UTC

    -------------------------
    Device ID: PE1
    SysName :
    Entry address(es):
      IPv4 address: 99.0.135.1
      IPv6 address: 2001:beef:0:135::29
      IPv6 address: fe80::5054:ff:fe00:b634
    Platform: cisco CSR1000V,  Capabilities: Router IGMP
    Interface: GigabitEthernet0/0/0/0
    Port ID (outgoing port): GigabitEthernet2
    Holdtime : 158 sec

    Version :
    Cisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.3.2, RELEASE SOFTWARE (fc3)
    Technical Support: http://www.cisco.com/techsupport
    Copyright (c) 1986-2020 by Cisco Systems, Inc.
    Compiled Sat 31-Oct-20 13:16 by mcpre

    advertisement version: 2
    Duplex: full

    -------------------------
    Device ID: PE2
    SysName :
    Entry address(es):
      IPv4 address: 99.0.137.1
      IPv6 address: 2001:beef:0:137::2
      IPv6 address: fe80::5054:ff:fe08:f404
    Platform: cisco CSR1000V,  Capabilities: Router IGMP
    Interface: GigabitEthernet0/0/0/1
    Port ID (outgoing port): GigabitEthernet2
    Holdtime : 171 sec

    Version :
    Cisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.3.2, RELEASE SOFTWARE (fc3)
    Technical Support: http://www.cisco.com/techsupport
    Copyright (c) 1986-2020 by Cisco Systems, Inc.
    Compiled Sat 31-Oct-20 13:16 by mcpre

    advertisement version: 2
    Duplex: full
    """

def add_l3_link(uut1,uut2):
    "P1                  Gi2            30         R               Gi0/0/0/0"
    "PE1             Gi0/0/0/0           30         R               Gi2"


def add_l3_link(uut1,nei_list):
    for uut in nei_list:
        op1=uut1.execute('show lldp ne | incl {a}'.format(a=uut.name))
        for line in op1.splitlines():
            if uut.name in line:
                a = random.randint(31,70)
                b = random.randint(31,70)
                encap = int(a+b)+random.randint(10,30)
                if encap == 127:
                    encap = encap + random.randint(25,50)
                elif encap == 100:
                    encap = encap + random.randint(25,50)
                elif encap > 200:
                    encap = random.randint(25,199)
                intf_uut1 = line.split()[1]
                intf_uut = line.split()[-1]
                c = random.randint(100,200)
                uut1_ip = "99.0."+str(encap)+".1"
                uut_ip = "99.0."+str(encap)+".2"
                description = uut1.name+"----"+uut.name
                configure_l3_intf(uut1,intf_uut1,encap,uut1_ip,description)
                configure_l3_intf(uut,intf_uut,encap,uut_ip,description)

def add_lldp(uut):
    if uut.os == 'iosxr':
        add_lldp_xr(uut)
    elif uut.os == 'iosxe':
         add_lldp_xe(uut)

def add_lldp_xe(uut):
    lldp = Lldp()
    uut.add_feature(lldp)
    lldp.device_attr[uut].enabled = True
    lldp.device_attr[uut].hello_timer = 20
    lldp.device_attr[uut].hold_timer = 30
    lldp.device_attr[uut].reinit_timer = 5
    lldp.device_attr[uut].tlv_select_attr.suppress_tlv_port_description = False
    lldp.device_attr[uut].tlv_select_attr.suppress_tlv_system_name = False
    lldp.device_attr[uut].tlv_select_attr.suppress_tlv_system_description = False
    lldp.device_attr[uut].tlv_select_attr.suppress_tlv_system_capabilities = False
    lldp.device_attr[uut].tlv_select_attr.suppress_tlv_system_description = False
    intf_list = get_igp_intf_list(uut)
    for intf1 in intf_list:
        if not 'oop' in intf1:
            lldp.device_attr[uut].interface_attr[intf1].if_enabled = True
    cfgs = lldp.build_config(apply=True)

def add_lldp_xr(uut):
    cfg = \
    """
    lldp
    timer 20
    holdtime 30
    """
    uut.configure(cfg)


def add_l2vpn_evpn_mh(uut):
    cfg = \
    """
    l2vpn evpn
     replication-type ingress
     router-id Loopback0
    !
    l2vpn evpn instance 10 vlan-based
    !
    l2vpn evpn instance 20 vlan-bundle
    !
    l2vpn evpn instance 30 vlan-aware
    !
    !
    !
    !
    bridge-domain 10
     mac aging-time 30
     member Port-channel1 service-instance 10
     member evpn-instance 10
    !
    bridge-domain 20
     mac aging-time 30
     member Port-channel1 service-instance 20
     member evpn-instance 20
    !
    bridge-domain 30
     mac aging-time 30
     member Port-channel1 service-instance 30
     member evpn-instance 30 ethernet-tag 30
    !
    !
    !
    interface Port-channel1
     no ip address
     no shutdown
     no negotiation auto
     no mop enabled
     no mop sysid
     evpn ethernet-segment 1
      identifier type 3 system-mac abcd.abcd.abc1
      redundancy all-active
     service instance 10 ethernet
      encapsulation dot1q 10
     !
     service instance 20 ethernet
      encapsulation dot1q 20-21
     !
     service instance 30 ethernet
      encapsulation dot1q 30
     !
    !
    interface GigabitEthernet1
     description PE1----CE1
     no ip address
     negotiation auto
     cdp enable
     no mop enabled
     no mop sysid
     channel-group 1
     no shutdown
    !
    """
    uut.configure(cfg)

def clean1(uut):
    cfg = \
    """
    !
    bridge-domain 10
     mac aging-time 30
     no member GigabitEthernet1 service-instance 10
     no member evpn-instance 10
    !
    bridge-domain 20
     mac aging-time 30
     no member GigabitEthernet1 service-instance 20
     no member evpn-instance 20
    !
    bridge-domain 30
     mac aging-time 30
     no member GigabitEthernet1 service-instance 30
     no member evpn-instance 30 ethernet-tag 30
    !
    no bridge-domain 30
    no bridge-domain 20
    no bridge-domain 10
    no l2vpn evpn
    no interf po 1
    default interface Gi1
    no router bgp 1
    """
    uut.configure(cfg)

def add_l2vpn_evpn_sa(uut):
    cfg = \
    """
    l2vpn evpn
     replication-type ingress
     router-id Loopback0
    !
    l2vpn evpn instance 10 vlan-based
    !
    l2vpn evpn instance 20 vlan-bundle
    !
    l2vpn evpn instance 30 vlan-aware
    !
    !
    !
    bridge-domain 10
     mac aging-time 30
     member GigabitEthernet1 service-instance 10
     member evpn-instance 10
    !
    bridge-domain 20
     mac aging-time 30
     member GigabitEthernet1 service-instance 20
     member evpn-instance 20
    !
    bridge-domain 30
     mac aging-time 30
     member GigabitEthernet1 service-instance 30
     member evpn-instance 30 ethernet-tag 30
    !
    !
    interface GigabitEthernet1
     no ip address
     no shut
     negotiation auto
     cdp enable
     no mop enabled
     no mop sysid
     service instance 10 ethernet
      encapsulation dot1q 10
     !
     service instance 20 ethernet
      encapsulation dot1q 20-21
     !
     service instance 30 ethernet
      encapsulation dot1q 30
     !
    !
    """
    uut.configure(cfg)

def random_ipv4():
    return  ipaddress.IPv4Address._string_from_ip_int(
        random.randint(0, MAX_IPV4)
    )

def random_ipv6():
    return ipaddress.IPv6Address._string_from_ip_int(
        random.randint(0, MAX_IPV6)
    )
def mpls_te_isis(uut):
    if "iosxr" in uut.os:
        mpls_te_xr_isis(uut)
    elif "iosxe" in uut.os:
        mpls_te_xe_isis(uut)

def mpls_te_xr_isis(uut):

    te_conf = \
    """
            mpls traffic-eng
            mpls traffic-eng tunnels
            rsvp
            router isis 100
            address-family ipv4 unicast
            metric-style wide
            no advertise passive-only
            mpls traffic-eng level-1
            mpls traffic-eng router-id loopback 0

    """

    try:
        uut.configure(te_conf)
    except:
        logger.info('Failed mpls_te_xr_isis device %s' % uut.name)
    te_xr_isis(uut)



def mpls_te_xe_isis(uut):
    te_conf = \
    """
             mpls traffic-eng tunnels
             router isis 100
            mpls traffic-eng level-1
            mpls traffic-eng router-id loopback 0

    """
    try:
        uut.configure(te_conf)
    except:
        logger.info('Failed mpls_te_xe_isis device %s' % uut.name)


def rsvp_isis(uut):
    if 'iosxr' in uut.os:
        rsvp_xr_isis(uut)
    elif 'iosxe' in uut.os:
        rsvp_xe_isis(uut)


def rsvp_xr_isis(uut):
    intf_list =[]
    op = uut.execute("show isis ne")
    cfg_rsvp = \
    """
    rsvp
    """
    for line in op.splitlines():
        if 'Gi0/0/0/' in line:
            intf = line.split()[1]
            cfg_rsvp += 'interface {intf} \n'.format(intf=intf)
            cfg_rsvp += 'bandwidth percentage 80 \n'

    uut.configure(cfg_rsvp)


def rsvp_xe_isis(uut):
    intf_list =[]
    op = uut.execute("show isis ne")
    cfg_rsvp = \
    """

    """
    for line in op.splitlines():
        if 'Gi' in line:
            intf = line.split()[2]
            cfg_rsvp += 'interface {intf} \n'.format(intf=intf)
            cfg_rsvp += 'ip rsvp bandwidth percent 80 \n'

    uut.configure(cfg_rsvp)

def te_xr_isis(uut):
    intf_list =[]
    op = uut.execute("show isis ne")
    cfg_te = \
    """
    mpls traffic-eng
    """
    for line in op.splitlines():
        if 'Gi0/0/0/' in line:
            intf = line.split()[1]
            cfg_te += 'interface {intf} \n'.format(intf=intf)

    uut.configure(cfg_te)

    uut.configure(cfg_rsvp)

def te_intf_xe_isis(uut):
    intf_list =[]
    op = uut.execute("show isis ne")
    cfg_te = \
    """
    """
    for line in op.splitlines():
        if 'Gi' in line:
            intf = line.split()[2]
            cfg_te += 'interface {intf} \n'.format(intf=intf)
            cfg_te += 'mpls traffic-eng tu \n'
    uut.configure(cfg_te)


"""
leaf1# sh cdp ne
Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater,
                  V - VoIP-Phone, D - Remotely-Managed-Device,
                  s - Supports-STP-Dispute

Device-ID          Local Intrfce  Hldtme Capability  Platform      Port ID
spine               Eth1/1         156    R B                     Gig0/1
spine               Eth1/2         158    R B                     Gig0/2
sw1                 Eth1/3         179    R S I                   Gig0/3

>>> random.seed(444)
>>> random_ipv4()
'79.19.184.109'

ipaddress.IPv4Address('192.168.0.1')
            cmdxr += 'interface {intf} \n'.format(intf=intf)
"""
def leaf_spine_l3_conf(uut,spine):
    #if uut.os == 'nxos':

    cfg1 = \
    """
    interface {intf}
    no shut
    """
    cfg2 = \
    """
    interface {intf}
    no shut
    """
    for line in uut.execute('show cdp neighbor').splitlines():
        if spine.name in line:
            if 'Eth' in line or 'Gig' in line:
                uut_intf = line.split()[1]
                spine_intf = line.split()[-1]
                #random.seed(444)
                ip1 = ipaddress.IPv4Address(ipaddress.IPv4Address._string_from_ip_int(random.randint(1000000000, 1100000000)))
                ip2 = ip1+1
                if uut.os == 'nxos':
                    cfg1 += 'no sw\n'
                cfg1 += 'ip address {ip}/24 \n'.format(ip=str(ip1))
                if spine.os == 'nxos':
                    cfg2 += 'no sw\n'
                    cfg2 += 'ip address {ip}/24 \n'.format(ip=str(ip2))
                else:
                    cfg2 += 'ip address {ip} 255.255.255.0 \n'.format(ip=str(ip2))
                uut.configure(cfg1.format(intf=uut_intf))
                spine.configure(cfg2.format(intf=spine_intf))



def bgpUMPLS(uut,nei_list):


    cmdxe =\
        """
        route-map RM_CONN_TO_BGP permit 10
        match interface Loopback0
        no router bgp 59
        router bgp 59

        template peer-policy IPV4_LUCAST
        send-community both
        send-label
        exit-peer-policy
        !
        template peer-session IBGP_SESSION
        remote-as 59
        update-source Loopback0
        exit-peer-session
        !
        bgp log-neighbor-changes
        no bgp default ipv4-unicast
        """
    if 'iosxe' in uut.os:
        if not 'pe' in uut.name:
            cmdxe += 'template peer-policy IPV4_LUCAST \n'
            cmdxe += 'route-reflector-client  \n'
        for nei in neigh_list:
            cmdxe += ' neighbor {nei} inherit peer-session IBGP_SESSION\n'.format(nei=nei)
            cmdxe += 'address-family ipv4 \n'
            cmdxe += 'redistribute connected route-map RM_CONN_TO_BGP\n'
            cmdxe += 'neighbor {nei} activate\n'.format(nei=nei)
            cmdxe += '  neighbor {nei} inherit peer-policy IPV4_LUCAST\n'.format(nei=nei)

        uut.configure(cmdxe)


    cmdxr =\
        """
        router bgp 59
        address-family ipv4 unicast
        network 12.12.12.12/32
        allocate-label all
        !
        af-group IPV4_LUCAST_CLIENT address-family ipv4 labeled-unicast
        route-reflector-client
        !
        session-group IBGP_SESSION
        remote-as 59
        update-source Loopback0
        !
        neighbor 4.4.4.4
        use session-group IBGP_SESSION
        address-family ipv4 labeled-unicast
        use af-group IPV4_LUCAST_CLIENT
        """

    if 'iosxe' in uut.os:
        #import pdb;pdb.set_trace()
        for line in uut.execute('show ip protocols').splitlines():
            if 'Routing Protocol is' in line:
                if 'isis' in line:
                    pid = line.replace('"','').split()[-1]
                    cmdxe += 'router isis {pid} \n'.format(pid=pid)
                    cmdxe += 'mpls ldp autoconfig \n'
        uut.configure(cmdxe)




def vrfConfigXr(uut,vrf,RT):
    cfg1 = \
    f"""
    vrf {vrf}
    address-family ipv4 unicast
    import route-target
    {RT}
    !
    export route-target
    {RT}   
    !
    !
    address-family ipv6 unicast
    import route-target
    {RT}
    !
    export route-target
    {RT}   
    !
    """
    uut.configure(cfg1)

def vrfIntfConfigXr(uut,vrf,intf):

    ip  = get_intf_ip(uut,intf)
    #import pdb;pdb.set_trace()
    cfg1 = \
    f"""
    interface {intf}
    no ipv4 address
    no ipv6 en
    vrf {vrf}
    ip address {ip}/24
    ipv6 en
    no sh
    """
    uut.configure(cfg1)

def peceOspfBgp(uut,intf,vrf):
    cfg = \
        f"""
        no router ospf 100
        router ospf 100
        vrf {vrf}
        redistribute bgp 65001
        area 0
        interface {intf}
        !
        !
    
        router bgp 65001
        address-family ipv4 unicast
        !
        vrf {vrf}
        rd 65001:1
        address-family ipv4 unicast
        redistribute connected
        redistribute ospf 100
        !
    
        """
    uut.configure(cfg)

def addL3VpnService(uut,vrf,intf,RT):
    vrfConfigXr(uut,vrf,RT)
    vrfIntfConfigXr(uut,vrf,intf)
    peceOspfBgp(uut,intf,vrf)


def addBgpUmplsxr(uut,nei_list):
    neigh_ip_list = []
    for uut1 in nei_list:
        ip = get_intf_ip(uut1,'Loopback0')
        neigh_ip_list.append(ip)
    nwk  = get_intf_ip(uut,'Loopback0')+"/32"
    AS1 = '65001'
    cmdxr =\
        f"""
        router bgp {AS1}
        ibgp policy out enforce-modifications
        address-family ipv4 unicast
        network {nwk}
        allocate-label all
        !
        af-group IPV4_LUCAST_CLIENT address-family ipv4 labeled-unicast
        """
    if not "PE" in uut.name: 
        cmdxr += ' route-reflector-client \n'   
        cmdxr += ' next-hop-self \n'   
    cmdxr += 'session-group IBGP_SESSION \n' 
    cmdxr += f'remote-as {AS1} \n' 
    cmdxr += 'update-source Loopback0 \n' 
  
    for neigh in neigh_ip_list:
        cmdxr += f' neighbor {neigh} \n'
        cmdxr += ' use session-group IBGP_SESSION \n'
        cmdxr += ' address-family ipv4 labeled-unicast \n'
        cmdxr += ' use af-group IPV4_LUCAST_CLIENT \n'
    
    uut.configure(cmdxr)


def addBgpVpnv4xr(uut,nei_list):
    neigh_ip_list = []
    for uut1 in nei_list:
        ip = get_intf_ip(uut1,'Loopback0')
        neigh_ip_list.append(ip)
    nwk  = get_intf_ip(uut,'Loopback0')+"/32"
    AS1 = '65001'
    cmdxr =\
        f"""
        router bgp {AS1}
        address-family vpnv4 unicast
        !
        """
      
 
    for neigh in neigh_ip_list:
        cmdxr += f' neighbor {neigh} \n'
        cmdxr += f'remote-as {AS1} \n' 
        cmdxr += 'update-source Loopback0 \n' 
        cmdxr += 'address-family vpnv4 unicast \n'
    
    uut.configure(cmdxr)


def mplsldpAutoconfig(uut):
    op = uut.execute("show interf desc")
    cmdxe =\
        """
        mpls ldp router-id loopback 0 force

        """
    cmdxr =\
        """
        mpls ldp

        """

    if 'iosxe' in uut.os:
        #import pdb;pdb.set_trace()
        for line in uut.execute('show ip protocols').splitlines():
            if 'Routing Protocol is' in line:
                if 'isis' in line:
                    pid = line.replace('"','').split()[-1]
                    cmdxe += 'router isis {pid} \n'.format(pid=pid)
                    cmdxe += 'mpls ldp autoconfig \n'
        uut.configure(cmdxe)


    if 'iosxr' in uut.os:
        #import pdb;pdb.set_trace()
        rid =  get_intf_ip(uut,'Loopback0')
        cmdxr += 'mpls ldp router-id {rid} \n'.format(rid=rid)
        for line in uut.execute('show ip protocols').splitlines():
            if 'IS-IS Router' in line:
                pid = line.replace('"','').split()[-1]
                cmdxr += 'router isis {pid} \n'.format(pid=pid)
                cmdxr += 'address-family ipv4 unicast \n'
                cmdxr += ' mpls ldp auto-config \n'
        uut.configure(cmdxr)





def sp_config(uut):
    op = uut.execute("show interf desc")
    if 'abr' in uut.name():
        core_intf_list = []
        agg_intf_list = []
        for line in op.splitlines():
            if 'core' in line:
                core_intf_list.append(line.split()[0])
            elif 'agg' in line:
                agg_intf_list.append(line.split()[0])

            isis_config(uut,intf_list,is_type)


    elif 'agg' in uut.name():
        abr_intf_list = []
        pe_intf_list = []
        for line in op.splitlines():
            if 'abr' in line:
                abr_intf_list.append(line.split()[0])
            elif 'pe' in line:
                pe_intf_list.append(line.split()[0])
    elif 'pe' in uut.name():
        agg_intf_list = []
        ce_intf_list = []
        for line in op.splitlines():
            if 'agg' in line:
                agg_intf_list.append(line.split()[0])
            elif 'pe' in line:
                ce_intf_list.append(line.split()[0])


def configure_isis(uut,conf_dict):


    """
    A router has a Network Entity Title (NET) of 49.001a.1122.3344.5566.00. To what area does this router belong, and what is its system ID?
    The area is 49.001a. The router's system ID is 1122.3344.5566. The easiest way to figure this out is to start from the right and work towards the left. The last two numbers of the NET are the NSEL; they are always 00 on a router. The next 12 numbers (separated into 3 groups of 4 numbers) are the system ID. On Cisco routers, the system ID is always this length—6 bytes. Anything to the left of the system ID is the area ID.
    """

    #net = '49.0000.0000.0000.0012.00'
    cmdxr = \
    """
    no router isis 100

    router isis 100
    net {net}
    log adjacency changes
    log pdu drops
    address-family ipv4 unicast
    metric-style wide
    advertise passive-only
    address-family ipv6 unicast
    metric-style wide
    advertise passive-only
    interface Loopback0
    passive
    address-family ipv4 unicast
    address-family ipv6 unicast
    exit
    exit
    """
    cmdxe = \
    """
    ipv6 unicast-routing
    no router isis 100
    router isis 100
    net {net}
    advertise passive-only
    metric-style wide
    no hello padding
    log-adjacency-changes all
    passive-interface Loopback0
    address-family ipv6
    advertise passive-only

    """
    node_list = conf_dict['protocols']['isis']
    for key in conf_dict['protocols']['isis'].keys():
        host_name = key
        net = conf_dict['protocols']['isis'][key]['net']
        if uut.name == host_name:
            if uut.os == 'iosxr':
                #cmd += 'net {net} \n'.format(net=net)
                if 'level-2' in conf_dict['protocols']['isis'][key]['interfaces'].keys():
                    l2_intf_list = conf_dict['protocols']['isis'][key]['interfaces']['level-2']
                    for intf in l2_intf_list:
                        cmdxr += 'interface {intf} \n'.format(intf=intf)
                        cmdxr += 'address-family ipv4 unicast \n'
                        cmdxr += 'address-family ipv6 unicast \n'
                        cmdxr += 'circuit-type level-2-only \n'

                if 'level-1' in conf_dict['protocols']['isis'][key]['interfaces'].keys():
                    l1_intf_list = conf_dict['protocols']['isis'][key]['interfaces']['level-1']
                    for intf in l1_intf_list:
                        cmdxr += 'interface {intf} \n'.format(intf=intf)
                        cmdxr += 'address-family ipv4 unicast \n'
                        cmdxr += 'address-family ipv6 unicast \n'
                        cmdxr += 'circuit-type level-1 \n'

                uut.configure(cmdxr.format(net=net))

            elif uut.os == 'iosxe':
                if 'level-2' in conf_dict['protocols']['isis'][key]['interfaces'].keys():
                    l2_intf_list = conf_dict['protocols']['isis'][key]['interfaces']['level-2']
                    for intf in l2_intf_list:
                        cmdxe += 'interface {intf} \n'.format(intf=intf)
                        cmdxe += 'ip router isis 100 \n'
                        cmdxe += 'isis circuit-type level-2  \n'
                if 'level-1' in conf_dict['protocols']['isis'][key]['interfaces'].keys():
                    l1_intf_list = conf_dict['protocols']['isis'][key]['interfaces']['level-1']
                    for intf in l1_intf_list:
                        cmdxe += 'interface {intf} \n'.format(intf=intf)
                        cmdxe += 'ip router isis 100 \n'
<<<<<<< HEAD
                        cmdxe += 'isis circuit-type level-1  \n'
                uut.configure(cmdxe.format(net=net))

def configure_isis_xe(uut,area):
    mac1 = str(RandMac("0000.0000.0000"))
    net = area+"."+mac1+'.00'



def configure_isis_new(uut,area,l1_uut_list):
    mac1 = str(RandMac("0000.0000.0000"))
    net = area+"."+mac1+'.00'
    cmdnx = \
    """
    feature isis
    no router isis 100
    router isis 100
    net {net}
     address-family ipv4 unicast
     router-id loopback 0
    """

=======
                        cmdxe += 'isis circuit-type level-1  \n' 
                uut.configure(cmdxe.format(net=net))    
 


 

def configureIsis(uut,conf_dict):
 
    cmdxe = \
    """
    ipv6 unicast-routing 
    no router isis 100
    router isis 100
    net {net}
    advertise passive-only
    metric-style wide
    no hello padding
    log-adjacency-changes all
    passive-interface Loopback0
    address-family ipv6
    advertise passive-only
  
    """
    node_list = conf_dict['protocols']['isis']
    for key in conf_dict['protocols']['isis'].keys():
        host_name = key
        for key2 in conf_dict['protocols']['isis'][key].keys():
            proc_id = key2
            net = conf_dict['protocols']['isis'][key][key2]['net']
            cmdxr = \
                f"""
                no router isis {proc_id}
                router isis {proc_id}
                net {net}
                log adjacency changes
                log pdu drops
                address-family ipv4 unicast
                metric-style wide
                advertise passive-only
                address-family ipv6 unicast
                metric-style wide
                advertise passive-only
                interface Loopback0
                passive
                address-family ipv4 unicast
                address-family ipv6 unicast
                exit
                exit
                """
            if uut.name == host_name:
                if uut.os == 'iosxr':
                #cmd += 'net {net} \n'.format(net=net)
                    if 'level-2' in conf_dict['protocols']['isis'][key][key2]['interfaces'].keys():
                        l2_intf_list = conf_dict['protocols']['isis'][key][key2]['interfaces']['level-2']
                        for intf in l2_intf_list:
                            cmdxr += 'interface {intf} \n'.format(intf=intf)
                            cmdxr += 'address-family ipv4 unicast \n'
                            cmdxr += 'address-family ipv6 unicast \n' 
                            cmdxr += 'circuit-type level-2-only \n' 

                    if 'level-1' in conf_dict['protocols']['isis'][key][key2]['interfaces'].keys():
                        l1_intf_list = conf_dict['protocols']['isis'][key][key2]['interfaces']['level-1']
                        for intf in l1_intf_list:
                            cmdxr += 'interface {intf} \n'.format(intf=intf)
                            cmdxr += 'address-family ipv4 unicast \n'
                            cmdxr += 'address-family ipv6 unicast \n' 
                            cmdxr += 'circuit-type level-1 \n' 
          
                    uut.configure(cmdxr.format(net=net))            
  
            elif uut.os == 'iosxe':
                if 'level-2' in conf_dict['protocols']['isis'][key]['interfaces'].keys():
                    l2_intf_list = conf_dict['protocols']['isis'][key]['interfaces']['level-2']
                    for intf in l2_intf_list:
                        cmdxe += 'interface {intf} \n'.format(intf=intf)
                        cmdxe += 'ip router isis 100 \n'
                        cmdxe += 'isis circuit-type level-2  \n' 
                if 'level-1' in conf_dict['protocols']['isis'][key]['interfaces'].keys():
                    l1_intf_list = conf_dict['protocols']['isis'][key]['interfaces']['level-1']
                    for intf in l1_intf_list:
                        cmdxe += 'interface {intf} \n'.format(intf=intf)
                        cmdxe += 'ip router isis 100 \n'
                        cmdxe += 'isis circuit-type level-1  \n' 
                uut.configure(cmdxe.format(net=net))    
 
  

  

def addIsis(uut,inst,area,intf_list):

  
    """
    A router has a Network Entity Title (NET) of 49.001a.1122.3344.5566.00. To what area does this router belong, and what is its system ID?
    The area is 49.001a. The router's system ID is 1122.3344.5566. The easiest way to figure this out is to start from the right and work towards the left. The last two numbers of the NET are the NSEL; they are always 00 on a router. The next 12 numbers (separated into 3 groups of 4 numbers) are the system ID. On Cisco routers, the system ID is always this length—6 bytes. Anything to the left of the system ID is the area ID.
    """
    op2 = uut.execute("show run router isis")
    for line in op2.splitlines():
        if 'net' in line:
            net = line.split()[1]
    #net = '49.0000.0000.0000.0012.00'
        else:    
            mac1 = str(RandMac("0000.0000.0000"))
            net = area+"."+mac1+'.00'
>>>>>>> a7c04b8bb5dce427b1aa358b2bfcb3a15aacc289
    cmdxr = \
    f"""
    no router isis {inst}

    router isis {inst}
    net {net}
    log adjacency changes
    log pdu drops
    address-family ipv4 unicast
    metric-style wide
    no advertise passive-only
    address-family ipv6 unicast
    metric-style wide
    advertise passive-only
    interface Loopback0
    passive
    address-family ipv4 unicast
    address-family ipv6 unicast
    exit
    exit
    """
    cmdxe = \
<<<<<<< HEAD
    """
    ipv6 unicast-routing
    no router isis 100
    router isis 100
    net {net}
    no advertise passive-only
    metric-style wide
    no hello padding
    log-adjacency-changes all
    passive-interface Loopback0
    address-family ipv6
    advertise passive-only

    """
    l1_intf_list = []

    op1 = uut.execute('show int desc')
    op2 = uut.execute('show ip interf brief')


    for line in op1.splitlines():
        if 'GigabitEthernet' in line:
            l1_intf_list.append(line.split()[0])

    for line in op2.splitlines():
        if 'GigabitEthernet' in line:
            if not "unassigned" in line:
                l1_intf_list.append(line.split()[0])

    l1_intf_list = list(set(l1_intf_list))
    if uut.os == 'iosxr':
        for intf in l1_intf_list:
            cmdxr += 'interface {intf} \n'.format(intf=intf)
            cmdxr += 'address-family ipv4 unicast \n'
            cmdxr += 'address-family ipv6 unicast \n'
            cmdxr += 'circuit-type level-1 \n'

        uut.configure(cmdxr.format(net=net))

    elif uut.os == 'iosxe':
        if l1_intf_list:
            for intf in l1_intf_list:
                cmdxe += 'interface {intf} \n'.format(intf=intf)
                cmdxe += 'ip router isis 100 \n'
                cmdxe += 'isis circuit-type level-1  \n'
        uut.configure(cmdxe.format(net=net))

    elif uut.os == 'nxos':
        for line in op2.splitlines():
            if 'Eth' in line:
                if not "unassigned" in line:
                    l1_intf_list.append(line.split()[0])
        if l1_intf_list:
            for intf in l1_intf_list:
                cmdnx += 'interface {intf} \n'.format(intf=intf)
                cmdnx += 'ip router isis 100 \n'
                cmdnx += 'isis circuit-type level-1  \n'
        uut.configure(cmdnx.format(net=net))

def configure_sr_isis_xe(uut):
    for line in uut.execute('show ip int brie').splitlines():
        if 'Loopback0' in line:
            ip = line.split()[1]

    index = random.randint(1,1000)

    cfg = \
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
    uut.configure(cfg.format(ip=ip,index=index))


def check_isis_sr(uut):
    """
    R1#sh isis database

    Tag 100:
    IS-IS Level-1 Link State Database:
    LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
    R1.00-00            * 0x00000018   0xAF19                1004/*         0/0/0
    R1.02-00            * 0x00000010   0xE4FD                 932/*         0/0/0
    R4.00-00              0x00000013   0xB970                 585/1198      0/0/0
    R6.00-00              0x00000012   0xA2DA                 909/1198      0/0/0
    R7.00-00              0x00000015   0x5FB1                 817/1199      0/0/0
    R7.02-00              0x00000010   0x7E31                1072/1199      0/0/0
    R8.00-00              0x00000016   0x3C67                 413/1198      0/0/0
    R8.01-00              0x00000010   0xBA77                1045/1198      0/0/0
    R5.00-00              0x00000017   0xEEF1                 968/1198      0/0/0
    R5.01-00              0x0000000E   0xB272                 419/1198      0/0/0
    R5.02-00              0x00000011   0xBC39                 534/1198      0/0/0
    R2.00-00              0x00000016   0x41EB                 765/1199      0/0/0
    R2.01-00              0x00000010   0xFFD0                 748/1199      0/0/0
    R2.02-00              0x0000000E   0xE7B9                 346/1199      0/0/0
    R3.00-00              0x00000016   0x8815                 750/1198      0/0/0
    R3.02-00              0x00000011   0x3630                1110/1198      0/0/0
    IS-IS Level-2 Link State Database:
    LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
    R1.00-00            * 0x0000001E   0x60E0                1047/*         0/0/0

    R1#sh isis database R1.00-00 verbose
    Tag 100:

    IS-IS Level-1 LSP R1.00-00
    LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
    R1.00-00            * 0x00000018   0xAF19                 985/*         0/0/0
      Area Address: 49.0001
      NLPID:        0xCC 0x8E
      Router CAP:   1.1.1.1, D:0, S:0
        Segment Routing: I:1 V:0, SRGB Base: 16000 Range: 8000
          Segment Routing Algorithms: SPF, Strict-SPF
      Hostname: R1
      Metric: 10         IS-Extended R1.02
        Lan Adjacency SID:
          SID Value:16, R2, F:0 B:0 V:1 L:1 S:0 Weight:0
      Metric: 10         IS-Extended R7.02
        Lan Adjacency SID:
          SID Value:17, R7, F:0 B:0 V:1 L:1 S:0 Weight:0
      IP Address:   1.1.1.1
      Metric: 0          IP 1.1.1.1/32
        Prefix-attr: X:0 R:0 N:1
        Prefix-SID Index: 847, Algorithm:SPF, R:0 N:1 P:0 E:0 V:0 L:0
      Metric: 10         IP 12.1.1.0/24
        Prefix-attr: X:0 R:0 N:0
      Metric: 10         IP 17.1.1.0/24
        Prefix-attr: X:0 R:0 N:0

    IS-IS Level-2 LSP R1.00-00
    LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
    R1.00-00            * 0x0000001E   0x60E0                1028/*         0/0/0
      Area Address: 49.0001
      NLPID:        0xCC 0x8E
      Router CAP:   1.1.1.1, D:0, S:0
        Segment Routing: I:1 V:0, SRGB Base: 16000 Range: 8000
          Segment Routing Algorithms: SPF, Strict-SPF
      Hostname: R1
      IP Address:   1.1.1.1
      Metric: 0          IP 1.1.1.1/32
        Prefix-attr: X:0 R:0 N:1
        Prefix-SID Index: 847, Algorithm:SPF, R:0 N:1 P:0 E:0 V:0 L:0
      Metric: 10         IP 1.1.1.2/32
        Prefix-attr: X:0 R:1 N:1
        Prefix-SID Index: 77, Algorithm:SPF, R:1 N:1 P:1 E:0 V:0 L:0
      Metric: 20         IP 1.1.1.3/32
        Prefix-attr: X:0 R:1 N:1
        Prefix-SID Index: 78, Algorithm:SPF, R:1 N:1 P:1 E:0 V:0 L:0
      Metric: 30         IP 1.1.1.4/32
        Prefix-attr: X:0 R:1 N:1
        Prefix-SID Index: 552, Algorithm:SPF, R:1 N:1 P:1 E:0 V:0 L:0
      Metric: 40         IP 1.1.1.5/32
        Prefix-attr: X:0 R:1 N:1
        Prefix-SID Index: 749, Algorithm:SPF, R:1 N:1 P:1 E:0 V:0 L:0
      Metric: 50         IP 1.1.1.6/32
        Prefix-attr: X:0 R:1 N:1
        Prefix-SID Index: 92, Algorithm:SPF, R:1 N:1 P:1 E:0 V:0 L:0
      Metric: 20         IP 78.1.1.0/24
        Prefix-attr: X:0 R:1 N:0
      Metric: 10         IP 12.1.1.0/24
        Prefix-attr: X:0 R:0 N:0
      Metric: 10         IP 17.1.1.0/24
        Prefix-attr: X:0 R:0 N:0
      Metric: 20         IP 23.1.1.0/24
        Prefix-attr: X:0 R:1 N:0
      Metric: 20         IP 28.1.1.0/24
        Prefix-attr: X:0 R:1 N:0
      Metric: 30         IP 34.1.1.0/24
        Prefix-attr: X:0 R:1 N:0
      Metric: 40         IP 45.1.1.0/24
        Prefix-attr: X:0 R:1 N:0
      Metric: 50         IP 56.1.1.0/24
        Prefix-attr: X:0 R:1 N:0
      Metric: 10         IP 1.1.1.7/32
        Prefix-attr: X:0 R:1 N:1
        Prefix-SID Index: 269, Algorithm:SPF, R:1 N:1 P:1 E:0 V:0 L:0
    R1#


    """
    result_list = []
    db_list = []
    op = uut.execute('show isis database')
    for line in op.splitlines():
        if '0x000' in line:
            db_list.append(line.split()[0])
    for db in db_list:
        op2 = uut.execute('show isis database {db} verbose'.format(db=db))
        for line in op2.splitlines():
            if 'Router CAP:' in line:
                logger.info('Router CAP is %s' % line)
                result_list.append('pass')
            elif 'SRGB Base::' in line:
                result_list.append('pass')
    if not 'pass' in result_list:
        return 0
    else:
        return 1

def configure_isis_xe(uut,area):


    """
    A router has a Network Entity Title (NET) of 49.001a.1122.3344.5566.00. To what area does this router belong, and what is its system ID?
    The area is 49.001a. The router's system ID is 1122.3344.5566. The easiest way to figure this out is to start from the right and work towards the left. The last two numbers of the NET are the NSEL; they are always 00 on a router. The next 12 numbers (separated into 3 groups of 4 numbers) are the system ID. On Cisco routers, the system ID is always this length—6 bytes. Anything to the left of the system ID is the area ID.
    """

    #net = '49.0000.0000.0000.0012.00'

    mac1 = str(RandMac("0000.0000.0000"))
    net = area+"."+mac1+'.00'

    cmdxe = \
    """
    ipv6 unicast-routing
    no router isis 100
    router isis 100
=======
    f"""
    ipv6 unicast-routing 
    no router isis {inst}
    router isis {inst}
>>>>>>> a7c04b8bb5dce427b1aa358b2bfcb3a15aacc289
    net {net}
    advertise passive-only
    metric-style wide
    no hello padding
    log-adjacency-changes all
    passive-interface Loopback0
    address-family ipv6
    advertise passive-only

    """
<<<<<<< HEAD
    intf_list = []
    op1 = uut.execute('show int desc')
    #show int desc | inc xrv
    #Wed May 26 12:21:05.634 UTC
    #Gi0/0/0/0.108      up          up          xrv-8----xrv-9
    #Gi0/0/0/0.128      up          up          xrv-7----xrv-9
    #RP/0/0/CPU0:xrv-9#



    for line in op1.splitlines():
        if 'igabitEthernet' in line:
            #for uut1 in l1_uut_list:
                #if uut1.name in line:
            intf_list.append(line.split()[0])
            #    else:
            #        l2_int_list.append(line.split()[0])
    print(intf_list)
    intf_list = list(set(intf_list))
    print(intf_list)
    #l2_int_list = list(set(l2_int_list))
    for intf in intf_list:
        cmdxe += 'interface {intf} \n'.format(intf=intf)
        cmdxe += 'ip router isis 100 \n'
        cmdxe += 'isis circuit-type level-1  \n'
    uut.configure(cmdxe.format(net=net))


=======
    int_list = intf_list
    op1 = uut.execute('sho ip int br | ex una')
    
    for line in op1.splitlines():
        if 'Lo' in line:
            int_list.append(line.split()[0])

    int_list = list(set(int_list))
    if uut.os == 'iosxr':
        for intf in int_list:
            if not "Gi" in op2:
                cmdxr += 'interface {intf} \n'.format(intf=intf)
                cmdxr += 'address-family ipv4 unicast \n'
                cmdxr += 'address-family ipv6 unicast \n' 
                cmdxr += 'circuit-type level-2-only \n' 
        
    uut.configure(cmdxr)            
  
   
  
>>>>>>> a7c04b8bb5dce427b1aa358b2bfcb3a15aacc289

def configure_interfaces(uut,conf_dict):
    """
    This function brings up subinterface & configures ipv4 & ipv6 address

    abr1xr:
      interfaces:
        GigabitEthernet0/0.1011:
          description : core1xe1
          type : l3
          ip_add : 101.1.1.111 255.255.255.0

    """
    node_list = conf_dict['ethernet']
    for node in conf_dict['ethernet'].keys():
        if uut.name in node:
            intf_list = conf_dict['ethernet'][node]['interfaces']
            cmd1 = \
                """
                """

            for intf in intf_list:
                cmd1 += 'interface {intf} \n'.format(intf=intf)
                if not 'Loopback' in intf:
                    vlan_id1 = int(intf.split('.')[1])
                    cmd1 += 'encap dot1q {vlan_id1}\n'.format(vlan_id1=vlan_id1)
                    desc = conf_dict['ethernet'][node]['interfaces'][intf]['description']
                    cmd1 += 'description connect_to_{desc}\n'.format(desc=desc)
                    v6_pref = '2001:'+str(vlan_id1)+'::0'
                    random.seed()
                    ipv6_a = IPAddress(v6_pref) + random.getrandbits(16)
                    ipv6_add = IPNetwork(ipv6_a)
                    ipv6_add.prefixlen = 96
                    cmd1 += 'ipv6 add {ipv6_add}\n'.format(ipv6_add=str(ipv6_add))
                else:
                    ipv6_add = conf_dict['ethernet'][node]['interfaces'][intf]['ipv6_add']
                    cmd1 += 'ipv6 add {ipv6_add} \n'.format(ipv6_add=ipv6_add)
                ip_add = conf_dict['ethernet'][node]['interfaces'][intf]['ip_add']
                if 'iosxr' in uut.os:
                    cmd1 += 'ipv4 add {ip_add} \n'.format(ip_add=ip_add)
                elif 'iosxe' in uut.os:
                    cmd1 += 'ip add {ip_add}\n'.format(ip_add=ip_add)
                cmd1 += 'no shut\n'
                uut.configure(cmd1)

def pe_node():
    pass

def abr_node():
    pass

def core_node():
    pass


def agg_node():
    pass


<<<<<<< HEAD
def bring_up_lan(uut_list,intf_list,vlan):
=======
def bringUpDot1qIntf(uut1,nei_list):
    #import pdb ; pdb.set_trace()
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        for line in op1.splitlines():
            if uut.name in line:
                if not '.' in line:
                    a = random.randint(31,70)
                    b = random.randint(31,70)
                    encap = int(a+b)+random.randint(10,30)
                    if encap > 200:
                        encap = random.randint(25,199)
                    if encap == 127:
                        encap = encap + random.randint(25,50)
                    intf_uut1 = line.split()[1] 
                    intf_uut = line.split()[-1]
                    intf_uut1=intf_uut1.strip('Cisco')
                    intf_uut=intf_uut.strip('Cisco')
                    c = random.randint(100,200)
                    uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                    uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                    description = uut1.name+"----"+uut.name
                    configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                    configure_subintf(uut,intf_uut,encap,uut_ip,description)

def bringUpL3Link(uut1,nei_list):
    #import pdb ; pdb.set_trace()
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        for line in op1.splitlines():
            if uut.name in line:
                if not '.' in line:
                    a = random.randint(31,100)
                    b = random.randint(101,200)
                    #encap = int(a+b)+random.randint(10,30)
                    #if encap > 200:
                    encap = random.randint(10,199)
                    if encap == 127:
                        encap = encap + random.randint(25,50)
                    intf_uut1 = line.split()[1] 
                    intf_uut = line.split()[-1]
                    intf_uut1=intf_uut1.strip('Cisco')
                    intf_uut=intf_uut.strip('Cisco')
                    c = random.randint(100,200)
                    uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                    uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                    description = uut1.name+"----"+uut.name
                    configureL3intf(uut1,intf_uut1,uut1_ip,description)
                    configureL3intf(uut,intf_uut,uut_ip,description)











def bring_up_subif4(uut1,nei_list):
>>>>>>> a7c04b8bb5dce427b1aa358b2bfcb3a15aacc289
    #import pdb ; pdb.set_trace()
    for uut,intf in zip(uut_list,intf_list):
        a = random.randint(2,250)
        #b = random.randint(31,70)
        #c = random.randint(100,200)
        encap = vlan
        uut_ip = "99.0."+str(encap)+"."+str(a)
        description = uut.name+"_lan_"+str(vlan)
        configure_subintf(uut,intf,encap,uut_ip,description)

def bring_up_l3_link_xr_nx(uut1,nei_list):
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        for line in op1.splitlines():
            if uut.name in line:
                a = random.randint(31,70)
                b = random.randint(31,70)
                encap = int(a+b)+random.randint(10,30)
                if encap == 127:
                    encap = encap + random.randint(25,50)
                elif encap == 100:
                    encap = encap + random.randint(25,50)
                elif encap > 200:
                    encap = random.randint(25,199)
                intf_uut1 = line.split()[1]
                intf_uut = line.split()[-1]
                c = random.randint(100,200)
                uut1_ip = "99.0."+str(encap)+".1"
                uut_ip = "99.0."+str(encap)+".2"
                description = uut1.name+"----"+uut.name
                configure_l3_intf(uut1,intf_uut1,encap,uut1_ip,description)
                configure_l3_intf(uut,intf_uut,encap,uut_ip,description)



def bring_up_l3_link(uut1,nei_list):
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        if 'xr' in uut1.os:
            if 'xr' in uut.os:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = random.randint(31,70)
                            b = random.randint(31,70)
                            encap = int(a+b)+random.randint(10,30)
                            if encap == 127:
                                encap = encap + random.randint(25,50)
                            elif encap == 100:
                                encap = encap + random.randint(25,50)
                            elif encap > 200:
                                encap = random.randint(25,199)

                            intf_uut1 = line.split()[1]
                            intf_uut = line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = "99.0."+str(encap)+".1"
                            uut_ip = "99.0."+str(encap)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_l3_intf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_l3_intf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'XRv' in line:
                                a = random.randint(31,70)
                                b = random.randint(31,70)
                                encap = int(a+b)+random.randint(10,30)
                                if encap == 127:
                                    encap = encap + random.randint(25,50)
                                elif encap == 100:
                                    encap = encap + random.randint(25,50)
                                elif encap > 200:
                                    encap = random.randint(25,199)
                                intf_uut1 =  line.split()[1]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                intf_uut=intf_uut.strip('Cisco')
                                intf_uut1=intf_uut1.strip('Cisco')
                                c = random.randint(100,200)
                                uut1_ip = "99.0."+str(encap)+".1"
                                uut_ip = "99.0."+str(encap)+".2"
                                description = uut1.name+"----"+uut.name
                                configure_l3_intf(uut1,intf_uut1,encap,uut1_ip,description)
                                configure_l3_intf(uut,intf_uut,encap,uut_ip,description)
        else:
            if 'xr' in uut.os:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = random.randint(31,70)
                            b = random.randint(31,70)
                            encap = int(a+b)+random.randint(30,60)
                            if encap == 127:
                                encap = encap + random.randint(25,50)
                            elif encap == 100:
                                encap = encap + random.randint(25,50)
                            elif encap > 200:
                                encap = random.randint(25,199)
                            if uut1.os == 'nxos':
                                intf_uut1 = line.split()[1]
                                intf_uut =  line.split()[-1]
                            else:
                                intf_uut1 = line.split()[1]+ line.split()[2]
                                intf_uut = line.split()[-2]+line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = "99.0."+str(encap)+".1"
                            uut_ip = "99.0."+str(encap)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_l3_intf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_l3_intf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if not "Gig 0/0" in line:
                        if uut.name in line:
                            if not '.' in line:
                                if not 'xr' in line:
                                    a = random.randint(31,70)
                                    b = random.randint(31,70)
                                    encap = int(a+b)+random.randint(60,90)
                                    if encap == 127:
                                        encap = encap + random.randint(25,50)
                                    elif encap == 100:
                                        encap = encap + random.randint(25,50)
                                    elif encap > 200:
                                        encap = random.randint(25,199)
                                    intf_uut1 = line.split()[1]+line.split()[2]
                                    intf_uut = line.split()[-2]+line.split()[-1]
                                    intf_uut1=intf_uut1.strip('Cisco')
                                    intf_uut=intf_uut.strip('Cisco')
                                    c = random.randint(100,200)
                                    uut1_ip = "99.0."+str(encap)+".1"
                                    uut_ip = "99.0."+str(encap)+".2"
                                    description = uut1.name+"----"+uut.name
                                    configure_l3_intf(uut1,intf_uut1,encap,uut1_ip,description)
                                    configure_l3_intf(uut,intf_uut,encap,uut_ip,description)


def bring_up_subif4(uut1,nei_list):
    #import pdb ; pdb.set_trace()
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        if 'xr' in uut1.name:
            if 'xr' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = random.randint(31,70)
                            b = random.randint(31,70)
                            encap = int(a+b)+random.randint(10,30)
                            if encap == 127:
                                encap = encap + random.randint(25,50)
                            elif encap == 100:
                                encap = encap + random.randint(25,50)
                            elif encap > 200:
                                encap = random.randint(25,199)

                            intf_uut1 = line.split()[1]
                            intf_uut = line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = "99.0."+str(encap)+".1"
                            uut_ip = "99.0."+str(encap)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'xrv' in line:
                                a = random.randint(31,70)
                                b = random.randint(31,70)
                                encap = int(a+b)+random.randint(10,30)
                                if encap == 127:
                                    encap = encap + random.randint(25,50)
                                elif encap == 100:
                                    encap = encap + random.randint(25,50)
                                elif encap > 200:
                                    encap = random.randint(25,199)
                                intf_uut1 =  line.split()[1]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                intf_uut=intf_uut.strip('Cisco')
                                intf_uut1=intf_uut1.strip('Cisco')
                                c = random.randint(100,200)
                                uut1_ip = "99.0."+str(encap)+".1"
                                uut_ip = "99.0."+str(encap)+".2"
                                description = uut1.name+"----"+uut.name
                                (uut1,intf_uut1,encap,uut1_ip,description)
                                configure_subintf(uut,intf_uut,encap,uut_ip,description)
        else:
            if 'xr' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = random.randint(31,70)
                            b = random.randint(31,70)
                            encap = int(a+b)+random.randint(30,60)
                            if encap == 127:
                                encap = encap + random.randint(25,50)
                            elif encap == 100:
                                encap = encap + random.randint(25,50)
                            elif encap > 200:
                                encap = random.randint(25,199)
                            if uut1.os == 'nxos':
                                intf_uut1 = line.split()[1]
                                intf_uut =  line.split()[-1]
                            else:
                                intf_uut1 = line.split()[1]+ line.split()[2]
                                intf_uut = line.split()[-2]+line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = "99.0."+str(encap)+".1"
                            uut_ip = "99.0."+str(encap)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if not "Gig 0/0" in line:
                        if uut.name in line:
                            if not '.' in line:
                                if not 'xr' in line:
                                    a = random.randint(31,70)
                                    b = random.randint(31,70)
                                    encap = int(a+b)+random.randint(60,90)
                                    if encap == 127:
                                        encap = encap + random.randint(25,50)
                                    elif encap == 100:
                                        encap = encap + random.randint(25,50)
                                    elif encap > 200:
                                        encap = random.randint(25,199)
                                    intf_uut1 = line.split()[1]+line.split()[2]
                                    intf_uut = line.split()[-2]+line.split()[-1]
                                    intf_uut1=intf_uut1.strip('Cisco')
                                    intf_uut=intf_uut.strip('Cisco')
                                    c = random.randint(100,200)
                                    uut1_ip = "99.0."+str(encap)+".1"
                                    uut_ip = "99.0."+str(encap)+".2"
                                    description = uut1.name+"----"+uut.name
                                    configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                                    configure_subintf(uut,intf_uut,encap,uut_ip,description)


def add_ospf_conf(uut_list,conf_dict):
    for key in list(conf_dict['protocols']['ospf'].keys()):
        cmd = \
                """
                router ospf 100
                """
        host_name = key
        rid = conf_dict['protocols']['ospf'][key]['rid']
        for uut in uut_list:
            if uut.name == host_name:
                if uut.os == 'iosxe':
                    cmd += 'router-id {rid} \n'.format(rid=rid)
                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        if 'redistribute' in conf_dict['protocols']['ospf'][key]['area'][key2].keys():
                            red_type = conf_dict['protocols']['ospf'][key]['area'][key2]['redistribute']
                            cmd += 'redistribute {red_type} tag {tag} \n'.format(tag=str(key2),red_type=red_type)
                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        if 'stub' == conf_dict['protocols']['ospf'][key]['area'][key2]['type']:
                            cmd += 'area {area} stub\n'.format(area=str(key2))
                        elif 'totalstb' == conf_dict['protocols']['ospf'][key]['area'][key2]['type']:
                            cmd += 'area {area} stub no-summ\n'.format(area=str(key2))
                        elif 'nssa' == conf_dict['protocols']['ospf'][key]['area'][key2]['type']:
                            cmd += 'area {area} nssa\n'.format(area=str(key2))

                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        intf_list = conf_dict['protocols']['ospf'][key]['area'][key2]['interfaces']
                        for intf in intf_list:
                            cmd += 'interface {intf} \n'.format(intf=intf)
                            cmd += 'ip ospf 100 area {area} \n'.format(area=str(key2))
                elif uut.os == 'iosxr':
                    cmd += 'router-id {rid} \n'.format(rid=rid)
                    cmd += 'address-family ipv4 unicast\n'
                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        intf_list = conf_dict['protocols']['ospf'][key]['area'][key2]['interfaces']
                        for intf in intf_list:
                            cmd += 'area {area} \n'.format(area=str(key2))
                            if 'oop' in intf:
                                cmd += 'interface {intf} \n'.format(intf=intf)
                                cmd += 'passive enable \n'
                            else:
                                cmd += 'interface {intf} \n'.format(intf=intf)
                uut.configure(cmd)
    for key in list(conf_dict['protocols']['ospf'].keys()):
        host_name = key
        rid = conf_dict['protocols']['ospf'][key]['rid']
        for uut in uut_list:
            if uut.name == host_name:
                if uut.os == 'iosxe':
                    cmd = \
                    """
                    ipv6 unicast-routing
                    router ospfv3 100
                    """
                    cmd += 'router-id {rid} \n'.format(rid=rid)
                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        if 'redistribute' in conf_dict['protocols']['ospf'][key]['area'][key2].keys():
                            red_type = conf_dict['protocols']['ospf'][key]['area'][key2]['redistribute']
                            cmd += 'redistribute {red_type} tag {tag} \n'.format(tag=str(key2),red_type=red_type)
                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        if 'stub' == conf_dict['protocols']['ospf'][key]['area'][key2]['type']:
                            cmd += 'area {area} stub\n'.format(area=str(key2))
                        elif 'totalstb' == conf_dict['protocols']['ospf'][key]['area'][key2]['type']:
                            cmd += 'area {area} stub no-summ\n'.format(area=str(key2))
                        elif 'nssa' == conf_dict['protocols']['ospf'][key]['area'][key2]['type']:
                            cmd += 'area {area} nssa\n'.format(area=str(key2))

                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        intf_list = conf_dict['protocols']['ospf'][key]['area'][key2]['interfaces']
                        for intf in intf_list:
                            cmd += 'interface {intf} \n'.format(intf=intf)
                            cmd += 'ipv6 ospf 100 area {area} \n'.format(area=str(key2))
                elif uut.os == 'iosxr':
                    cmd = \
                    """
                    router ospfv3 100
                    """
                    cmd += 'router-id {rid} \n'.format(rid=rid)
                    cmd += 'address-family ipv6 unicast\n'
                    for key2 in conf_dict['protocols']['ospf'][key]['area'].keys():
                        intf_list = conf_dict['protocols']['ospf'][key]['area'][key2]['interfaces']
                        for intf in intf_list:
                            cmd += 'area {area} \n'.format(area=str(key2))
                            if 'oop' in intf:
                                cmd += 'interface {intf} \n'.format(intf=intf)
                                cmd += 'passive enable \n'
                            else:
                                cmd += 'interface {intf} \n'.format(intf=intf)
                uut.configure(cmd)



def add_isis_conf(uut_list,conf_dict):
    #import pdb ; pdb.set_trace()
    for key in list(conf_dict['protocols']['isis'].keys()):
        cmd = \
                """
                no router isis 100
                router isis 100
                is-type level-2-only
                address-family ipv4 unicast
                metric-style wide
                address-family ipv6 unicast
                metric-style wide
                """
        host_name = key
        net = conf_dict['protocols']['isis'][key]['net']
        for uut in uut_list:
            if uut.name == host_name:
                if uut.os == 'iosxr':
                    cmd += 'net {net} \n'.format(net=net)
                    intf_list = conf_dict['protocols']['isis'][key]['interfaces']
                    for intf in intf_list:
                        cmd += 'interface {intf} \n'.format(intf=intf)
                        cmd += 'address-family ipv4 unicast \n'
                        cmd += 'address-family ipv6 unicast \n'
                    uut.configure(cmd)
                    #import pdb; pdb.set_trace()
                    if 'redistribute' in conf_dict['protocols']['isis'][key].keys():
                        #import pdb; pdb.set_trace()
                        cmd = \
                        """
                        """
                        cmd += 'route-policy OSPF_to_ISIS\n'
                        cmd += 'if tag eq 2000 then\n'
                        cmd += 'drop\n'
                        cmd += 'exit\n'
                        cmd += 'set tag 1000\n'
                        cmd += 'end-policy\n'
                        cmd += 'route-policy ISIS_to_OSPF\n'
                        cmd += 'if tag eq 1000 then\n'
                        cmd += 'drop\n'
                        cmd += 'exit\n'
                        cmd += 'set tag 2000\n'
                        cmd += 'end-policy\n'
                        uut.configure(cmd)
                        cmd = \
                        """
                        """
                        cmd += 'router isis 100\n'
                        cmd += 'address-family ipv4 unicast\n'
                        cmd +='redistribute ospf 100 level-2 route-policy OSPF_to_ISIS\n'
                        cmd += 'address-family ipv6 unicast\n'
                        cmd +='redistribute ospfv3 100 level-2 route-policy OSPF_to_ISIS\n'
                        cmd += 'router ospf 100\n'
                        cmd += 'address-family ipv4 unicast\n'
                        cmd +='redistribute isis 100 route-policy ISIS_to_OSPF\n'
                        cmd += 'router ospfv3 100\n'
                        cmd += 'address-family ipv6 unicast\n'
                        cmd +='redistribute isis 100 route-policy ISIS_to_OSPF\n'
                        uut.configure(cmd)

def add_static_route(uut,prefix,next_hop_list):
    cmd = \
        """
        router static
        address-family ipv4 unicast
        """
    for next_hop in next_hop_list:
        cmd += '{prefix}/32 {next_hop} \n'.format(prefix=prefix,next_hop=next_hop)

    uut.configure(cmd)


def add_ebgp_conf(uut1,uut2,conf_dict):
    op1 = uut1.execute('show ip int br')
    for line in op1.splitlines():
        if 'Loopback0' in line:
            uut1_loop0 = line.split()[1]
        elif 'GigabitEthernet0/0/0/0.50' in line:
            gw1_1 =  line.split()[1]
        elif 'GigabitEthernet0/0/0/0.51' in line:
            gw1_2 =  line.split()[1]
    op2 = uut2.execute('show ip int br')
    for line in op2.splitlines():
        if 'Loopback0' in line:
            uut2_loop0 = line.split()[1]
        elif 'GigabitEthernet0/0/0/0.50' in line:
            gw2_1 =  line.split()[1]
        elif 'GigabitEthernet0/0/0/0.51' in line:
            gw2_2 =  line.split()[1]

    add_static_route(uut1,uut2_loop0,[gw2_1,gw2_2])
    add_static_route(uut2,uut1_loop0,[gw1_1,gw1_2])

    #bgp:
    #    xrv-2:
    #      as: 65001
    #      networks:
    #        [loopback]
    #      neighbor:
    #          1.1.1.1
    #        remote-as:
    #          65002
    #      redistribute:
    #        ospf
    cmd = \
    """
    route-policy pass-all
    pass
    end-policy
    """
    for uut in [uut1,uut2]:
        uut.configure(cmd)

    cmdxr = \
    """
    router bgp {as_num}
    address-family ipv4 unicast
    redistribute ospf 100 match internal external
    neighbor {neigh}
    ebgp-multihop
     remote-as {rem_as}
     update-source loopback 0
     address-family ipv4 unicast
     route-policy pass-all in
     route-policy pass-all out
    router ospf 100
    address-family ipv4 unicast
    redistribute static
    redistribute bgp {as_num} tag {tag}

    """
    for uut in [uut1,uut2]:
        tag = random.randint(2000,3000)
        as_num = conf_dict['protocols']['bgp'][uut.name]['as']
        neigh = conf_dict['protocols']['bgp'][uut.name]['neighbor']
        rem_as = conf_dict['protocols']['bgp'][uut.name]['remote-as']
        if uut.os == 'iosxr':
            uut.configure(cmdxr.format(as_num=as_num,neigh=neigh,rem_as=rem_as,tag=tag))


def get_ipv6_link_addr(prefix):
    random.seed()
    ip_a = IPAddress('2001::cafe:0') + random.getrandbits(16)
    ip_n = IPNetwork(ip_a)
    ip_n.prefixlen = 96


def add_subintf(uut1,uut2,scale):
    for i in range(scale+1):
        encap = random.randint(10,199)
        for uut in [uut1,uut2]:
            cmd = \
                """
                """
            if uut.os == iosxr:
                intf = 'gi0/0/0/0'
            elif uut.os == iosxe:
                intf = 'gi0/0'
            intf_uut = intf+"."+str(encap)
            cmd += 'interface {intf}\n'.format(intf=intf_uut)
            cmd += 'encap dot1q {encap}\n'.format(encap=encap)
            ip_add = '172.16.'+str(encap)+'.'+str(random.randint(1,200))
            cmd += 'ipv4 add {ip_add} 255.255.255.0\n'.format(ip_add=ip_add)
            v6_pref = '2001::'+str(encap)+':0'
            random.seed()
            ipv6_a = IPAddress(v6_pref) + random.getrandbits(16)
            ipv6_add = IPNetwork(ipv6_a)
            ipv6_add.prefixlen = 96
            cmd += 'ipv6 add {ipv6_add}\n'.format(ipv6_add=str(ipv6_add))
            uut.configure(cmd)


def add_interface_config(uut,conf_dict):
    """
    This function brings up subinterface & configures ipv4 & ipv6 address

    #nxos9000-0 :
    interfaces:
      Ethernet1/1:
        type : l3
        ip_add : 100.1.1.1/24
      Ethernet1/2:
        type : trunk
        vlan : 100-110
    """

    cfg_sw = \
        """
        vlan {vlan}
        interface {intf}
        switchport
        switchport mode trunk
        switchport trunk encapsulation dot1q
        switchport trunk allowed vlan {vlan}
        """
    cfg_sw_nxos = \
        """
        vlan {vlan}
        interface {intf}
        switchport
        switchport mode trunk
        switchport trunk allowed vlan {vlan}
        """
    cfg_l3 = \
        """
        interface {intf}
        ip address {ip_add}
        """
    cfg_l3_nxos = \
        """
        interface {intf}
        no switchport
        ip address {ip_add}
        """
    #for uut in uut_list:
    for intf in conf_dict['ethernet'][uut.name]['interfaces'].keys():
        #import pdb ; pdb.set_trace()
        if conf_dict['ethernet'][uut.name]['interfaces'][intf]['type'] == 'l3':
            ip_add = conf_dict['ethernet'][uut.name]['interfaces'][intf]['ip_add']
            if uut.os == 'nxos':
                uut.configure(cfg_l3_nxos.format(ip_add=ip_add,intf=intf))
            else:
                uut.configure(cfg_l3.format(ip_add=ip_add,intf=intf))

        elif conf_dict['ethernet'][uut.name]['interfaces'][intf]['type'] == 'trunk':
            vlan = conf_dict['ethernet'][uut.name]['interfaces'][intf]['vlan']
            if uut.os == 'nxos':
                uut.configure(cfg_sw_nxos.format(vlan=vlan,intf=intf))
            else:
                uut.configure(cfg_sw.format(vlan=vlan,intf=intf))


def add_subintf_all(uut,conf_dict):
    """
    This function brings up subinterface & configures ipv4 & ipv6 address

    dot1q:
      iosv-0:
        interfaces:
          [GigabitEthernet0/0.100,GigabitEthernet0/0.101]

      iosv-1:
        interfaces:
          [GigabitEthernet0/0.100,GigabitEthernet0/0.101]
    """
    node_list = conf_dict['dot1q']
    for node in conf_dict['dot1q'].keys():
        if uut.name in node:
            intf_list = conf_dict['dot1q'][node]['interfaces']

            for intf in intf_list:
                vlan_id1 = int(intf.split('.')[1])
                cmd1 = \
                """
                """
                cmd1 += 'interface {intf} \n'.format(intf=intf)
                cmd1 += 'encap dot1q {vlan_id1}\n'.format(vlan_id1=vlan_id1)
                ip_add = '172.16.'+str(vlan_id1)+'.'+str(random.randint(1,200))
                if 'iosxr' in uut.os:
                    cmd1 += 'ipv4 add {ip_add} 255.255.255.0\n'.format(ip_add=ip_add)
                elif 'iosxe' in uut.os:
                    cmd1 += 'ip add {ip_add} 255.255.255.0\n'.format(ip_add=ip_add)
                v6_pref = '2001:'+str(vlan_id1)+'::0'
                random.seed()
                ipv6_a = IPAddress(v6_pref) + random.getrandbits(16)
                ipv6_add = IPNetwork(ipv6_a)
                ipv6_add.prefixlen = 96
                cmd1 += 'ipv6 add {ipv6_add}\n'.format(ipv6_add=str(ipv6_add))
                cmd1 += 'no shut\n'
                uut.configure(cmd1)

def get_igp_intf_listOLD(uut):
    intf_list= []
    op1= uut.execute('show ip interface brief | beg ddress')
    for line in op1.splitlines():
        if line:
            if not 'administratively down' in line:
                if not 'unassigned' in line:
                    if not 'IP-Address' in line:
                        if 'protocol-up/link-up/admin-up' in line:
                            intf_list.append(line.split()[0])
                        elif 'up     ' in line:
                            intf_list.append(line.split()[0])
    return intf_list

def getInterfacList(uut):
    intf_list = []
    op1 = uut.execute('sh ip int br | ex unass')
    for line in op1.splitlines():
        if line:
            if "Lo" in line:
                intf_list.append(line.split()[0])
            elif "Gi" in line:
                intf_list.append(line.split()[0])                
    return intf_list

def addOspfXr(uut):
    rid = get_intf_ip(uut,"Loop0")
    intf_list = getInterfacList(uut)
    cfg = \
    f"""
    router ospf 100
    router-id {rid}
    are 0
    """
    for intf in intf_list:
         cfg += f'interface {intf}\n'
   
    uut.configure(cfg)

def get_intf_ip(uut,intf):
    for line in uut.execute('show run interface {intf}'.format(intf=intf)).splitlines():
        if line:
            if 'ip address' in line:
                ip_add =  line.split()[2]
            elif 'ipv4 address' in line:
                ip_add =  line.split()[2]
    if '/' in ip_add:
        ip_add =  ip_add.split("/")[0]
    return ip_add

#def add_mpls_interface_config(uut):
#    intf_list = get_igp_intf_list(uut)
#    intf_list2 = []
#    for intf in intf_list:
#        if not 'oopback' in intf:
#            intf_list2.append(intf)
#            Genie.config_mpls_ldp_on_interface(uut,intf)


def configureSRxr(uut,igp_inst,index):
    cfg = \
    f"""        
    router isis {igp_inst}
    address-family ipv4 unicast
    segment-routing mpls
    segment-routing mpls sr-prefer

    !
    interface Loopback0
    address-family ipv4 unicast
    prefix-sid index {index}
    !
    """

    uut.configure(cfg)

def removeLdp(uut,igp_inst):
    cfg = \
    f"""        
    router isis {igp_inst}
    address-family ipv4 unicast
    no  mpls ldp auto-config
    """
    uut.configure(cfg)


def add_mpls_interface_config(uut):
    intf_list = get_igp_intf_list(uut)
    print(intf_list)
    # Create LDP object
    ldp = Ldp()
    dev1 = uut
    vrf0 = Vrf('default')
    #uut.os = 'iosxe'
    i = 100
    for intf1 in intf_list:
        link = Link(name='link_'+str(i))
        if not 'oopback' in intf1:
            intf = Interface(name=intf1,device=uut)
            link.connect_interface(interface=intf)
            i= i + 1
            link.add_feature(ldp)
    ldp.hello_holdtime = 100
    ldp.hello_interval = 200
    ldp.targeted_hello_accept = True
    loop0 = Interface(name='Loopback0',device=uut)
    #pdb.set_trace()
    #ldp.device_attr[dev1].router_id = loop0
    #ldp.gr = True
    #ldp.gr_fwdstate_holdtime = 60
    #ldp.nsr = True
    #ldp.device_attr['PE1'].session_holdtime = 444
    ldp.session_protection = True
    #ldp.session_protection_dur = 222
    #ldp.device_attr['PE2'].session_protection_dur = 333
    #ldp.session_protection_for_acl = acl1

    out = ldp.build_config(apply=True)


def add_mpls_conf(uut):

    #vrf_interface_dict = {'default':['lo0','Gi0/0.100','Gi0/0.200'],'vrf1':['lo10','Gi0/0.110','Gi0/0.210']}
    cfg = \
    """
    mpls ldp
    """
    cfg2 = \
    """
    mpls ldp router-id loopback 0 f
    """
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    if 'iosxr' in uut.os:
        cfg += 'router-id {rid}\n'.format(rid=rid)
        for intf in intf_list:
            if not 'Loopbac' in intf:
                cfg += 'interface {intf}\n'.format(intf=intf)
        uut.configure(cfg.format(rid=rid))
        return
    elif 'iosxe' in uut.os:
        for intf in intf_list:
            if not 'Loopbac' in intf:
                cfg2 += 'interface {intf}\n'.format(intf=intf)
                cfg2 += 'mpls ip\n'
        uut.configure(cfg2.format(rid=rid))
        return


def add_ospf_config2(uut,os=None):

    #vrf_interface_dict = {'default':['lo0','Gi0/0.100','Gi0/0.200'],'vrf1':['lo10','Gi0/0.110','Gi0/0.210']}
    cfg = \
    """
    router ospf 1
    router-id {rid}
    area 0
    """
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    if 'iosxr' in uut.os:
        for intf in intf_list:
            cfg += 'interface {intf}\n'.format(intf=intf)
        uut.configure(cfg.format(rid=rid))
        return

    intf_obj_list = []
    print("++++++++")
    print(intf_list)
    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)

    # Create OSPF object
    ospf1 = Ospf()
    dev1 = uut
    vrf0 = Vrf('default')
    #uut.os = 'iosxe'
    # Add OSPF configurations to vrf default
    ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '100'
    ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = rid
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True

    for intf1 in intf_obj_list:
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10

    # Add OSPF to the device
    dev1.add_feature(ospf1)

    # Build config
    cfgs = ospf1.build_config(apply=True)


def add_ospf_config(uut,os=None,instance=None):

    #vrf_interface_dict = {'default':['lo0','Gi0/0.100','Gi0/0.200'],'vrf1':['lo10','Gi0/0.110','Gi0/0.210']}
    cfg = \
    """
    router ospf {instance}
    router-id {rid}
    area 0
    """
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    if 'iosxr' in uut.os:
        for intf in intf_list:
            cfg += 'interface {intf}\n'.format(intf=intf)
        if instance:
            uut.configure(cfg.format(rid=rid,instance=instance))
        else:
            uut.configure(cfg.format(rid=rid,instance=1))

        return

    intf_obj_list = []
    print("++++++++")
    print(intf_list)
    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)

    # Create OSPF object
    ospf1 = Ospf()
    dev1 = uut
    vrf0 = Vrf('default')
    #uut.os = 'iosxe'
    # Add OSPF configurations to vrf default
    if not instance:
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '100'
    else:
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = instance
    ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = rid
    #ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
    #ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
    #ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True

    for intf1 in intf_obj_list:
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10

    # Add OSPF to the device
    dev1.add_feature(ospf1)

    # Build config
    cfgs = ospf1.build_config(apply=True)


def add_ospf_config_all(uut,os=None):

    #vrf_interface_dict = {'default':['lo0','Gi0/0.100','Gi0/0.200'],'vrf1':['lo10','Gi0/0.110','Gi0/0.210']}

    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')


    intf_obj_list = []

    print(intf_list)
    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)

    # Create OSPF object
    ospf1 = Ospf()
    dev1 = uut
    vrf0 = Vrf('default')
    #uut.os = 'iosxe'
    # Add OSPF configurations to vrf default
    ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '100'
    ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = rid
    #ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
    #ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
    #ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True

    for intf1 in intf_obj_list:
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10

    # Add OSPF to the device
    dev1.add_feature(ospf1)

    # Build config
    cfgs = ospf1.build_config(apply=True)


def add_isis_configs(uut):
    if uut.os == 'iosxe':
        add_isis_configs_xe(uut)
    elif uut.os == 'iosxr':
        add_isis_configs_xr(uut)


def add_isis_configs_xe(uut):
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    intf_obj_list = []

    isis = Isis("core")
    id1 = secrets.token_hex(2)


    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)

    for intf_iter in intf_obj_list:
        intf_iter.add_feature(isis)

    isis.is_type = Isis.IsType.level_1
    isis.device_attr[uut].is_type = Isis.IsType.level_1
    isis.ldp_auto_config=True
    isis.ldp_sync=False
    isis.metric_style="wide"
    isis.device_attr[uut].net_id = "49.0001.0000.{}.00".format(id1)

    cfg1 = isis.build_config(apply=True)

def add_isis_configs_xr(uut):
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    intf_obj_list = []

    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)

    isis = Isis("core")
    id1 = secrets.token_hex(2)

    isis = Isis("core")
    for intf in intf_obj_list:
        inft.add_feature(isis)
    isis.is_type = Isis.IsType.level_1
    isis.device_attr[uut].is_type = Isis.IsType.level_1
    isis.ldp_auto_config=True
    isis.ldp_sync=False
    isis.metric_style="wide"
    isis.device_attr[uut].net_id = "49.0001.0000.{}.00".format(id1)
    cfg1 = isis.build_config(apply=True)

def add_ospf_configs(uut):
    if uut.os == 'iosxe':
        add_ospf_configs_xe(uut)
    elif uut.os == 'iosxr':
        add_ospf_configs_xr(uut)


def add_ospf_configs_xe(uut):
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    intf_obj_list = []

    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)
    # Create OSPF object
    ospf1 = Ospf()
    dev1 = uut
    vrf0 = Vrf('default')
    #uut.os = 'iosxe'
    # Add OSPF configurations to vrf default
    ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '100'
    ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = rid
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = False
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True

    for intf1 in intf_obj_list:
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10

    # Add OSPF to the device
    dev1.add_feature(ospf1)

    # Build config
    cfgs = ospf1.build_config(apply=True)

def add_ospf_configs_xr(uut):
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    intf_obj_list = []
    #print("#######")
    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)
    # Create OSPF object


    dev1 = uut
    # Create VRF objects
    vrf0 = Vrf('default')
    ospf1 = Ospf()

    # ---------------------------------------
    # Configure OSPF instance 1 VRF 'default'
    # ---------------------------------------


    ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '100'
    ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = rid
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = False
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True
    # Add area configuration to VRF 'default'
    ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_id = '0.0.0.0'
    ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_ldp_sync = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_ldp_auto_config = True

    for intf1 in intf_obj_list:
        #intf1 = Interface(name=intf.name,device=dev1)
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_admin_control = True



    dev1.add_feature(ospf1)

    # Build config
    cfgs = ospf1.build_config(apply=True)



def add_isis_configsOLD(uut):
    intf_list = get_igp_intf_list(uut)
    rid =  get_intf_ip(uut,'Loopback0')
    intf_obj_list = []

    for i in range(len(intf_list)):
        intf = Interface(name=intf_list[i],device=uut)
        intf_obj_list.append(intf)
    # Create OSPF object
    ospf1 = Ospf()
    dev1 = uut
    vrf0 = Vrf('default')
    #uut.os = 'iosxe'
    # Add OSPF configurations to vrf default
    ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '100'
    ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = rid
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
    ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True

    for intf1 in intf_obj_list:
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10

    # Add OSPF to the device
    dev1.add_feature(ospf1)

    # Build config
    cfgs = ospf1.build_config(apply=True)



#smtp.host = mail.google.com
#smtp.port = 25
#default_domain = gmail.com
"""
f35e7f        n0        0,1                  R1          test1_iosv.virl
f35e7f        n1        0,1                  R2          test1_iosv.virl
f35e7f       n10        0,1                 R11          test1_iosv.virl
f35e7f       n11        0,1                 R12          test1_iosv.virl
f35e7f       n12        0,1                 R13          test1_iosv.virl
f35e7f       n13        0,1                 R14          test1_iosv.virl
f35e7f        n2        0,1                  R3          test1_iosv.virl
f35e7f       n20      0,1,2                 XR1          test1_iosv.virl
f35e7f       n21      0,1,2                 XR2          test1_iosv.virl
f35e7f       n22      0,1,2                 XR3          test1_iosv.virl
f35e7f       n23      0,1,2                 XR4          test1_iosv.virl
f35e7f        n3        0,1                  R4          test1_iosv.virl
f35e7f        n4        0,1                  R5          test1_iosv.virl
f35e7f        n5        0,1                  R6          test1_iosv.virl
f35e7f        n6        0,1                  R7          test1_iosv.virl
f35e7f        n7        0,1                  R8          test1_iosv.virl
f35e7f        n8        0,1                  R9          test1_iosv.virl
f35e7f        n9        0,1                 R10          test1_iosv.virl

"""


<<<<<<< HEAD
def configure_l3_intf(uut,intf,dot1q,ip_add,description):

    ipv6_add = '2001:beef:0:'+str(dot1q)+'::'+str(random.randint(2,200))+'/64'
    #ipv6_addr=
    #import pdb; pdb.set_trace()
    cfg = \
    """
    interface {intf}
    description {description}
    no ip address
    no ipv6 address
    ip address {ip_add} 255.255.255.0
    ipv6 address {ipv6_add}
    ipv6 enable
    no shut
    """
    cfg2 = \
    """
    interface {intf}
    description {description}
    no ip address
    no ipv6 address
    ip address {ip_add} 255.255.255.0
    ipv6 address {ipv6_add}
    no shut
    """
    try:
        if 'nxos' in uut.os:
            uut.configure(cfg2.format(ipv6_add=ipv6_add,intf=intf,ip_add=ip_add,description=description))
        else:
            uut.configure(cfg.format(ipv6_add=ipv6_add,intf=intf,ip_add=ip_add,description=description))
    except:
        logger.info('Failed configure_subintf device %s' % uut.name)

def get_ipv4(uut,intf):
    if uut.os == 'iosxe':
        cmd = "sh run int {intf} | inc ip address"
    elif uut.os == 'iosxr':
        cmd = "sh run int {intf} | inc ipv4 address"
    op=uut.execute(cmd.format(intf=intf))
    for line in op.splitlines():
        if 'address' in line:
            ip = line.split()[2]
    return ip
#pe_conf(PE1AS1,"AS1","1:1","1:1",rr1,"Gi1",'1',"100")


def bgp_l2vpn_evpn_xr(uut,nei_list):
    bgp = Bgp(asn=1,bgp_id=1)
    nbr_af_name = 'l2vpn evpn'
    neighbor_id = '10.2.0.2'
    for nei in nei_list:
        bgp.device_attr[uut].vrf_attr[None].neighbor_attr[nei].\
            nbr_update_source = 'Loop 0'
        bgp.device_attr[uut].vrf_attr[None].neighbor_attr[nei].\
            nbr_remote_as = 1
        bgp.device_attr[uut].vrf_attr[None].address_family_attr[nbr_af_name]

        bgp.device_attr[uut].vrf_attr[None].neighbor_attr[nei].\
            address_family_attr[nbr_af_name].nbr_af_route_reflector_client = True

    bgp.device_attr[uut]
    uut.add_feature(bgp)

    cfgs = bgp.build_config(apply=True)


def evpn_pe_conf_bgp_xe(uut,nei,rid,asn):
    cfg = \
    """
    router bgp {asn}
     bgp router-id {rid}
     bgp log-neighbor-changes
     bgp graceful-restart
     neighbor {nei} remote-as {asn}
     neighbor {nei} update-source Loopback0
     !
     address-family ipv4
      neighbor {nei} activate
     exit-address-family
     !
     address-family l2vpn evpn
      neighbor {nei} activate
      neighbor {nei}  send-community both
      neighbor {nei}  soft-reconfiguration inbound
     exit-address-family
         """
    try:
        uut.configure(cfg.format(nei=nei,asn=asn,rid=rid))
    except:
        logger.info('Failed configure_PE device %s' % uut.name)

def evpn_rr_conf_bgp_xe(uut,nei1,nei2,nei3,rid,asn):
    cfg = \
    """
    router bgp {asn}
     bgp router-id {rid}
     bgp log-neighbor-changes
     bgp graceful-restart
     neighbor {nei1} remote-as {asn}
     neighbor {nei1} update-source Loopback0
     neighbor {nei2} remote-as {asn}
     neighbor {nei2} update-source Loopback0
     neighbor {nei3} remote-as {asn}
     neighbor {nei3} update-source Loopback0

     !
     address-family ipv4
      neighbor {nei1} activate
      neighbor {nei1} route-reflector-client
      neighbor {nei2} activate
      neighbor {nei2} route-reflector-client
      neighbor {nei3} activate
      neighbor {nei3} route-reflector-client
     exit-address-family
     !
     address-family l2vpn evpn
      neighbor {nei1} activate
      neighbor {nei1}  send-community both
      neighbor {nei1}  soft-reconfiguration inbound
      neighbor {nei1}  route-reflector-client
      neighbor {nei2} activate
      neighbor {nei2}  send-community both
      neighbor {nei2}  soft-reconfiguration inbound
      neighbor {nei2}  route-reflector-client
      neighbor {nei3} activate
      neighbor {nei3}  send-community both
      neighbor {nei3}  soft-reconfiguration inbound
      neighbor {nei3}  route-reflector-client
     exit-address-family
         """
    try:
        print(cfg.format(nei1=nei1,nei2=nei2,nei3=nei3,asn=asn,rid=rid))
        uut.configure(cfg.format(nei1=nei1,nei2=nei2,nei3=nei3,asn=asn,rid=rid))
    except:
        logger.info('Failed configure_PE device %s' % uut.name)

def pe_conf(uut,vrf,rd,rt,rr,intf,asn,ospfp,ceip1):
    cfg = \
    """
	vrf definition {vrf}
	 rd {rd}
	 !
	 address-family ipv4
	  route-target export {rt}
	  route-target import {rt}
	 exit-address-family


	interface {intf}
	 description PE1AS1----CE1
	 vrf forwarding {vrf}
	 ip address {ceip1} 255.255.255.0
	 ip ospf {ospfp} area 0
	 negotiation auto
	 no mop enabled
	 no mop sysid
	 cdp enable


	router ospf {ospfp} vrf {vrf}
	 redistribute connected subnets
	 redistribute bgp {asn} subnets


	router bgp {asn}
	 bgp log-neighbor-changes
	 no bgp default ipv4-unicast
	 no bgp default route-target filter
	 neighbor {rr} remote-as {asn}
	 neighbor {rr} update-source Loopback0
	 !
	 address-family vpnv4
	  neighbor {rr} activate
	  neighbor {rr} send-community extended
	 exit-address-family
	 !
	 address-family ipv4 vrf {vrf}
	  redistribute connected
	  redistribute ospf {ospfp}
	 exit-address-family
         """
    try:
        uut.configure(cfg.format(vrf=vrf,rd=rd,rt=rt,rr=rr,intf=intf,asn=asn,ospfp=ospfp,ceip1=ceip1))
    except:
        logger.info('Failed configure_PE device %s' % uut.name)

#pe_conf(PE1AS1,"AS1","1:1","1:1",rr1,"Gi1",'1',"100")


def csc_bgp_bringup(cscpe,csc_as,csc_vrf,cse_ip,cscce,pe_as,pe_vrf,pe_ip):


    cfg_cscpe = \
        """
	router bgp {csc_as}
     address-family ipv4 vrf {csc_vrf}
      neighbor {pe_ip} remote-as {pe_as}
      neighbor {pe_ip} activate
      neighbor {pe_ip} as-override
      neighbor {pe_ip} send-label
     exit-address-family
        """
    cfg_cscce = \
        """
	router bgp {pe_as}
     address-family ipv4 vrf {pe_vrf}
      neighbor {cse_ip} remote-as {csc_as}
      neighbor {cse_ip} activate
      neighbor {cse_ip} send-label
     exit-address-family
        """

    try:
        cscpe.configure(cfg_cscpe.format(csc_as=csc_as,csc_vrf=csc_vrf,pe_ip=pe_ip,ce_as=ce_as))
        cscce.configure(cfg_cscce.format(pe_as=pe_as,pe_vrf=pe_vrf,cse_ip=cse_ip,csc_as=csc_as))
    except:
        logger.info('Failed configure_PE device csc_bgp_bringup')



def rr_conf(uut,pe1,pe2,asn):
    cfg = \
        """
	router bgp {asn}
	 bgp log-neighbor-changes
	 no bgp default ipv4-unicast
	 no bgp default route-target filter
	 neighbor {pe1} remote-as {asn}
	 neighbor {pe1} update-source Loopback0
	 neighbor {pe2} remote-as {asn}
	 neighbor {pe2} update-source Loopback0
	 !
	 address-family vpnv4
	  neighbor {pe1} activate
	  neighbor {pe1} send-community extended
	  neighbor {pe1} route-reflector-client
	  neighbor {pe2} activate
	  neighbor {pe2} send-community extended
	  neighbor {pe2} route-reflector-client
	 exit-address-family

        """
    try:
        uut.configure(cfg.format(asn=asn,pe1=pe1,pe2=pe2))
    except:
        logger.info('Failed configure_PE device %s' % uut.name)


=======
def configureL3intf(uut,intf,ip_add,description):
    cfg = \
    f"""
    interface {intf}
    description {description}
    ip address {ip_add} 255.255.255.0
    ipv6 enable
    no shut
    """
    try:
        uut.configure(cfg)
    except:
        logger.info(f'Failed configure_subintf device @ {uut.name}')
>>>>>>> a7c04b8bb5dce427b1aa358b2bfcb3a15aacc289

def configure_subintf(uut,intf,dot1q,ip_add,description):

    ipv6_add = '2001:beef:0:'+str(dot1q)+'::'+str(random.randint(2,200))+'/64'
    #ipv6_addr=
    #import pdb; pdb.set_trace()
    cfg = \
    """
    interface {intf}.{dot1q}
    description {description}
    encap dot1q {dot1q}
    ip address {ip_add} 255.255.255.0
    ipv6 address {ipv6_add}
    ipv6 enable
    no shut
    """
    try:
        uut.configure(cfg.format(ipv6_add=ipv6_add,intf=intf,dot1q=dot1q,ip_add=ip_add,description=description))
    except:
        logger.info('Failed configure_subintf device %s' % uut.name)

def remove_subintf(uut):
    op1 = uut.execute("show ip int brief")
    for line in op1.splitlines():
        if 'hernet' in line:
            if '.' in line.split()[0]:
                intf = line.split()[0]
                if not 'deleted' in line:
                    time.sleep(2)
                    uut.configure('no interface {intf}'.format(intf=intf))


def remove_loop(uut):
    op1 = uut.execute("show ip int brief | inc Loop")
    for line in op1.splitlines():
        if 'Loop' in line:
            intf = line.split()[0]
            uut.configure('no interface {intf}'.format(intf=intf))

def remove_tunnel(uut):
    op1 = uut.execute("show ip int brief | inc Tunne")
    for line in op1.splitlines():
        if 'Tunne' in line:
            intf = line.split()[0]
            uut.configure('no interface {intf}'.format(intf=intf))

def cleanup_igp(uut):
    #R2#sh ip protocols summary
    #Index Process Name
    #0     connected
    ##1     static
    #2     application
    #3     ospf 100
    #4     ospf 1
    #*** IP Routing is NSF
    if uut.os == 'iosxe':
        op1= uut.execute('show ip protocols summary')
        for line in op1.splitlines():
            if 'ospf' in line:
                cmd = 'no router ' + line.strip(line.split()[0])
                uut.configure(cmd)
            if 'bgp' in line:
                if not 'state' in line:
                    cmd = 'no router ' + line.strip(line.split()[0])
                    uut.configure(cmd)
    elif uut.os == 'iosxr':
        op1= uut.execute('sh protocols ipv4 all')
        for line in op1.splitlines():
            if 'OSPF' in line:
                cmd = 'no router ospf ' + line.split()[-1]
                uut.configure(cmd)
            elif 'BGP' in line:
                if not 'state' in line:
                    cmd = 'no router bgp ' + line.split()[-1]
        op1= uut.execute('sh protocols ipv6 all')
        for line in op1.splitlines():
            if 'OSPFv3' in line:
                cmd = 'no router ospfv3 ' + line.split()[-1]
                uut.configure(cmd)
            elif 'BGP' in line:
                if not 'state' in line:
                    cmd = 'no router bgp ' + line.split()[-1].strip('"')
                    uut.configure(cmd)
            elif 'IS-IS Route' in line:
                cmd = 'no router isis ' + line.split()[-1]
                uut.configure(cmd)


def remove_intf_all(uut):
    remove_tunnel(uut)
    remove_loop(uut)
    remove_subintf(uut)

def unshut_intf(uut):
    intf_list =[]
    if uut.os == 'nxos':
        cfg1 = \
        """
        interface eth1/1-4
        no shut
        cdp en
        """
        uut.configure(cfg1)
    else:
        op1 = uut.execute("show ip int brief")
        for line in op1.splitlines():
            if 'NVRAM' in line:
                intf = line.split()[0]
                intf_list.append(intf)
            elif 'Gig' in line:
                intf = line.split()[0]
                intf_list.append(intf)
            elif 'default' in line:
                intf = line.split()[0]
                intf_list.append(intf)
            elif 'admin' in line:
                intf = line.split()[0]
                intf_list.append(intf)
            elif '     eth  ' in line:
                intf = line.split()[0]
                intf_list.append(intf)

        if 'iosxr' in uut.os:
            cfg = \
            """
            cdp
            """
        elif 'iosxe' in uut.os:
            cfg = \
            """
            cdp run
            """

        for intf in intf_list:
            if "Gig" in intf:
                if 'iosxe' in uut.os:
                    cfg += 'interface {intf}\n'.format(intf=intf)
                    cfg += 'no ip address\n'
                    if "ipv6 add" in uut.execute("show run | inc ipv6"):
                        cfg += 'no ipv6 address\n'
                    cfg += 'no shut\n'
                    cfg += 'cdp en\n'
                elif 'iosxr' in uut.os:
                    cfg += 'interface {intf}\n'.format(intf=intf)
                    cfg += 'no shut\n'
                    cfg += 'no ip address\n'
                    if "ipv6 add" in uut.execute("show run | inc ipv6"):
                        cfg += 'no ipv6 address\n'
                    cfg += 'cdp\n'

        uut.configure(cfg)

def loopback_config(uut_list):
    i=1
    for uut in uut_list:
        loop0_ip_add = str(i)+"."+str(i)+"."+str(i)+".1"
        loop10_ip_add = str(i)+"."+str(i)+"."+str(i)+".10"
        loop100_ip_add = str(i)+"."+str(i)+"."+str(i)+".100"
        cfg = \
        v6_pref = '2001:'+str(i)+':'+str(random.randint(100,200))+':'+str(i)+':'+str(i)+':'+':0'
        random.seed()
        ipv6_a = IPAddress(v6_pref) + random.getrandbits(16)
        ipv6_add = IPNetwork(ipv6_a)
        ipv6_add.prefixlen = 128
        ipv6_add1 = str(ipv6_add)
        v6_pref = '2001:'+str(i)+':'+str(random.randint(100,200))+':'+str(i)+':'+str(i)+':'+':0'
        random.seed()
        ipv6_a = IPAddress(v6_pref) + random.getrandbits(16)
        ipv6_add = IPNetwork(ipv6_a)
        ipv6_add.prefixlen = 128
        ipv6_add2 = str(ipv6_add)
        v6_pref = '2001:'+str(i)+':'+str(random.randint(100,200))+':'+str(i)+':'+str(i)+':'+':0'
        random.seed()
        ipv6_a = IPAddress(v6_pref) + random.getrandbits(16)
        ipv6_add = IPNetwork(ipv6_a)
        ipv6_add.prefixlen = 128
        ipv6_add3 = str(ipv6_add)
        cfg = \
        """
        interface loopb 0
        ip address {loop0_ip_add} 255.255.255.255
        ipv6 address {ipv6_add1}
        no shut
        interface loopb 10
        ip address {loop10_ip_add} 255.255.255.255
        ipv6 address {ipv6_add2}
        no shut
        interface loopb 100
        ip address {loop100_ip_add} 255.255.255.255
        ipv6 address {ipv6_add3}
        no shut
        """
        #import pdb;pdb.set_trace()

        uut.configure(cfg.format(loop0_ip_add=loop0_ip_add,loop10_ip_add=loop10_ip_add,\
            loop100_ip_add=loop100_ip_add,ipv6_add1=ipv6_add1,ipv6_add2=ipv6_add2,ipv6_add3=ipv6_add3))
        i = i + 1


    intf_list =[]
    op1 = uut.execute("show ip int brief")
    for line in op1.splitlines():
        if 'NVRAM' in line:
            intf = line.split()[0]
            intf_list.append(intf)

    cfg = \
    """
    interface {intf}
    no shut
    """
    for intf in intf_list:
        uut.configure(cfg.format(intf=intf))



def bgp_evpn_conf(uut,neigh_list,as_num):
    if uut.os == 'iosxr':
        cfg = \
        """
        router bgp 65001
        bgp log neighbor changes detail
        address-family vpnv4 unicast

        address-family l2vpn evpn

        neighbor-group EDGE
        remote-as 65001
        update-source Loopback0
        address-family vpnv4 unicast
        route-reflector-client

        address-family l2vpn evpn
        route-reflector-client


        neighbor 10.10.10.1
        use neighbor-group EDGE

        router bgp 65001
        bgp log neighbor changes detail
        address-family vpnv4 unicast
        address-family l2vpn evpn
        neighbor-group RR
        remote-as 65001
        update-source Loopback0
        address-family vpnv4 unicast
        address-family l2vpn evpn
        neighbor 5.5.5.1
        use neighbor-group RR
        neighbor 6.6.6.1
        use neighbor-group RR


        router bgp {as}
        bgp log neighbor changes detail
        address-family vpnv4 unicast

        neighbor 102.2.2.1
        remote-as 200
        update-source Loopback0
         address-family vpnv4 unicast
         !
        !
        vrf CU02
        rd 1:2
        address-family ipv4 unicast
        redistribute connected
        !
        neighbor 2.202.103.2
        remote-as 300
         address-family ipv4 unicast
        route-policy ALL-PASS in
        route-policy ALL-PASS out
        send-extended-community-ebgp


         router bgp 200
         bgp log neighbor changes detail
         address-family vpnv4 unicast
         !
         neighbor 102.2.2.1
         remote-as 200
         update-source Loopback0
         address-family vpnv4 unicast
         !
        !
        vrf CU02
        rd 1:2
        address-family ipv4 unicast
        redistribute connected
        !
        neighbor 2.202.103.2
        remote-as 300
        address-family ipv4 unicast
        route-policy ALL-PASS in
        route-policy ALL-PASS out
        send-extended-community-ebgp

        """

def bring_up_subif3(uut1,nei_list):
    #import pdb ; pdb.set_trace()
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        if 'xr' in uut1.name:
            if 'xr' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = uut1.name.strip('xrv')
                            b = uut.name.strip('xrv')
                            encap = int(a+b)+random.randint(10,30)
                            if encap > 200:
                                encap = random.randint(25,199)
                            intf_uut1 = line.split()[1]
                            intf_uut = line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                            uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'xrv' in line:
                                a = uut1.name.strip('xrv')
                                b = uut.name.strip('iosv')
                                encap = int(a+b)+random.randint(10,30)
                                if encap > 200:
                                    encap = random.randint(25,199)
                                intf_uut1 =  line.split()[1]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                intf_uut=intf_uut.strip('Cisco')
                                intf_uut1=intf_uut1.strip('Cisco')
                                c = random.randint(100,200)
                                uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                                uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                                description = uut1.name+"----"+uut.name
                                configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                                configure_subintf(uut,intf_uut,encap,uut_ip,description)
        else:
            if 'xrv' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = uut1.name.strip('iosv')
                            b = uut.name.strip('xrv')
                            encap = int(a+b)+random.randint(30,60)
                            if encap > 200:
                                encap = random.randint(25,199)
                            intf_uut1 = line.split()[1]+ line.split()[2]
                            intf_uut = line.split()[-2]+line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                            uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'xrv' in line:
                                a = uut1.name.strip('iosv')
                                b = uut.name.strip('iosv')
                                encap = int(a+b)+random.randint(60,90)
                                if encap > 200:
                                    encap = random.randint(25,199)
                                intf_uut1 = line.split()[1]+line.split()[2]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                intf_uut1=intf_uut1.strip('Cisco')
                                intf_uut=intf_uut.strip('Cisco')
                                c = random.randint(100,200)
                                uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                                uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                                description = uut1.name+"----"+uut.name
                                configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                                configure_subintf(uut,intf_uut,encap,uut_ip,description)


def bring_up_subif2(uut1,nei_list):
    #pdb.set_trace()
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        if 'xr' in uut1.name:
            if 'xr' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = uut1.name.strip('xrv-')
                            b = uut.name.strip('xrv-')
                            encap = int(a+b)+random.randint(10,30)
                            if encap > 200:
                                encap = random.randint(25,199)
                            intf_uut1 = line.split()[1]
                            intf_uut = line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                            uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'xrv' in line:
                                a = uut1.name.strip('xrv-')
                                b = uut.name.strip('iosv-')
                                encap = int(a+b)+random.randint(10,30)
                                if encap > 200:
                                    encap = random.randint(25,199)
                                intf_uut1 =  line.split()[1]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                intf_uut=intf_uut.strip('Cisco')
                                intf_uut1=intf_uut1.strip('Cisco')
                                c = random.randint(100,200)
                                uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                                uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                                description = uut1.name+"----"+uut.name
                                configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                                configure_subintf(uut,intf_uut,encap,uut_ip,description)
        else:
            if 'XR' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = uut1.name.strip('iosv-')
                            b = uut.name.strip('xrv-')
                            encap = int(a+b)+random.randint(30,60)
                            if encap > 200:
                                encap = random.randint(25,199)
                            intf_uut1 = line.split()[1]
                            intf_uut = line.split()[-2]+line.split()[-1]
                            intf_uut1=intf_uut1.strip('Cisco')
                            intf_uut=intf_uut.strip('Cisco')
                            c = random.randint(100,200)
                            uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                            uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'xrv' in line:
                                a = uut1.name.strip('iosv-')
                                b = uut.name.strip('iosv-')
                                encap = int(a+b)+random.randint(60,90)
                                if encap > 200:
                                    encap = random.randint(25,199)
                                intf_uut1 = line.split()[1]+line.split()[2]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                intf_uut1=intf_uut1.strip('Cisco')
                                intf_uut=intf_uut.strip('Cisco')
                                c = random.randint(100,200)
                                uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                                uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                                description = uut1.name+"----"+uut.name
                                configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                                configure_subintf(uut,intf_uut,encap,uut_ip,description)

def bring_up_subif(uut1,nei_list):
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        if 'XR' in uut1.name:
            if 'XR' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = uut1.name.strip('XR')
                            b = uut.name.strip('XR')
                            encap = int(a+b)+random.randint(10,30)
                            intf_uut1 = line.split()[1]
                            intf_uut = line.split()[-1]
                            c = random.randint(100,200)
                            uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                            uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'XRv' in line:
                                a = uut1.name.strip('XR')
                                b = uut.name.strip('R')
                                encap = int(a+b)+random.randint(31,60)
                                intf_uut1 =  line.split()[1]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                c = random.randint(100,200)
                                uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                                uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                                description = uut1.name+"----"+uut.name
                                configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                                configure_subintf(uut,intf_uut,encap,uut_ip,description)
        else:
            if 'XR' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = uut1.name.strip('R')
                            b = uut.name.strip('XR')
                            encap = int(a+b)+random.randint(61,90)
                            intf_uut1 = line.split()[1]
                            intf_uut = line.split()[-2]+line.split()[-1]
                            c = random.randint(100,200)
                            uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                            uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                            description = uut1.name+"----"+uut.name
                            configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                            configure_subintf(uut,intf_uut,encap,uut_ip,description)
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'XRv' in line:
                                a = uut1.name.strip('R')
                                b = uut.name.strip('R')
                                encap = int(a+b)+random.randint(91,120)
                                intf_uut1 = line.split()[1]+line.split()[2]
                                intf_uut = line.split()[-2]+line.split()[-1]
                                c = random.randint(100,200)
                                uut1_ip = str(encap)+"."+str(encap)+"."+str(c)+".1"
                                uut_ip = str(encap)+"."+str(encap)+"."+str(c)+".2"
                                description = uut1.name+"----"+uut.name
                                configure_subintf(uut1,intf_uut1,encap,uut1_ip,description)
                                configure_subintf(uut,intf_uut,encap,uut_ip,description)

def copy_run_start(uut):
    if uut.os == 'iosxe':
        copy_run_start_xe(uut)
    elif uut.os == 'iosxr':
        copy_run_start_xr(uut)

def copy_run_start_xe(uut):
    dialog = Dialog([
        Statement(pattern=r'.*Destination filename \[startup-config\]\?',
                        action='sendline()',
                        loop_continue=True,
                        continue_timer=False)
        ])
    uut.execute("copy run startup-config", reply=dialog)


def copy_run_start_xr(uut):
    dialog = Dialog([
        Statement(pattern=r'.*Destination filename \[startup-config\]\?',
                        action='sendline()',
                        loop_continue=True,
                        continue_timer=False)
        ])

        #Destination file name (control-c to abort): [/startup-config]?
        #The destination file already exists. Do you want to overwrite? [no]: y



def add_ospf(uut):
 """
 router ospf 100
 router-id 1.1.1.1
 int lo0
 ip  ospf 12 area 12
 int lo10
 ip  ospf 12 area 12
 int GigabitEthernet0/1.12
 ip  ospf 12 area 12
 int GigabitEthernet0/2.12
 ip  ospf 12 area 12
 """
 cmd = \
 """
 """
<<<<<<< HEAD
 cmd += 'router ospf {id}'
 cmd += 'router-id  {rid}'

def add_bgp_vxlan(uut,conf_dict):

=======
 cmd += 'router ospf {id}' 
 cmd += 'router-id  {rid}' 
 

 


def add_bgp_vxlan(uut,conf_dict): 
 
>>>>>>> a7c04b8bb5dce427b1aa358b2bfcb3a15aacc289
    cfg_bgp = \
    """
    router bgp {as_num}
    router-id {rid}
    neighbor {neigh_id} remote-as {rem_as}
    update-source loopback0
    address-family l2vpn evpn
      send-community both
    vrf vxlan-900001
      address-family ipv4 unicast
      advertise l2vpn evpn
    """
    rid = conf_dict['protocols']['bgp'][uut.name]['rid']
    as_num = conf_dict['protocols']['bgp'][uut.name]['as']
    neigh_id = conf_dict['protocols']['bgp'][uut.name]['neighbor']
    rem_as = conf_dict['protocols']['bgp'][uut.name]['remote-as']
    uut.configure(cfg_bgp.format(as_num=as_num,neigh_id=neigh_id,rem_as=rem_as,rid=rid))


def add_vxlan_common_conf(uut):
    cfg_vxlan = \
    """
                    no vlan 1001-1002
                    nv overlay evpn
                    feature ospf
                    feature bgp
                    feature pim
                    feature interface-vlan
                    feature vn-segment-vlan-based
                    feature nv overlay
                    fabric forwarding anycast-gateway-mac 0000.2222.3333

                    evpn
                      vni 2001001 l2
                      vni 2001002 l2
                    rd auto
                        route-target import auto
                        route-target export auto

                    vlan 10
                      vn-segment 900001

                    interface Vlan10
                      no shutdown
                      vrf member vxlan-900001
                      ip forward

                    vlan 10
                    vlan 101
                      vn-segment 2001001
                    vlan 102
                      vn-segment 2001002

                    vrf context vxlan-900001
                      vni 900001
                      rd auto
                      address-family ipv4 unicast
                        route-target both auto
                        route-target both auto evpn
                      address-family ipv6 unicast
                        route-target both auto
                        route-target both auto evpn


                    interface Vlan101
                      no shutdown
                      vrf member vxlan-900001
                      ip address 101.1.1.1/24
                      ipv6 address 101:1:0:1::1/64
                      fabric forwarding mode anycast-gateway

                    interface Vlan102
                      no shutdown
                      vrf member vxlan-900001
                      ip address 102.1.1.1/24
                      ipv6 address 102:1:0:1::1/64
                      fabric forwarding mode anycast-gateway

                    interface nve1
                      no shutdown
                      source-interface loopback0
                      host-reachability protocol bgp
                      member vni 900001 associate-vrf
                      member vni 2001001
                      ingress-replication protocol bgp
                      member vni 2001002
                      ingress-replication protocol bgp

                    """
    uut.configure(cfg_vxlan)

def add_pim_config_all(uut,conf_dict):

    #vrf_interface_dict = {'default':['lo0','Gi0/0.100','Gi0/0.200'],'vrf1':['lo10','Gi0/0.110','Gi0/0.210']}

    intf_list = get_igp_intf_list(uut)
    rp_add = conf_dict['protocols']['pim'][uut.name]['rp_add']

    pim_conf = \
            """
            """
    if uut.os == 'nxos':
        pim_conf += 'ip pim rp-address {rp_add} group-list 224.0.0.0/4\n'.format(rp_add=rp_add)
        pim_conf += 'ip pim ssm range 232.0.0.0/8 \n'
    elif uut.os == 'iosxe':
        pim_conf += 'ip pim rp-address {rp_add}\n'.format(rp_add=rp_add)

    for intf in intf_list:
        pim_conf += 'interface {intf} \n'.format(intf=intf)
        pim_conf += 'ip pim sparse-mode \n'

    uut.configure(pim_conf)


def add_ebgp_ms_vxlan(uut,conf_dict):

    cfg_bgp = \
    """
    router bgp {as_num}
    neighbor {neigh_id} remote-as {rem_as}
    update-source {update_src}
    address-family l2vpn evpn
      send-community both
    """

    as_num = conf_dict['protocols']['ebgp'][uut.name]['as']
    neigh_id = conf_dict['protocols']['ebgp'][uut.name]['neighbor']
    rem_as = conf_dict['protocols']['ebgp'][uut.name]['remote-as']
    update_src = conf_dict['protocols']['ebgp'][uut.name]['update-source']

    uut.configure(cfg_bgp.format(as_num=as_num,neigh_id=neigh_id,rem_as=rem_as,update_src=update_src))

def add_mpls_config(uut):
    #import pdb ; pdb.set_trace()
    if uut.os == 'iosxr':
        cfg =\
        """
        mpls ldp
        address-family ipv4
        """
        intf_list = get_igp_intf_list(uut)
        for intf in intf_list:
            if not "Loop" in intf:
                cfg += 'interface {intf} \n'.format(intf=intf)
        uut.configure(cfg)

    elif uut.os == 'iosxe':
        cfg =\
        """
        mpls ldp router-id Loopback 0 for
        """

        intf_list = get_igp_intf_list(uut)
        for intf in intf_list:
            if not "oop" in intf:
                cfg += 'interface {intf} \n'.format(intf=intf)
                cfg += 'mpls ip\n'

        uut.configure(cfg)

def get_igp_intf_list(uut):
    intf_list= []
    op1= uut.execute('show ip interface brief | beg ddress')
    for line in op1.splitlines():
        if line:
            if not 'delete' in line:
                if  'GigabitEthernet0/1.' in line:
                    intf_list.append(line.split()[0])
                elif  'GigabitEthernet0/0/0/0.' in line:
                    intf_list.append(line.split()[0])
                elif  'GigabitEthernet0/0.' in line:
                    intf_list.append(line.split()[0])
                elif  'Loopbac' in line:
                    intf_list.append(line.split()[0])



    op2= uut.execute('show ip interface brief')
    for line in op2.splitlines():
        if "GigabitEthernet" in line:
            if not "unassigned" in line:
                intf_list.append(line.split()[0])


    print(intf_list)
    return intf_list

def vrf_conf(uut):
    if uut.os == 'iosxr':
        cfg = \
        """
        vrf CU02
        address-family ipv4 unicast
        import route-target
        1:2
        !
        export route-target
        1:2
        """
    elif uut.os == 'iosxr':
        cfg = \
        """
        vrf definition CU03
         rd 1:3
        route-target export 1:3
        route-target import 1:3
        !
        address-family ipv4
        exit-address-family
        !
        address-family ipv6
        exit-address-family
        """

def bgp_conf(uut):
    if uut.os == 'iosxr':
       cfg = \
        """
        router bgp 200
        bgp log neighbor changes detail
        address-family vpnv4 unicast
        !
        neighbor 102.2.2.1
        remote-as 200
        update-source Loopback0
         address-family vpnv4 unicast
         !
        !
        vrf CU02
        rd 1:2
        address-family ipv4 unicast
        redistribute connected
        !
        neighbor 2.202.103.2
        remote-as 300
         address-family ipv4 unicast
        route-policy ALL-PASS in
        route-policy ALL-PASS out
        send-extended-community-ebgp

        """
    elif uut.os == 'iosxe':
        cfg = \
         """
         router bgp 200
         bgp log neighbor changes detail
         address-family vpnv4 unicast
         !
         neighbor 102.2.2.1
         remote-as 200
         update-source Loopback0
         address-family vpnv4 unicast
         !
        !
        vrf CU02
        rd 1:2
        address-family ipv4 unicast
        redistribute connected
        !
        neighbor 2.202.103.2
        remote-as 300
        address-family ipv4 unicast
        route-policy ALL-PASS in
        route-policy ALL-PASS out
        send-extended-community-ebgp

        """


def mpls_igp_auto_conf(uut):
    cfg = \
        """
       interface GigabitEthernet0/1.303
       no mpls ip
       interface GigabitEthernet0/1.305
       no mpls ip
       interface GigabitEthernet0/1.307
       no mpls ip
       interface GigabitEthernet0/1.308
       no mpls ip
       exit
        mpls ip
       mpls label protocol ldp

       router isis 300
       mpls ldp autoconfig
       """

def consistency_check(uut):

    for mask in ['/24','/32']:
        op1 = uut.execute('sh route  | inc /{mask}'.format(mask=mask))
        op2 = uut.execute('sh mpls forwarding | inc {mask}'.format(mask=mask))

        for line in op1.splitlines():
            if mask in line:
                if not 'directly connected' in line:
                    ip = line.split()[1]
                    print('================== ip',ip)
                    if not ip in op2:
                        print('IP NOT Found in LFIB')
                        return 0

                    for line in op2.splitlines():
                        if ip in line:
                            if 'Gi' in line:
                                print('Found IP/Egress intf in LFIB')
                            else:
                                print('NOT Found Egress intf in LFIB')
                                return 0
    return 1

def configureBGP(uut):
    pe_xr =\
        """
        router bgp 49
        address-family ipv4 unicast
        network 1.1.1.1/32
        allocate-label all
        !
        neighbor 1.112.1.1
        remote-as 49
        update-source Loopback0
        address-family ipv4 labeled-unicast
        """

    abr_xr =\
        """
        route-policy nhsabr2
        set next-hop 2.112.2.1

        router bgp 49
        ibgp policy out enforce-modifications
        address-family ipv4 unicast
        network 2.112.2.1/32
        allocate-label all
        !
        neighbor 2.2.2.1
        remote-as 49
        update-source Loopback0
        address-family ipv4 labeled-unicast
        route-reflector-client
        route-policy nhsabr2 out
        next-hop-self
        !
        !
        neighbor 1.112.1.1
        remote-as 49
        update-source Loopback0
        address-family ipv4 labeled-unicast
        route-reflector-client
        route-policy nhsabr2 out
        next-hop-self
        !
        """
