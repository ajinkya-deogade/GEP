#!/usr/bin/perl
########################################
# Generate a training dataset to be used by the classifiers/clustering methods 
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
my ($chrSizeFile,$listFeatureFile,$output_folder,$fracOverlap,$gmsize,$tss,$aTSS, $gbFile,$inFile) = commandLine_options();
$chrSizeFile=realpath($chrSizeFile);
$listFeatureFile=realpath($listFeatureFile);
$gmsize=realpath($gmsize);
$tss = realpath($tss);
$gbFile = realpath($gbFile);
$inFile = realpath($inFile);
$aTSS = realpath($aTSS);

`mkdir $output_folder/temp`;

########################################
#Generate negative dataset having the same distribution as positive dataset and having following genomic elements as:
	# Non-enhancer cis-regulatory element - 50%
	# GeneBody - 30%
	# Heterochromatin region - 20%
########################################
`cut -f1 $chrSizeFile | sort | uniq -c | awk '{print \$2"\t"\$1}' | sed 's/chrX/chr23/' | sort -nk1.4 | sed 's/chr23/chrX/' |  awk '{print \$1"\t"(\$2*0.5)}'   > $output_folder/temp/t`;
roundOff("$output_folder/temp/t","$output_folder/temp/temp_promoter_count"); #Promoter
`cut -f1 $chrSizeFile | sort | uniq -c | awk '{print \$2"\t"\$1}' | sed 's/chrX/chr23/' | sort -nk1.4 | sed 's/chr23/chrX/' |  awk '{print \$1"\t"(\$2*0.15)}'   > $output_folder/temp/t`;
roundOff("$output_folder/temp/t","$output_folder/temp/temp_gene_count"); #Exon
`cut -f1 $chrSizeFile | sort | uniq -c | awk '{print \$2"\t"\$1}' | sed 's/chrX/chr23/' | sort -nk1.4 | sed 's/chr23/chrX/' |  awk '{print \$1"\t"(\$2*0.2)}'   > $output_folder/temp/t`;
roundOff("$output_folder/temp/t","$output_folder/temp/temp_hetero_count"); #Heterochromatin region

if(-e "$output_folder/temp/temp_promoter_count" && -e "$output_folder/temp/temp_gene_count" && -e "$output_folder/temp/temp_hetero_count" && -e $gbFile && -e $tss && -e $inFile) {
	
	print LOGF "Making negative instances for Promoter, genebody and heterochromatin regions\n\n";
	`Rscript $installation_path/negSampleGenearate.R $chrSizeFile $gmsize $output_folder/temp/temp_promoter_count $tss $gbFile $inFile $output_folder/temp/temp_gene_count $output_folder/temp/temp_hetero_count  $output_folder/temp`;
}
else{
	print "Error:Problem in making negative dataset\n";exit;
}

my $numNeg = `cat $output_folder/temp/*neg.txt | wc -l | cut -d" " -f1 `;
my $numPos = `wc -l $chrSizeFile | cut -d" " -f1 `;

`awk '{print \$_"\t"1}' $chrSizeFile > $output_folder/temp/pos` ;
`awk '{print \$_"\t"0}' $output_folder/temp/*neg.txt > $output_folder/temp/neg` ;

if($numNeg != $numPos){
	my $diff = $numNeg - $numPos;
	print "the difference in the entries between pos and neg is:\n";	
	if($diff > 0){
		`shuf $output_folder/temp/neg | sed '1,$diff d' > $output_folder/temp/negative`;
		`mv $output_folder/temp/negative $output_folder/temp/neg`;
	}
	elsif($diff < 0){
		print "Error: Problem in generating negative dataset. Please check the format of the files\n";
	}
}
	
`cat $output_folder/temp/pos $output_folder/temp/neg > $output_folder/temp/training`;
print LOGF "Instances creation are finished, now generating training dataset\n";
$string=$string." "."$output_folder/temp/training";

########################################
#Processing feature file
########################################
open(LIST,"$listFeatureFile") || die "cant open feature list file";
while(defined(my $_=<LIST>)){
	chomp($_);
	my @s=split(/\t/,$_);
	#Check if the file is in compressed format
	if($s[0]=~/\.gz/){
		my $oFile=$s[0];
		$oFile=~s/.gz/.bed/;
		print LOGF "The file is gz format, so uncompress it\n";
		`gunzip -c $s[0] > $oFile`;
		$s[0]=$oFile;
		
	}	 	
	if($s[0]){
		`intersectBed -a $output_folder/temp/training -b $s[0] -wo -f $fracOverlap > $output_folder/temp/temp_$s[1]`;
	}
	else{
		print "Error: input file does not exist \n";
		exit;
	}
	my %chrHash=();
	my $colNo="";
	my @stat_calculate=();
	my $chrHash=makeFeatureHash4("$output_folder/temp/temp_$s[1]");
	%chrHash = %$chrHash;
	open(I,"$output_folder/temp/training") || die "can't open file";
	open(OUT,">$output_folder/temp/norm_$s[1]") || die "can't open output file\n";	
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
	$string=$string." "."$output_folder/temp/norm_$s[1]";
	close(OUT);
}

`closestBed -a $output_folder/temp/training -b $aTSS -d -t "first" | cut -f11 > $output_folder/temp/norm_tss`;
$string=$string." "."$output_folder/temp/norm_tss";

