import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("ex. 1")
sales_data = pd.read_csv('./sales_data.csv')
total_profit = sales_data['total_profit']
plt.figure(1)
plt.plot(total_profit)
plt.xlabel('months')
plt.ylabel('profit')
#plt.show()

print("ex. 2")
plt.figure(2)
plt.plot(total_profit, label='Total profit for month', color='r', marker='o', markerfacecolor='k', linestyle='-', linewidth=3)
plt.legend()
#plt.show()

print("ex. 3")
products = sales_data.iloc[1:, 1:7]
headers = sales_data.columns
print(products)
plt.figure(3)
lines = plt.plot(products)
plt.legend(lines, headers)
#plt.show()

print("ex. 4")
toothpaste = sales_data['toothpaste']
month = sales_data['month_number']
plt.figure(4)
plt.scatter(month, toothpaste, label='Toothpaste')
plt.legend()
#plt.show()

print("ex. 5")
bathingsoap = sales_data['bathingsoap']
plt.figure(5)
plt.bar(month, bathingsoap, label='Bathing soap')
plt.legend()
plt.savefig('./bathsoap.png')
#plt.show()

print("ex. 6")
plt.figure(6)
plt.hist(total_profit, label='total profit')
plt.legend()
#plt.show()

print("ex. 7")

plt.figure(7)
facewash = sales_data['facewash']
plt.subplot(2,1,1)
plt.plot(bathingsoap, label='bathingsoap')
plt.legend()
plt.subplot(2,1,2)
plt.plot(facewash, label='facewash')
plt.legend()
plt.show()

