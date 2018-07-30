#! /usr/bin/env python

##########################################################################
""" Perform model training using Random Forest classifier
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
import sys
import os
from optparse import OptionParser
from GEPmodules import np, myClassifiers, myScores, myDataSplitter, myDataLogger
from GEPmodules import sanityCheck, performScaling, myDataShuffler, findParamaters, plotLearningCurve, plotROC

def main(options, args):

##########################################################################
# Retrieve user defined options
##########################################################################
    if len(sys.argv[1:]) == 0:
        print "no argument given!"
        print parser.print_help()
        sys.exit(2)
    if not options.data_file:
        print "No Data File Present \n Aborting....."
        sys.exit(2)
    if not int(options.label_column):
        print "Label column is missing: \n Preovide label column\n Aborting....\n";
        sys.exit(2)

    out_folder = options.output_folder
    dataCols = options.data_columns
    label_col = int(options.label_column)

    if int(options.verbosity) > 0:
        print "Options: ", options

    if options.n_estimators:
        n_estimators = [int(x) for x in options.n_estimators.split(",")]

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

##########################################################################
# Process data
##########################################################################

    # Get columns indices of the features
    dataCols = [int(x) for x in dataCols.split(",")]

    # Read features and labelData
    featureData = np.loadtxt(options.data_file, usecols=dataCols, delimiter = "\t", skiprows = 1)
    labelData = np.genfromtxt(options.data_file,  usecols=label_col, delimiter = "\t", skip_header = 1)

    # Perform same scaling on training and testing data
    labelDataShuffled, featureDataShuffled, shuffled_indices, scalerData = performScaling(featureData, labelData)

    scalerDataFile = options.output_folder + "/" + "Scaler_" + options.save_file + ".pkl"
    # with open(scalerDataFile, 'wb') as fin_save_pos:
    myDataLogger.dump(scalerData, scalerDataFile, compress=2)

##########################################################################
# Training and parameter tuning
##########################################################################

    # Train and test on the whole dataset
    sanityResult = sanityCheck(featureDataShuffled, labelDataShuffled, int(options.verbosity))
    if sanityResult > 0:
        print "Data is Sane..... Hurray !!!"
    else:
        print "Data is corrupted... Please check the input files !!"
        exit()

    # Get indices of 2 classes seperately to make a test dataset with 20% split in the whole dataset in straified manner
    featureTrainData, labelTrainData, featureTestData, labelTestData = myDataShuffler(featureDataShuffled, labelDataShuffled, shuffled_indices, float(options.percent_test_size), int(options.verbosity))

    # Make cross-validation iterator to tune the parameters by taking 20% of the remaining 80% of the training data using STRAITIFIED shuffled 10 fold cross-validation
    crossValidator = myDataSplitter(labelTrainData, int(options.fold_cross_validation), test_size=float(options.percent_test_size), random_state=0)

    # Apply the cross-validation iterator on the Training set for Optimization
    if int(options.verbosity) > 0:
        print "Cross Validation: ", crossValidator

    # Parallel processing during grid search
    best_max_depth, best_n_estimators = findParamaters(crossValidator, featureTrainData, labelTrainData, n_estimators, int(options.max_depth_start), int(options.max_depth_end), int(options.n_jobs), int(options.verbosity))
    if int(options.verbosity) > 0:
        print "Best parameters: \n Max_Depth = ", best_max_depth, "\n N_Estimators = ", best_n_estimators, '\n'

    # Fit estimators with the best parameters
    myClassifier = myClassifiers.RF(n_estimators=best_n_estimators, max_depth=best_max_depth, random_state=0)
    myClassifier.fit(featureTrainData, labelTrainData)

    # Plot the Learning Curve
    title = "Learning Curve (Random Forests, n_estimators=%.6f)" %(best_n_estimators)
    learning_plot=plotLearningCurve(myClassifier, title, featureTrainData, labelTrainData, crossValidator, int(options.verbosity))
    learning_curve_figure_file = options.output_folder + "/" + "Learning_Curve_" + options.save_file + ".svg"
    learning_plot.savefig(learning_curve_figure_file, bbox_inches='tight', pad_inches=0.2)
    learning_plot.show()
    learning_plot.close()
    if int(options.verbosity) > 0:
        print "Checking Model Biases - Learning Curve for Test and Training Dataset\n";

##########################################################################
# Testing
##########################################################################
    # Save the model to load afterwards
    fileNameModel = options.output_folder + "/" + "Model_" + options.save_file + ".pkl"
    # myDataLogger.dump(myClassifier, fileNameModel, compress=9)
    myDataLogger.dump(myClassifier, fileNameModel, compress=9)

    # Predict on the test set
    predictedLabels = myClassifier.predict(featureTestData)

    # Plot ROC Curve
    roc_plt = plotROC(myClassifier, featureTestData, labelTestData, predictedLabels, int(int(options.verbosity)))
    ROC_curve_figure_file = options.output_folder + "/" + "ROC_Curve_" + options.save_file + ".svg"
    roc_plt.savefig(ROC_curve_figure_file, bbox_inches='tight', pad_inches=0.2)
    roc_plt.show()
    roc_plt.close()
    if int(options.verbosity) > 0:
        print myScores.classification_report(labelTestData, predictedLabels)
        print "Classifier -- Final Generalization Accuracy: %.6f" %myScores.accuracy_score(labelTestData,predictedLabels)
        print "Classifier -- Feature Importances: ", myClassifier.feature_importances_

##########################################################################
# Options
##########################################################################
if __name__ == "__main__":
    usage = "\n\n##############################################\n python %prog [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --percent-test-size <float> --save-file <output-filename> --n-estimators <value> --max-depth-start <value> --max-depth-end <value>--n-jobs <int>]\n##############################################\n"
    parser = OptionParser(usage=usage)
    parser.add_option("", "--data-file", dest="data_file", default="", help="A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features: see example folder for test file")
    parser.add_option("", "--output-folder", dest="output_folder", default="../output/", help="An output folder: Default is ../output")
    parser.add_option("", "--label-column", dest="label_column", default=1, help="Column index containing class of instances: Default: 1 (2nd column)")
    parser.add_option("", "--feature-columns", dest="data_columns", default="2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", help="Column index containing features in data-file")
    parser.add_option("", "--percent-test-size", dest="percent_test_size", default=0.20, help="Size of the test dataset in percentage: Default: 20")
    parser.add_option("", "--fold-cross-validation", dest="fold_cross_validation", default=10, help="n-fold: Default:10")
    parser.add_option("", "--save-file", dest="save_file", default="output_file", help="Output filename: Deafult: output_file")
    parser.add_option("", "--n-estimators", dest="n_estimators", default=[10, 100, 1000], help="n_estimator list: Default: [10, 100, 1000]")
    parser.add_option("", "--max-depth-start", dest="max_depth_start", default=5, help="max-depth start: Default:5")
    parser.add_option("", "--max-depth-end", dest="max_depth_end", default=10, help="max-depth end: Default: 10")
    parser.add_option("", "--n-jobs", dest="n_jobs", default=1, help="no. of cores: Default:1")
    parser.add_option("", "--verbosity", dest="verbosity", default=1, help="Verbosity: Default on: provide 0 to turn off")
    (options, args) = parser.parse_args()
    main(options, args)
