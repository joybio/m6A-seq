library(MeTDiff)

GENOME="/home/l/backup1/refgenome/SARS_coro_2/GCF_009858895.2_ASM985889v3_genomic.fa"
TXDB=makeTxDbFromGFF("/home/l/backup1/refgenome/SARS_coro_2/GCF_009858895.2_ASM985889v3_genomic.gff")
GENE_ANNO_GTF="/home/l/backup1/refgenome/SARS_coro_2/GCF_009858895.2_ASM985889v3_genomic.format.gtf"
IN24_1="IN24-1_combined.mapped.h.sorted.p.bam"
IN24_2="IN24-2_combined.mapped.h.sorted.p.bam"
INPUT_BAM=c(IN24_1,IN24_2)
IP24_1="IP24-1_combined.mapped.h.sorted.p.bam"
IP24_2="IP24-2_combined.mapped.h.sorted.p.bam"
IP_BAM=c(IP24_1,IP24_2)
IN48_1="IN48-1_combined.mapped.h.sorted.p.bam"
IN48_2="IN48-2_combined.mapped.h.sorted.p.bam"
TREATED_INPUT_BAM=c(IN48_1,IN48_2)
IP48_1="IP48-1_combined.mapped.h.sorted.p.bam"
IP48_2="IP48-2_combined.mapped.h.sorted.p.bam"
TREATED_IP_BAM=c(IP48_1,IP48_2)

metdiff(INPUT_BAM=INPUT_BAM,IP_BAM=IP_BAM,TREATED_INPUT_BAM=TREATED_INPUT_BAM,TREATED_IP_BAM=TREATED_IP_BAM,GENOME=GENOME,TXDB=TXDB, GENE_ANNO_GTF=GENE_ANNO_GTF,EXPERIMENT_NAME="metdiff_out_48-IP_vs_24-IP",WINDOW_WIDTH=100, SLIDING_STEP=10,FRAGMENT_LENGTH=150,TESTING_MODE=NA,PEAK_CUTOFF_PVALUE=NA,PEAK_CUTOFF_FDR=0.05,FOLD_ENRICHMENT=1)


