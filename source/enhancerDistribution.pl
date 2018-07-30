########################################
# Program to see the distribution of genome-wide predicted enhancers along with other softwares
# Shalu Jhanwar
# 28 May 2015
########################################

#!/usr/bin/perl
use strict;
use warnings;

########################################
#Using in-built perl modules
########################################
use Getopt::Long;
use Cwd 'realpath';

########################################
#Defining prototype for sub-routines
########################################
sub sysRequirement;
sub prtUsage;
sub prtError;
sub commandLine_options;

if(!@ARGV){
	prtUsage();
}

########################################
#Checking systems requirement
########################################
&sysRequirement();
########################################
#Check user defined options
########################################
my $command_line = join (" ", @ARGV);
print "Command used is: perl $0 $command_line\n\n";
my ($enhancerFile,$list,$output_folder) = commandLine_options();
$output_folder=realpath($output_folder);
$list=realpath($list);
$enhancerFile=realpath($enhancerFile);

#Make a temperary dir to process
`mkdir $output_folder/compTemp`;
my $nEnhancer= `wc -l $enhancerFile | cut -d" " -f1`; 
print "Total no. of enhancers are:", $nEnhancer, "\n";

########################################
#Processing of the files
########################################
open(LIST, $list) || die "cant open file";
my $stringOverlap = ""; 
my $flag = 0;
my $sum=0;

while(defined(my $_=<LIST>)){
	chomp($_);
	print "$list\n";
	$flag++;
	my @s=split(/\t/,$_);
	if($flag==1){
		`intersectBed -a $enhancerFile -b $s[0] -wo | cut -f1,2,3 | sort | uniq > $output_folder/compTemp/temp_$s[1]`;
		my $val=`wc -l $output_folder/compTemp/temp_$s[1] | cut -d" " -f1`;
		chomp($val);
		$sum = $sum + $val;
		print "Overlap with $s[1] is $val \n";
		$stringOverlap = $stringOverlap." ".$val;
		`cat $enhancerFile $output_folder/compTemp/temp_$s[1] | sort | uniq -u > $output_folder/compTemp/remainFile.bed`;
		
	}
	else{
		`intersectBed -a $output_folder/compTemp/remainFile.bed -b $s[0] -wo | cut -f1,2,3 | sort | uniq > $output_folder/compTemp/temp_$s[1]`;
		my $val=`wc -l $output_folder/compTemp/temp_$s[1] | cut -d" " -f1`;
		chomp($val);	
		$sum = $sum + $val;	
		print "Overlap with $s[1] is $val \n";
		$stringOverlap = $stringOverlap." ".$val;
		`cat $output_folder/compTemp/remainFile.bed $output_folder/compTemp/temp_$s[1] | sort | uniq -u > $output_folder/compTemp/remain`;
		`mv $output_folder/compTemp/remain $output_folder/compTemp/remainFile.bed`;
	}
}
#Calculate No overlaps
my $header = `cat $list | cut -f2 | tr '\n' '\t' | sed 's/\$/No_overlap/'`;
my $noOverlap = $nEnhancer - $sum;
$stringOverlap = $stringOverlap." ".$noOverlap;
$sum = $sum + $noOverlap;
print "$header", "\n", "$stringOverlap", "\n";
print "The total no. of enhancers are:$sum\n";

#Remove temp_dir
print "$output_folder\n";
exit;

########################################
#Define functions:
########################################
sub commandLine_options{
	my $enhancerFile;
	my $list;
	my $output_folder;
	my $helpUsage;
	$command_line=GetOptions(
			"h|help" => \$helpUsage,
			"eFile|EnhancerFile=s" => \$enhancerFile,
			"l|listFeatureFile=s" => \$list,
			"temp|outDir=s" => \$output_folder,
	);
	if(!defined($output_folder)){
		$output_folder= getcwd(); 
		$output_folder=$output_folder."/outputFolder";
		`mkdir $output_folder`;
	
		
		print "Output dir is not mentioned. So default output directory is $output_folder \(current directory\)\n";
		if(`ls $output_folder | wc -l | cut -d" " -f1` > 0){
			print "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";
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
			print "Output dir does not exist, so creating output directory $output_folder\n";
			`mkdir $output_folder`;
			$output_folder =~ s/$/\//;
		}
		if(`ls $output_folder | wc -l | cut -d" " -f1` > 0){
			print "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";
			print "Warn: $output_folder is not empty, please provide another output folder or rename the existing folder\n";exit;

		}
	}
	if(!$list){
		prtError("Missing: A tab-delimited list with two cloumns (filename, region) of bed files of all the states/regions of software IN THE ORDER OF their preferences\n");
	}
	if(!$enhancerFile){
		prtError("Error: Predicted enhancer file is missing\n");
	}
	if(defined($helpUsage)){
		prtUsage();
	}
	return($enhancerFile,$list,$output_folder);
}


sub sysRequirement{

	my $bedtools=`bedtools`;
	if($bedtools =~ /command not found/){
		prtError("bedtools either not installed or not found in the path");
	}	
	else{
		print "System requirements are fine :)\n";
	}
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

sub prtUsage { # This sub will provide the Usage of the program.
	 print << "HOW_TO";

Description: See the distribution of enhancers within the regions of other softwares
System requirements:
		 bedtools - Assumed it in the path
Usage:
###############################################################################################
	Example:perl enhancerDistribution.pl <Enhancer bed file> <A tab-delimited list with two cloumns (filename, region) of bed files of all the states/regions of software IN THE ORDER OF their preferences> <OutputFolder>
###############################################################################################

### Required parameters:
	--eFile| --EnhancerFile		<A tab delimited file of positive samples containing chrName, start and end>
					
	--l | --listFeatureFile			<A tab delimited file containing 2 columns: i) the name of the files (along with the path) ii) the name of the feature to be displayed>

### Optional parameters:
	--temp | --outDir				<output_folder: All the output files will be saved in the output folder>
						default output folder:current folder/output_folder
	
HOW_TO
print "\n";exit;

}
