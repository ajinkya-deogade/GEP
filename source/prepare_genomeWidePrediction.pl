#!/usr/bin/perl
########################################
# Segment whole genome in overlapping windows to identify potentially active enhancers 
# Shalu Jhanwar
# 28 May 2015
########################################
use strict;
use warnings;

########################################
#Using in-built perl modules
########################################
use Getopt::Long;
use Cwd 'realpath';
use Cwd;
use Math::Round;

########################################
#Defining prototype for sub-routines
########################################
sub commandLine_options;
sub sysRequirement;
sub prtUsage;
sub prtError;
sub makeFeatureHash4;
sub roundOff;

my $logFile=getcwd();
my $string="";
open(LOGF,">",$logFile."/error.log") || die "cant open file";

########################################
#Checking systems requirement
########################################
&sysRequirement();

my $installation_path=realpath($0);
$installation_path=~s/\/([^\/]+)$//;
my $command_line = join (" ", @ARGV);
print "Command used is: perl $0 $command_line\n\n";

########################################
#Retrieve user defined options
########################################
my ($bin,$listFeatureFile,$output_folder,$fracOverlap,$gmsize, $tss, $aTSS, $active) = commandLine_options();
my $overlapbinSize = abs($bin/2);
$listFeatureFile=realpath($listFeatureFile);
$gmsize=realpath($gmsize);
$tss = realpath($tss);
$aTSS = realpath($aTSS);
my @activeFiles=split(/\,/,$active);
my $activeFile="";
if(scalar(@activeFiles)>1){
	print LOGF "A Total of ", scalar(@activeFiles), " active files has mentioned as active regions: ";
	
	for my $i(0..$#activeFiles){
		chomp($activeFiles[$i]);
		$activeFiles[$i]=realpath($activeFiles[$i]);
		$activeFile=" ".$activeFiles[$i]." ".$activeFile;
		
	}
	
	print LOGF "$activeFile\n\n";	
		
}
else{
	$activeFile=realpath($activeFiles[0]);
	print LOGF "$activeFile files has mentioned as active regions\n\n";
}

########################################
#Segment whole genome into windows
########################################
`mkdir $output_folder/WholeGenome_temp`;
`bedtools makewindows -g /no_backup/so/sjhanwar/BenchMark_Enhancer/validationFANTOM_H1/chrom.bed -w $bin -s $overlapbinSize > $output_folder/WholeGenome_temp/hg19_bin_genome.bed`;

#Subselect regions of the active regions:
print "Extracting those regions of the genome which will overlap with genome\n";
`cat $activeFile | sortBed -i stdin | mergeBed -i stdin | intersectBed -a $output_folder/WholeGenome_temp/hg19_bin_genome.bed -b stdin -wo | cut -f1,2,3 | sort | uniq > $output_folder/WholeGenome_temp/overlapped_H3K27ac_H3k9ac.bed_genomehg19.bed`;

#Remove Encode predicted promoters from the active dataset:
`awk '{print \$1"\t"\$2-1"\t"\$2"\t.\t.\t"\$3}' $tss |  tail -n +2 | slopBed -i stdin -g $gmsize -l 1000 -r 500 -s | egrep -v "chrY|chrM" > $output_folder/WholeGenome_temp/temp_tss.bed`;
`intersectBed -a $output_folder/WholeGenome_temp/overlapped_H3K27ac_H3k9ac.bed_genomehg19.bed -b $output_folder/WholeGenome_temp/temp_tss.bed -wo | cut -f1,2,3 | sort | uniq > $output_folder/WholeGenome_temp/comm_pro`;
`cat $output_folder/WholeGenome_temp/overlapped_H3K27ac_H3k9ac.bed_genomehg19.bed $output_folder/WholeGenome_temp/comm_pro | sort | uniq -u > $output_folder/WholeGenome_temp/exclude_promoter_overlapped_K27ac_K9ac_genomehg19.bed`;
`awk '{print \$_"\t"1}' $output_folder/WholeGenome_temp/exclude_promoter_overlapped_K27ac_K9ac_genomehg19.bed > $output_folder/WholeGenome_temp/training` ;
`sed -i '2,20s/1\$/0/' $output_folder/WholeGenome_temp/training` ;
print LOGF "Instances creation are finished, now generating training dataset\n";
$string=$string." "."$output_folder/WholeGenome_temp/training";

########################################
#Processing feature files
########################################
open(LIST,"$listFeatureFile") || die "cant open feature list file";
#If format of the files are different

