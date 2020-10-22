import numpy as np

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
prod = num1*num2
if prod > 1000:
    result = num1+num2
else:
    result = prod
print("The result is", result)

num = 10
print("Printing current and previous number sum in a given range")
prev = 0
for curr in range(num):
    tot = curr + prev
    print("Sum: ", tot)
    prev = curr

list1 = [1, 2, 3, 4, 5, 6]
list2 = [1, 2, 3, 4, 5, 1]

print("Comparing first and last element of list1")
if list1[0] == list1[-1]:
    print("Values are the same")
else:
    print("Values are not the same")

print("Comparing first and last element of list2")
if list2[0] == list2[-1]:
    print("Values are the same")
else:
    print("Values are not the same")

list3 = [5, 10, 12, 20, 23]
for x in list3:
    if x % 5 == 0:
        print(x, " is divisible by 5")


string = "Emma is a good developer, Emma is also a writer"
count = 0
chunks = string.split(' ')
for x in chunks:
    if x == 'Emma':
        count = count + 1

print("The word 'Emma' is repeated ", count, " times")

list4 = []

for x in list1:
    if x % 2 != 0:
        list4.append(x)

for x in list2:
    if x % 2 == 0:
        list4.append(x)

print("The merged list is: ", list4)

s1 = "Laboratorio di OON numero 1"
s2 = " mi metto in mezzo "
middle = int(len(s1) / 2)

s3 = s1[:middle] + s2 + s1[middle:]
print("Sentence with second sentence in the middle: ", s3)

s1 = "Prima stringa"
s2 = "Seconda stringa"
s3 = s1[0] + s1[int(len(s1)/2)] + s1[-1] + s2[0] + s2[int(len(s2)/2)] + s2[-1]
print("String made of first, middle and last char of two strings: ", s3)

s1 = "Ciao a tUTTI e 127!! STo Bene_"
char_lower_count = 0
char_upper_count = 0
digit_count = 0
special_count = 0
for i in range(len(s1)-1):
    if s1[i].islower():
        char_lower_count += 1
    elif s1[i].isupper():
        char_upper_count += 1
    elif s1[i].isnumeric():
        digit_count += 1
    else:
        special_count += 1

print("In the string ", s1, " there are ", char_lower_count, " lowercase chars, ", char_upper_count,
      " uppercase chars, ", digit_count, " digits and ", special_count, " special chars")

s1 = "Welcome in USA where USA are fascinating"
s2 = "USA"

tmp_string = s1.lower()
count = tmp_string.count(s2.lower())

print("USA is present ", count, " times")

s1 = "Vote of sub1 is 10 , vote of sub2 is 7"
chunks = s1.split()
print(chunks)
numbers = [int(num) for num in chunks if num.isnumeric()]
total = sum(numbers)
percentage = total / len(numbers)
print("Sum is ", total, " and percentage is ", percentage)

s1 = "aaabbbcccdddeee"

count_dict = dict()
for char in s1:
    count = s1.count(char)
    count_dict[char] = count
print(count_dict)


