#!/bin/bash
#macs2 callpeak -t 24_combined.sort.bam -c input-24_combined.sort.bam -f BAM -n macs2_dup_peaks/24.dup -q 0.05 -g 1.0e8

#macs2 callpeak -t 38_combined.sort.bam -c input-38_combined.sort.bam -f BAM -n macs2_dup_peaks/38.dup -q 0.05 -g 1.0e8

#macs2 callpeak -t Col-0_combined.sort.bam -c input-Col-0_combined.sort.bam -f BAM -n macs2_dup_peaks/Col0-1.dup -q 0.05 -g 1.0e8

#macs2 callpeak -t Col-0_2_combined.sort.bam -c input-Col-0_2_combined.sort.bam -f BAM -n macs2_dup_peaks/Col0-2.dup -q 0.05 -g 1.0e8

#macs2 callpeak -t bam_file/24_combined.sort.bam -c bam_file/Col-0_combined.sort.bam -f BAM -n macs2/24 -q 0.05 -g 1.0e8 &
#macs2 callpeak -t bam_file/38_combined.sort.bam -c bam_file/Col-0_2_combined.sort.bam -f BAM -n macs2/38 -q 0.05 -g 1.0e8 &

macs2 callpeak -m 2 100 -t bam_file/Col-0_2_combined.sort.bam -c bam_file/24_combined.sort.bam -f BAM -n macs2_Col0_mut/24 -q 0.05 -g 1.2e8 &
macs2 callpeak -m 2 100 -t bam_file/Col-0_combined.sort.bam -c bam_file/38_combined.sort.bam -f BAM -n macs2_Col0_mut/38 -q 0.05 -g 1.2e8 &