while(defined(my $_=<LIST>)){
	chomp($_);
	my @s=split(/\t/,$_);
	
	#Check if the file is in BigBed format
	if($s[0]=~/\.gz/){
		my $oFile=$s[0];
		$oFile=~s/.gz/.bed/;
		print LOGF "The file is gz format, so uncompress it\n";
		`gunzip -c $s[0] > $oFile`;
		$s[0]=$oFile;
		
	}	 	
	if($s[0]){
		#`intersectBed -a $output_folder/temp/training -b $s[0] -wo -f $fracOverlap | awk -F"\t" '{ if (\$11 != 0) print \$0 }' > $output_folder/temp/temp_$s[1]`;
		print "processing $s[0] file \n";
		`intersectBed -a $output_folder/WholeGenome_temp/training -b $s[0] -wo -f $fracOverlap > $output_folder/WholeGenome_temp/temp_$s[1]`;
	}
	else{
		print "Error: input file does not exist \n";
		exit;
	}
	my %chrHash=();
	my $colNo="";
	my @stat_calculate=();
	
	my $chrHash=makeFeatureHash4("$output_folder/WholeGenome_temp/temp_$s[1]");
	%chrHash = %$chrHash;
	open(I,"$output_folder/WholeGenome_temp/training") || die "can't open file";
	
	open(OUT,">$output_folder/WholeGenome_temp/norm_$s[1]") || die "can't open output file\n";	
	#This will work for both continuous and discrete variable	
	while(defined(my $_=<I>))
	{
		chomp($_);
		$_=~/([^\t]+\t[^\t]+\t[^\t]+)/;
		
		if($chrHash{$1}){
			my @array=@{$chrHash{$1}};
			if(scalar(@array)>1){
				my @sorted_numbers = sort {$a <=> $b} @array;
				print OUT pop(@sorted_numbers),"\n";
			}
			else{
				print OUT $array[0],"\n";
			} 		
		}
		else{
			print OUT 0,"\n";
		}
	}
	close(I);
	$string=$string." "."$output_folder/WholeGenome_temp/norm_$s[1]";
	close(OUT);


}

########################################
#Form training data matrix:
########################################
print LOGF "Files are: $string\n";

`closestBed -a $output_folder/WholeGenome_temp/training -b $aTSS -d -t "first" | cut -f11 > $output_folder/WholeGenome_temp/norm_tss`;
$string=$string." "."$output_folder/WholeGenome_temp/norm_tss";
`paste $string | sed 's/\t/_/' | sed 's/\t/_/' > $output_folder/matrix.txt`;
my $header = `cat $listFeatureFile | cut -f2 | tr '\n' '\t' | sed 's/^/Position\tClass\t/'`;
$header=$header."tss_Dist";
`sed -i '1i$header' $output_folder/matrix.txt`;
exit;

########################################
#Define functions:
########################################
sub makeFeatureHash4(){
	my ($featureTempFile) = $_[0];
	 
	open(FEA,$featureTempFile) || die "cant open file";
	
	my %featureHash = ();
	while(defined(my $_=<FEA>)){
		chomp($_);
		my @split_anno_line=split(/\t/,$_);
		(my $val) = $_=~/([^\t]+)\t[^\t]+$/;
		#if($split_anno_line[0] eq $key){
		my $h_key=$split_anno_line[0]."\t".$split_anno_line[1]."\t".$split_anno_line[2];
		if(!$featureHash{$h_key}){
			my @arr=();
			push(@arr,$val); ##Pushing overlap values in the second last column
			$featureHash{$h_key}=\@arr;
		}
		else{
			push (@{$featureHash{$h_key}}, $val); ##Pushing overlap values in the second last column
		}
	}
	return(\%featureHash);
	close(FEA);
}

