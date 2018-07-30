.. _howitworks/enrichment:

===================
Enrichment analysis
===================

There are certain characteristic elements associative to active enhancers such as: open-chromatin, few histone modifications, 3D-interaction data and experimental evidances etc. In order to provide support for potential regulatory activity of these in-silico predicted enahncers using GEP, we propose enrichment of these elements in predicted enhancers.

Overlap with enhancers
======================

See the overlap of characteristic elements with predicted enhancers.

    * Necessary files

        * Enhancer bed-file: A three column bed file
        * List: A list containing file path and name of the characteristic elements
        * outputFolder

    Run::

        perl votingScore.pl --chrSize <enhancer bedFile> --l <list> --o <outFolder>


Enrichment test
===============

To see the significance of the overlap, we propose a enrichment test. In this test, we consider estimating the distribution of base pair overlap in randomized genomes 1000 times. If the P-value is less than 0.05, we consider the enrichment of characteristic element as "significant" in enhancers.

    * Necessary files

        * Enhancer bed-file
        * gFile: A tab-delimited file with Chromosome and size
        * List: A list containing file path and name of the characteristic elements
        * outputFolder
        * outFileName

    Run::

        Rscript enrichmentAnalysis.R <enhancer bedFile> <gFile> <list> <outputFolder> <outFileName>


Output
======

Visit :ref:`howitworks/o_ea` for output 