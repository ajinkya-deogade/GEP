##########################################################################
# Functions for Calculating "Enrichment" p-value using Randomization Test
# Shalu Jhanwar, Jose Davila-Velderrain
# 9 Nov 2015
##########################################################################
# Libraries
###############################################################################
library("GenomicRanges")
###############################################################################

###############################################################################
# Input Files
###############################################################################
args<-commandArgs(TRUE)
Ebed <- args[1] #Enhancer file 
gFile<-args[2] #GenomeFile
FactorBedList<-args[3] #List of all the FactorBeds
outPath<-args[4] #Output path
enrichResultFile=args[5] #File prefix 

###############################################################################
# Creating the output file
###############################################################################
if(file.exists(enrichResultFile)){
    write(paste("File exist"), file = enrichResultFile)
} else{
    file.create(enrichResultFile)
}
enrichResultFile<-paste(outPath,"/",basename(normalizePath(as.character(enrichResultFile))), sep="")

Ebed<-paste(dirname(normalizePath(as.character(Ebed))),"/",basename(normalizePath(as.character(Ebed))), sep="")
FactorBedList<-paste(dirname(normalizePath(as.character(FactorBedList))),"/",basename(normalizePath(as.character(FactorBedList))), sep="")
FactorBedList<-read.table(FactorBedList, header=F, stringsAsFactors=F, sep="\t")
write(paste("Calculating the enrichment of characteristic elements"), file = enrichResultFile, append=TRUE)
bedFile <- read.table(Ebed, header=F, stringsAsFactors=F)
colnames(bedFile) <- c('chr','start','end')
bed <- with(bedFile, GRanges(chr, IRanges(start, end)))
elementMetadata(bed)
genomedata <-read.table(gFile, sep = '\t', header=F, stringsAsFactors=F)
set.seed(200)

###############################################################################
# FUNCTIONS
###############################################################################
Generate.Random.Background <- function(bedInput, bedTableFile, ChromSizes) {
    seqnames <- as.character(unique(bedTableFile$chr))   # get chrom names
    bedTableFile.Chrom.Splited <- split(bedTableFile, bedTableFile$chr)
    N.elements.chrom <- sapply(bedTableFile.Chrom.Splited, nrow)
    Elements.Sizes.chrom <- lapply(bedTableFile.Chrom.Splited, function(i) i$end - i$start)
    
    ChromSizes.ordered <- ChromSizes[match(names(bedTableFile.Chrom.Splited), ChromSizes[,1]), 2]
    
    Random.Initials.Chrom <- lapply(1:length(ChromSizes.ordered), function(i) sample(1:ChromSizes.ordered[i], N.elements.chrom[i]))
    
    Random.Coordinates.L <- lapply(1:length(Random.Initials.Chrom), function(i) as.data.frame(cbind(chr=rep(seqnames[[i]], N.elements.chrom[[i]])  , start=as.numeric(as.character(Random.Initials.Chrom[[i]])), end=as.numeric(as.character(Random.Initials.Chrom[[i]]+ Elements.Sizes.chrom[[i]])))))
    
    Random.Coordinates <- do.call(rbind.data.frame, Random.Coordinates.L)
    Random.Coordinates[,2] <- as.numeric(as.character(Random.Coordinates[,2]))
    Random.Coordinates[,3] <- as.numeric(as.character(Random.Coordinates[,3]))
    
    
    if(sum(Random.Coordinates[,3]<Random.Coordinates[,2])>0) {
       temp.ind <- which(Random.Coordinates[,3]<Random.Coordinates[,2])
       Random.Coordinates[temp.ind,] <- Random.Coordinates[temp.ind, c(1, 3, 2)]
    }

    write.table(Random.Coordinates, file="tempFile", quote=F, sep="\t", row.names=F, col.names=F)
    tempBed <- with(Random.Coordinates, GRanges(chr, IRanges(start, end)))
    return("tempFile")
}

for (i in 1:nrow(FactorBedList)){
    cat("Performing enrichment for ",FactorBedList[i,2], "\n")
    pdfName <-paste(outPath,"/",FactorBedList[i,2],".pdf", sep ="")
    write_table <-paste(outPath,"/",FactorBedList[i,2],".txt", sep = "")
    titleName = paste("Expected null distribution:", FactorBedList[i,2], collapse="")
    
    Factor<-paste(dirname(normalizePath(as.character(FactorBedList[i,1]))),"/",basename(normalizePath(as.character(FactorBedList[i,1]))), sep="")
    data2 <- read.table(Factor, header=F, stringsAsFactors=F)
    colnames(data2) <- c('chr','start','end')
    bed2 <- with(data2, GRanges(chr, IRanges(start, end)))
    #Calculate no. of enhancers
    com=paste("wc -l", Ebed, "| awk '{print $1}'")
    nEnhancer=system(com, intern=TRUE)

    #Calculate bp overlap
    command=paste("intersectBed -a", Ebed, "-b", Factor," -wo | groupBy -i stdin -grp 1,2,3 -c 7 -o max | cut -f4")
    #Observed mean overlap base overlap
    ObsOv <- mean(as.numeric(system(command, intern=TRUE)))
    cat("overlap with the feature", FactorBedList[i,2], "is", ObsOv, "\n")
    #Generate random bp overlap
    #Randomizing enhancer positions
    RandomOvs <- numeric(1000)
    for(i in 1:length(RandomOvs)) {
        Random.Background <- Generate.Random.Background(bedInput=bed, bedTableFile=bedFile, ChromSizes=genomedata)
        cat("Sample", i)
        comRan=paste("intersectBed -a", Random.Background, "-b", Factor," -wo | groupBy -i stdin -grp 1,2,3 -c 7 -o max | cut -f4")
        m <- mean(as.numeric(system(comRan, intern=TRUE)))
	if(is.na(m)){
   		m = 0
   	}
	#RandomOvs[i] <- mean(as.numeric(system(comRan, intern=TRUE)))
	RandomOvs[i] <- m
    }
    #if there is any NA value, replace it with 0
    RandomOvs[is.na(RandomOvs)] <- 0
    write.table(RandomOvs, write_table)
    pdf(pdfName)
    hist(RandomOvs, xlim=c(min(c(RandomOvs, ObsOv)), max(c(RandomOvs, ObsOv))), col="grey", main=titleName, xlab="Mean bp overlap")
    abline(v=ObsOv, col=2, lwd=2)
    dev.off()
}
###############################################################################
