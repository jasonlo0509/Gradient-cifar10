import sys

new_data = []
data = open('test.bin',"rb").read()

for i in range(0, len(data), 8):
    new_data.append(data[i:i+8])  # 8 digit binary list
int_data = [] 
for i in new_data:
    int_data.append(int(i,2))  # bytearray will convert decimal to hex
a= bytearray(int_data)

write(a)