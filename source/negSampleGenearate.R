##########################################################################
# Functions for preparing negative samples follwoing the same distribution as positive samples
# Shalu Jhanwar
# 28 May 2015
#########################################################################

###############################################################################
# Input Files
###############################################################################
args<-commandArgs(TRUE)
posEnhancer<-args[1]
genomeFile<-args[2] 
pcFile<-args[3]
tssFile<-args[4]
geneBody<-args[5]
intronFile<-args[6]
gcFile<-args[7]
hcFile<-args[8]
outpath<-args[9]

p300data<-read.table(posEnhancer, sep = '\t', header=F, stringsAsFactors=F)
data<-read.table(genomeFile, sep = '\t', header=F)
set.seed(200)
###############################################################################

###############################################################################
# FUNCTIONS
###############################################################################
###############################################################################
# TSS
###############################################################################

tssFunc <- function(tssfile, pcFile) {
	tss_file<-read.table(tssFile, sep="\t",header=T, stringsAsFactors=F)
	countFile<-read.table(pcFile, sep = '\t', header=F, stringsAsFactors=F)
	k = 1
	final<-c()
	tss_pos<-c()

	for (j in as.vector(data$V1)){
        	excludeVec=c()
		chromVec=c()
        	size<-c()
		cc<-c()
        	df<-p300data[p300data$V1 %in% j,]
		colnames(df)<-c("chr","start","end")
		excludeVec<-as.numeric(unlist(mapply(function(start,end) (start-1000):(end+1000), df$start, df$end)))
		excludeVec<-as.integer(excludeVec)	
        	excludeVec<-unique(excludeVec)
		colnames(tss_file)<-c("Chromosome","Start","end")
		df_tss<-tss_file[tss_file$Chromosome %in% j,]
		chromVec <- df_tss$Start
		chromVec <-chromVec[!chromVec%in%excludeVec]
        	chromVec<-unique(chromVec)
        	sampleVec<-sample(chromVec, countFile$V2[k])
        	temp<-cbind(j,as.numeric(sampleVec)-500, as.numeric(sampleVec))
        	final<-rbind(final,temp)
        	k=k+1      
	}
	final<-as.data.frame(final)
	colnames(final)<-c("chr","start","end")
	return(final)
}

###############################################################################
# Genebody
###############################################################################
gbFunc <- function(factor, fcount){
	gbFile<-read.table(factor, sep="\t",header=F, stringsAsFactors=F)
	countFile<-read.table(fcount, sep = '\t', header=F, stringsAsFactors=F)
	colnames(gbFile)<-c("Chromosome","Start","end")
	k = 1
	final<-c()
	tss_pos<-c()
	for (j in as.vector(data$V1)){
        	excludeVec=c()
        	size<-c()
        	sampleVec<-c()
        	df<-p300data[p300data$V1 %in% j,]
		colnames(df)<-c("chr","start","end")
        	excludeVec<-as.numeric(unlist(mapply(function(start,end) (start-1000):(end+1000), df$start, df$end)))
        	excludeVec<-unique(excludeVec)
        	df_tss<-gbFile[gbFile$Chromosome %in% j,]
        	chromVec <- df_tss$Start
		chromVec <-chromVec[!chromVec%in%excludeVec]
        	chromVec<-unique(chromVec)
        	sampleVec<-sample(chromVec, countFile$V2[k])
        	temp<-cbind(j,as.numeric(sampleVec), as.numeric(sampleVec)+500)
        	final<-rbind(final,temp)
        	k=k+1
	}
	final<-as.data.frame(final)
	colnames(final)<-c("chr","start","end")
	return(final)
}

