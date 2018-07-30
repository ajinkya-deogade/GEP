##########################################################################
# Plot enhancer size distribution
# Shalu Jhanwar
# 28 May 2015
##########################################################################
args<-commandArgs(TRUE)
data1<-read.table(args[1], sep="\t", header=F)
hist(data1$V1, breaks=200)
mean(data1$V1)
png("size_distribution.png")
hist(data1$V1, xlab="Size of Enhancers (bp)", main="Size distribution of enhancers", breaks=200)
mx<-mean(data1$V1)
abline(v = mx, col = "blue", lwd = 2)
dev.off()
