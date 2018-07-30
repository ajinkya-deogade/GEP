#! /usr/bin/env python

##########################################################################
""" Perform feature selection using Random Forest classifier
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
from GEPmodules import np, myPlot, myScaler, myClassifiers

#########################################################################
# Retrieve user defined options
#########################################################################
def main(options, args):
    out_folder = options.output_folder
    data_cols = options.data_columns
    label_col = int(options.label_column)
    if not options.data_file:
        print "No Data File Present \n Aborting....."
        sys.exit(2)
    if options.verbosity > 0:
        print "Label Column: ", label_col
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

##########################################################################
# Process data
##########################################################################
    # Get columns indices of the features
    data_cols = [int(x) for x in data_cols.split(",")]

    # Get names of the features from header of file
    infile = open(options.data_file, 'r')
    firstline = infile.readline().rstrip()
    names = [x for x in firstline.split("\t")]
    del names[0]  # delete column for position
    del names[0]  # delete column for class
    infile.close()

    # Read features and labels
    featureData = np.loadtxt(options.data_file, usecols=data_cols, delimiter="\t", skiprows=1)
    labelData = np.genfromtxt(options.data_file, usecols=label_col, delimiter="\t", skip_header=1)

    # Same scaling on both test and train data (centering the data scaling)
    featureData = myScaler.fit_transform(featureData)

    # Shuffle rows of the data
    np.random.seed(0)
    shuffled_indices = np.random.permutation(len(featureData))
    featureDataTraining = featureData[shuffled_indices]
    labelDataTraining = labelData[shuffled_indices]

    # With significant data after feature selection: Provide importance of the feature
    myClassifier = myClassifiers.RF(n_estimators=int(options.n_estimators), random_state=0)
    myClassifier.fit(featureDataTraining, labelDataTraining)

    # Importance of the feature is given by:
    featureImportances = myClassifier.feature_importances_
    if options.verbosity > 0:
        print "Feature Importance:", featureImportances

    # Get the indices of the features according to their importance
    feature_rank_descend = np.argsort(featureImportances)[::-1]  # Descending Order

    # Print feature ranking
    if options.verbosity > 0:
        for f in xrange(len(data_cols)):
            print "%d. feature %d (%f) %s" % (
            f + 1, feature_rank_descend[f], featureImportances[feature_rank_descend[f]], names[feature_rank_descend[f]])

    # Get Feature Importance from the classifier
    feature_rank_ascend = np.argsort(myClassifier.feature_importances_)  # Ascending Order

##########################################################################
# Plotting feature importance
##########################################################################
    # Plot the importance of the feature as bar plot
    if int(options.plot_bar_without_std) == 1:
        myPlot.barh(np.arange(len(names)), myClassifier.feature_importances_[feature_rank_ascend])
        myPlot.yticks(np.arange(len(names)) + 0.25, np.array(names)[feature_rank_ascend])
        _ = myPlot.xlabel('Relative importance')
        myPlot.savefig(out_folder + '/withNames_RFClassifier_Feature_importance.svg', bbox_inches='tight', pad_inches=0.2)
        myPlot.show()
        myPlot.close()

    if int(options.plot_bar_with_std) == 1:
        std = np.std([feature.feature_importances_ for feature in myClassifier.estimators_], axis=0)
        myPlot.figure()
        myPlot.title("Feature Importances")
        myPlot.bar(xrange(len(data_cols)), featureImportances[feature_rank_descend], color="r", yerr=std[feature_rank_descend],
                align="center")
        myPlot.xticks(xrange(len(data_cols)), feature_rank_descend)
        myPlot.xlim([-1, len(data_cols)])
        myPlot.savefig(out_folder + '/RF_classifier_tssDist_include_Feature_importance.svg', transparent=True,
                    bbox_inches='tight', pad_inches=0.2)
        # pl.savefig(out_folder + '/RF_classifier_No_transperant_tssDist_include_Feature_importance.svg', bbox_inches='tight', pad_inches=0.2)
        myPlot.show()
        myPlot.close()

    # Plot the feature featureImportances of the trees and of the forest
    if int(options.plot_line) == 1:
        myPlot.figure()
        myPlot.title("Feature Importances")

        for feature in myClassifier.estimators_:
            myPlot.plot(xrange(len(data_cols)), feature.feature_importances_[feature_rank_descend], "r")

        myPlot.plot(xrange(len(data_cols)), featureImportances[feature_rank_descend], "b")
        myPlot.show()
        myPlot.close()

    # Select only those features which are important by leaving other features
    featureDataTraining = myClassifier.fit(featureDataTraining, labelDataTraining).transform(featureDataTraining)
    if options.verbosity > 0:
        print "The shape of the data after feature selection is", featureDataTraining.shape, "\n"

##########################################################################
# Options
##########################################################################
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("", "--data-file", dest="data_file", default="", help="A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features: see example folder for test file")
    parser.add_option("", "--output-folder", dest="output_folder", default="../output/", help="An output folder: Default is ../output")
    parser.add_option("", "--label-column", dest="label_column", default=1, help="Column index containing class of instances: Default: 1 (2nd column)")
    parser.add_option("", "--feature-columns", dest="data_columns", default="2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", help="Column index containing features in data-file")
    parser.add_option("", "--plot-bar-without-std", dest="plot_bar_without_std", default=1, help="Bar plot without std deviation: Default:on")
    parser.add_option("", "--plot-bar-with-std", dest="plot_bar_with_std", default=0, help="Bar plot with std deviation: Default:off, provide 1 value to turn on")
    parser.add_option("", "--plot-line", dest="plot_line", default=0, help="Line plot: Default off: provide 1 value to turn on")
    parser.add_option("", "--n-estimators", dest="n_estimators", default=int(100), help="n_estimator: Default=100")
    parser.add_option("", "--verbosity", dest="verbosity", default=1, help="Verbosity: Default on: provide 0 to turn off")
    (options, args) = parser.parse_args()
    main(options, args)
