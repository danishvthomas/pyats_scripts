
def configure_subint2(uut,conf_dict):
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
 
            for intf in intf_list:
                vlan_id1 = int(intf.split('.')[1])
                cmd1 = \
                """
                """
                cmd1 += 'interface {intf} \n'.format(intf=intf)    
                cmd1 += 'encap dot1q {vlan_id1}\n'.format(vlan_id1=vlan_id1) 
                desc = conf_dict['ethernet'][node]['interfaces'][intf]['description']
                cmd1 += 'description connect_to_{desc}\n'.format(desc=desc)       
                ip_add = conf_dict['ethernet'][node]['interfaces'][intf]['ip_add']
                if 'iosxr' in uut.os:
                    cmd1 += 'ipv4 add {ip_add} \n'.format(ip_add=ip_add)
                elif 'iosxe' in uut.os:
                    cmd1 += 'ip add {ip_add}\n'.format(ip_add=ip_add)
                #v6_pref = '2001:'+str(vlan_id1)+'::0'
                #random.seed()
                #ipv6_a = IPAddress(v6_pref) + random.getrandbits(16)
                #ipv6_add = IPNetwork(ipv6_a)
                #ipv6_add.prefixlen = 96
                #cmd1 += 'ipv6 add {ipv6_add}\n'.format(ipv6_add=str(ipv6_add))
                cmd1 += 'no shut\n'
                uut.configure(cmd1)