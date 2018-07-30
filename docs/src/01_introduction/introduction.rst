.. _introduction/quickstart:

Quick-Start
-----------

Quickly identify genome-wide enhancers in a particular cell-type or tissue using GEP. Perform following:

1. Prepare genomewide prediction (Usage :ref:`howitworks/pgp`)

* Input files:
    * List: A file containing list of all the histone marks in the **same order**:  Dnase, H3k27ac, H3k27me3, H3k36me3, H3k4me1, H3k4me1_H3K4me3, H3k4me3, P300. The file contains two columns: name of the file  (along with path) and name of the mark. Please refer “example” (link) folder for details.
    * gmSize: A file containing Chromosome name and size of the chromosomes in tab-delimited manner. For Human and Mouse, the files are provided with the package.
    * TSS: A file containing coding TSS information in 3 columns: Chr, Position, and Strand. For Human and Mouse, the files are provided with the package.
    * Acetylation marks: Four columns bed files of active marks (e.g. H3K27ac, H3K9ac etc)
    * aTSS: A 6 column bed file containing all (coding and non-coding) TSS information. For Human and Mouse, the files are provided with the package (see folder).

* Run::

    Perl prepare_genomeWidePrediction.pl –l <List> --gmSize <gmSize> --tss <tss> –o <outputFolder> --active <acetylation marks> –aTSS <aTSS>

2. Perform enhancer prediction (Usage :ref:`howitworks/predict`)

* Input files:

    * output of <prepare_genomeWidePrediction.pl>: In above example, <outputFolder/matrix.txt>
    * Model File: Please see <Git link> folder for the model file. There are 2 models provided. Depending on your data, choose either from below:
    * with P300 (Name)
    * without P300 (Name)
    * Scaler file: Scaler files corresponding to models are provided in <X> folder

* Run

with P300::

    python genomewidePrediction.py --output-folder <genomewideEnhancers> --feature-columns ”2,3,4,5,6,7,8,9,10” --genome_file <outputFolder/matrix.txt> --model_file <Model.pkl> --scalar_file <Scaler.pkl> --save-file ”genomefile_prediction”

without P300::

    python genomewidePrediction.py --output-folder <genomewideEnhancers> --feature-columns ”2,3,4,5,6,7,8,9” --genome_file <outputFolder/matrix.txt> --model_file <Model_without_P300.pkl> --scalar_file <Scaler_without_P300.pkl> --save-file "genomefile_prediction”


