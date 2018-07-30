#! /usr/bin/env python

##########################################################################
""" Perform model training using SVM Classifier
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
from GEPmodules import sanityCheck, performScaling, myDataShuffler, findParamatersSVM, plotLearningCurve, plotROC

##########################################################################
# Retrieve user defined options
##########################################################################
def main(options, args):
    if len(sys.argv[1:]) == 0:
        print "no argument given!"
        print parser.print_help()
        sys.exit(2)
    if not options.data_file:
        print "No Data File Present \n Aborting....."
        sys.exit(2)
    out_folder = options.output_folder
    data_cols = options.data_columns
    label_col = int(options.label_column)
    if int(options.verbosity) > 0:
        print "Options: ", options
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

##########################################################################
# Process data
##########################################################################
    # Get columns indices of the features
    data_cols = [int(x) for x in data_cols.split(",")]

    # Read features and labels
    featureData = np.loadtxt(options.data_file, usecols=data_cols, delimiter = "\t", skiprows = 1)
    labelData = np.genfromtxt(options.data_file,  usecols=label_col, delimiter = "\t", skip_header = 1)

    #Perform same scaling on training and testing data
    labelDataShuffled, featureDataShuffled, shuffled_indices, scalerData = performScaling(featureData, labelData)

    scalerFile = options.output_folder + "/" + "Scaler_" + options.save_file + ".pkl"
    myDataLogger.dump(scalerData, scalerFile)

##########################################################################
# Training and parameter tuning
##########################################################################
    # Train and test on the whole dataset
    sanityResult = sanityCheck(featureDataShuffled, labelDataShuffled, int(options.verbosity))
    if sanityResult > 0:
        print "Data is Sane..... Hurray !!!"
    else:
        print "Data is corrupted... Please check the input files !!"
        # exit()

    # Get indices of 2 classes seperately to make a test dataset with 20% split in the whole dataset in straified manner
    featureDataTrain, labelDataTrain, featureDataTest, labelDataTest = myDataShuffler(featureDataShuffled, labelDataShuffled, shuffled_indices, float(options.percent_test_size), int(options.verbosity))

    #Make cross-validation iterator to tune the parameters by taking 20% of the remaining 80% of the training data using STRAITIFIED shuffled 10 fold cross-validation
    crossValidator = myDataSplitter(labelDataTrain, int(options.fold_cross_validation), test_size=float(options.percent_test_size), random_state=0)

    #Apply the cross-validation iterator on the Training set using GridSearchCV
    if int(options.verbosity) > 0:
        print "Cross Validation is: ", crossValidator

    #Parallel processing during grid search
    SVM_C_min = int(options.SVM_C_min)
    SVM_C_max = int(options.SVM_C_max)
    SVM_gamma_min = int(options.SVM_gamma_min)
    SVM_gamma_max = int(options.SVM_gamma_max)

    C_range = 10.0 ** np.arange(SVM_C_min, SVM_C_max)
    gamma_range = 10.0 ** np.arange(SVM_gamma_min, SVM_gamma_max)
    param_grid = dict(gamma=gamma_range, C=C_range)
    if int(options.verbosity) > 0:
        print "Method Chosen: SVM\n"
    best_C, best_gamma = findParamatersSVM(crossValidator, featureDataTrain, labelDataTrain, param_grid, int(options.n_jobs), int(options.verbosity))

    myClassifier = myClassifiers.svm(kernel= 'rbf', gamma=best_gamma, C=best_C,random_state=0, probability=True)
    myClassifier.fit(featureDataTrain, labelDataTrain)

    #Below is a plot_learning_curve module that's provided by scikit-learn. It allows us to quickly and easily visualize how #well the model is performing based on number of samples we're training on. It helps to understand situations such as  #high variance or bias.
    if int(options.verbosity) > 0:
        print "See how well the model is fitting - plot learning curve for testing and training dataset\n";
    title = "Learning Curves (Random Forests, C=%.9f)" %(best_C)
    learning_plot=plotLearningCurve(myClassifier, title, featureDataTrain, labelDataTrain, crossValidator, int(int(options.verbosity)))
    learning_curve_figure_file = options.output_folder + "/" + "Learning_Curve_" + options.save_file + ".svg"
    learning_plot.savefig(learning_curve_figure_file, bbox_inches='tight', pad_inches=0.2)
    learning_plot.show()
    learning_plot.close()

##########################################################################
# Testing
##########################################################################
    #Save the model to load afterwards
    filename_model = options.output_folder + "/" + "Model_" + options.save_file + ".pkl"
    myDataLogger.dump(myClassifier, filename_model, compress=9)

    #Predict on the test set
    predicted_labels = myClassifier.predict(featureDataTest)

    #Plot ROC Curve
    roc_plt = plotROC(myClassifier, featureDataTest, labelDataTest, predicted_labels, int(int(options.verbosity)))
    ROC_curve_figure_file = options.output_folder + "/" + "ROC_Curve_" + options.save_file + ".svg"
    roc_plt.savefig(ROC_curve_figure_file, bbox_inches='tight', pad_inches=0.2)
    roc_plt.show()
    roc_plt.close()

    if int(options.verbosity) > 0:
        print myScores.classification_report(labelDataTest, predicted_labels)
        print "Random Forests: Final Generalization Accuracy: %.6f" %myScores.accuracy_score(labelDataTest, predicted_labels)

##########################################################################
# Options
##########################################################################
if __name__ == "__main__":
    usage = "usage: %prog [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --percent-test-size <float> --save-file <output-filename> --n-estimators <value> --max-depth-start <value> --max-depth-end <value>--n-jobs <int>]"
    parser = OptionParser(usage=usage)
    parser.add_option("", "--data-file", dest="data_file", default="", help="A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features: see example folder for test file")
    parser.add_option("", "--output-folder", dest="output_folder", default="../output/", help="An output folder: Default is ../output")
    parser.add_option("", "--label-column", dest="label_column", default=1, help="Column index containing class of instances: Default: 1 (2nd column)")
    parser.add_option("", "--feature-columns", dest="data_columns", default="2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", help="Column index containing features in data-file")
    parser.add_option("", "--percent-test-size", dest="percent_test_size", default=0.20, help="Size of the test dataset in percentage: Default: 20")
    parser.add_option("", "--fold-cross-validation", dest="fold_cross_validation", default=10, help="n-fold: Default:10")
    parser.add_option("", "--save-file", dest="save_file", default="output_file", help="Output filename: Deafult: output_file")
    parser.add_option("", "--SVM_C_min", dest="SVM_C_min", default=-2, help="C <power of 10>: Default: -2 == 0.01")
    parser.add_option("", "--SVM_C_max", dest="SVM_C_max", default=9, help="C <power of 10>: Default: 9 == 1000000000.0")
    parser.add_option("", "--SVM_gamma_min", dest="SVM_gamma_min", default=-4, help="gamma: <power of 10> default: -4 == 0.0001")
    parser.add_option("", "--SVM_gamma_max", dest="SVM_gamma_max", default=5, help="gamma: <power of 10> default: 5 == 100000.0")
    parser.add_option("", "--method", dest="method", default="RF", help="Method: 'RF': Random Forest, 'SVM': Support Vector Machine: Default: RF")
    parser.add_option("", "--n-jobs", dest="n_jobs", default=10, help="no. of CPUs: Default:10")
    parser.add_option("", "--verbosity", dest="verbosity", default=1, help="Verbosity: Default on: provide 0 to turn off")
    (options, args) = parser.parse_args()
    main(options, args)
