import sys
import numpy as np

def unpickle(file):
    global dict
    import cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict


def main():


	unpickle("batch.bin")
	show(dict)

if __name__ == '__main__':
	main()