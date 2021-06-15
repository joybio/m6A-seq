library('MeTDiff')
library("GenomicFeatures")
GENOME="/home/l/backup1/refgenome/Arabidopsis/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa"
#TXDB=makeTxDbFromGFF("/home/l/backup1/refgenome/Arabidopsis/Arabidopsis_thaliana.TAIR10.42.gff3")
GENE_ANNO_GTF="/home/l/backup1/refgenome/Arabidopsis/Arabidopsis_thaliana.TAIR10.41.gtf"
col0_INPUT="INPUT-COL-1.sort.rmdup.bam"
col0_2_INPUT="INPUT-COL-2.sort.rmdup.bam"
INPUT_BAM=c(col0_INPUT,col0_2_INPUT)
col0_IP="M6aIP-COL-1.sort.rmdup.bam"
col0_2_IP="M6aIP-COL-2.sort.rmdup.bam"
IP_BAM=c(col0_IP,col0_2_IP)
alk10B_1_INPUT="INPUT-10B-1.sort.rmdup.bam"
alk10B_2_INPUT="INPUT-10B-2.sort.rmdup.bam"
TREATED_INPUT_BAM=c(alk10B_1_INPUT,alk10B_2_INPUT)
alk10B_1_IP="M6aIP-10B-1.sort.rmdup.bam"
alk10B_2_IP="M6aIP-10B-2.sort.rmdup.bam"
TREATED_IP_BAM=c(alk10B_1_IP,alk10B_2_IP)

metdiff(INPUT_BAM=INPUT_BAM,IP_BAM=IP_BAM,TREATED_INPUT_BAM=TREATED_INPUT_BAM,TREATED_IP_BAM=TREATED_IP_BAM,GENOME=GENOME,TXDB=NA, GENE_ANNO_GTF=GENE_ANNO_GTF,EXPERIMENT_NAME="10B_metdiff_out_treat_mut_vs_WT",WINDOW_WIDTH=100, SLIDING_STEP=10,FRAGMENT_LENGTH=150,TESTING_MODE=NA,PEAK_CUTOFF_PVALUE=NA,PEAK_CUTOFF_FDR=0.05,FOLD_ENRICHMENT=1)




