library('exomePeak')
library("GenomicFeatures")
GENOME="/home/l/backup1/refgenome/Arabidopsis/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa"
#TXDB=makeTxDbFromGFF("/home/l/backup1/refgenome/Arabidopsis/Arabidopsis_thaliana.TAIR10.42.gff3")
GENE_ANNO_GTF="/home/l/backup1/refgenome/Arabidopsis/Arabidopsis_thaliana.TAIR10.41.gtf"
col0_INPUT="/home/l/backup1/WCL/201812/bam_file/input-Col-0_combined.sort.bam"
col0_2_INPUT="/home/l/backup1/WCL/201812/bam_file/input-Col-0_2_combined.sort.bam"
INPUT_BAM=c(col0_INPUT,col0_2_INPUT)
col0_IP="/home/l/backup1/WCL/201812/bam_file/Col-0_combined.sort.bam"
col0_2_IP="/home/l/backup1/WCL/201812/bam_file/Col-0_2_combined.sort.bam"
IP_BAM=c(col0_IP,col0_2_IP)
mut24_INPUT="/home/l/backup1/WCL/201812/bam_file/input-24_combined.sort.bam"
mut38_INPUT="/home/l/backup1/WCL/201812/bam_file/input-38_combined.sort.bam"
TREATED_INPUT_BAM=c(mut24_INPUT,mut38_INPUT)
mut24_IP="/home/l/backup1/WCL/201812/bam_file/24_combined.sort.bam"
mut38_IP="/home/l/backup1/WCL/201812/bam_file/38_combined.sort.bam"
TREATED_IP_BAM=c(mut24_IP,mut38_IP)
exomepeak(INPUT_BAM=INPUT_BAM,IP_BAM=IP_BAM,TREATED_INPUT_BAM=TREATED_INPUT_BAM,TREATED_IP_BAM=TREATED_IP_BAM,GENOME=GENOME,UCSC_TABLE_NAME=NA,TXDB=NA, GENE_ANNO_GTF=GENE_ANNO_GTF,EXPERIMENT_NAME="2020.7.7.exomepeak_treat_mut_vs_Col0_p0.05",WINDOW_WIDTH=100, SLIDING_STEP=10,FRAGMENT_LENGTH=150,TESTING_MODE=NA,PEAK_CUTOFF_PVALUE=0.05,PEAK_CUTOFF_FDR=NA,FOLD_ENRICHMENT=1,CONSISTENT_PEAK_CUTOFF_PVALUE=0.05,CONSISTENT_PEAK_FOLD_ENRICHMENT=1)




