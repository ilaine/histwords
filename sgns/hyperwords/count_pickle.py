#!/usr/bin/python
# -*- coding: utf-8 -*-

# usage: python count_pickle.py input_folder

# creates pickled files using cPickle module (necessary for seq_procustes.py)
# input: the name of the folder containing the corpus (already processed with pairs2counts.py)
# output: for each decade, create a pickled count file

import os, sys
import cPickle as pickle

def count_pickle(location):
	""" 
		:param location: name of the folder where the corpus is
		:type location: str
		
		creates a "counts" directory if necessary and a pickled count file for each decade (default: from 1860 to 2000)
	"""
	
	startYear = 1860
	endYear = 2000
	
	if not os.path.exists('%s/counts' % location):
		os.mkdir('%s/counts' % location)
			
	for i in range(startYear,endYear+10,10):

		with open('%s/%s/%s.counts.words.vocab' % (location,str(i),str(i))) as x:
			for line in x:
				items = line.split()
				key, values = items[0], items[1]
				data[key] = values
			
		o = open('%s/counts/%s-counts.pkl' % (location,str(i)), 'wb')
		pickle.dump(data,o)
		
		o.close()

if __name__ == '__main__':

	folder = sys.argv[1]
	
	data = {}
	
	count_pickle(folder)
