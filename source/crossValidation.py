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
import os
import sys
import random
from optparse import OptionParser
import warnings
from GEPmodules import np, myClassifiers, myScores, myDataSplitterFold, interpolator, myStats, performScaling, myPlot

warnings.filterwarnings("ignore")

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
    out_folder = options.output_folder
    data_cols = options.data_columns
    label_col = int(options.label_column)

    if int(options.verbosity) > 0:
        print "Options: ", options
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        print "output_folder is", options.output_folder, "\n"

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

    # Define lists to store ML measures
    scores = list()
    train_score = list()    #train_score
    test_score=list()   #test_score
    accuracySelectedCalssifier = list()   #Accuracy
    prec = list()   #Precision
    rec = list()    #Recall
    areaRoc = list()    #AUC
    fscore = list() #F-measure

    # For random classification
    accuracyRandomClassifier = list()
    recRand = list()
    precRand = list()
    fscoreRand = list()

    # For Plotting ROC-curve
    random_mean_tpr_nFold = 0.0
    random_mean_fpr_nFold = np.linspace(0, 1, 100)
    random.seed(80)

##########################################################################
# Training
##########################################################################
    #Generate object for n-fold CV
    skf = myDataSplitterFold(labelDataShuffled, n_folds=int(options.fold_cross_validation))
    for feature_train_index, feature_test_index in skf:
        rand_list = list()
        featureDataTrain, featureDataTest = featureDataShuffled[feature_train_index], featureDataShuffled[feature_test_index]
        labelDataTrain, labelDataTest = labelDataShuffled[feature_train_index], labelDataShuffled[feature_test_index]

        if int(options.verbosity) > 0:
            print featureDataTrain, featureDataTest, "\n"

        #choose a method of your choice
        if options.method == "SVM":
            C = float(10**options.SVM_C)
            gamma = float(10**options.SVM_gamma)
            myClassifier = myClassifiers.svm(kernel='rbf',probability=True, C=C, gamma = gamma)
            if int(options.verbosity) > 0:
                print "Method chosen is: SVM\n"
        else:
            n_estimators = int(options.RF_n_estimators)
            max_depth = float(options.RF_max_depth)
            myClassifier = myClassifiers.RF(n_estimators=n_estimators, max_depth=max_depth)
            if int(options.verbosity) > 0:
                print "Method chosen is: Random Forest\n"

        # Calculate Scores for the Method Selected
        scores.append(myClassifier.fit(featureDataTrain, labelDataTrain).score(featureDataTest, labelDataTest))
        y_pred = myClassifier.predict(featureDataTest)
        predicted_label_score = myClassifier.predict_proba(featureDataTest)
        predicted_label_score = np.around(predicted_label_score, decimals=2)
        accuracySelectedCalssifier.append(myScores.accuracy_score(labelDataTest, y_pred))

        # Calculate accuracy for each cross-validation (classification + Random classification)
        for i in range(0,len(y_pred)):
            rand_list.append(random.randint(0, 1))

        y_rand = np.array(rand_list)
        accuracyRandomClassifier.append(myScores.accuracy_score(labelDataTest, y_rand))

        # Calculate precision, recall, fscore for each cross-validation (classification + Random classification)
        prec.append(myScores.precision_score(labelDataTest, y_pred, average='micro'))
        rec.append(myScores.recall_score(labelDataTest, y_pred, average='micro'))
        fscore.append(myScores.fbeta_score(labelDataTest, y_pred, average='micro', beta=0.5))
        precRand.append(myScores.precision_score(labelDataTest, y_rand, average='micro'))
        recRand.append(myScores.recall_score(labelDataTest, y_rand, average='micro'))
        fscoreRand.append(myScores.fbeta_score(labelDataTest, y_rand, average='micro', beta=0.5))
        areaRoc.append(myScores.roc_auc_score(labelDataTest, predicted_label_score[:,1]))

        # Generate ROC curve for each cross-validation
        fpr, tpr, thresholds = myScores.roc_curve(labelDataTest, predicted_label_score[:,1], pos_label = 1)  #Pos level for positive class
        random_mean_tpr_nFold += interpolator(random_mean_fpr_nFold, fpr, tpr)
        random_mean_tpr_nFold[0] = 0.0
        train_score.append(myClassifier.fit(featureDataTrain, labelDataTrain).score(featureDataTrain, labelDataTrain))
        test_score.append(myClassifier.fit(featureDataTest, labelDataTest).score(featureDataTest, labelDataTest))

    random_mean_tpr_nFold /= int(options.fold_cross_validation)
    random_mean_tpr_nFold[-1] = 1.0
    random_mean_auc_nFold = myScores.auc(random_mean_fpr_nFold, random_mean_tpr_nFold)

    if int(options.verbosity) > 0:
        print "scores are:\n", scores, "\n"

    combined_measures = zip(accuracySelectedCalssifier, accuracyRandomClassifier, prec, precRand, rec, recRand, fscore, fscoreRand, areaRoc)
    if int(options.verbosity) > 0:
        print "######################################################"
        print "1. Length Accuracy Selected Classifier", len(accuracySelectedCalssifier)
        print "2. Length Accuracy Random Classifier", len(accuracyRandomClassifier)
        print "3. Length Precision Selected Classifier", len(prec)
        print "4. Length Precision Random Classifier", len(precRand)
        print "######################################################"

