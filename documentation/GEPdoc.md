[GEP](index.html#document-index)

-   [Introduction](index.html#document-01_introduction/index)
    -   [Quick-Start](index.html#document-01_introduction/introduction)
-   [Installation](index.html#document-02_installation/index)
    -   [Dependencies](index.html#document-02_installation/sources)
    -   [Installation](index.html#document-02_installation/sources#installation)
-   [GEP functionality](index.html#document-03_how_it_work/index)
    -   [Usage](index.html#document-03_how_it_work/usage)
    -   [Predict only](index.html#document-03_how_it_work/predict_only)
    -   [Train and Predict](index.html#document-03_how_it_work/train_and_predict)
    -   [nFold cross-validation](index.html#document-03_how_it_work/nFold)
    -   [Outputs](index.html#document-03_how_it_work/output)
    -   [Enrichment analysis](index.html#document-03_how_it_work/enrichment_analysis)
    -   [Accessary programs](index.html#document-03_how_it_work/accessary_programs)
-   [Configuration](index.html#document-04_configuration/index)
    -   [FAQ](index.html#document-04_configuration/faq)

 
** [GEP](index.html#document-index)
-   [Docs](index.html#document-index) »
-   [GEP 0.1 documentation]()
-   

------------------------------------------------------------------------

Welcome to GEP documentation![¶](#welcome-to-gep-documentation "Permalink to this headline")
============================================================================================

<span id="document-01_introduction/index"></span>
<span id="introduction-index"></span>
Introduction[¶](#introduction "Permalink to this headline")
-----------------------------------------------------------

For code and examples visit GitHub (Link).

GEP is machine learning based computational tool for genome-wide prediction of active enhancers in various cell-types and tissues. The rationale behind the tool is to learn exclusively from experimentally characterized active enhancers, those epigenomic patterns with discriminatory power by contrasting active enhancers with comparable background genomic regions. Importantly, the genomic background is structured in a balanced way representative of potential, non-enhancer regulatory elements and gene body regions, instead of randomly sampled genomic regions. The Random Forest based model is implemented in Python. The package contains accessary programs required for data processing.

<span id="document-01_introduction/introduction"></span>
<span id="introduction-quickstart"></span>
### Quick-Start[¶](#quick-start "Permalink to this headline")

Quickly identify genome-wide enhancers in a particular cell-type or tissue using GEP. Perform following:

1.  Prepare genomewide prediction (Usage [<span>Prepare genomewide prediction</span>](index.html#howitworks-pgp))

-   Input files:  
    -   List: A file containing list of all the histone marks in the **same order**: Dnase, H3k27ac, H3k27me3, H3k36me3, H3k4me1, H3k4me1\_H3K4me3, H3k4me3, P300. The file contains two columns: name of the file (along with path) and name of the mark. Please refer “example” (link) folder for details.
    -   gmSize: A file containing Chromosome name and size of the chromosomes in tab-delimited manner. For Human and Mouse, the files are provided with the package.
    -   TSS: A file containing coding TSS information in 3 columns: Chr, Position, and Strand. For Human and Mouse, the files are provided with the package.
    -   Acetylation marks: Four columns bed files of active marks (e.g. H3K27ac, H3K9ac etc)
    -   aTSS: A 6 column bed file containing all (coding and non-coding) TSS information. For Human and Mouse, the files are provided with the package (see folder).

-   Run:

        Perl prepare_genomeWidePrediction.pl –l <List> --gmSize <gmSize> --tss <tss> –o <outputFolder> --active <acetylation marks> –aTSS <aTSS>

1.  Perform enhancer prediction (Usage [<span>Predict</span>](index.html#howitworks-predict))

-   Input files:

    > -   output of &lt;prepare\_genomeWidePrediction.pl&gt;: In above example, &lt;outputFolder/matrix.txt&gt;
    > -   Model File: Please see &lt;Git link&gt; folder for the model file. There are 2 models provided. Depending on your data, choose either from below:
    > -   with P300 (Name)
    > -   without P300 (Name)
    > -   Scaler file: Scaler files corresponding to models are provided in &lt;X&gt; folder
    >
-   Run

with P300:

    python genomewidePrediction.py --output-folder <genomewideEnhancers> --feature-columns ”2,3,4,5,6,7,8,9,10” --genome_file <outputFolder/matrix.txt> --model_file <Model.pkl> --scalar_file <Scaler.pkl> --save-file ”genomefile_prediction”

without P300:

    python genomewidePrediction.py --output-folder <genomewideEnhancers> --feature-columns ”2,3,4,5,6,7,8,9” --genome_file <outputFolder/matrix.txt> --model_file <Model_without_P300.pkl> --scalar_file <Scaler_without_P300.pkl> --save-file "genomefile_prediction”

<span id="document-02_installation/index"></span>
<span id="installation-index"></span>
Installation[¶](#installation "Permalink to this headline")
-----------------------------------------------------------

<span id="document-02_installation/sources"></span>
<span id="installation-sources"></span>
### Dependencies[¶](#dependencies "Permalink to this headline")

For successful implementation of the software, please make sure that your system has following:

-   Software

    > -   Bedtools: The tool assumes bedtools in the path. Else You can download the latest version of the bedtools from page: <https://code.google.com/p/bedtools/downloads/list>. After installation, please make sure bedtools is in the path.
    >
-   Python modules:

    > -   Scipy: visit <http://www.scipy.org/install.html>
    > -   Matplotlib: visit <http://matplotlib.org/users/installing.html>
    > -   Numpy: visit <http://docs.scipy.org/doc/numpy/user/install.html>
    > -   Scikit-learn: visit <http://scikit-learn.org/stable/install.html>
    >
-   Perl modules:

    > -   CWD: visit <http://search.cpan.org/~rjbs/PathTools-3.59/Cwd.pm>
    > -   Math::Round visit http://search.cpan.org/dist/Math-Round/Round.pm
    > -   Or install them from CPAN shell: <http://www.twiki.org/cgi-bin/view/TWiki/HowToInstallCpanModules>
    >
-   R library:

    > -   GenomicRanges: visit <https://bioconductor.org/packages/release/bioc/html/GenomicRanges.html>
    >
### Installation[¶](#installation "Permalink to this headline")

1.  GitHub: source archive on this page: <https://github.com/Alignak-monitoring/alignak/releases>

    > Run in a terminal: git colne &lt;http link&gt;
    >
2.  Download from &lt;ftp.//………/GEP.tar.gz&gt;

    > Download it and uncompressed the code as: tar –xvzf GEP.tar.gz
    >
<span id="document-03_how_it_work/index"></span>
<span id="how-it-works-index"></span>
GEP functionality[¶](#gep-functionality "Permalink to this headline")
---------------------------------------------------------------------

<span id="document-03_how_it_work/usage"></span>
<span id="howitworks-usage"></span>
### Usage[¶](#usage "Permalink to this headline")

Help usage of different functionalities of the package is shown here:

<span id="howitworks-fs"></span>
#### Feature selection[¶](#feature-selection "Permalink to this headline")

python featureSelection.py –h

    Usage: featureSelection.py [options]

    Options:
    -h, --help            show this help message and exit
    --data-file=DATA_FILE
                A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-
                delimited features: see example folder for test file
    --output-folder=OUTPUT_FOLDER
                    An output folder: Default is ../output
    --label-column=LABEL_COLUMN
                    Column index containing class of instances: Default: 1 (2nd column)
    --feature-columns=DATA_COLUMNS
                    Column index containing features in data-file
    --plot-bar-without-std=PLOT_BAR_WITHOUT_STD
                    Bar plot without std deviation: Default:on
    --plot-bar-with-std=PLOT_BAR_WITH_STD
                    Bar plot with std deviation: Default:off, provide 1 value to turn on
    --plot-line=PLOT_LINE
                    Line plot: Default off: provide 1 value to turn on
    --n-estimators=N_ESTIMATORS
                    n_estimator: Default=100
    --verbosity=VERBOSITY
                Verbosity: Default on: provide 0 to turn off

<span id="howitworks-predict"></span>
#### Predict[¶](#predict "Permalink to this headline")

python genomewidePrediction.py –h

    Usage: genomewidePrediction.py [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --save-file <output-filename> --n-estimators <value> --max-depth <value>]

    Options:
    -h, --help            show this help message and exit
    --output-folder=OUTPUT_FOLDER
                    An output folder: Default is ../output
    --feature-columns=DATA_COLUMNS
                      Column index containing features in data-file
    --fold-cross-validation=FOLD_CROSS_VALIDATION
                            n-fold: Default:10
    --save-file=SAVE_FILE
                            Output filename: Deafult: output_file
    --n-jobs=N_JOBS         No. of CPUs <value>
    --genome_file=GENOME_FILE
                            Genome-wide file: 1st column as rownames and additional columns as tab-delimite features: see example folder for test file
    --model_file=MODEL_FILE
                            A file containing model
    --scaler_file=SCALER_FILE
                            A file containing scaled training data in pkl format:
                            see example folder for help
    --verbosity=VERBOSITY
                            Verbosity: Default on: provide 0 to turn off

<span id="howitworks-tapg"></span>
#### Train and Predict GEP[¶](#train-and-predict-gep "Permalink to this headline")

python trainAndPredictGEP.py –h

    Usage: trainAndPredictGEP.py [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --percent-test-size <float> --save-file <output-filename> --n-estimators <value> --max-depth-start <value> --max-depth-end <value>--n-jobs <int>]

    Options:
    -h, --help            show this help message and exit
    --data-file=DATA_FILE
                    A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features: see example folder for test file
    --output-folder=OUTPUT_FOLDER
                    An output folder: Default is ../output
    --label-column=LABEL_COLUMN
                    Column index containing class of instances: Default: 1 (2nd column)
    --feature-columns=DATA_COLUMNS
                    Column index containing features in data-file
    --percent-test-size=PERCENT_TEST_SIZE
                        Size of the test dataset in percentage: Default: 20
    --fold-cross-validation=FOLD_CROSS_VALIDATION
                            n-fold: Default:10
    --save-file=SAVE_FILE
                Output filename: Deafult: output_file
    --n-estimators=N_ESTIMATORS
                    n_estimator list: Default: [10, 100, 1000]
    --max-depth-start=MAX_DEPTH_START
                    max-depth start: Default:5
    --max-depth-end=MAX_DEPTH_END
                    max-depth end: Default: 10
    --n-jobs=N_JOBS       no. of cores: Default:1
    --verbosity=VERBOSITY
                Verbosity: Default on: provide 0 to turn off

<span id="howitworks-taps"></span>
#### Train and Predict SVM[¶](#train-and-predict-svm "Permalink to this headline")

python trainAndPredictSVM.py –h

    Usage: trainAndPredictSVM.py [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --percent-test-size <float> --save-file <output-filename> --n-estimators <value> --max-depth-start <value> --max-depth-end <value>--n-jobs <int>]

    Options:
    -h, --help            show this help message and exit
    --data-file=DATA_FILE
                    A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features: see example folder for test file
    --output-folder=OUTPUT_FOLDER
                    An output folder: Default is ../output
    --label-column=LABEL_COLUMN
                    Column index containing class of instances: Default: 1 (2nd column)
    --feature-columns=DATA_COLUMNS
                    Column index containing features in data-file
    --percent-test-size=PERCENT_TEST_SIZE
                    Size of the test dataset in percentage: Default: 20
    --fold-cross-validation=FOLD_CROSS_VALIDATION
                    n-fold: Default:10
    --save-file=SAVE_FILE
                Output filename: Deafult: output_file
    --SVM_C_min=SVM_C_MIN
                C <power of 10>: Default: -2 == 0.01
    --SVM_C_max=SVM_C_MAX
                C <power of 10>: Default: 9 == 1000000000.0
    --SVM_gamma_min=SVM_GAMMA_MIN
                gamma: <power of 10> default: -4 == 0.0001
    --SVM_gamma_max=SVM_GAMMA_MAX
                gamma: <power of 10> default: 5 == 100000.0
    --n-jobs=N_JOBS       no. of CPUs: Default:10
    --verbosity=VERBOSITY
                Verbosity: Default on: provide 0 to turn off

<span id="howitworks-nf"></span>
#### n-fold cross-validation[¶](#n-fold-cross-validation "Permalink to this headline")

python crossValidation.py –h

    Usage:

    python crossValidation.py [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --save-file <output-filename> --n-estimators <value> --max-depth <value>]

    Options:
    -h, --help            show this help message and exit
    --data-file=DATA_FILE
                    A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features: see example folder for test file
    --output-folder=OUTPUT_FOLDER
                    An output folder: Default is ../output
    --label-column=LABEL_COLUMN
                    Column index containing class of instances: Default: 1 (2nd column)
    --feature-columns=DATA_COLUMNS
                    Column index containing features in data-file
    --fold-cross-validation=FOLD_CROSS_VALIDATION
                    n-fold: Default:10
    --save-file=SAVE_FILE
                    Output filename: Deafult: output_file
    --RF_n-estimators=RF_N_ESTIMATORS
                    RF_n_estimator list: Default: 100
    --RF_max-depth=RF_MAX_DEPTH
                    RF_max_depth=<value>: Default:5
    --n-jobs=N_JOBS       no. of cores: Default:10
    --SVM_C=SVM_C         SVM_C <power of 10>: Default: 8 == 100000000.0
    --SVM_gamma=SVM_GAMMA
                SVM_gamma: <power of 10> default: -2 == 0.01
    --method=METHOD       Method: 'RF': Random Forest, 'SVM': Support Vector
                            Machine: Default: RF
    --verbosity=VERBOSITY
                    Verbosity: Default on: provide 0 to turn off

<span id="howitworks-pgp"></span>
#### Prepare genomewide prediction[¶](#prepare-genomewide-prediction "Permalink to this headline")

perl prepare\_genomeWidePrediction.pl –h

    Description: Prepare genome to perform prediction using GEP
    System requirements:
    Perl:
    Module - Cwd
    bedtools - Assumed it in the path

    Usage:

    perl prepare_genomeWidePrediction.pl --l  FeatureFileList --gmSize <ChromosomeSize.txt> --tss <A three column file containing TSS to exclude from genome> --aTSS <A six column bed file containing all coding and non-coding TSS> --active <active histones bedFile> --o <output_folder> <optional parameters>

    ### Required parameters:

    --l | --listFeatureFile                     <A tab delimited file containing the name of the files (along with the path) and the name of the feature to be displayed>

    --gmSize | --genomeSizeFile         <A tab delimited file containing chromosome name and its size>
    For Human hg19: Hg19_ChromosomeSize.txt
    For Mouse mm9: mm9_ChromosomeSize.txt

    --tss | --tssFile                   <A three column file containing TSS>

    --active | --activeRegionFiles              <Active region bed files containing three regions: chrName, start and end

    --aTSS | --allTssFile                       <A six column bed file containing all coding and non-coding TSS>
                                    For Mouse mm9: Please mention "Mouse_gencode.vM1_tss_coding_non-coding_6_column.bed" for annotation from gencode.vM1
                                    For Human hg19: Please mention "Human_gencode.v19_tss_coding_non-coding_6_column.bed" for annotation from gencode.v19

    ### Optional parameters:

    --f | --fractionOverlap                     <Fraction cut-off of the bin required to overlap with the feature in order to consider the signal in that bin>

    --h | --help                                <Print help usage>

    --o | --outDir                              <output_folder: All the output files will be saved in the output folder>
                                default output folder:current folder/output_folder

    --bin                                       <Bin size in bp: default is 500>


    This script was last edited on 29th July 2015.

<span id="howitworks-pt"></span>
#### Prepare training[¶](#prepare-training "Permalink to this headline")

perl buildTrainingData.pl –h

    Description: Form training datatset of positive and negative samples in 1:1 ratio

    System requirements:
    Perl:
    Module - Cwd
    bedtools - Assumed it in the path

    Usage:
    perl buildTrainingData.pl --chrSize <pos_samples.bed> --gmSize <ChromosomeSize.txt> --l FeatureFileList --tss <tssFile> --gbFile <exonBed> --inFile <intronBed> --aTSS <A six column bed file containing all coding and non-coding TSS> <optional parameters>


    ### Required parameters:
    --chrSize | --chrSizeFile           <A tab delimited file of positive samples containing chrName, start and end>

    --l | --listFeatureFile                     <A tab delimited file containing 2 columns: i) the name of the files (along             with the path) ii) the name of the feature to be displayed>

    --gmSize | --genomeSizeFile         <A tab delimited file containing chromosome name and sizes>
                                    For Human hg19: Hg19_ChromosomeSize.txt
                                    For Mouse mm9: mm9_ChromosomeSize.txt

    --tss | --tssFile               <A three column: <chrom><txStart><strand> tab delimited file containing TSS
                                    corresponding to protein coding genes>
                                        For Mouse mm9 gencode.vM1 annotation, please mention: "Mouse_gencode.vM1_tss_coding.bed"
                                        For Human hg19: Please mention "Human_gencode.v19_tss_coding.bed"

    --gbFile | --geneBodyFile           <A three column bed file containing all the exons information>
                                    For Human hg19: Human_gencode.v19_exon_Protein_coding.bed

    --inFile | --intronFile                     <A three column bed file containing all the introns information>
                                    For Human hg19: Please mention: Human_gencode.v19_intron_Protein_coding.bed

    --aTSS | --allTssFile                       <A six column bed file containing all coding and non-coding TSS>
                                    Already preprocessed Files provided with the package are:
                                    For Mouse mm9: Please mention "Mouse_gencode.vM1_tss_coding_non-coding_6_column.bed" for annotation from gencode.vM1
                                    For Human hg19: Please mention "Human_gencode.v19_tss_coding_non-coding_6_column.bed" for annotation from gencode.v19

    ### Optional parameters:

    --f | --fractionOverlap                     <Fraction cut-off of the bin required to overlap with the feature in order to consider the signal in that bin>

    --h | --help                                <Print help usage>

    --o | --outDir                              <output_folder: All the output files will be saved in the output folder>
                                default output folder:current folder/output_folder


    This script was last edited on 5th Nov 2015.

<span id="document-03_how_it_work/predict_only"></span>
<span id="howitworks-predict-only"></span>
### Predict only[¶](#predict-only "Permalink to this headline")

Identify potential enhancers in any cell-type/tissue using already trained models (K562 and HepG2) priovided in the pacakge. Visit [<span>Quick-Start</span>](index.html#introduction-quickstart)

#### OutPut[¶](#output "Permalink to this headline")

Visit [<span>Predict</span>](index.html#howitworks-o-predict)

<span id="document-03_how_it_work/train_and_predict"></span>
<span id="howitworks-train-and-predict"></span>
### Train and Predict[¶](#train-and-predict "Permalink to this headline")

In machine-learning(ML)approaches, the outcome largely depends on the training. In case of an appropriate training dataset availability, it might be worth to perform predictions with a newly trained model. For that purpose, you need to first build a trianing dataset and train the model.

#### Train[¶](#train "Permalink to this headline")

Perform following:

1.  Generate training dataset (Usage [<span>Prepare training</span>](index.html#howitworks-pt)):  
    The training dataset comprised of 2 classes: Positive classes as enhancers (provided by you) and negative classes which contain different genomic regions as promoter, gene-body and heterochromatin in 5:3:2 ratio approximately. Following are the input files required:

-   Necessary files

    > -   Positive samples: A 3 column bed file containing positive samples (Enhancers)
    > -   List: A text file containing a list of all the feature files and names (see XX folder for an example: Link to Gitfolder)
    > -   Chromosome: A two column tab-delimited file with Chr and sizes
    > -   TSS: A three column tab-delimited coding TSS file with Chr, Pos, Strand
    > -   Exon: A three-column exon bed file
    > -   Intron: A three-column intron bed file
    > -   aTSS: A six column bedfile with all (coding and non-coding TSS)
    >
    > Note:
    >
    >     For Human (hg19) and mouse (mm9), refer (link to the folder) for Chromosome, TSS, aTSS files.
    >     For Human (hg19), intron and exon files are provided (link to the folder)
    >
-   Build trining data:

        Perl buildTrainingData.pl –chrSize <positive_samples.txt> --l <list.txt> --gmSize  <Chromosome_sizes.txt> --tss <tssFile> --gbFile <exon.bed> –inFile <intron.bed> --o <outputFolder> --aTSS <All TSS file>

-   Visit [<span>Prepare training</span>](index.html#howitworks-o-pt) for output

1.  Building model (Usage [<span>Train and Predict GEP</span>](index.html#howitworks-tapg))

Build a model on your own trainign data using GEP. Provide more number of cores to enable parallel processing.

-   Necessary files

    > -   Output of &lt;buildTrainingData.pl&gt;: In above example, &lt;outfolder/matrix.txt&gt; file
    > -   feature column index: index of the feature columns in &lt;outfolder/matrix.txt&gt; file
    > -   label column: index of label column in &lt;outfolder/matrix.txt&gt; file
    > -   Optional params
    >
Run:

    python trainAndPredictGEP.py --data-file <outfolder/matrix.txt> --output-folder outputFolder --feature-columns “<comma separated column indices>” --label-column <label column index> --percent-test-size <float value> --fold-cross-validation <int> --save-file “<filename>” --n-estimators "<comma separated n-estimators for optimization>" --max-depth-start <int> --max-depth-end <int> --n-jobs <int> --verbosity <binary value>

Note:

    Training can be performed using SVM classifier. See :ref:`howitworks/tapS`

-   Visit [<span>Train and Predict GEP</span>](index.html#howitworks-o-tapg) for output

#### Predict[¶](#predict "Permalink to this headline")

Perform prediction on the new model in the simialr way as using in-built models. Visit [<span>Quick-Start</span>](index.html#introduction-quickstart)

-   Visit [<span>Predict</span>](index.html#howitworks-o-predict) for output

<span id="document-03_how_it_work/nFold"></span>
<span id="howitworks-n-fold"></span>
### nFold cross-validation[¶](#nfold-cross-validation "Permalink to this headline")

cross validation is one of the model validation technique. It assess the generalizability of the model on an independent dataset. GEP provides utility to performs n-fold cross-validation on the entire dataset and obtain different statistic measures such as f-measures, accuracy, precision and recall. Additionally it also provides the measures corresponding to random classification.

#### Usage[¶](#usage "Permalink to this headline")

Visit [<span>n-fold cross-validation</span>](index.html#howitworks-nf) for Usage

Run the following command on your own training data or in-built training data:

    python nFold_CrossValidation_measures.py --data-file <training data> --output-folder <outFolder> --feature-columns <"comma separated column indices"> --label-column <"label column index"> --fold-cross-validation <int> --save-file <"file-prefix"> --method <classifier>

#### Output[¶](#output "Permalink to this headline")

Visit [<span>n-fold cross-validation</span>](index.html#howitworks-o-nf) for output

<span id="document-03_how_it_work/output"></span>
<span id="howitworks-output"></span>
### Outputs[¶](#outputs "Permalink to this headline")

Output provided by various functionality is shown here:

<span id="howitworks-o-fs"></span>
#### Feature selection[¶](#feature-selection "Permalink to this headline")

python featureSelection.py

-   It provides the relative importance of the features provided by GEP on the command prompt
-   Based on the options chosen, it also shows the relative importance of the features as bar or line graph with or without variance. (see example folder link)

<span id="howitworks-o-predict"></span>
#### Predict[¶](#predict "Permalink to this headline")

python genomewidePrediction.py

-   Provides the statistics on the command prompt

-   Predicted enhancer positions (.txt): There are four columns corresponding to “chr”, “start”, “End”, “Confidence”

-   UCSC browser file: A file (.bed) to upload on UCSC browser (default: hg19 assembly). Once uploaded in the browser, the colour corresponds to the confidence of prediction (dark blue - high confidence)

    > Note:: If you are working on other species, please change within the UCSC browser file on 2nd line. Change db = hg19 to db = “your species”). For e.g. if you are working with mouse mm9, then write in the file db = “mm9”
    >
<span id="howitworks-o-tapg"></span>
#### Train and Predict GEP[¶](#train-and-predict-gep "Permalink to this headline")

python trainAndPredictGEP.py

-   Provides best parameters and classification report with machine-learning measures (precision, recall, F-measure) on the command prompt
-   Learning\_Curve: A learning curve represents training and validation score for different numbers of training samples. This is used to determine if the model can be benefitted on addition of more no. of samples.
-   Model: Trained model on your training data
-   ROC(Receiver Operating Characteristic) Curve: ROC curve obtained on the test dataset using the trained model
-   Scaler: A scalar storing the statistics of traning data

<span id="howitworks-o-taps"></span>
#### Train and Predict SVM[¶](#train-and-predict-svm "Permalink to this headline")

python trainAndPredictSVM.py

-   Provides best parameters and classification report with machine-learning measures (precision, recall, F-measure) on the command prompt
-   Learning\_Curve: A learning curve represents training and validation score for different numbers of training samples. This is used to determine if the model can be benefitted on addition of more no. of samples.
-   Model: Trained SVM model on your training data
-   ROC(Receiver Operating Characteristic) Curve: ROC curve obtained on the test dataset using the trained model
-   Scaler: A scalar storing the statistics of traning data

<span id="howitworks-o-nf"></span>
#### n-fold cross-validation[¶](#n-fold-cross-validation "Permalink to this headline")

python crossValidation.py

-   Measures (.txt): A txt file with machine-learning measures (accuracy, precision, recall, F-measure) corresponding to random and true classification at each fold. It also provides average measures of all the folds
-   ROC(Receiver Operating Characteristic) Curve

<span id="howitworks-o-pgp"></span>
#### Prepare genomewide prediction[¶](#prepare-genomewide-prediction "Permalink to this headline")

perl prepare\_genomeWidePrediction.pl

-   matix.txt: A 2D matrix with features as columns (same order as training data) and samples as row

<span id="howitworks-o-pt"></span>
#### Prepare training[¶](#prepare-training "Permalink to this headline")

perl buildTrainingData.pl

-   matix.txt: A 2D matrix with features as columns samples as row. You can use this file as input during model building step

<span id="howitworks-o-pes"></span>
#### Plot size distribution[¶](#plot-size-distribution "Permalink to this headline")

Rscript plot\_size\_distribution.R &lt;size\_file.txt&gt;

-   histogram of the size of enhancers

<span id="howitworks-o-ed"></span>
#### Comparison with other enhancer set[¶](#comparison-with-other-enhancer-set "Permalink to this headline")

perl enhancerDistribution.pl –eFile &lt;enhancer bedFile&gt; –l &lt;list (a tab-delimited file with fileName and name of the states)&gt; –temp &lt;tempDir&gt;

-   It provides the no. of enhancers overlapped with different regions provided by the user

<span id="howitworks-o-calml"></span>
#### Calculate ML measures[¶](#calculate-ml-measures "Permalink to this headline")

python calculateML\_measures.py

> It provides different measures (e.g. Recall, Precision, F-measure, PPV, Methiew correlation coefficient etc) on stdout

<span id="howitworks-o-vt"></span>
#### Validation dataset[¶](#validation-dataset "Permalink to this headline")

python validationTestSet.py –output-folder &lt;outFolder&gt; –label-column &lt;”class indices”&gt; –feature-columns &lt;”feature indices”&gt; –test\_file “test\_file.txt” –model\_file &lt;ModelFile&gt; –scaler\_file &lt;ScalerFile&gt; –save-file “File Prefix” –verbosity 1

-   It provides ML measures obtained on the test dataset on application of the model on stdout
-   ROC curve

<span id="howitworks-o-ea"></span>
#### Enrichment analysis[¶](#enrichment-analysis "Permalink to this headline")

perl votingScore.pl

> -   HistoFile.txt: This gives the no. of characteristic element supporting each enhancer
> -   votingTable.txt: Presence or absence of each element corrosponding to enhancers in tabular format
> -   No\_validation\_evidence.txt: An additional table corresponding to enhancers not supported by any element
>
Enrichment test

Rscript enrichmentAnalysis.R &lt;enhancer bedFile&gt; &lt;gFile&gt; &lt;list&gt; &lt;outputFolder&gt; &lt;outFileName&gt;

-   .txt: It will generate a .txt file corresponding to each factor containing means of random overlap
-   .pdf: It will generate a .pdf file showing the distribution of means of random overlaps

<span id="document-03_how_it_work/enrichment_analysis"></span>
<span id="howitworks-enrichment"></span>
### Enrichment analysis[¶](#enrichment-analysis "Permalink to this headline")

There are certain characteristic elements associative to active enhancers such as: open-chromatin, few histone modifications, 3D-interaction data and experimental evidances etc. In order to provide support for potential regulatory activity of these in-silico predicted enahncers using GEP, we propose enrichment of these elements in predicted enhancers.

#### Overlap with enhancers[¶](#overlap-with-enhancers "Permalink to this headline")

See the overlap of characteristic elements with predicted enhancers.

> -   Necessary files
>
>     > -   Enhancer bed-file: A three column bed file
>     > -   List: A list containing file path and name of the characteristic elements
>     > -   outputFolder
>     >
> Run:
>
>     perl votingScore.pl --chrSize <enhancer bedFile> --l <list> --o <outFolder>
>
#### Enrichment test[¶](#enrichment-test "Permalink to this headline")

To see the significance of the overlap, we propose a enrichment test. In this test, we consider estimating the distribution of base pair overlap in randomized genomes 1000 times. If the P-value is less than 0.05, we consider the enrichment of characteristic element as “significant” in enhancers.

> -   Necessary files
>
>     > -   Enhancer bed-file
>     > -   gFile: A tab-delimited file with Chromosome and size
>     > -   List: A list containing file path and name of the characteristic elements
>     > -   outputFolder
>     > -   outFileName
>     >
> Run:
>
>     Rscript enrichmentAnalysis.R <enhancer bedFile> <gFile> <list> <outputFolder> <outFileName>
>
#### Output[¶](#output "Permalink to this headline")

Visit [<span>Enrichment analysis</span>](index.html#howitworks-o-ea) for output

<span id="document-03_how_it_work/accessary_programs"></span>
<span id="howitworks-accessary-programs"></span>
### Accessary programs[¶](#accessary-programs "Permalink to this headline")

There are few accessary programs provided along with the package which might be helpful during the analysis of enhancers.

-   Plot size distribution of enhancers:

        Rscript plot_size_distribution.R <size_file.txt>

        It provides histogram of sizes

-   Enhancer distribution: see the distribution of enhancers within different states provided by other softwares (e.g.: ChromHMM)

        perl enhancerDistribution.pl --eFile <enhancer bedFile> --l <list (a tab-delimited file with fileName and name of the states)> --temp <tempDir>

Overlaps with different categories will be shown on stdout

-   Calculate ML measures: If you have predictions from different softwares on the same dataset and you want to compare ML measures provided by each of them, use

python calculateML\_measures.py –data-file &lt;dataFile&gt; –label-column &lt;label indice&gt; where, datafile is a 2D matrix with Name, class and features columns

Note: see example folder (Link). Visit [<span>Calculate ML measures</span>](index.html#howitworks-o-calml) for output

-   validationTestSet.py: If you have a test dataset with the information of the classes, then use this program to get the accuracy given by the model on the test dataset.

Run:

python validationTestSet.py –output-folder &lt;outFolder&gt; –label-column &lt;”class indices”&gt; –feature-columns &lt;”feature indices”&gt; –test\_file “test\_file.txt” –model\_file &lt;ModelFile&gt; –scaler\_file &lt;ScalerFile&gt; –save-file “File Prefix” –verbosity 1

Visit [<span>Validation dataset</span>](index.html#howitworks-o-vt) for output

<span id="document-04_configuration/index"></span>
<span id="configuration-index"></span>
Configuration[¶](#configuration "Permalink to this headline")
-------------------------------------------------------------

<span id="document-04_configuration/faq"></span>
### FAQ[¶](#faq "Permalink to this headline")

------------------------------------------------------------------------

