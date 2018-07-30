########################################
# Program to make consistent table for enrichment evidences
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
sub cleanTemp;

my $string="";
my $logFile=getcwd();
open(LOGF,">",$logFile."/Enrichment_error.log") || die "cant open file";

########################################
#Checking systems requirement
########################################
&sysRequirement();

my $installation_path=realpath($0);
$installation_path=~s/\/([^\/]+)$//;

if(!@ARGV){
	prtUsage();
}
my $command_line = join (" ", @ARGV);
print "Command used is: perl $0 $command_line\n\n";

########################################
#Retrieve user defined options
########################################
my ($enhancer,$listFeatureFile,$output_folder) = commandLine_options();
$listFeatureFile=realpath($listFeatureFile);
$output_folder=realpath($output_folder);
$enhancer=realpath($enhancer);
`mkdir $output_folder/temp_hist`;
$string=$string." "."$enhancer";
my $total=`wc -l $enhancer | cut -d" " -f1`;
my $totalFiles=`wc -l $listFeatureFile | cut -d" " -f1`;
$totalFiles=$totalFiles+1;

########################################
#Processing feature file
########################################
open(LIST,"$listFeatureFile") || die "cant open feature list file";
while(defined(my $_=<LIST>)){
	chomp($_);
	my @s=split(/\t/,$_);
	
    #my $comm = `intersectBed -a $enhancer -b $s[0] -wo  | cut -f1,2,3 | sort | uniq | wc -l | cut -d" " -f1`;
	`intersectBed -a $enhancer -b $s[0] -wo  | cut -f1,2,3 | sort | uniq > $output_folder/temp_hist/overlappedEnhancers_$s[1]`;
	
	
	print LOGF "Calculating the enrichment analysis for $s[1]...\n";
	
	my %chrHash=();
	my $colNo="";
	my @stat_calculate=();
	
	my $chrHash=makeFeatureHash4("$output_folder/temp_hist/overlappedEnhancers_$s[1]");
	%chrHash = %$chrHash;
	open(I,"$enhancer") || die "can't open file";
	open(OUT,">$output_folder/temp_hist/val_$s[1]") || die "can't open output file\n";	
	while(defined(my $_=<I>))
	{
		chomp($_);
		$_=~/([^\t]+\t[^\t]+\t[^\t]+)/;
		if($chrHash{$1}){
			print OUT "Yes\n";
		}
		else{
			print OUT "No\n";
		}
	}
	
	close(OUT);
	close(I);
	print LOGF "Instances creation are finished, now generating training dataset\n";
	$string=$string." "."$output_folder/temp_hist/val_$s[1]";
	
}
print LOGF "Files are: $string\n";
`paste $string | sed 's/\t/_/' | sed 's/\t/_/' > $output_folder/votingTable.txt`;

########################################
#Calculate the frequency of the enrichment elements
########################################
my @arr = (0) x $totalFiles;
open(II, "$output_folder/votingTable.txt") || die "can't open output file\n";
open(O,">$output_folder/No_validation_evidence.txt") || die "can't ioen output file\n";
open(H,">$output_folder/HistoFile.txt") || die "can't ioen output file\n";
my $sum=0;
while(defined(my $_=<II>)){
	chomp($_);
	my $count=0;
	
	my @s=split(/\t/,$_);
	
	foreach my $s(@s){
		chomp($s);
		
		if($s eq "Yes"){
				
			$count++;
		}
	}
	$arr[$count]++;
	if($count==0){
		print O "$_\n";
	}	
	$sum=$sum+1;
	$_=~/([^\t]+)/;
	# print "c is $c\n";
	print H $1,"\t",$count,"\n";
}
close(II);
close(O);
close(H);
print LOGF "@arr\n";
print "Total no. of entries are: $sum\n";
my $header = `cat $listFeatureFile | cut -f2 | tr '\n' '\t' `;
`sed -i '1i$header' $output_folder/votingTable.txt`;
print "Cleaning up temp files\n";
cleanTemp("$output_folder/temp_hist");

########################################
#Define functions:
########################################
sub commandLine_options{
	my $helpUsage;
	my $output_folder;
	my $chrSizeFile;
	my $listFeatureFile;
	

	$command_line=GetOptions(
			"h|help" => \$helpUsage,
			"chrSize|chrSizeFile=s" => \$chrSizeFile,
			"o|outDir=s" => \$output_folder,
			"l|listFeatureFile=s" => \$listFeatureFile,
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
			#`rm -rf $output_folder/*`;
		}
	}
	else{ 
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
		
	if(!$listFeatureFile){
		prtError("Feature description file is missing");
	}
	if(!$chrSizeFile){
		prtError("File containing enhancer coordinates is missing");
	}
	return($chrSizeFile,$listFeatureFile,$output_folder);
}
sub makeFeatureHash4(){
	my ($featureTempFile) = $_[0];
	 
	open(FEA,$featureTempFile) || die "cant open file";
	
	my %featureHash = ();
	while(defined(my $_=<FEA>)){
		chomp($_);
		
		if(!$featureHash{$_}){
			$featureHash{$_}=1;
		}
		else{
			print "Error: duplicate values exist:\n";exit;
		}
	}
	return(\%featureHash);
}

sub cleanTemp{
	my $msg = $_[0];
	chomp($msg);
	`rm -rf $msg/*`;
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

Description: Make a comprehensive table for all the enrichment set

System requirements:
		Perl:
		 Module - Cwd
		 bedtools - Assumed it in the path
Usage:

	Example:perl votingScore.pl -chrSize CHROMSIZEFILE.txt -l FeatureFileList <optional parameters>
	
### Required parameters:
	--chrSize | --chrSizeFile		<A tab delimited file containing chrName, start and end>
					
	--l | --listFeatureFile			<A tab delimited file containing the name of the files (along with the path) and the name of the feature to be displayed>
  
### Optional parameters:	

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

