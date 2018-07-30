#! /usr/bin/env python

##########################################################################
""" Perform validation of a model on an independent test set
    Copyright(C) 2015  Shalu Jhanwar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""
##########################################################################

##########################################################################
# Import modules
##########################################################################
import os
import sys
from optparse import OptionParser
import warnings
from StringIO import StringIO
from GEPmodules import np, myScores, myDataLogger, rescaleTestData, plotROC

warnings.filterwarnings("ignore")

def main(options, args):

##########################################################################
# Retrieve user defined options
##########################################################################
    if len(sys.argv[1:]) == 0:
        print "no argument given!"
        print parser.print_help()
        sys.exit(2)
    if not options.test_file:
        print "Either test file is missing \n Please provide the file and run the program again\nAborting....\n"
        sys.exit(2)
    if not options.model_file:
        print "Model file is missing \n Please provide the model file and run the program again\nAborting....\n"
        sys.exit(2)
    if not options.scalar_file:
        print "Scaler file is missing \n Please provide the scalar file (see document) and run the program again\n Aborting.......\n"
        sys.exit(2)

    out_folder = options.output_folder
    dataCols = options.data_columns
    label_col = int(options.label_column)
    model_filename = os.path.abspath(options.model_file)
    test_file = os.path.abspath(options.test_file)
    scalerFile = os.path.abspath(options.scalar_file)
    
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    if int(options.verbosity) > 0:
        print "Options: ", options
        print "Model file is", model_filename, "\n"

##########################################################################
# Process data
##########################################################################
    dataCols = [int(x) for x in dataCols.split(",")]
    featureDataTest = np.loadtxt(test_file, usecols=dataCols, delimiter = "\t", skiprows=1)
    labelDataTest = np.genfromtxt(test_file,  usecols = label_col, delimiter = "\t", skip_header=1)
    print "No. of samples in the validation dataset: ", len(labelDataTest),"\n"

    # Load the model file
    myEstimator = myDataLogger.load(model_filename)

    # Perform same scaling on training and testing data
    labelDataTestScaled, featureDataTestScaled,  shuffled_indices = rescaleTestData(featureDataTest, labelDataTest, scalerFile)

##########################################################################
# Perform prediction on independent validation dataset
##########################################################################
    # Get enhancers names:
    cols = 0
    with open (test_file,"r") as temp:
        a =  '\n'.join(line.strip("\n") for line in temp)
        allEnhancerNames = np.genfromtxt(StringIO(a), usecols = cols, delimiter="\t", dtype=None, skip_header=1)
        enhancerNamesTest = allEnhancerNames[shuffled_indices]

    temp.close()
    y_pred = myEstimator.predict(featureDataTestScaled)
    y_score_test = myEstimator.predict_proba(featureDataTestScaled)
    combined_test_predictions = zip(enhancerNamesTest, labelDataTestScaled, y_pred, y_score_test[:,0], y_score_test[:,1])
    prediction_output = open(out_folder + "/Predictions_" + options.save_file + ".txt", 'w')
    prediction_output.write("Enhancer_name\tY_true_labels\tY_predicted_labels\tProb_Class0\tProb_class1\n")
    for i in combined_test_predictions:
        line = '\t'.join(str(x) for x in i)
        prediction_output.write(line + '\n')
    prediction_output.close()

    print "Classification report of the prediction is", myScores.classification_report(labelDataTestScaled, y_pred), "\n"
    print "Random Forests: Final Generalization Accuracy: %.6f" %myScores.accuracy_score(labelDataTestScaled, y_pred)
    print "Number of mislabeled samples : %d" % (labelDataTestScaled != y_pred).sum()

    if int(int(options.verbosity)) > 0:
        # Get names of the features from header of file
        infile = open(options.test_file, 'r')
        firstline = infile.readline().rstrip()
        names = [x for x in firstline.split("\t")]
        names_sel = []
        for i in dataCols:
            names_sel.append(names[i])
        print "names", names_sel,"\n"
        infile.close()

        # Get the indices of the features according to their importance
        feature_rank_descend = np.argsort(myEstimator.feature_importances_)[::-1]  # Descending Order
        for f in xrange(len(dataCols)):
            print "%d. feature %d (%f) %s" % (
            f + 1, feature_rank_descend[f], myEstimator.feature_importances_[feature_rank_descend[f]], names_sel[feature_rank_descend[f]])

    # Plot ROC
    roc_plt = plotROC(myEstimator, featureDataTestScaled, labelDataTestScaled, y_pred, options.verbosity)
    roc_plt.savefig(out_folder + "/ROC-curve_" + options.save_file + ".svg", bbox_inches='tight', pad_inches=0.2)
    roc_plt.show()
    roc_plt.close()

##########################################################################
# Options
##########################################################################
if __name__ == "__main__":
    usage = "\n\n##############################################\n python %prog [required: --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --save-file <output-filename> --n-estimators <value> --max-depth <value>]\n##############################################\n"
    parser = OptionParser(usage=usage)
    parser.add_option("", "--output-folder", dest="output_folder", default="../output/", help="An output folder: Default is ../output")
    parser.add_option("", "--label-column", dest="label_column", default=1, help="Column index containing class of instances in test file: Default: 1 (2nd column)")
    parser.add_option("", "--feature-columns", dest="data_columns", default="2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", help="Column index containing features in data-file")
    parser.add_option("", "--fold-cross-validation", dest="fold_cross_validation", default=10, help="n-fold: Default:10")
    parser.add_option("", "--save-file", dest="save_file", default="output_file", help="Output filename: Deafult: output_file")
    parser.add_option("", "--n-jobs", dest="n_jobs", default=10, help="no. of CPUs <value>")
    parser.add_option("", "--test_file", dest="test_file", default="", help="A test file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features in the same order as of training data: see example folder for test file")
    parser.add_option("", "--model_file", dest="model_file", default="", help="A file containing model")
    parser.add_option("", "--scaler_file", dest="scalar_file", default="", help="A file containing scaled training data in pkl format: see example folder for help")
    parser.add_option("", "--verbosity", dest="verbosity", default=1, help="Verbosity: Default on: provide 0 to turn off")

    (options, args) = parser.parse_args()

    main(options, args)
