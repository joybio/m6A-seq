# m6A-seq
#step1
nohup python NEB_RNA.pipeline.py 2>&1 > log &
#step2
nohup sh macs2.sh 2>&1 > macs.log &
#step3
nohup Rscript exomepeak.r 2>&1 > exomepeak.log &
