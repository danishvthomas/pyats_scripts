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
        global uut_list,SP1PE1,SP1P1,SP1P2,SP1PE2,CE2,SP2PE1,SP2P1,SP2PE2,SP3PE1,\
            SP3PE2,SP3PE3,CE3,CE4,SP3P1,SP3P2,SP3P3,SP3P4,SP3P5,SP3P6,\
            core_uut_list_iosxe,xr_uut_list,xe_uut_list
  
        # connect to device
    
        CE1 = testbed.devices['CE1']
 
        SP1PE1 = testbed.devices['SP1PE1']
 
        SP1P1 = testbed.devices['SP1P1']
 
        SP1P2 = testbed.devices['SP1P2']
       

        uut_list1 =  list(testbed.devices.keys())            

        uut_list = [] 
        xe_uut_list = []
        for uut in testbed.devices.keys():
            if not 'jumphost' in uut:
                dev = testbed.devices[uut]
                uut_list.append(dev)
                if not 'xr' in dev.os:
                    xe_uut_list.append(dev)

        #import pdb ; pdb.set_trace()       


        #uut_list = [ios1,ios2,ios3,ios4,ios5,ios6,ios7,ios8,ios9,ios10,xrv1,xrv2,xrv3,xrv4]
        #uut_list = [r1,ios2,ios3,ios4]
        #uut_list_iosxe = [ios1,ios2,ios3,ios4,ios5,ios6,ios7,ios8,ios9,ios10]    

        #core_uut_list_iosxe = [ios1,ios2,ios3,ios4,ios5,ios6,ios7,ios8]    
         
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13

        for uut in uut_list:
            print(uut.name)
 

        

        jumphost = testbed.devices['jumphost']
        jumphost.connect()
        op1 = jumphost.execute("list")
        for line in op1.splitlines():
            if 'iosv' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    #if uut.name == node_label:
                    uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'
            elif 'xrv' in line:
                lab_id = str(line.split()[0])
                node_label = str(line.split()[3])
                node_id = str(line.split()[1])
                for uut in uut_list:
                    #if uut.name == node_label:
                    uut.connections['cli']["command"]='open /'+lab_id+'/'+node_id+'/0'
                logger.info('lab_id is : %s' % lab_id)

        
        #r1.connections['cli']["command"]='open /'+lab_id+'/n0/0'
        import pdb ; pdb.set_trace()
        for dev in uut_list:
            import pdb ; pdb.set_trace()
            dev.connect(learn_hostname=True)
            dev.configure('hostname {name}'.format(name=r.name))
            
 
       
    @aetest.subsection
    def basic_conf_devices(self, testbed):
         
        #R11----R1--R2--R3--R4------R12
        #       | X | X | X |
        #       R5--R6--R7--R8 
        #       | X | X | X |
        #R11---XR1--XR2-XR3--XR4 ----R13


        pcall(unshut_intf,uut=tuple(uut_list))
        
        #import pdb ; pdb.set_trace()
        kk =  []  
        for uut in uut_list:
            op = uut.execute('show cdp neigh')
            for line in op.splitlines():
                if 'Gig' in line:
                    kk.append(line) 
                    #print(line)
                    #cmd += 'area {area} \n'.format(area=str(key2))
                #elif 'cisco' in line:
                #    kk += line + 'n\'                        
        import pdb ; pdb.set_trace()
        for line in kk:
            print(line)   
        print(kk)

        pcall(copy_run_start,uut=tuple(xe_uut_list))

    	
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))