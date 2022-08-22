#!/bin/python

"""Create a summary that shows the assignment of enrichment peak to annotation features"""

__date__ = "2022-8-22"
__author__ = "Junbo Yang"
__email__ = "yang_junbo_hi@126.com"

#imports
import re
import os
import optparse
import bisect
#sort  package
from optparse import OptionParser

parser = OptionParser('Usage: %prog ')
parser.add_option('-i','--input',
                dest='input',
                help='input file: gtf file')

parser.add_option('-f','--feature',
                dest='feature',
		default="gene",
		type="str",
                help='feature type: gene or transcript. default: gene')

parser.add_option('-o','--out',
                dest='out',
                help='out annotation file')

(options,args) = parser.parse_args()

import sys
from sys import argv
if len(sys.argv) == 1:
	parser.print_help()
	sys.exit(1)

gtf_file = open(options.input,"r")
output_file = open(options.out,"w")
feature = options.feature
if feature != "gene" and feature != "transcript":
	parser.print_help()
	sys.exit(1)

for i in gtf_file:
	if i.startswith("#"):
		pass
	else:
		line = i
		i = i.strip().split("\t")
		if i[2] == feature:
			pattern_id = feature + '_id'
			pattern_biotype = feature + '_biotype'
			id_pattern = re.compile('{} "(.*?)"'.format(pattern_id))
			biotype_pattern = re.compile('{} "(.*?)";'.format(pattern_biotype))
			#print(id_pattern,biotype_pattern)
			Id = id_pattern.search(line)[1]
			Biotype = biotype_pattern.search(line)[1]
			output_file.write(Id+"\t"+Biotype+'\n')
gtf_file.close()
output_file.close()

