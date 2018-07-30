.. _howitworks/n-fold:

======================
nFold cross-validation
======================

cross validation is one of the model validation technique. It assess the generalizability of the model on an independent dataset. GEP provides utility to performs n-fold cross-validation on the entire dataset and obtain different statistic measures such as f-measures, accuracy, precision and recall. Additionally it also provides the measures corresponding to random classification.

Usage
-----

Visit :ref:`howitworks/nf` for Usage

Run the following command on your own training data or in-built training data::

    python nFold_CrossValidation_measures.py --data-file <training data> --output-folder <outFolder> --feature-columns <"comma separated column indices"> --label-column <"label column index"> --fold-cross-validation <int> --save-file <"file-prefix"> --method <classifier>


Output
------

Visit ref:`howitworks/o_nf` for output