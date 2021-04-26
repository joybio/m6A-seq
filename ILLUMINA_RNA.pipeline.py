#!/bin/python
#hisat2: 3'ligation: FR; dUTP: RF
import os

'''
indexD501='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGGCTATA'
indexD502='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTGCCTCTAT'
indexD503='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGGATAGG'
indexD504='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTTCAGAGCC'
indexD505='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTCTTCGCCT'
indexD506='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTTAAGATTA'
indexD507='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTACGTCCTG'
indexD508='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTGTCAGTAC'
indexD701='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACATTACTCG'
indexD702='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACTCCGGAGA'
indexD703='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACCGCTCATT'
indexD704='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACGAGATTCC'
indexD705='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACATTCAGAA'
indexD706='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACGAATTCGT'
indexD707='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACCTGAAGCT'
indexD708='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACTAATGCGC'
indexD709='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACCGGCTATG'
indexD710='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACTCCGCGAA'
indexD711='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACTCTCGCGC'
indexD712='NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCACAGCGATAG'
'''

data = open("QC_summary.xls","r")
index_dict1 = {}
index_dict2 = {}
for i in data:
	if i.startswith("Lane"):
		pass
	else:
		i = i.strip().split("\t")
		if i[1].startswith("Undetermined"):
			pass
		else:
			sample = i[1]
			seq = i[2].split("+")
			# if insert size <150 remain NNN;else:remove NNN 
			index_dict1[sample] = "NNNGATCGGAAGAGCACACGTCTGAACTCCAGTCAC" + seq[0]
			index_dict2[sample] = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT" + seq[1]
data.close()

for i in index_dict1.keys():
	index1 = index_dict1[i]
	index2 = index_dict2[i]
	os.system("cutadapt -a {} -A {} -j 10 -e 0.1 -O 5 -m 50 -o {}.trimmed.R1.fq.gz -p {}.pre_trimmed.R2.fq.gz {}_combined_R1.fastq.gz {}_combined_R2.fastq.gz".format(index1,index2,i,i,i,i))
#remove 3_nt in R2
os.system("ls *.pre_trimmed.R2.fq.gz | while read id;do(trimmomatic SE $id $(basename $id 'pre_trimmed.R2.fq.gz')trimmed.R2.fq.gz HEADCROP:3);done")
os.system("mkdir sfastqc_results")
#QC
os.system("ls *.trimmed.R1.fq.gz | while read id; do(mkdir -p sfastqc_results/$(basename $id '.fq.gz');fastqc -o sfastqc_results/$(basename $id '.fq.gz') $id);done")
os.system("ls *.trimmed.R2.fq.gz | while read id; do(mkdir -p sfastqc_results/$(basename $id '.fq.gz');fastqc -o sfastqc_results/$(basename $id '.fq.gz') $id);done")
#multiQC
os.system("multiqc sfastqc_results/ -o multiqc_resluts")
#map
os.system("ls *.trimmed.R1.fq.gz | while read id; do(hisat2 -p 20 --rna-strandness FR --pen-noncansplice 1000000 -x /home/l/backup1/refgenome/homo_sapiens/hisat2/GRCh38 -1 $id -2 $(basename $id 'trimmed.R1.fq.gz')trimmed.R2.fq.gz -S $(basename $id '.trimmed.R1.fq.gz').sam); done")
#sort
os.system("ls *.sam | while read id; do(picard SortSam INPUT=$id OUTPUT=$(basename $id 'sam')coord.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT);done")
#remove dup
os.system("ls *.coord.bam | while read id; do(picard MarkDuplicates REMOVE_DUPLICATES= true  MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=8000 INPUT=$id OUTPUT=$(basename $id 'coord.bam')rmdup.bam METRICS_FILE=$(basename $id '.coord.bam').rmdup.bam.metrics VALIDATION_STRINGENCY=LENIENT -Xmx10G);done")
#stats
os.system("ls *.rmdup.bam | while read id; do(samtools flagstat $id > $(basename $id '.rmdup.bam').txt &); done")
#index
os.system("ls *.rmdup.bam | while read id; do(samtools index $id &); done")







