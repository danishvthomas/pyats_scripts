import time



def checkPrime(n):
    if n > 1:
        for i in range(2,int(n/2)+1):
            if (n%i) == 0:
                print("NO PRIME",n)
                break
        else:
            print("PRIME",n)      
    else:
         print("NO PRIME",n)   


for i in range(102):
    checkPrime(i)


def sortList(List1):
    print(List1)
    n = len(List1)
    for i in range(0,n):
        for j in range(0,n-i-1):
            if List1[j]>List1[j+1]:
                List1[j],List1[j+1]=List1[j+1],List1[j]
    print("SORTED")
    print(List1)

k = [33,4,232,3,23323,1,220]
pp = ["a","b","c","d","e","f","g"]

dict1 = {}
for i,j in zip(pp,k):
    dict1[i] = j

print(dict1)
sortList(k)


op1 = \
"""
RP/0/0/CPU0:XR1#sh route ipv4
Mon Feb 19 17:27:38.228 UTC


L    1.1.1.1/32 is directly connected, 00:25:01, Loopback0
L    1.1.1.10/32 is directly connected, 00:25:01, Loopback10
L    1.1.1.100/32 is directly connected, 00:25:01, Loopback100
i L2 2.2.2.1/32 [115/10] via 133.133.198.2, 00:18:33, GigabitEthernet0/0/0/2
i L2 3.3.3.1/32 [115/10] via 145.145.186.2, 00:18:33, GigabitEthernet0/0/0/1
i L2 9.9.9.1/32 [115/10] via 40.40.163.2, 00:18:33, GigabitEthernet0/0/0/0
i L2 10.10.10.1/32 [115/10] via 108.108.193.2, 00:18:33, GigabitEthernet0/0/0/3
C    40.40.163.0/24 is directly connected, 00:24:20, GigabitEthernet0/0/0/0
L    40.40.163.1/32 is directly connected, 00:24:20, GigabitEthernet0/0/0/0
C    108.108.193.0/24 is directly connected, 00:24:16, GigabitEthernet0/0/0/3
L    108.108.193.1/32 is directly connected, 00:24:16, GigabitEthernet0/0/0/3
C    133.133.198.0/24 is directly connected, 00:24:13, GigabitEthernet0/0/0/2
L    133.133.198.1/32 is directly connected, 00:24:13, GigabitEthernet0/0/0/2
C    145.145.186.0/24 is directly connected, 00:24:10, GigabitEthernet0/0/0/1
L    145.145.186.1/32 is directly connected, 00:24:10, GigabitEthernet0/0/0/1
"""

def getRouteDetails(cliOut):
    routeDict = {}
    for line in cliOut.splitlines():
        if 'directly' in line:
            prefix = line.split()[1]
            interface = line.split()[-1]
            routeDict[prefix]=interface
        elif 'via' in line:
            prefix = line.split()[2]
            nh = line.split()[5]
            routeDict[prefix]=nh    
    print("ROute Dict")                    
    print(routeDict)


getRouteDetails(op1)    