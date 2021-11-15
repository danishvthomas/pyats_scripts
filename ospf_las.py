import logging

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
                    uut.configure('no interface {intf}'.format(intf=intf))



def unshut_intf(uut):
    intf_list =[]
    op1 = uut.execute("show ip int brief")
    for line in op1.splitlines():
        if 'NVRAM' in line:
            intf = line.split()[0]
            intf_list.append(intf)
        elif 'default' in line:
            intf = line.split()[0]
            intf_list.append(intf)

    cfg = \
    """
    interface {intf}
    no shut
    cdp en
    """
    if 'iosxr' in uut.os:
        cfg = \
        """
        cdp
        interface {intf}
        no shut
        cdp
        """
    for intf in intf_list:
        uut.configure(cfg.format(intf=intf))

def loopback_config(uut_list):
    i=1
    for uut in uut_list:
        loop0_ip_add = str(i)+"."+str(i)+"."+str(i)+".1"
        loop10_ip_add = str(i)+"."+str(i)+"."+str(i)+".10"
        loop100_ip_add = str(i)+"."+str(i)+"."+str(i)+".100"
        cfg = \
        """
        interface loopb 0
        ip address {loop0_ip_add} 255.255.255.255
        no shut 
        interface loopb 10
        ip address {loop10_ip_add} 255.255.255.255
        no shut 
        interface loopb 100
        ip address {loop100_ip_add} 255.255.255.255
        no shut 
        """
        uut.configure(cfg.format(loop0_ip_add=loop0_ip_add,loop10_ip_add=loop10_ip_add,loop100_ip_add=loop100_ip_add))
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



def bring_up_subif(uut1,nei_list):
    for uut in nei_list:
        op1=uut1.execute('show cdp ne | incl {a}'.format(a=uut.name))
        for line in op1.splitlines():
            if uut.name in line:
                intf_uut1 = line.split()[1]+line.split()[2]
                intf_uut = line.split()[-2]+line.split()[-1]
                if 'iosxr' in uut.os:
                    intf_uut1 = line.split()[-1] 
                    intf_uut = line.split()[1]                
                encap = random.randint(100,200)
                b = random.randint(100,200)
                uut1_ip = str(encap)+"."+str(b)+".88.1"
                uut_ip = str(encap)+"."+str(b)+".88.2"
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

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    

    @aetest.subsection
    def connect_to_tb_devices(self, testbed):
        # convert a pyATS testbed to Genie testbed
        # genie testbed extends pyATS testbed and does more with it, eg, 
        # adding .learn() and .parse() functionality
        # this step will be harmonized and no longer required in near future
        self.parent.parameters['testbed'] = testbed = load(testbed)
        global uut_list,uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut15,uut16,uut17,uut18,uut_list_iosxe,\
            core_uut_list_iosxe,xr_uut_list
            
            


        # connect to device
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
        uut16 = testbed.devices['uut16']
        uut17 = testbed.devices['uut17']
        uut18 = testbed.devices['uut18']                        
        xr_uut_list = [uut15,uut16,uut17,uut18]
        #Genie.testbed = testbed = Testbed()
        #uut1 = Device(testbed=testbed, name='R1', os='iosxe')

        uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut15,uut16,uut17,uut18]
        #uut_list = [uut1,uut2,uut3,uut4]
        uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14]    

        core_uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8]    
         
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13


        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if '.virl' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                	if uut.name == node_label:
                		uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'

                logger.info('lab_id is : %s' % lab_id)

        
        #uut1.connections['cli']["command"]='open /'+lab_id+'/n0/0'
        
        for uut in xr_uut_list:
        	uut.connect()

        #pdb.set_trace()

        #add_ospf_config(uut1)
      
      
        #pcall(add_ospf_config,uut=tuple(xr_uut_list))
        import pdb ; pdb.set_trace()
        pcall(add_mpls_interface_config,uut=tuple(xr_uut_list))
        add_mpls_interface_config(xr_uut_list[0])
        pcall(copy_run_start,uut=(xr_uut_list))
        '''
        # compute our neighbors
        #original_stdout = sys.stdout # Save a reference to the original standard output
        #with open('show_logg.txt', 'w') as f:
        #    sys.stdout = f # Change the standard output to the file we created.
        #    for uut in [uut8,uut16]:
        #        uut.execute("show logg")

        #    sys.stdout = original_stdout # Reset the standard output to its original value

        #result = pcall(connect_device,uut=tuple(uut_list))
 
        #remove_subintf(uut1," Gi0/2",'12')

 
    @aetest.subsection
    def basic_conf_devices(self, testbed):
        #    1             0
        # r1----r2---|-r3-----r4---|-------R5 (stub)
                     /  |     |
                    /   |     |
                  r6   r7----r8-----Ext Redis Loop    
                  Ts    |
                        r6

        #                 
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13


        
        loopback_config(uut_list)
 
        pcall(unshut_intf,uut=tuple(uut_list))
        pcall(remove_subintf,uut=tuple(uut_list))



        bring_up_subif(uut1,[uut11,uut2,uut5,uut6])
        bring_up_subif(uut2,[uut5,uut6,uut7,uut3])
        bring_up_subif(uut3,[uut6,uut7,uut8,uut4])
        bring_up_subif(uut4,[uut7,uut8,uut12])
        bring_up_subif(uut5,[uut6,uut15,uut16])
        bring_up_subif(uut6,[uut7,uut15,uut16,uut17])
        bring_up_subif(uut7,[uut8,uut16,uut17,uut18])
        bring_up_subif(uut8,[uut17,uut18])
        bring_up_subif(uut15,[uut11,uut16])
        bring_up_subif(uut16,[uut17])
        bring_up_subif(uut17,[uut18])
        bring_up_subif(uut18,[uut13])

 
        for uut in uut_list:
            #pdb.set_trace()
            uut.connect()


class Test_BGP(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        #pdb.set_trace()
        # do our learning
        uut16.execute("show ver")
        self.bgp = testbed.devices['uut1'].learn('bgp')

    @aetest.test
    def test_bgp_has_neighbors(self):
        # compute our neighbors
        
        uut16.execute("show ver")       
        nbr_info = []
        for bgp_instance in self.bgp.routes_per_peer['instance']:
            for vrf in self.bgp.routes_per_peer['instance'][bgp_instance]['vrf']:
                for nbr in self.bgp.routes_per_peer['instance'][bgp_instance]['vrf'][vrf]['neighbor']:
                    nbr_info.append((bgp_instance, vrf, nbr))

        # decide whether this testcase is pass or fail
        if not nbr_info:
            self.failed('BGP neighbors are missing!')
        else:
            # on pass - save the neighbor data for future analysis
            # in the final report
            self.passed('We have %s neigbors' % len(nbr_info), 
                        data = {'neighbors': nbr_info})

class log_analyse(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        # do our learning
        pass

    @aetest.test
    def log_analyse_uut(self):
        # compute our neighbors
        file = open('show_logg.txt', mode = 'r', encoding = 'utf-8-sig')
        lines = file.readlines()
        file.close()
        for line in lines:
        	print(line)

'''        	
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))