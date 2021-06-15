#!/root/miniconda3/bin/python

"""Create a summary that shows the assignment of enrichment peak to annotation features"""

__date__ = "2019-10-2"
__author__ = "Junbo Yang"
__email__ = "yang_junbo_hi@126.com"
__license__ = "PKU.jia.group"

#imports
import re
import os
import optparse
import bisect
#sort  package
from optparse import OptionParser

parser = OptionParser('Usage: %prog ')
parser.add_option('-b','--bed',
                dest='bed',
                help='enrichment peak file in bed format')

parser.add_option('-g','--gtf',
                dest='gtf',
                help='gtf file:/home/l/backup1/refgenome/Arabidopsis/annotate_rnatype.gtf')

parser.add_option('-o','--out',
                dest='out',
                help='out annotation file')
(options,args) = parser.parse_args()

type_dict = {}
data = open(options.bed,"r")
out = open(options.out,"w")
gtf = open(options.gtf,"r")

for i in gtf:
	i = i.strip().split("\t")
	key = i[0]
	value = i[1]
	type_dict[key] = value
gtf.close()

for i in data:
	line = i.strip()
	i = i.strip().split("\t")
	key = i[7]
	out.write(line + "\t" + type_dict[key] + "\n")
data.close()
out.close()


