

"""
A Fibonacci sequence is the integer sequence of 0, 1, 1, 2, 3, 5, 8....
Program to print the fibonacci series upto n_terms
# Recursive function
"""
import requests
from bs4 import BeautifulSoup
import re
import random



list2 = []
for i in range(200):
    list2.append(random.randint(1,2000000))

def sortSel(list2):
    list_new = []
    for i in range(len(list2)):
        min1 = min(list2)
        list_new.append(min1)
        list2.remove(min1)
    print(list_new)

sortSel(list2)


list3 = []
for i in range(200):
    list3.append(random.randint(1,2000000))
 
def sortBub(list3):
    list1 = list3
    len_list = len(list1)
    for i in range(len_list-1,0,-1):
        for j in range(i):
            if list1[j] > list1[j+1]:
                list1[j],list1[j+1] = list1[j+1],list1[j]

    print(list1)
    
sortBub(list3)
    
def searchLin(list1,element):
    for i in range(len(list1)):
        if list1[i] == element:
            print('Found, Index is:',i)
            return True
    return False

def searchBin(list1,element):
    list2 = list1
    list2.sort()
    index_min = 0
    index_max = len(list2)-1
    while index_min <= index_max:
        mid_index =  index_min+index_max//2
        if list2[mid_index] == element:
            print('Found, index is:',mid_index)
            return True
        elif list2[mid_index] > element:
            index_min =mid_index+1
        else:
            index_max = mid_index-1
        return False


        
listBig = []
for i in range(2000):
    listBig.append(random.randint(1,2000000))

   
for i in range(10):
    k = random.randint(8888,29000)
    searchBin(listBig,k)
    
for i in range(10):
    k = random.randint(8888,29000)
    searchLin(listBig,k)
    
    
    
show_evpn = \
	"""
	 PE1#show l2vpn evpn mac bridge-domain 10 detail 
	MAC Address:               000c.2911.6d2a
	EVPN Instance:             10
	Bridge Domain:             10
	Ethernet Segment:          03AB.CDAB.CDAB.C100.0001	-> ESI number assigned to the MAC learnt on this EFP
	Ethernet Tag ID:           0
	Next Hop(s):               Port-channel1 service instance 10	-> MAC learnt locally on port-channel 1
		                           3.3.3.3
	Local Address:             0.0.0.0
	Label:                     17
	Sequence Number:           0
	MAC only present:          Yes
	MAC Duplication Detection: Timer not running	

	MAC Address:               000c.29f8.5078
	EVPN Instance:             10
	Bridge Domain:             10
	Ethernet Segment:          03AB.CDAB.CDAB.C200.0002
	Ethernet Tag ID:           0
	Next Hop(s):               6.6.6.6
	Local Address:             1.1.1.1
	Label:                     19
	Sequence Number:           0
	MAC only present:          Yes
	MAC Duplication Detection: Timer not running
	"""

url = 'https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/mp_l2_vpns/configuration/xe-16-9/mp-l2-vpns-xe-16-9-book/evpn-multihoming.html'

def checkValidMACAddress(str):
    regex = ("^([0-9A-Fa-f]{2}[:-])" +
             "{5}([0-9A-Fa-f]{2})|" +
             "([0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4})$")
 
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False

def checkValidIPAddress(str):
    regex = "((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False

def checkValidIPV6Address(str):
    regex = ("^([0-9A-Fa-f]{2}[:-])" +
             "{5}([0-9A-Fa-f]{2})|" +
             "([0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4})$")
 
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False
                
def parse_show_evpn(op):
    for line in op.splitlines():
        if checkValidMACAddress(line):
            print(line)
        if checkValidIPAddress(line):
            print(line)



parse_show_evpn(show_evpn)

        
def find_string_in_url(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  test = soup.findAll(text = re.compile('Multihoming'))
  #import pdb;pdb.set_trace()
  print(test)


#find_string_in_url(url)


def complement(sequence):
   """ (str) -> str
   Return the complement of sequence.
   """
   res = ""
   for i in range(1,len(sequence)+1):
       i = -i
       res = res + sequence[i]
       print(res)
   return(res)

print(complement("ABCTEFH"))

def find_min_two(L):
   list1 = L
   list1.sort()
   print (list1[0])
   print (list1[1])

#import pdb,pdb.set_trace()
aa = [222,4444,55555,1,33333,44444,44444,122,-1000,0]

find_min_two(aa)

def find_min_two2(L):
   if L[0] < L[1]:
       min1,min2 = 0,1
   else:
       min1,min2 = 1,0

   for i in range(2,len(L)):
       print("-----",i)
       if L[i] < L[min1]:
           min2 = min1
           min1 = i
       elif L[i] < L[min2]:
           min2 = i
   return (min1,min2)

a = find_min_two2(aa)
print(a)

def fib2(n):
   list1 = []

   n1,n2 = 0,1
   list1.append(n1)
   list1.append(n2)

   for i in range(n-1):
       fib = n1+n2
       list1.append(fib)
       n1 = n2
       n2 = fib

   print(list1)

fib2(10)
def fact(n):
   # 1 * 2 * 3 *
   if n == 1:
       return n
   else:
       a = n * fact(n-1)
       print(a)
