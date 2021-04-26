#!/bin/python
#hisat2: 3'ligation: FR; dUTP: RF
#fr-secondstrand。意思就是read1在+链，相对的gene也同样在+链上，而read2在+链，相对的gene在-链上。
import os

'''
index1='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACG'
index2='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACCGATGT'
index3='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACTTAGGC'
index4='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACTGACCA'
index5='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACACAGTG'
index6='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGCCAAT'
index7='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACCAGATC'
index8='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACACTTGA'
index9='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGATCAG'
index10='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACTAGCTT'
index11='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGGCTAC'
index12='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACCTTGTA'
index13='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACAGTCAACA'
index14='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACAGTTCCGT'
index15='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACATGTCAGA'
index16='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACCCGTCC'
index18='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGTCCGCAC'
index19='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGTGAAACG'
index20='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGTGGCCTT'
index21='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGTTTCGGA'
index22='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACCGTACGTA'
index23='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGAGTGGAT'
index25='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACACTGATAT'
index27='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACATTCCTTT'

primer5='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGAT'
SR_primer='GATCGTCGGACTGTAGAACTCTGAACGTGTAGAT'

data = open("QC_summary.xls","r")
index_dict = {}
for i in data:
	if i.startswith("Lane"):
		pass
	else:
		i = i.strip().split("\t")
		if i[1].startswith("Undetermined"):
			pass
		else:
			sample = i[1]
			seq = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC" + i[2][:-2]
			index_dict[sample] = seq
data.close()

for i in index_dict.keys():
        index = index_dict[i]
        os.system("cutadapt -a {} -A {} -j 10 -e 0.1 -O 5 -m 50 -o {}.trimmed.R1.fq.gz -p {}.trimmed.R2.fq.gz {}_combined_R1.fastq.gz {}_combined_R2.fastq.gz".format(index,primer5,i,i,i,i))

os.system("mkdir sfastqc_results")
#QC
os.system("ls *.trimmed.R1.fq.gz | while read id; do(mkdir -p sfastqc_results/$(basename $id '.fq.gz');fastqc -o sfastqc_results/$(basename $id '.fq.gz') $id);done")
os.system("ls *.trimmed.R2.fq.gz | while read id; do(mkdir -p sfastqc_results/$(basename $id '.fq.gz');fastqc -o sfastqc_results/$(basename $id '.fq.gz') $id);done")
#multiQC
os.system("multiqc sfastqc_results/ -o multiqc_resluts")
'''
#rRNA
os.system("ls *.fastq.gz | while read id; do(hisat2 -p 20 --pen-noncansplice 1000000 -x /home/l/backup1/refgenome/homo_sapiens/rRNA_tRNA/rRNA_tRNA -U $id -S $(basename $id '.fastq.gz').rRNA.sam); done")
#unmapped
os.system("ls *.rRNA.sam | while read id;do(samtools view -bS -@ 15 -h -f 4 $id > $(basename $id 'sam')unmapped.bam);done")
os.system("ls *.rRNA.unmapped.bam | while read id;do(samtools sort -@ 15 -n -o $(basename $id 'bam')sorted.bam $id);done")
os.system("ls *.unmapped.sorted.bam | while read id;do(bamToFastq -i $id -fq $(basename $id '.rRNA.unmapped.sorted.bam').non_rRNA.fq);done")
#
os.system("rm *.sam")
#map
os.system("ls *.fq | while read id; do(hisat2 -p 20 --pen-noncansplice 1000000 -x /home/l/backup1/refgenome/homo_sapiens/hisat2/GRCh38 -U $id -S $(basename $id '.fq').sam); done")
#sort
os.system("ls *non_rRNA.sam | while read id; do(picard SortSam INPUT=$id OUTPUT=$(basename $id 'sam')coord.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT);done")
#remove dup
os.system("ls *.coord.bam | while read id; do(picard MarkDuplicates REMOVE_DUPLICATES= true  MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=8000 INPUT=$id OUTPUT=$(basename $id 'coord.bam')rmdup.bam METRICS_FILE=$(basename $id '.coord.bam').rmdup.bam.metrics VALIDATION_STRINGENCY=LENIENT -Xmx10G);done")
#stats
os.system("ls *.rmdup.bam | while read id; do(samtools flagstat $id > $(basename $id '.rmdup.bam').txt &); done")
#index
os.system("ls *.rmdup.bam | while read id; do(samtools index $id  &); done")







