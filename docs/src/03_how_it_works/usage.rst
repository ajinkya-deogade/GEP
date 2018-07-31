.. _howitworks/usage:

=====
Usage
=====

Help usage of different functionalities of the package is shown here:


.. _howitworks/fs:

Feature selection
-----------------

python featureSelection.py --h ::

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


.. _howitworks/predict:

Predict
-------

python genomewidePrediction.py  --h ::

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
    --scalar_file=SCALAR_FILE
                            A file containing scaled training data in pkl format:
                            see example folder for help
    --verbosity=VERBOSITY
                            Verbosity: Default on: provide 0 to turn off


.. _howitworks/tapG:

Train and Predict GEP
---------------------

python trainAndPredictGEP.py --h ::

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


.. _howitworks/tapS:

Train and Predict SVM
---------------------

python trainAndPredictSVM.py --h ::

    Usage: trainAndPredictSVM.py [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --percent-test-size <float> --save-file <output-filename> --n-estimators <value> --max-depth-start <value> --max-depth-end <value>--n-jobs <int>]

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


.. _howitworks/nf:

n-fold cross-validation
-----------------------

python crossValidation.py --h ::

    Usage:

    python crossValidation.py [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --save-file <output-filename> --n-estimators <value> --max-depth <value>]

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


.. _howitworks/pgp:

Prepare genomewide prediction
-----------------------------

perl prepare_genomeWidePrediction.pl --h ::

    Description: Prepare genome to perform prediction using GEP
    System requirements:
    Perl:
    Module - Cwd
    bedtools - Assumed it in the path

    Usage:

    perl prepare_genomeWidePrediction.pl --l  FeatureFileList --gmSize <ChromosomeSize.txt> --tss <A three column file containing TSS to exclude from genome> --aTSS <A six column bed file containing all coding and non-coding TSS> --active <active histones bedFile> --o <output_folder> <optional parameters>

    ### Required parameters:

    --l | --listFeatureFile			<A tab delimited file containing the name of the files (along with the path) and the name of the feature to be displayed>

    --gmSize | --genomeSizeFile		<A tab delimited file containing chromosome name and its size>
    For Human hg19: Hg19_ChromosomeSize.txt
    For Mouse mm9: mm9_ChromosomeSize.txt

    --tss | --tssFile 			<A three column file containing TSS>

    --active | --activeRegionFiles		<Active region bed files containing three regions: chrName, start and end

    --aTSS | --allTssFile			<A six column bed file containing all coding and non-coding TSS>
                                    For Mouse mm9: Please mention "Mouse_gencode.vM1_tss_coding_non-coding_6_column.bed" for annotation from gencode.vM1
                                    For Human hg19: Please mention "Human_gencode.v19_tss_coding_non-coding_6_column.bed" for annotation from gencode.v19

    ### Optional parameters:

    --f | --fractionOverlap			<Fraction cut-off of the bin required to overlap with the feature in order to consider the signal in that bin>

    --h | --help				<Print help usage>

    --o | --outDir				<output_folder: All the output files will be saved in the output folder>
                                default output folder:current folder/output_folder

    --bin					<Bin size in bp: default is 500>


    This script was last edited on 29th July 2015.

.. _howitworks/pt:

Prepare training
----------------

perl buildTrainingData.pl --h ::

    Description: Form training datatset of positive and negative samples in 1:1 ratio

    System requirements:
    Perl:
    Module - Cwd
    bedtools - Assumed it in the path

    Usage:
    perl buildTrainingData.pl --chrSize <pos_samples.bed> --gmSize <ChromosomeSize.txt> --l FeatureFileList --tss <tssFile> --gbFile <exonBed> --inFile <intronBed> --aTSS <A six column bed file containing all coding and non-coding TSS> <optional parameters>


    ### Required parameters:
    --chrSize | --chrSizeFile		<A tab delimited file of positive samples containing chrName, start and end>

    --l | --listFeatureFile			<A tab delimited file containing 2 columns: i) the name of the files (along             with the path) ii) the name of the feature to be displayed>

    --gmSize | --genomeSizeFile		<A tab delimited file containing chromosome name and sizes>
                                    For Human hg19: Hg19_ChromosomeSize.txt
                                    For Mouse mm9: mm9_ChromosomeSize.txt

    --tss | --tssFile               <A three column: <chrom><txStart><strand> tab delimited file containing TSS
                                    corresponding to protein coding genes>
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

    --f | --fractionOverlap			<Fraction cut-off of the bin required to overlap with the feature in order to consider the signal in that bin>

    --h | --help				<Print help usage>

    --o | --outDir				<output_folder: All the output files will be saved in the output folder>
                                default output folder:current folder/output_folder
    --bin					<Bin size in bp: default is 200>
