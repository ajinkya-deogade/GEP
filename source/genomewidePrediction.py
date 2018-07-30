#! /usr/bin/env python

##########################################################################
""" Perform genome-wide prediction
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
from GEPmodules import np, myDataLogger, rescaleGenomeData, sortCoordinate, clusterByOverlap

warnings.filterwarnings("ignore")

def main(options, args):
##########################################################################
# Retrieve user defined options
##########################################################################
    if len(sys.argv[1:]) == 0:
        print "no argument given!"
        print parser.print_help()
        sys.exit(2)
    if not options.genome_file:
        print "Either genome region file is missing \n Please provide the file and run the program again\nAborting....\n"
        sys.exit(2)
    if not options.scalar_file:
        print "Scalar file is missing \n Please provide the scalar file (see document) and run the program again\nAborting....\n"
        sys.exit(2)

    model_filename = os.path.abspath(options.model_file)
    genome_file = os.path.abspath(options.genome_file)
    out_folder = options.output_folder
    data_cols = options.data_columns
    scalerFile = os.path.abspath(options.scalar_file)

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    if int(options.verbosity) > 0:
        print "Options: ", options
        print "Model File: ", model_filename

##########################################################################
# Process data
##########################################################################

    data_cols = [int(x) for x in data_cols.split(",")]
    genomeFeatureData = np.loadtxt(genome_file, usecols=data_cols, delimiter = "\t", skiprows=1)

    # Load the model file#
    myEstimator = myDataLogger.load(model_filename)

    # Perform same scaling on training and testing data
    genomeFeatureDataScaled, shuffled_indices  = rescaleGenomeData(genomeFeatureData, scalerFile)

    if int(options.verbosity) > 0:
        print "Genome Feature Data: ", genomeFeatureData.shape
        print "Genome Feature Scaled Data: ", genomeFeatureDataScaled.shape

    cols = 0
    with open (genome_file, "r") as temp:
        next(temp)
        a =  '\n'.join(line.strip("\n") for line in temp)
        b = np.genfromtxt(StringIO(a), usecols = cols, delimiter="\t", dtype=None)
        enhancer_names_test = b[shuffled_indices]
    temp.close()

    if int(options.verbosity) > 0:
        print "Number of Regions: ", enhancer_names_test.shape

##########################################################################
# Carryout Genomewide Prediction
##########################################################################

    ## Predict
    y_pred = myEstimator.predict(genomeFeatureDataScaled)
    y_score_test = myEstimator.predict_proba(genomeFeatureDataScaled)
    combined_test = zip(enhancer_names_test, y_pred, y_score_test[:,0], y_score_test[:,1])
    predictionAllLociFile = out_folder + "/GenomewidePredictionAllLocus_" + options.save_file + ".txt"
    prediction_output= open(predictionAllLociFile, 'w')
    prediction_output.write("Chromosome\tY_predicted_labels\tProb_Class0\tProb_class1\n")
    for i in combined_test:
        line = '\t'.join(str(x) for x in i)
        prediction_output.write(line + '\n')
    prediction_output.close()

    y_pred_pos_ind = np.where(y_pred == 1)
    enhancer_names_test_pos = enhancer_names_test[y_pred_pos_ind]

    ## Create a BED file for the Enhancers
    positiveEnhancerBED = map(lambda x: x.split('_'), enhancer_names_test_pos)
    positiveEnhancerBED = np.array(positiveEnhancerBED)

    y_pred_pos = y_pred[y_pred_pos_ind]
    y_score_neg = y_score_test[y_pred_pos_ind, 0]
    y_score_neg = y_score_neg.T
    y_score_pos = y_score_test[y_pred_pos_ind, 1]
    y_score_pos = y_score_pos.T
    y_score_pos_2 = map(lambda x: round(x, 4), y_score_pos)

    combinedPositiveEnhancers = zip(positiveEnhancerBED[:, 0], positiveEnhancerBED[:, 1], positiveEnhancerBED[:, 2], y_score_pos_2)

    refs = {}
    for line in combinedPositiveEnhancers:
        l = list(line)
        l[3] = 10000*l[3]
        if not l[0] in refs.keys():
            refs[l[0]] = []
        refs[l[0]].append([int(x) for x in l[1:]])

    allData = []
    for ref, val in refs.items():
        sortedCoords = sortCoordinate(val)
        clusters = clusterByOverlap(sortedCoords)
        for cluster in clusters:
            info1 = []
            for i in cluster[2]:
                info1.append(float(val[i][2])/10000)
            allData.append(np.hstack(('00'+ref[3:], cluster[0], cluster[1], round(np.mean(info1),4))))

    for it in range(0, len(allData)):
        allData[it][0] = allData[it][0].replace('00X', '0024')

    allData = np.array(allData, dtype=float)
    allDataSorted = sorted(allData, key = lambda t: t[0])
    allDataSorted_2 = map(lambda x: (int(x[0]), int(x[1]), int(x[2]), x[3]), allDataSorted)
    allDataSorted_2 = np.array(allDataSorted_2, str)

    for it in range(0, len(allDataSorted_2)):
        allDataSorted_2[it][0] = allDataSorted_2[it][0].replace('24', 'X')
        allDataSorted_2[it][0] = 'chr'+ allDataSorted_2[it][0]

    ## Write Predictions to a File
    predictionPositiveOutputFile = out_folder + "/GenomewidePredictedEnhancers_" + options.save_file + ".txt"
    predictionPositiveOutput = open(predictionPositiveOutputFile, 'w')
    predictionPositiveOutput.write("Chromosome\tStart\tEnd\tID\tConfidence\n")
    idx = 1
    # colorCode = []
    for row in allDataSorted_2:
        line = row[0] + '\t' + row[1] + '\t' + row[2] + '\t' + 'E_' + str(idx).rjust(6, '0') + '\t' + row[3]
        # colorCode.append(row[3]*200)
        idx+=1
        predictionPositiveOutput.write(line + '\n')
    predictionPositiveOutput.close()

    ## Write Predictions to a File for Genome Browser
    predictionPositiveOutputFile_2 = out_folder + "/GenomewidePredictedEnhancers_BrowserUpload_" + options.save_file + ".bed"
    predictionPositiveOutput_2 = open(predictionPositiveOutputFile_2, 'w')
    predictionPositiveOutput_2.write("browser position chr1:1-200000\ntrack name=GEP_Enhancer_Prediction description=\"GEP_Enhancer_Prediction\" color=0,60,120 useScore=1 db=hg19\n")
    for row in allDataSorted_2:
        line = row[0] + '\t' + row[1] + '\t' + row[2] + '\t' + '.' + '\t' + str(float(row[3])*1000)
        predictionPositiveOutput_2.write(line + '\n')
    predictionPositiveOutput_2.close()

    print "Finished enhancer predictions !!!\nPredictions saved to: %s" %(str(predictionPositiveOutputFile))

if __name__ == "__main__":
    usage = "usage: %prog [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --save-file <output-filename> --n-estimators <value> --max-depth <value>]"
    parser = OptionParser(usage=usage)
    parser.add_option("", "--output-folder", dest="output_folder", default="../output/", help="An output folder: Default is ../output")
    parser.add_option("", "--feature-columns", dest="data_columns", default="2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", help="Column index containing features in data-file")
    parser.add_option("", "--fold-cross-validation", dest="fold_cross_validation", default=10, help="n-fold: Default:10")
    parser.add_option("", "--save-file", dest="save_file", default="output_file", help="Output filename: Deafult: output_file")
    parser.add_option("", "--n-jobs", dest="n_jobs", default=10, help="No. of CPUs <value>")
    parser.add_option("", "--genome_file", dest="genome_file", default="", help="Genome-wide file: 1st column as rownames and additional columns as tab-delimited features: see example folder for test file")
    parser.add_option("", "--model_file", dest="model_file", default="", help="A file containing model")
    parser.add_option("", "--scaler_file", dest="scalar_file", default="", help="A file containing scaled training data in pkl format: see example folder for help")
    parser.add_option("", "--verbosity", dest="verbosity", default=1, help="Verbosity: Default on: provide 0 to turn off")

    (options, args) = parser.parse_args()

    main(options, args)


