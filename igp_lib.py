#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

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
                        cmdxe += 'isis circuit-type level-1  \n' 
                uut.configure(cmdxe.format(net=net))    
 
  

def configure_isis_new(uut,area,l1_uut_list):

  
    """
    A router has a Network Entity Title (NET) of 49.001a.1122.3344.5566.00. To what area does this router belong, and what is its system ID?
    The area is 49.001a. The router's system ID is 1122.3344.5566. The easiest way to figure this out is to start from the right and work towards the left. The last two numbers of the NET are the NSEL; they are always 00 on a router. The next 12 numbers (separated into 3 groups of 4 numbers) are the system ID. On Cisco routers, the system ID is always this length—6 bytes. Anything to the left of the system ID is the area ID.
    """

    #net = '49.0000.0000.0000.0012.00'

    mac1 = str(RandMac("0000.0000.0000"))
    net = area+"."+mac1+'.00'
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
    l1_int_list = []
    l2_int_list = []
    op1 = uut.execute('show int desc | inc xrv')
    #show int desc | inc xrv
    #Wed May 26 12:21:05.634 UTC
    #Gi0/0/0/0.108      up          up          xrv-8----xrv-9
    #Gi0/0/0/0.128      up          up          xrv-7----xrv-9
    #RP/0/0/CPU0:xrv-9#


    
    for line in op1.splitlines():
        if 'Gi' in line:
            for uut1 in l1_uut_list:
                if uut1.name in line:
                    l1_int_list.append(line.split()[0])
                else:    
                    l2_int_list.append(line.split()[0])
    
    l1_int_list = list(set(l1_int_list))
    l2_int_list = list(set(l2_int_list))
    if uut.os == 'iosxr':
        for intf in l2_int_list:
            cmdxr += 'interface {intf} \n'.format(intf=intf)
            cmdxr += 'address-family ipv4 unicast \n'
            cmdxr += 'address-family ipv6 unicast \n' 
            cmdxr += 'circuit-type level-2-only \n' 
        for intf in l1_int_list:
            cmdxr += 'interface {intf} \n'.format(intf=intf)
            cmdxr += 'address-family ipv4 unicast \n'
            cmdxr += 'address-family ipv6 unicast \n' 
            cmdxr += 'circuit-type level-1 \n' 
          
        uut.configure(cmdxr.format(net=net))            
  
    elif uut.os == 'iosxe':
        for intf in l2_intf_list:
            cmdxe += 'interface {intf} \n'.format(intf=intf)
            cmdxe += 'ip router isis 100 \n'
            cmdxe += 'isis circuit-type level-2  \n' 
        for intf in l1_intf_list:
            cmdxe += 'interface {intf} \n'.format(intf=intf)
            cmdxe += 'ip router isis 100 \n'
            cmdxe += 'isis circuit-type level-1  \n' 
        uut.configure(cmdxe.format(net=net))    
 
  

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
            else:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            if not 'xrv' in line:
                                a = random.randint(31,70)
                                b = random.randint(31,70)
                                encap = int(a+b)+random.randint(10,30)
                                if encap > 200:
                                    encap = random.randint(25,199)
                                    if encap == 127:
                                        encap = encap + random.randint(25,50)
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
            if 'xr' in uut.name:
                for line in op1.splitlines():
                    if uut.name in line:
                        if not '.' in line:
                            a = random.randint(31,70)
                            b = random.randint(31,70)
                            encap = int(a+b)+random.randint(30,60)
                            if encap > 200:
                                encap = random.randint(25,199)
                                if encap == 127:
                                    encap = encap + random.randint(25,50)
                            if uut1.os == 'nxos':
                                intf_uut1 = line.split()[1]
                                intf_uut =  line.split()[-1]
                            else:
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
                            if not 'xr' in line:
                                a = random.randint(31,70)
                                b = random.randint(31,70)
                                encap = int(a+b)+random.randint(60,90)
                                if encap > 200:
                                    encap = random.randint(25,199)
                                    if encap == 127:
                                        encap = encap + random.randint(25,50)
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
            
def get_igp_intf_list(uut):
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
 

def add_mpls_conf(uut,os=None):

    #vrf_interface_dict = {'default':['lo0','Gi0/0.100','Gi0/0.200'],'vrf1':['lo10','Gi0/0.110','Gi0/0.210']}
    cfg = \
    """
    mpls ldp
    """
    cfg2 = \
    """
    mpls ldp router-id loopback 0
    """
    intf_list = get_igp_intf_list2(uut)
    rid =  get_intf_ip(uut,'Loopback0')   
    if 'iosxr' in uut.os:
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
    intf_list = get_igp_intf_list2(uut)
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


def add_ospf_config(uut,os=None,instance=None):

    #vrf_interface_dict = {'default':['lo0','Gi0/0.100','Gi0/0.200'],'vrf1':['lo10','Gi0/0.110','Gi0/0.210']}
    cfg = \
    """
    router ospf {instance}
    router-id {rid}
    area 0
    """
    intf_list = get_igp_intf_list2(uut)
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



def configure_subintf(uut,intf,dot1q,ip_add,description):
    cfg = \
    """
    interface {intf}.{dot1q}
    description {description}
    encap dot1q {dot1q}
    ip address {ip_add} 255.255.255.0
    no shut
    """
    try:
        uut.configure(cfg.format(intf=intf,dot1q=dot1q,ip_add=ip_add,description=description))
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
        interface eth1/1-128
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
                    cfg += 'no shut\n'
                    cfg += 'cdp en\n'
                elif 'iosxr' in uut.os:
                    cfg += 'interface {intf}\n'.format(intf=intf) 
                    cfg += 'no shut\n'
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
    pdb.set_trace()
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
 cmd += 'router ospf {id}' 
 cmd += 'router-id  {rid}' 
 
def add_bgp_vxlan(uut,conf_dict): 
 
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
        intf_list = get_igp_intf_list2(uut)
        for intf in intf_list:
            cfg += 'interface {intf} \n'.format(intf=intf)
        uut.configure(cfg)

    elif uut.os == 'iosxe':
        cfg =\
        """
        mpls ldp router-id Loopback 0
        """       

        intf_list = get_igp_intf_list2(uut)
        for intf in intf_list:
            cfg += 'interface {intf} \n'.format(intf=intf)
            cfg += 'mpls ip\n'

        uut.configure(cfg)

def get_igp_intf_list2(uut):
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