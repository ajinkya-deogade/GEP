#! /usr/bin/env python

##########################################################################
""" Perform cross-validation on the training dataset
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
import optparse
from GEPmodules import np, mc, confM, myScores

##########################################################################
# Retrieve user defined options
##########################################################################
def main(options, args):

    if len(sys.argv[1:]) == 0:
       print "no argument given!"
       print parser.print_help()
       sys.exit(2)
    if not options.data_file:
       print "The data file is missing\n Please provide the file and run the program again\nAborting....\n"
       sys.exit(2)
    if not options.label_column:
       print "Labels missing. Please provide column index containing label and un the program again\nAborting....\n"
       sys.exit(2)
    if not options.output_folder:
       print "output filename not given\n"
       sys.exit(2)

    y_true = np.genfromtxt(options.data_file,  usecols = int(options.label_column), delimiter = "\t", skip_header=1)
    with open(options.data_file) as f:
        line = f.readline()
        nCol = len(line.split('\t'))
    print "Total no of columns in the file is:", nCol,"\n"
    nCol = nCol-2;
    print "Total no of columns in the file is:", nCol,"\n"
    for lab in range(2,nCol):
        print "lab", lab
        y_pred = np.genfromtxt(options.data_file,  usecols = lab, delimiter = "\t", skip_header=1)
        print "The classification report for Column", lab, "is \n"
        print myScores.classification_report(y_true, y_pred)
        print "Accuracy: %.6f" %myScores.accuracy_score(y_true,y_pred)
        cm = confM(y_true, y_pred)
        print "Confusion matrix as \n", cm
        tn = int(cm[0,0])
        fp = int(cm[0,1])
        print "tn", tn
        print "fp", fp
        s = tn/(tn + fp)
        print "Speicificity is", s , "\n"
        print "Metthiew correlation co-efficient: %.6f" %mc(y_true, y_pred)


if __name__ == "__main__":
    usage = "\n\n##############################################\n python %prog [required: --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --save-file <output-filename> --n-estimators <value> --max-depth <value>]\n##############################################\n"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("", "--output-folder", dest="output_folder", default="../output/", help="An output folder: Default is ../output")
    parser.add_option("", "--label-column", dest="label_column", default=1, help="Column index containing class of instances in test file: Default: 1 (2nd column)")
    parser.add_option("", "--data-file", dest="data_file", default="", help="A data file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features in the same order as of training data: see example folder for data file")
    (options, args) = parser.parse_args()
    main(options, args)