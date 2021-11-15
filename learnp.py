import random
print("Test")




listBig = []
for i in range(200):
    listBig.append(random.randint(1,2000000))


def searchLin(list,element):
    for i in range(len(list)):
        if list[i] == element:
            print('Found, Index is:',i)
            return True
    return False


 

def searchBin(list2,element):
    list2.sort()
    #print(list2)
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


    for i in range(len(list)):
        if list[i] == element:
            print('Found, Index is:',i)
            return True
    return False

 
def sortBub(list2):
    list1 = list2
    len_list = len(list1)
    for i in range(len_list-1,0,-1):
        for j in range(i):
            if list1[j] > list1[j+1]:
                #temp = list1[j]
                #list1[j] = list1[j+1]
                #list1[j+1] = temp 
                list1[j],list1[j+1] = list1[j+1],list1[j]

    print(list1)

def sortSel(list2):
    list_new = []
    for i in range(len(list2)):
        min1 = min(list2)
        list_new.append(min1)
        list2.remove(min1)
    
 
    print(list_new)


list10 = [1,2,344,1,22,333,45,1,0,7777]

def feb(n):
    a = 0
    b = 1
    print(a)
    print(b)
    for i in range(2,n):
        c = a+b
        print(c)
        a,b = b,c


import pdb ; pdb.set_trace()
feb(10)

sortBub(list10)
sortBub(listBig)