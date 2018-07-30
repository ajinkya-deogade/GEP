.. _howitworks/output:

=======
Outputs
=======

Output provided by various functionality is shown here:

.. _howitworks/o_fs:

Feature selection
-----------------

python featureSelection.py

* It provides the relative importance of the features provided by GEP on the command prompt
* Based on the options chosen, it also shows the relative importance of the features as bar or line graph with or without variance. (see example folder link)

.. _howitworks/o_predict:

Predict
-------

python genomewidePrediction.py

* Provides the statistics on the command prompt
* Predicted enhancer positions (.txt): There are four columns corresponding to "chr", "start", "End", "Confidence"
* UCSC browser file: A file (.bed) to upload on UCSC browser (default: hg19 assembly). Once uploaded in the browser, the colour corresponds to the confidence of prediction (dark blue - high confidence)

    Note::
    If you are working on other species, please change within the UCSC browser file on 2nd line. Change db = hg19 to db = "your species"). For e.g. if you are working with mouse mm9, then write in the file db = "mm9"


.. _howitworks/o_tapG:

Train and Predict GEP
---------------------

python trainAndPredictGEP.py

* Provides best parameters and classification report with machine-learning measures (precision, recall, F-measure) on the command prompt
* Learning_Curve: A learning curve represents training and validation score for different numbers of training samples. This is used to determine if the model can be benefitted on addition of more no. of samples.
* Model: Trained model on your training data
* ROC(Receiver Operating Characteristic) Curve: ROC curve obtained on the test dataset using the trained model
* Scaler: A scalar storing the statistics of traning data


.. _howitworks/o_tapS:

Train and Predict SVM
---------------------

python trainAndPredictSVM.py

* Provides best parameters and classification report with machine-learning measures (precision, recall, F-measure) on the command prompt
* Learning_Curve: A learning curve represents training and validation score for different numbers of training samples. This is used to determine if the model can be benefitted on addition of more no. of samples.
* Model: Trained SVM model on your training data
* ROC(Receiver Operating Characteristic) Curve: ROC curve obtained on the test dataset using the trained model
* Scaler: A scalar storing the statistics of traning data


.. _howitworks/o_nf:

n-fold cross-validation
-----------------------

python crossValidation.py

* Measures (.txt): A txt file with machine-learning measures (accuracy, precision, recall, F-measure) corresponding to random and true classification at each fold. It also provides average measures of all the folds

* ROC(Receiver Operating Characteristic) Curve


.. _howitworks/o_pgp:

Prepare genomewide prediction
-----------------------------

perl prepare_genomeWidePrediction.pl

* matix.txt: A 2D matrix with features as columns (same order as training data) and samples as row

.. _howitworks/o_pt:

Prepare training
----------------

perl buildTrainingData.pl

* matix.txt: A 2D matrix with features as columns samples as row. You can use this file as input during model building step


.. _howitworks/o_pes:

Plot size distribution
----------------------

Rscript plot_size_distribution.R <size_file.txt>

* histogram of the size of enhancers


.. _howitworks/o_ed:

Comparison with other enhancer set
----------------------------------

perl enhancerDistribution.pl --eFile <enhancer bedFile> --l <list (a tab-delimited file with fileName and name of the states)> --temp <tempDir>

* It provides the no. of enhancers overlapped with different regions provided by the user

.. _howitworks/o_calML:

Calculate ML measures
---------------------

python calculateML_measures.py

    It provides different measures (e.g. Recall, Precision, F-measure, PPV, Methiew correlation coefficient etc) on stdout


.. _howitworks/o_vt:

Validation dataset
------------------

python validationTestSet.py --output-folder <outFolder> --label-column <"class indices"> --feature-columns <"feature indices"> --test_file "test_file.txt" --model_file <ModelFile> --scalar_file <ScalerFile> --save-file "File Prefix" --verbosity 1

* It provides ML measures obtained on the test dataset on application of the model on stdout

* ROC curve

.. _howitworks/o_ea:

Enrichment analysis
-------------------

perl votingScore.pl

    * HistoFile.txt: This gives the no. of characteristic element supporting each enhancer
    * votingTable.txt: Presence or absence of each element corrosponding to enhancers in tabular format
    * No_validation_evidence.txt: An additional table corresponding to enhancers not supported by any element


Enrichment test

Rscript enrichmentAnalysis.R <enhancer bedFile> <gFile> <list> <outputFolder> <outFileName>

* .txt: It will generate a .txt file corresponding to each factor containing means of random overlap
* .pdf: It will generate a .pdf file showing the distribution of means of random overlaps