##########################################################################
# Output and plotting
##########################################################################
    nFold_result_file = options.output_folder + "/" +"measures_" + options.save_file + ".txt"
    predictedOutput = open(nFold_result_file, 'w')
    predictedOutput.write("Accuracy\tAccuracy_Rand\tPrecision\tPrecision_Rand\tRecall\tRecall_Rand\tFscore\tFscore_rand\tareaRoc\n")
    for i in combined_measures:
        line = '\t'.join(str(x) for x in i)
        predictedOutput.write(line + '\n')
    mean_measures = str(np.mean(accuracySelectedCalssifier)) + "\t" + str(np.mean(accuracyRandomClassifier)) + "\t" + str(np.mean(prec)) + "\t" + str(np.mean(precRand)) + "\t" + str(np.mean(rec)) + "\t" + str(np.mean(recRand)) + "\t" + str(np.mean(fscore)) + "\t" + str(np.mean(fscoreRand)) + "\t" + str(np.mean(areaRoc))
    if int(options.verbosity) >0:
        print "All the average measures are: ", mean_measures, "\n"
    predictedOutput.write(mean_measures + '\n')

    # Get variance across the cross-validation scores
    predictedOutput.write ("Mean score n-fold: {0:.3f} (+/-{1:.3f})".format(np.mean(scores), myStats.sem(scores)) + '\n')
    predictedOutput.write ("Mean train score: {0:.3f} (+/-{1:.3f})".format(np.mean(train_score), myStats.sem(train_score)) + '\n')
    predictedOutput.write ("Mean test score: {0:.3f} (+/-{1:.3f})".format(np.mean(test_score), myStats.sem(test_score)) + '\n')
    predictedOutput.close()

    if int(options.verbosity)>0:
        print "Area Under the ROC : ", areaRoc, "mean AUC", np.mean(areaRoc)

    # Print ROC curve for n-fold cross-validation
    myPlot.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Standard')
    myPlot.plot(random_mean_fpr_nFold, random_mean_tpr_nFold, 'k--',label='Random Forest (area = %0.2f)' % random_mean_auc_nFold, lw=2, color=(0.45, 0.42, 0.18)) #Plot mean ROC area in cross validation
    myPlot.xlim([-0.05, 1.05])
    myPlot.ylim([-0.05, 1.05])
    myPlot.xlabel('False Positive Rate')
    myPlot.ylabel('True Positive Rate')
    myPlot.title('ROC: fold_cross_validation fold CV')
    myPlot.legend(loc="lower right")

    # Save plot in svg format
    ROC_curve_figure_file =  options.output_folder + "/" + "ROC-curve_" + options.save_file + ".svg"
    myPlot.savefig(ROC_curve_figure_file, bbox_inches='tight', pad_inches=0.2)
    myPlot.show()
    myPlot.close()

##########################################################################
# Options
##########################################################################
if __name__ == "__main__":
    usage = "\n\n##############################################\n python %prog [required: --data-file <Filename> --feature-columns <feature column indices> --label-column <label column>] [optional: --output-folder <Output_folder> --fold-cross-validation <no. of cross-validation-folds> --save-file <output-filename> --n-estimators <value> --max-depth <value>]\n##############################################\n"
    parser = OptionParser(usage=usage)
    parser.add_option("", "--data-file", dest="data_file", default="", help="A tab delimited file: 1st column as rownames, 2nd column as class and additional columns as tab-delimited features: see example folder for test file")
    parser.add_option("", "--output-folder", dest="output_folder", default="../output/", help="An output folder: Default is ../output")
    parser.add_option("", "--label-column", dest="label_column", default=1, help="Column index containing class of instances: Default: 1 (2nd column)")
    parser.add_option("", "--feature-columns", dest="data_columns", default="2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", help="Column index containing features in data-file")
    parser.add_option("", "--fold-cross-validation", dest="fold_cross_validation", default=10, help="n-fold: Default:10")
    parser.add_option("", "--save-file", dest="save_file", default="output_file", help="Output filename: Deafult: output_file")
    parser.add_option("", "--RF_n-estimators", dest="RF_n_estimators", default=100, help="RF_n_estimator list: Default: 100")
    parser.add_option("", "--RF_max-depth", dest="RF_max_depth", default=5, help="RF_max_depth=<value>: Default:5")
    parser.add_option("", "--n-jobs", dest="n_jobs", default=10, help="no. of cores: Default:10")
    parser.add_option("", "--SVM_C", dest="SVM_C", default=8, help="SVM_C <power of 10>: Default: 8 == 100000000.0")
    parser.add_option("", "--SVM_gamma", dest="SVM_gamma", default=-2, help="SVM_gamma: <power of 10> default: -2 == 0.01")
    parser.add_option("", "--method", dest="method", default="RF", help="Method: 'RF': Random Forest, 'SVM': Support Vector Machine: Default: RF")
    parser.add_option("", "--verbosity", dest="verbosity", default=1, help="Verbosity: Default on: provide 0 to turn off")
    (options, args) = parser.parse_args()
    main(options, args)
