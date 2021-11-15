router bgp 49
 bgp log-neighbor-changes
 neighbor 1.112.1.1 remote-as 49
 neighbor 1.112.1.1 update-source Loopback0
 neighbor 2.112.2.1 remote-as 49
 neighbor 2.112.2.1 update-source Loopback0
 neighbor 3.3.3.1 remote-as 49
 neighbor 3.3.3.1 update-source Loopback0
 !
 address-family ipv4
  network 3.112.3.1 mask 255.255.255.255
  neighbor 1.112.1.1 activate
  neighbor 1.112.1.1 route-reflector-client
  neighbor 1.112.1.1 next-hop-self all
  neighbor 1.112.1.1 send-label
  neighbor 2.112.2.1 activate
  neighbor 2.112.2.1 route-reflector-client
  neighbor 2.112.2.1 next-hop-self  all
  neighbor 2.112.2.1 send-label
  neighbor 3.3.3.1 activate
  neighbor 3.3.3.1 route-reflector-client
  neighbor 3.3.3.1 next-hop-self  all
  neighbor 3.3.3.1 send-label
