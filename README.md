# m6A-seq
#step1: cutadapt, map and remove PCR duplacted reads.
nohup python NEB_RNA.pipeline.py 2>&1 > log &

#step2: call peaks.
nohup sh macs2.sh 2>&1 > macs.log &

#step3: identify differential methylated peaks.
nohup Rscript exomepeak.r 2>&1 > exomepeak.log &
