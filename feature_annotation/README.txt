Annotation v1.0
****************************************************************
IMPORTANT
To run Annotation v1.0 you must install bedtools

Recommended:

before run Annotation v1.0

>which python

and replace #!/bin/miniconda3/bin/python
****************************************************************
USAGE:

Running Annotation v1.0

feature_annotation.py -b "bed" -g "gtf" -o "output1" -d "output2"
output1: feature
output2: distribution

bed format:
1       5561    5840
1       6816    7194
1       30964   31727
1       45323   45699
1       47538   47822
1       50094   50496
1       64173   64599
1       73703   74356
1       89545   89763
1       90312   90578


#before genetype.py
options1：
awk '$3~/gene/' Arabidopsis_thaliana.TAIR10.53.gtf > Arabidopsis_thaliana.TAIR10.53.gene.gtf
awk '{print $10"\t"$NF}' Arabidopsis_thaliana.TAIR10.53.gene.gtf > annotate_rnatype.gtf
sed -i 's/"//g' annotate_rnatype.gtf
sed -i 's/;//g' annotate_rnatype.gtf
options2：
python annotate_build.py -i [gtf] -o annotate_rnatype.gtf -f gene

#
awk '{print $1"\t"$4"\t"$5"\t"$7"\t"$10}' Arabidopsis_thaliana.TAIR10.53.gene.gtf | sort | uniq > Arabidopsis_thaliana.TAIR10.53.gtf.bed
sed -i 's/"//g' Arabidopsis_thaliana.TAIR10.53.gtf.bed
sed -i 's/;//g' Arabidopsis_thaliana.TAIR10.53.gtf.bed

#
intersectBed -a [].narrowPeak.bed -b Arabidopsis_thaliana.TAIR10.53.gtf.bed -wo > [].narrowPeak.gene.bed
genetype.py -b [].narrowPeak.gene.bed -g annotate_rnatype.gtf -o [].gene.type
awk '{print $1"\t"$2"\t"$3"\t"$NF}' [].narrowPeak.gene.type | sort | uniq > uniq.[].narrowPeak.gene.type
awk '{a[$4]++}END{for(i in a)print i"\t"a[i]}' uniq.[].narrowPeak.gene.type > uniq.[].narrowPeak.gene.type.xls
