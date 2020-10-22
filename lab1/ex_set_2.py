print("ex. 1")
listOne = [3, 6, 9, 12, 15, 18, 21]
listTwo = [4, 8, 12, 16, 20, 24, 28]
listThree = []
for i in range(len(listOne)):
    if i % 2 == 0:
        listThree.append(listTwo[i])
    else:
        listThree.append(listOne[i])

print(listThree)

#soluzione prof
#odd_elements = listOne[1::2]
#even_elements = listTwo[0::2]
#listThree.extend(odd_elements)
#listThree.extend(even_elements)

print("ex. 2")
sampleList = [34, 54, 67, 89, 11, 43, 94]
value = sampleList.pop(4)
sampleList.insert(1, value)
sampleList.append(value)
print(sampleList)

print("ex. 3")
sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]
num_el_for_chunk = int(len(sampleList)/3)
chunk1 = sampleList[0:num_el_for_chunk]
chunk2 = sampleList[num_el_for_chunk:2*num_el_for_chunk]
chunk3 = sampleList[2*num_el_for_chunk:len(sampleList)]
chunk1.reverse()
chunk2.reverse()
chunk3.reverse()
print("Chunk 1: ", chunk1)
print("Chunk 2: ", chunk2)
print("Chunk 3: ", chunk3)

#soluzione prof
"""
length = len( sample_list )
chunk_size = int( length / 3)
start = 0
end = chunk_size
4
for i in range (1 , chunk_size +1):
    indexes = slice (start , end , 1)
    list_chunk = sample_list [ indexes ]
    print (’Chunk ’, i, list_chunk )
    print (’After reversing it ’, list ( reversed ( list_chunk )))
    start = end
    if i < chunk_size :
        end += chunk_size
    else :
        end += length - chunk_size"""

print("ex. 4")
sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]
count_dict = dict()
for x in sampleList:
    count = sampleList.count(x)
    count_dict[x] = count

print(count_dict)

print("ex. 5")
firstList = [2, 3, 4, 5, 6, 7, 8]
secondList = [4, 9, 16, 25, 36, 49, 64]
result = zip(firstList, secondList)
print(result)
result_set = set(result)
print(result_set)

print("ex. 6")

firstSet = {23, 42, 65, 57, 78, 83, 29}
secondSet = {57, 83, 29, 67, 73, 43, 48}
intersection = firstSet.intersection(secondSet) #trova gli elementi in comune tra i due set
firstSet.difference_update(intersection) #rimuove dal primo set gli elementi in comune con il secondo
print(firstSet)

print("ex. 7")

firstSet = {57, 83, 29}
secondSet = {57, 83, 29, 67, 73, 43, 48}
if firstSet.issubset(secondSet): print("firstSet is subset")
if firstSet.issuperset(secondSet): print("firstSet is superset")
if secondSet.issubset(firstSet): print("secondSet is subset")
if secondSet.issuperset(firstSet): print("secondSet is superset")
if firstSet.issubset(secondSet):
    firstSet.clear()
if secondSet.issubset(firstSet):
    secondSet.clear()

print("ex. 8")
rollNumber = [47, 64, 69, 37, 76, 83, 95, 97]
sampleDict = {'Jhon':47, 'Emma':69, 'Kelly':76, 'Jason':97}
rollNumber[:] = [item for item in rollNumber if item in sampleDict.values()]
print(rollNumber)

print("ex. 9")
speed = {'Jan': 47, 'Feb': 52, 'March': 47, 'April': 44, 'May': 52, 'June': 53, 'July': 54, 'Aug': 44, 'Sept': 54}
list1 = []
for x in speed.values():
    if x not in list1:
        list1.append(x)
print(list1)

print("ex. 10")
sampleList = [87, 52, 44, 53, 54, 87, 52, 53]
list1 = list(set(sampleList))
print(list1)
my_tuple = tuple(list1)
print(my_tuple)
print("max is ", max(my_tuple))
print("min is ", min(my_tuple))