sub commandLine_options{
	my $helpUsage;
	my $output_folder;
	my $bin;
	my $listFeatureFile;
	my $fracOverlap;
	my $type;
	my $train;
	my $gmsize;
	my $tss;
	my $gbFile;
	my $aTSS;

	$command_line=GetOptions(
			"h|help" => \$helpUsage,
			"o|outDir=s" => \$output_folder,
			"bin=i" => \$bin,
			"f|fracOverlap=f" => \$fracOverlap,
			"l|listFeatureFile=s" => \$listFeatureFile,
			"gmSize|genomeSizeFile=s" => \$gmsize,
			"tss|tssFile=s" => \$tss,
			"active|activeRegionFiles=s" => \$active,
			"aTSS|allTssFile=s" => \$aTSS,
          );
	
	if(defined($helpUsage)){
		prtUsage();
	}
	if(!defined($output_folder)){
		$output_folder= getcwd(); #Default: current folder to generate all output files
		$output_folder=$output_folder."/outputFolder";
		`mkdir $output_folder`;
	
		open (LOGF, ">error.log");
		print LOGF "Output dir is not mentioned. So default output directory is $output_folder \(current directory\)\n";
		if(`ls $output_folder | wc -l | cut -d" " -f1` > 0){
			print LOGF "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";
			print "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";exit;
			#`rm -rf $output_folder/*`;
		}
	}
	else{ #Check dir exist or not
		$output_folder=realpath($output_folder);
		if(-d $output_folder){
			unless ($output_folder =~ /\/$/){
				$output_folder =~ s/$/\//;
			}
		}
		else{
			print LOGF "Output dir does not exist, so creating output directory $output_folder\n";
			`mkdir $output_folder`;
			$output_folder =~ s/$/\//;
		}
		if(`ls $output_folder | wc -l | cut -d" " -f1` > 0){
			print LOGF "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";
			print "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";exit;
                        #`rm -rf $output_folder/*`;
		}
	}
	$bin=500 if(!defined($bin));
		
	if(!$listFeatureFile){
		prtError("Feature description file is missing");
	}
	
	$fracOverlap=0 if(!$fracOverlap);
	if(!$gmsize){
		prtError("File containing genome size is missing");
	}
	if(!$tss){
		prtError("TSS file is missing");
	}
	if(!$active){
		prtError("Active region file is missing");
	}
	if(!$aTSS){
		prtError("A 6 column file with coding - noncoding TSS file is missing");
	}
	return($bin,$listFeatureFile,$output_folder,$fracOverlap,$gmsize, $tss, $aTSS, $active);
	
}

sub prtError {
	my $msg = $_[0];
	
	print STDERR "+===================================================================================================================+\n";
	printf STDERR "|%-115s|\n", "  Error:";
	printf STDERR "|%-115s|\n", "       $msg";
	print STDERR "+===================================================================================================================+\n";
	prtUsage();
	exit;
}

sub prtUsage{ # This sub will provide the Usage of the program.
	 print << "HOW_TO";

Description: Prepare genome to perform prediction using GEP

System requirements:
		Perl:
		 Module - Cwd
		 bedtools - Assumed it in the path
Usage:

	Example: perl prepare_genomeWidePrediction.pl --l  FeatureFileList --gmSize <ChromosomeSize.txt> --tss <A three column file containing TSS to exclude from genome> --aTSS <A six column bed file containing all coding and non-coding TSS> --active <active histones bedFile> --o <output_folder> <optional parameters>

### Required parameters:
					
	--l | --listFeatureFile			<A tab delimited file containing the name of the files (along with the path) and the name of the feature to be displayed>

	--gmSize | --genomeSizeFile		<A tab delimited file containing chromosome name and its size>
						For Human hg19: Hg19_ChromosomeSize.txt
						For Mouse mm9: mm9_ChromosomeSize.txt

	--tss | --tssFile 			<A three column file containing TSS>

	--active | --activeRegionFiles		<Active region bed files containing three regions: chrName, start and end for the acetylation files. If you have more than one file to be 							considered as active genome region, please mention them in comma seperated manner. For eg. two active files a.bed and b.bed could be 
						mentioned as:"--active a.bed,b.bed">

	--aTSS | --allTssFile			<A six column bed file containing all coding and non-coding TSS>
						Already preprocessed Files provided with the package are:						
						For Mouse mm9: Please mention "Mouse_gencode.vM1_tss_coding_non-coding_6_column.bed" for annotation from gencode.vM1
						For Human hg19: Please mention "Human_gencode.v19_tss_coding_non-coding_6_column.bed" for annotation from gencode.v19

### Optional parameters:	

	--f | --fractionOverlap			<Fraction cut-off of the bin required to overlap with the feature in order to consider the signal in that bin>
						
	--h | --help				<Print help usage>
	
	--o | --outDir				<output_folder: All the output files will be saved in the output folder>
						default output folder:current folder/output_folder

	--bin					<Bin size in bp: default is 500>
	
	This script was last edited on 29th July 2015.

HOW_TO
print "\n";exit;
}

sub sysRequirement{

	my $bedtools=`bedtools`;
	prtError("bedtools either not installed or not found in the path") if($bedtools =~ /command not found/);
	
	eval {
        	require Cwd; #Required for shell and R (and so if("xtable" %in% rownames(installed.packages()) == FALSE) {install.packages("xtable")})
	};
	if($@) {
        	my $errorText = join("", $@);
		prtError("Cwd perl module is not installed; Try to install and run again")if($errorText =~ /Cwd/);
		
	}	
	else{
		print LOGF "System requirements are fine :)\n";
	}
}
  
exit;
	

