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
		help='gtf file:/home/l/backup1/refgenome/Arabidopsis/Arabidopsis_thaliana.TAIR10.41.gtf')

parser.add_option('-o','--out',
		dest='out',
		help='out annotation file')

parser.add_option('-d','--distribution',
		dest='dis',
		help='distribution annotation file')
(options,args) = parser.parse_args()

#generating row_feature_annotate.gtf
'''
iterate through gtf file and return a gtf.bed that contains for every 
genomic position of exon, 5' UTR, 3' UTR, gene
'''
# The following features are used:
# CDS
# intron
# 5' UTR
# 3' UTR
# intergenic
with open("row_feature_annotate.gtf.bed","w") as out:
	with open(options.gtf,'r') as data:
		for i in data:
			if i.startswith("#"):
				pass
			else:
				i=i.strip().split('\t')
				if len(i) < 3:
					pass
				else:
					if i[2] == 'transcript':
						pass
					elif i[2] == 'CDS':
						pass
					elif i[2] == "mRNA":
						pass
					else:
						out.write(i[0] + '\t' + i[3] + '\t' + i[4] +'\t' + i[2] + "\t" + i[6] + '\n')
		data.close()
	out.close()

os.system("intersectBed -a %s -b row_feature_annotate.gtf.bed -wo > temp_step1_feature_annotate.gtf.bed" % (options.bed))

data = open('temp_step1_feature_annotate.gtf.bed','r')
out = open('temp_step2_feature_annotate.gtf.bed','w')
#We divided transcripts into five segments: 5'UTRs, start codons (200-nucleotide window centered on the start codon), coding sequences (CDSs), stop codons (200-nucleotide window centered on the stop codon), and 3'UTRs.
for i in data:
	TYPE = i
	i = i.strip().split("\t")
	L = i[0] + "\t" + i[1] + "\t" + i[2] + '\t' + i[3] + '\t' + i[4] + '\t' + i[5] + '\t' + i[7]
	l = L.strip()
	if re.search("start_codon",TYPE):
		start = int(i[4])
		stop = int(i[5])
		left_border = int(i[1])
		right_border = int(i[2])
		if i[7] == "+":
			if (start - left_border >= 100) and (right_border - stop >= 100):
				out.write(l + "\t"  + "start_codon" + "\n")
			elif (start - left_border) > (right_border - stop):
				out.write(l + "\t"  + "five_prime_utr" + "\n")
			else:
				out.write(l + "\t"  + "exon" + "\n")
		else:
			if (start - left_border <= -100) and (right_border - stop <= -100):
				out.write(l + "\t"  + "start_codon" + "\n")
			elif (start - left_border) < (right_border - stop):
				out.write(l + "\t"  + "exon" + "\n")
			else:
				out.write(l + "\t"  + "five_prime_utr" + "\n")
	elif re.search("stop_codon",TYPE):
		start = int(i[4])
		stop = int(i[5])
		left_border = int(i[1])
		right_border = int(i[2])		
		if i[7] == "+":
			if (start - left_border >= 100) and (right_border - stop >= 100):
				out.write(l + "\t"  + "stop_codon" + "\n")
			elif (start - left_border) > (right_border - stop):
				out.write(l + "\t"  + "three_prime_utr" + "\n")
			else:
				out.write(l + "\t"  + "exon" + "\n")
		else:
			if (start - left_border <= -100) and (right_border - stop <= -100):
				out.write(l + "\t"  + "stop_codon" + "\n")
			elif (start - left_border) < (right_border - stop):
				out.write(l + "\t"  + "exon" + "\n")
			else:
				out.write(l + "\t"  + "three_prime_utr" + "\n")
	else:
		out.write(l + "\t"  + i[6] + "\n")
data.close()
out.close()

temp1_dict = {}
with open('temp_step2_feature_annotate.gtf.bed','r') as f:
	for i in f:
		i = i.strip().split('\t')
		key = str(str(i[0])+','+str(i[1])+','+str(i[2]))
		if key in temp1_dict.keys():
			temp1_dict[key] += '\t' + i[7]
		else:
			temp1_dict[key] = i[7]
	with open('temp_step3_feature_annotate.gtf.bed','w') as fh:
		for i in temp1_dict.keys():
			fh.write(i + '\t' + temp1_dict[i] + '\n')
	fh.close()
f.close()

def prior(TYPE):
	if re.search("start_codon",TYPE):
		return("Start_Codon")
	elif re.search("stop_codon",TYPE):
		return("Stop_Codon")
	elif re.search("three_prime",TYPE):
		return("3'UTR")
	elif re.search("five_prime",TYPE):
		return("5'UTR")
	elif re.search("exon",TYPE):
		return("CDS")
	elif re.search("gene",TYPE):
		return("intron")

data = open(options.bed,'r')
out = open(options.out,'w')
for i in data:
	i = i.strip().split("\t")
	key=str(i[0]) + ',' + str(i[1]) + ',' + str(i[2])
	if key in temp1_dict.keys():
		out.write(key + "\t"  + prior(temp1_dict[key]) + "\n")
	else:
		out.write(key + "\t"  + 'intergenic' + '\n')
data.close()
out.close()

start = 0
stop = 0
UTR3 = 0
UTR5 = 0
intron = 0
intergenic =0
CDS = 0
total = 0
with open(options.out,'r') as f:
	for i in f:
		TYPE = i.strip().split('\t')
		total += 1
		if re.search("Start_Codon",TYPE[1]):
			start += 1
		elif re.search("Stop_Codon",TYPE[1]):
			stop += 1
		elif re.search("3",TYPE[1]):
			UTR3 += 1
		elif re.search("5",TYPE[1]):
			UTR5 += 1
		elif re.search("CDS",TYPE[1]):
			CDS += 1
		elif re.search("intron",TYPE[1]):
			intron += 1
		elif re.search("intergenic",TYPE[1]):
			intergenic += 1
f.close()

with open(options.dis,'w') as data:
	data.write("Type" + '\t' + "number" + "\t" + "percentage" + "\n" \
		+ "Start_codon"+'\t'+str(start)+'\t'+str(round(start,4)/round(total,4))+'\n' \
		+ "Stop_codon" + '\t' + str(stop) + '\t' + str(round(stop,4)/round(total,4)) + '\n' \
		+ "3UTR" + '\t' + str(UTR3) + '\t' + str(round(UTR3,4)/round(total,4)) + '\n' \
		+ "5UTR" + '\t' + str(UTR5) + '\t' + str(round(UTR5,4)/round(total,4)) + '\n' \
		+ "CDS" + '\t' + str(CDS) + '\t' + str(round(CDS,4)/round(total,4)) + '\n' \
		+ "intron" + '\t' + str(intron) + '\t' + str(round(intron,4)/round(total,4)) + '\n' \
		+ "intergenic" + '\t' + str(intergenic) + '\t' + str(round(intergenic,4)/round(total,4)) + "\n")
data.close()

os.system("rm row_feature_annotate.gtf.bed temp_step*")

