
nodes = \
    """
    aae319        n0        0,1             core1xe              unifiedMPLS
    aae319        n1      0,1,2              abr2xr              unifiedMPLS
    aae319       n10        0,1                 ce1              unifiedMPLS
    aae319       n11        0,1                 ce2              unifiedMPLS
    aae319       n12        0,1                 ce3              unifiedMPLS
    aae319        n2      0,1,2              abr1xr              unifiedMPLS
    aae319        n3        0,1              abr3xe              unifiedMPLS
    aae319        n4        0,1             agg2pxe              unifiedMPLS
    aae319        n5      0,1,2             agg1pxr              unifiedMPLS
    aae319        n6        0,1             agg3pxe              unifiedMPLS
    aae319        n7      0,1,2               pe2xr              unifiedMPLS
    aae319        n8      0,1,2               pe1xr              unifiedMPLS
    aae319        n9        0,1               pe3xe              unifiedMPLS
    """

def get_node_list(nodes,name):
    node_list = []
    xe_node_list = []
    xr_node_list = []
    nx_node_list = []
    for line in nodes.splitlines():
        if name in line:
            node = line.split()[3]
            node_list.append(node)
            if 'xe' in node:
                xe_node_list.append(node)
            elif 'xr' in node:
                xr_node_list.append(node)
            if 'nx' in node:
                nx_node_list.append(node)
    print(node_list)
    print(xe_node_list)
    print(xr_node_list)
    print(nx_node_list)
    

get_node_list(nodes,'unifiedMPLS')
