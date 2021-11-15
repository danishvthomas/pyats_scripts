from igp_lib import *
def add_mpls_conf10(uut,os=None):

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