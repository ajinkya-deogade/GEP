.. _howitworks/accessary_programs:

==================
Accessary programs
==================

There are few accessary programs provided along with the package which might be helpful during the analysis of enhancers.

* Plot size distribution of enhancers::

    Rscript plot_size_distribution.R <size_file.txt>

    It provides histogram of sizes


* Enhancer distribution: see the distribution of enhancers within different states provided by other softwares (e.g.: ChromHMM) ::

    perl enhancerDistribution.pl --eFile <enhancer bedFile> --l <list (a tab-delimited file with fileName and name of the states)> --temp <tempDir>

Overlaps with different categories will be shown on stdout


* Calculate ML measures: If you have predictions from different softwares on the same dataset and you want to compare ML measures provided by each of them, use ::

    python calculateML_measures.py --data-file <dataFile> --label-column <label indice>

    where, datafile is a 2D matrix with Name, class and features columns

Note: see example folder (Link). Visit :ref:`howitworks/o_calML` for output


* validationTestSet.py: If you have a test dataset with the information of the classes, then use this program to get the accuracy given by the model on the test dataset.

    Run::
    python validationTestSet.py --output-folder <outFolder> --label-column <"class indices"> --feature-columns <"feature indices"> --test_file "test_file.txt" --model_file <ModelFile> --scalar_file <ScalerFile> --save-file "File Prefix" --verbosity 1

Visit :ref:`howitworks/o_vt` for output
