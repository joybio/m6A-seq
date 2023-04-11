setwd("E://多重PCR/20220822/")
library(ggradar)
library(dplyr)
library(ggplot2)

"""
argv <- commandArgs(T)
if (length(argv) != 2 ) {
  cat('\nuseage:\nRscript radar.r JK-173-H1N1-Q-B.homo.blast.dis\n\n')
  q('no')
}
"""
distribution <- read.csv("all_distribution.xls",header = T,row.names = 1,sep="\t")

distribution <- distribution[order(-distribution$JK.173.H1N1.Q.B_number),]
distribution_1 <- distribution[c(1,2,3),]
distribution_2 <- distribution[4:(nrow(distribution)),]
others <- data.frame(c("Others"))
colnames(others) <- "Type"
others$number <- sum(distribution_2$number)
distribution_1 <- subset(distribution_1,select = c("Type","number"))
data<- rbind(distribution_1,others)
data$labels <- data$Type
data$proportion <- round(100 * data$number / sum(data$number),4)
data$label_value <- paste(data$labels," (",data$proportion,"%)",sep = '')
row.names(data) <- data$label_value

distribution_per = subset(data,select = "proportion")
#row.names(distribution_per) <- distribution$
t_distribution_per <- data.frame(t(distribution_per))
t_distribution_per <- round(t_distribution_per*100,2)

distribution_radar=rbind(rep(100,3) , rep(0,3) , t_distribution_per)


pdf("distribution_radar.pdf")
colors_border=c(rgb(0.2,0.5,0.5,0.9), rgb(0.8,0.2,0.5,0.9) , rgb(0.7,0.5,0.1,0.9) )
colors_in=c(rgb(0.2,0.5,0.5,0.4), rgb(0.8,0.2,0.5,0.4) , rgb(0.7,0.5,0.1,0.4) )
radarchart(distribution_radar  , axistype=1 ,
           pcol=colors_border , pfcol=colors_in , plwd=1 , plty=1,
           cglcol="grey", cglty=1, axislabcol="grey", caxislabels=seq(0,1,5), cglwd=0.8,
) 
legend(x=0.8, y=1, legend = rownames(coverage_radar[-c(1,2),]), bty = "n", pch=20 , col=colors_in , text.col = "black", cex=1, pt.cex=2)

#radarchart()函数中，有个参数maxmin默认值是T，意味着，雷达图最大值为第一行，
#最小值为第二行，如果选为F，雷达图就会就会自动判每个因素的最大值和最小值，
#此时雷达图呈现得并不对称（在同一个线上的值并不相等）
dev.off()
