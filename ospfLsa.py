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
        uut16 = testbed.devices['uut16']
        uut17 = testbed.devices['uut17']
        uut18 = testbed.devices['uut18']                        
        xr_uut_list = [uut15,uut16,uut17,uut18]
        #Genie.testbed = testbed = Testbed()
        #uut1 = Device(testbed=testbed, name='R1', os='iosxe')

        #uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut9,uut10,uut11,uut12,uut13,uut14,uut15,uut16,uut17,uut18]
        uut_list = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8,uut15,uut16,uut17,uut18]
        uut_list_iosxe = [uut1,uut2,uut3,uut4,uut5,uut6,uut7,uut8]    

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

        
        for uut in uut_list:
         	uut.connect()     

    @aetest.subsection
    def basic_conf_devices(self, testbed):
        #              xr1-----xr2 ---xr3---xr4  
        #    1          |   0
        # r1----r2---|-r3-----r4---|-------R5 (stub)
        #            /  |     |
        #           /   |     |
        #          r6   r7   r8-----Ext Redis Loop    
        #         Ts    |
        #              NSSOA 
        
        conf_dict=yaml.load(open('topo1.yaml'))
   
        print(conf_dict)

        conf_dict['protocols']['ospf']['R1']['area']
        for key in list(conf_dict['protocols']['ospf'].keys()):
 
        pcall(unshut_intf,uut=tuple(uut_list))
        pcall(remove_intf_all,uut=tuple(uut_list))

        loopback_config(uut_list)
        bring_up_subif(uut1,[uut2])
        bring_up_subif(uut2,[uut3])
        bring_up_subif(uut3,[uut6,uut7,uut4,uut8,uut15])
        bring_up_subif(uut4,[uut5,uut8])
        bring_up_subif(uut15,[uut16])   
        bring_up_subif(uut16,[uut17])
        bring_up_subif(uut17,[uut18])     
        pcall(cleanup_igp,uut=tuple(uut_list))
        
        
        for key in list(conf_dict['dot1q'].keys()):
            for key2 in conf_dict['dot1q'][key].keys():
                cmd = \
                """
                router ospf 100
                """


        for key in list(conf_dict['protocols']['ospf'].keys()):
            cmd = \
                """
                router ospf 100
                """
            host_name = key
            rid = conf_dict['protocols']['ospf'][key]['rid']
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
                intf_list = conf_dict['protocols']['ospf'][key]['area'][key2]['interfaces'].split(',')
                for intf in intf_list:
                    cmd += 'interface {intf} \n'.format(intf=intf)
                    cmd += 'ip ospf 100 area {area} \n'.format(area=str(key2))

            for uut in uut_list_iosxe:
                if uut.name == host_name:
                    #import pdb ; pdb.set_trace() 
                    uut.configure(cmd)



        pcall(copy_run_start,uut=tuple(uut_list))
        import pdb ; pdb.set_trace() 
 
if __name__ == "__main__":
    # if this script is run stand-alone
    import os
    from genie.testbed import load

    HERE = os.path.dirname(__file__)

    aetest.main(testbed = load(os.path.join(HERE, '..', 'files', 'workshop-testbed.yaml')))