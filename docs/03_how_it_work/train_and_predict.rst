.. _howitworks/train_and_predict:

=================
Train and Predict
=================
In machine-learning(ML)approaches, the outcome largely depends on the training. In case of an appropriate training dataset availability, it might be worth to perform predictions with a newly trained model. For that purpose, you need to first build a trianing dataset and train the model.


Train
=====

Perform following:

1. Generate training dataset (Usage :ref:`howitworks/pt`):
    The training dataset comprised of 2 classes: Positive classes as enhancers (provided by you) and negative
    classes which contain different genomic regions as promoter, gene-body and heterochromatin in 5:3:2 ratio approximately. Following are the input files required:

* Necessary files

    * Positive samples: A 3 column bed file containing positive samples (Enhancers)
    * List: A text file containing a list of all the feature files and names (see XX folder for an example: Link to Gitfolder)
    * Chromosome: A two column tab-delimited file with Chr and sizes
    * TSS: A three column tab-delimited coding TSS file with Chr, Pos, Strand
    * Exon: A three-column exon bed file
    * Intron: A three-column intron bed file
    * aTSS: A six column bedfile with all (coding and non-coding TSS)

    Note::

        For Human (hg19) and mouse (mm9), refer (link to the folder) for Chromosome, TSS, aTSS files.
        For Human (hg19), intron and exon files are provided (link to the folder)

* Build trining data::

    Perl buildTrainingData.pl –chrSize <positive_samples.txt> --l <list.txt> --gmSize  <Chromosome_sizes.txt> --tss <tssFile> --gbFile <exon.bed> –inFile <intron.bed> --o <outputFolder> --aTSS <All TSS file>


* Visit :ref:`howitworks/o_pt` for output

2. Building model (Usage :ref:`howitworks/tapG`)

Build a model on your own trainign data using GEP. Provide more number of cores to enable parallel processing.

* Necessary files

    * Output of <buildTrainingData.pl>: In above example, <outfolder/matrix.txt> file
    * feature column index: index of the feature columns in <outfolder/matrix.txt> file
    * label column: index of label column in <outfolder/matrix.txt> file
    * Optional params

Run::

    python trainAndPredictGEP.py --data-file <outfolder/matrix.txt> --output-folder outputFolder --feature-columns “<comma separated column indices>” --label-column <label column index> --percent-test-size <float value> --fold-cross-validation <int> --save-file “<filename>” --n-estimators "<comma separated n-estimators for optimization>" --max-depth-start <int> --max-depth-end <int> --n-jobs <int> --verbosity <binary value>


Note::

    Training can be performed using SVM classifier. See :ref:`howitworks/tapS`

* Visit :ref:`howitworks/o_tapG` for output

Predict
=======

Perform prediction on the new model in the simialr way as using in-built models. Visit :ref:`introduction/quickstart`

* Visit :ref:`howitworks/o_predict` for output