########################################
#Form training data:
########################################
print LOGF "Files are: $string\n";

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
		my $h_key=$split_anno_line[0]."\t".$split_anno_line[1]."\t".$split_anno_line[2];
		if(!$featureHash{$h_key}){
			my @arr=();
			push(@arr,$val); 
			$featureHash{$h_key}=\@arr;
		}
		else{
			push (@{$featureHash{$h_key}}, $val); 
		}
	}
	return(\%featureHash);
}

sub commandLine_options{
	my $helpUsage;
	my $output_folder;
	my $chrSizeFile;
	my $listFeatureFile;
	my $fracOverlap;
	my $gmsize;
	my $tss;
	my $gbFile;
	my $inFile;
	my $aTSS;

	$command_line=GetOptions(
			"h|help" => \$helpUsage,
			"chrSize|chrSizeFile=s" => \$chrSizeFile,
			"o|outDir=s" => \$output_folder,
			"f|fracOverlap=f" => \$fracOverlap,
			"l|listFeatureFile=s" => \$listFeatureFile,
			"gmSize|genomeSizeFile=s" => \$gmsize,
			"tss|tssFile=s" => \$tss,
			"gbFile|geneBodyFile=s" => \$gbFile,
			"inFile|intronFile=s" => \$inFile,
			"aTSS|allTssFile=s" => \$aTSS,
          );
	
	if(defined($helpUsage)){
		prtUsage();
	}
	if(!defined($output_folder)){
		$output_folder= getcwd(); 
		$output_folder=$output_folder."/outputFolder";
		`mkdir $output_folder`;
	
		open (LOGF, ">error.log");
		print LOGF "Output dir is not mentioned. So default output directory is $output_folder \(current directory\)\n";
		if(`ls $output_folder | wc -l | cut -d" " -f1` > 0){
			print LOGF "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";
			print "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";exit;
		}
	}
	else{ 	#Check dir exist or not
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

		}
	}
	if(!$listFeatureFile){
		prtError("Feature description file is missing");
	}
	if(!$chrSizeFile){
		prtError("File containing enhancer coordinates is missing");
	}
	$fracOverlap=0 if(!$fracOverlap);
	if(!$gmsize){
		prtError("File containing genome size is missing");
	}
	if(!$tss){
		prtError("TSS file is missing");
	}
	if(!$gbFile){
		prtError("GeneBody file is missing");
	}
	if(!$inFile){
		prtError("Intron file is missing");
	}
	if(!$aTSS){
		prtError("A 6 column file with coding - noncoding TSS file is missing");
	}	
	return($chrSizeFile,$listFeatureFile,$output_folder,$fracOverlap, $gmsize, $tss, $aTSS, $gbFile, $inFile);
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

sub roundOff(){
	my ($file) = $_[0]; #Taking chromosome File
	my ($outFile) = $_[1];
	open(O,">$outFile") || die "cant open feature list file";
	open(F,"$file") || die "cant open feature list file";
	while(defined(my $_=<F>)){
		chomp($_);
		my @s=split(/\t/,$_);
		print O "$s[0]\t", round($s[1]),"\n";
			
	}
	close($file);
	close($outFile);

}

sub prtUsage{ # This sub will provide the Usage of the program.
	 print << "HOW_TO";

Description: Form training datatset of positive and negative samples in 1:1 ratio 

System requirements:
		Perl:
		 Module - Cwd
		 bedtools - Assumed it in the path
Usage:
	
	Example:perl buildTrainingData.pl --chrSize <pos_samples.bed> --gmSize <ChromosomeSize.txt> --l FeatureFileList --tss <tssFile> --gbFile <exonBed> --inFile <intronBed> --aTSS <A six column bed file containing all coding and non-coding TSS> <optional parameters>
	

### Required parameters:
	--chrSize | --chrSizeFile		<A tab delimited file of positive samples containing chrName, start and end>
					
	--l | --listFeatureFile			<A tab delimited file containing 2 columns: i) the name of the files (along with the path) ii) the name of the feature to be displayed>

	--gmSize | --genomeSizeFile		<A tab delimited file containing chromosome name and sizes>
						For Human hg19: Hg19_ChromosomeSize.txt
						For Mouse mm9: mm9_ChromosomeSize.txt

	--tss | --tssFile 			<A three column: <chrom><txStart><strand> tab delimited file containing TSS corresponding to protein coding genes>
						For Mouse mm9 gencode.vM1 annotation, please mention: "Mouse_gencode.vM1_tss_coding.bed"
						For Human hg19: Please mention "Human_gencode.v19_tss_coding.bed"

	--gbFile | --geneBodyFile		<A three column bed file containing all the exons information>
						For Human hg19: Human_gencode.v19_exon_Protein_coding.bed

	--inFile | --intronFile			<A three column bed file containing all the introns information>
						For Human hg19: Please mention: Human_gencode.v19_intron_Protein_coding.bed

	--aTSS | --allTssFile			<A six column bed file containing all coding and non-coding TSS>
						Already preprocessed Files provided with the package are:						
						For Mouse mm9: Please mention "Mouse_gencode.vM1_tss_coding_non-coding_6_column.bed" for annotation from gencode.vM1
						For Human hg19: Please mention "Human_gencode.v19_tss_coding_non-coding_6_column.bed" for annotation from gencode.v19
  
### Optional parameters:	

	--f | --fractionOverlap			<Fraction cut-off required to overlap with the feature in order to consider the signal in that bin>

	--h | --help				<Print help usage>
	
	--o | --outDir				<output_folder: All the output files will be saved in the output folder>
						default output folder:current folder/output_folder

											
	This script was last edited on 5th Nov 2015.

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
	

