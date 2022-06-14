# m6A-seq
#step1: cutadapt, map and remove PCR duplacted reads. Before you fun this python, please make sure that you have replaced the genome index in hisat2.

nohup python NEB_RNA.pipeline.py 2>&1 > log &

#step2: call peaks. caution: -t treated -c control. Before you call peak, please make sure samples are in right group.

nohup sh macs2.sh 2>&1 > macs.log &

#step3: identify differential methylated peaks. you can repace R package exomepeak with MeTDiff (another R package).

nohup Rscript exomepeak.r 2>&1 > exomepeak.log &

#step4: feature_annotation: locate m6A peaks among genome. We separate genome inf six non-overlapping segments: Intergenic, 5'UTRs, start codons (100-nucleotide window centered on the start codon), coding sequences (CDSs), stop codons (100-nucleotide window centered on the stop codon), and 3'UTRs.

feature_annotation.py --help


