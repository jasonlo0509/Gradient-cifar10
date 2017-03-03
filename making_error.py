from PIL import Image
import numpy as np
import random
import sys
import struct
import cifar10_eval 
import csv

from matplotlib import pyplot as plt
label=[]
dataset=[]	
err = []
tmp1 = []
Gmap = []
Y = []
def show(im):
	test = im
	test = np.array(test,np.uint8)
	test = test.reshape(3,1024)
	test = test.T
	test = test.reshape(32,32,3)

	plt.figure()
	plt.imshow(test)
	plt.show()

def show_Gmap(im):
	test = im


# return the indexes of the square of size size
def square(size):
#	index of inside area
	inside =[]
	head = (32-size)/2
	head = head*32+head
	for j in range(size):	
		inside = inside+range(head+j*32,head+j*32+size)+range(head+1024+j*32,head+1024+j*32+size)+range(head+2048+j*32,head+2048+j*32+size)
	return inside 	

def addError(ori, err_rate):
	err=ori[:]
	print(len(err))
	inside = square(16)
#	index of outside area
	outside = range(0,3072,1)
	outside = list(set(outside).difference(set(inside)))

#	random error
	err_area = outside		
	ran_bit=random.sample(xrange(len(err_area)*8),len(err_area)*8/err_rate)
	
	for i in ran_bit:
		err[err_area[i/8]] = err[err_area[i/8]] ^ (2**(i%8))
	return err

def Gradient(ori, input):
#	Define a function which is used to produce a map which shows high gradient spots
	tmp = np.array(ori)
	tmp = tmp.reshape(32,32,3)
	print(tmp[0][0][:] , tmp[1][0][:])

	threshold = 100
	Fraq = 0
	
	Y = np.zeros((32,32,3))
	Gmap = np.zeros((32,32))
	print(Gmap)
	while Fraq < 0.5 :
		count = 0
		threshold = threshold-1
		for k in range(3):
			for i in range(32):
				for j in range(32):
					if i==0 and j==0:
						if tmp[i][j][k]-tmp[i+1][j][k] > threshold or tmp[i][j][k]-tmp[i][j+1][k] > threshold or tmp[i][j][k]-tmp[i+1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j+1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1

					elif i==31 and j==0:
						if tmp[i][j][k]-tmp[i-1][j][k] > threshold or tmp[i][j][k]-tmp[i][j+1][k] > threshold or tmp[i][j][k]-tmp[i-1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j+1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
					elif i==0 and j==31:
						if tmp[i][j][k]-tmp[i+1][j][k] > threshold or tmp[i][j][k]-tmp[i][j-1][k] > threshold or tmp[i][j][k]-tmp[i+1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j-1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
					elif i==31 and j==31:
						if tmp[i][j][k]-tmp[i-1][j][k] > threshold or tmp[i][j][k]-tmp[i][j-1][k] > threshold or tmp[i][j][k]-tmp[i-1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j-1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
					elif i==0:
						if tmp[i][j][k]-tmp[i+1][j][k] > threshold or tmp[i][j][k]-tmp[i][j-1][k] > threshold or tmp[i][j][k]-tmp[i][j+1][k] > threshold or tmp[i][j][k]-tmp[i+1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j+1][k] < -threshold or tmp[i][j][k]-tmp[i][j-1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
					elif i==31:
						if tmp[i][j][k]-tmp[i-1][j][k] > threshold or tmp[i][j][k]-tmp[i][j-1][k] > threshold or tmp[i][j][k]-tmp[i][j-1][k] > threshold or tmp[i][j][k]-tmp[i-1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j+1][k] < -threshold or tmp[i][j][k]-tmp[i][j-1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
					elif j==0:
						if tmp[i][j][k]-tmp[i+1][j][k] < -threshold or tmp[i][j][k]-tmp[i+1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j+1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
					elif j==31:
						if tmp[i][j][k]-tmp[i+1][j][k] > threshold or tmp[i-1][j][k]-tmp[i][j][k] > threshold or tmp[i][j][k]-tmp[i][j-1][k] > threshold or tmp[i][j][k]-tmp[i+1][j][k] < -threshold or tmp[i][j][k]-tmp[i-1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j-1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
					else:
						if tmp[i][j][k]-tmp[i-1][j][k] > threshold or tmp[i][j][k]-tmp[i+1][j][k] > threshold or tmp[i][j][k]-tmp[i][j-1][k] > threshold or tmp[i][j][k]-tmp[i][j+1][k] > threshold or tmp[i][j][k]-tmp[i-1][j][k] < -threshold or tmp[i][j][k]-tmp[i+1][j][k] < -threshold or tmp[i][j][k]-tmp[i][j-1][k] < -threshold or tmp[i][j][k]-tmp[i][j+1][k] < -threshold:
							Y[i][j][k] = 255
							Gmap[i][j] = 255
							count += 1
						
		Fraq=count/32/32/3

	'''out = open("test_"+str(input)+".bin","wb")
	
	back = np.array(Gmap,np.uint8)               
	out.write(back)
	out.close()'''
	#out = open("test.bmp","wb")
	#show(Gmap)
	#plt.plot(Gmap)
	#plt.show()
	print(Y)
	print(Gmap)


def main():
#	get all images in format of [r*1024,g*1024,b*1024]
#	store them in dataset[0~9999]
	#save = open("check.csv","w")
	#a=csv.writer(save)
	#bool gradient[:]

	print("END\n")
	f=open("data_batch_1.bin","rb")
	data = f.read()			
	for i in range(len(data)/3073):
		label.append(struct.unpack("B",data[i*3073])[0])
		datatmp = data[i*3073+1:i*3073+3073]
		
		
		dataset.append(list(struct.unpack("B"*(len(datatmp)),datatmp[:])))
		
		
	for k in range(len(dataset)):
		Gradient(dataset[k], k)
	
	f.close()	
#	add error
	for err_rate in range(1,2):
		print (err_rate)	
		
		for k in range(len(dataset)):
			err.append(addError(dataset[k],err_rate))
			#show(dataset[k])

#	show image 	
		
		#	save back
		#out = open("test.bmp","wb")
		for j in range(len(dataset)):
			back=[label[j]]+ list(err[j])
			back = np.array(back,np.uint8)               
			out.write(back)
		out.close()
		#a.writerows([[str(err_rate),str(cifar10_eval.evaluate())]])
		del err[:]
	#save.close()

if __name__ == '__main__':
	main()