###############################################################################
# Heterochromatin
###############################################################################
hFunc <- function(hcFile){
	p300data<-read.table(posEnhancer, sep = '\t', header=F, stringsAsFactors=F)
	tss_file<-read.table(tssFile, sep="\t",header=T, stringsAsFactors=F)
	gbFile<-read.table(geneBody, sep="\t",header=F, stringsAsFactors=F)
	inFile<-read.table(intronFile, sep="\t",header=F, stringsAsFactors=F)
	countFile<-read.table(hcFile, sep = '\t', header=F, stringsAsFactors=F)
	k = 1
	final<-c()
	tss_pos<-c()
	for (j in as.vector(data$V1)){
        	excludeVec=c()
		chromVec=c()
		tssexcludeVec=c()
		gbexcludeVec=c()
		inexcludeVec=c()
        	size<-c()
		cc<-c()
		#exclude positive
		df<-p300data[p300data$V1 %in% j,]
		colnames(df)<-c("chr","start","end")
		excludeVec<-as.numeric(unlist(mapply(function(start,end) (start-1000):(end+1000), as.numeric(df$start), as.numeric(df$end))))
		excludeVec<-as.integer(excludeVec)
		#exclude promoter
		colnames(tss_file)<-c("Chromosome","Start","end")	
		df_tss<-tss_file[tss_file$Chromosome %in% j,]
		tssexcludeVec<-as.numeric(unlist(mapply(function(start) (start-1000):(start+1000), as.numeric(df_tss$Start))))
		tssexcludeVec<-as.integer(tssexcludeVec)
		#exclude exon
		colnames(gbFile)<-c("Chromosome","Start","end")
		df_gb<-gbFile[gbFile$Chromosome %in% j,]
		gbexcludeVec<-as.numeric(unlist(mapply(function(start,end) (start-1000):(end+1000), df_gb$Start, df_gb$end)))
		gbexcludeVec<-as.integer(gbexcludeVec)
		#exclude introns
		colnames(inFile)<-c("Chromosome","Start","end")
		df_in<-inFile[inFile$Chromosome %in% j,]
		inexcludeVec<-as.numeric(unlist(mapply(function(start,end) (start-1000):(end+1000), df_in$Start, df_in$end)))
		inexcludeVec<-as.integer(inexcludeVec)
		#chromVec<-chromVec[-excludeVec]
		excludeVec<-c(excludeVec, gbexcludeVec, tssexcludeVec, inexcludeVec)
		excludeVec<-unique(excludeVec)
		chromVec=1:data$V2[k]
		chromVec <-chromVec[!chromVec%in%excludeVec]   
        	sampleVec<-sample(chromVec, countFile$V2[k])
        	temp<-cbind(j,as.numeric(sampleVec)-500, as.numeric(sampleVec))
       	 	final<-rbind(final,temp)
        	k=k+1
	}
	final<-as.data.frame(final)
	colnames(final)<-c("chr","start","end")
	return(final)
}

###############################################################################
# Calling functions
###############################################################################

p_df=tssFunc(tssFile, pcFile)
cat("Total Promoter entries",nrow(p_df),"\n")
outfile<-paste(outpath,"/promoter_neg.txt", sep = "", collapse = NULL)
write.table(file =outfile, sep="\t", quote=F, row.names=F, col.names=F, format(p_df, scientific=FALSE))

e_df=gbFunc(geneBody, gcFile)
cat("Total Promoter entries",nrow(e_df),"\n")
outfile<-paste(outpath,"/genebody_neg.txt", sep = "", collapse = NULL)
write.table(file =outfile, sep="\t", quote=F, row.names=F, col.names=F, format(e_df, scientific=FALSE))

i_df=gbFunc(intronFile, gcFile)
cat("Total Promoter entries",nrow(i_df),"\n")
outfile<-paste(outpath,"/intron_neg.txt", sep = "", collapse = NULL)
write.table(file =outfile, sep="\t", quote=F, row.names=F, col.names=F, format(i_df, scientific=FALSE))

h_df=hFunc(hcFile)
cat("Total Promoter entries",nrow(h_df),"\n")
outfile<-paste(outpath,"/hetero_neg.txt", sep = "", collapse = NULL)
write.table(file =outfile, sep="\t", quote=F, row.names=F, col.names=F, format(h_df, scientific=FALSE))

