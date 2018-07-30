#! /usr/bin/env python
##########################################################################
"""
    This file is included in GEP and is based on source code from
    the scikit-learn library. The original code is released under
    the BSD 3 clause license and, as required by this license, the
    original copyright notice is included here. All changes to the
    original code are released under the Apache License, Version 2.0
    and a copyright notice for these is also included below.

    Original code license:

    Copyright (c) 2007-2013 The scikit-learn developers.
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    a. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    b. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
    c. Neither the name of the Scikit-learn Developers  nor the names of
    its contributors may be used to endorse or promote products
    derived from this software without specific prior written
    permission.


    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    DAMAGE.

    Authors: Gilles Louppe, Brian Holt
    License: BSD 3

    GEP code licence:

    Defines Functions and Imports Essential Python Modules
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
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Author: Shalu Jhanwar
    License: GPL version 3
"""
##########################################################################

print "Checking Required Modules..........."

module = "numpy"
try:
    np = __import__(module, globals(), locals(), [], -1)
    print module + " Found"
    np.random.seed(0)
except ImportError:
    print module + " : Module Not Found. Please install the module."
    exit()

module = "matplotlib"
try:
    matplotlib = __import__(module, globals(), locals(), ['pyplot'], -1)
    myPlot = matplotlib.pyplot
    print module + " Found"
except ImportError:
    print module + " : Module Not Found. Please install the module."
    exit()

module = "sklearn"
try:
    sklearn = __import__(module, globals(), locals(), ['preprocessing', 'ensemble', 'learning_curve', 'grid_search', 'svm', 'metrics', 'externals','cross_validation'], -1)
    myScaler = sklearn.preprocessing.StandardScaler()
    class classifiers:
        pass
    myClassifiers = classifiers
    myClassifiers.RF = sklearn.ensemble.RandomForestClassifier
    myClassifiers.svm = sklearn.svm.SVC
    myLearningCurve = sklearn.learning_curve.learning_curve
    myOptimizer = sklearn.grid_search.GridSearchCV
    myScores = sklearn.metrics
    myDataSplitter = sklearn.cross_validation.StratifiedShuffleSplit
    myDataSplitterFold = sklearn.cross_validation.StratifiedKFold
    myDataLogger = sklearn.externals.joblib
    mc = sklearn.metrics.matthews_corrcoef
    confM = sklearn.metrics.confusion_matrix

    print module + " Found"
except ImportError:
    print module + " : Module Not Found. Please install the module."
    exit()

module = "scipy"
try:
    scipy = __import__(module, globals(), locals(), ['stats', 'interp'], -1)
    myStats = scipy.stats
    interpolator = scipy.interp
    print module + " Found"
except ImportError:
    print module + " : Module Not Found. Please install the module."
    exit()

""" Checks Classifier Accuracy on Train Data """
def sanityCheck(X, y, verbosity):
    myClassifier = myClassifiers.RF().fit(X, y)
    prediction = myClassifier.predict(X)
    if verbosity > 0:
        print "Classification Report After Sanity Check: \n";
        print myScores.classification_report(y, prediction)
        print "Accuracy After Sanity Check: %.6f" %myScores.accuracy_score(y,prediction)
    if myScores.accuracy_score(y, prediction) >= 0.99:
        return 1
    else:
        return 0

""" Brings Train and Test Data at the Same Scale """
def performScaling(feature_data, labels):
    feature_data_scaled = myScaler.fit_transform(feature_data)
    shuffled_indices = np.random.permutation(len(feature_data_scaled))
    feature_data_shuffled = feature_data_scaled[shuffled_indices]
    labels_shuffled = labels[shuffled_indices]
    return labels_shuffled, feature_data_shuffled, shuffled_indices, myScaler

""" Brings Train and Test Data at the Same Scale Using a File """
def rescaleTestData(feature_data, labels, scalerFile):
    myScaler = myDataLogger.load(scalerFile)
    feature_data_scaled = myScaler.transform(feature_data)
    shuffled_indices = np.random.permutation(len(feature_data_scaled))
    feature_data_shuffled = feature_data_scaled[shuffled_indices]
    labels_shuffled = labels[shuffled_indices]
    return labels_shuffled, feature_data_shuffled, shuffled_indices

""" Brings Genome Data to the Same Scale As of Train Data """
def rescaleGenomeData(test_data, scalerFile):
    scaler = myDataLogger.load(scalerFile)
    test_data = scaler.transform(test_data)
    shuffled_indices = np.random.permutation(len(test_data))
    test_dataScaled = test_data[shuffled_indices]
    return test_dataScaled, shuffled_indices

""" Assmebles and Partitions Data into Train and Test Set """
def myDataShuffler(Xtrain, Ytrain, indices, percentage_select, verbosity):
    indices_1 = indices[Ytrain[indices]!=0]
    indices_0 = indices[Ytrain[indices]!=1]
    n_test = round((indices.size*percentage_select)/2) #No. of instances for each class #SHUFFLE DATA X and Y for splitting purpose
    n_test = int(n_test)
    if verbosity > 0:
        print "Number of Instances In Each Class: ", n_test
    test_indices = np.concatenate([(indices_1[:n_test]), (indices_0[:n_test])])
    np.random.shuffle(test_indices)
    X_test = Xtrain[test_indices]
    y_test = Ytrain[test_indices]

    train_indices = np.concatenate([(indices_1[n_test:]), (indices_0[n_test:])])
    np.random.shuffle(train_indices)
    X_train = Xtrain[train_indices]
    y_train = Ytrain[train_indices]

    if verbosity > 0:
        print "Number of Train Data Samples: ", X_test.shape[0]
        print "Number of Test Data Samples: ", X_train.shape[0]

    return X_train, y_train, X_test, y_test

""" Performs Parameter Optimisation Random Forest Classifier"""
def findParamaters(cv, X_train, y_train, n_estimators, max_depth_start, max_depth_end, n_jobs, verbosity):
    max_depth = np.linspace(max_depth_start, max_depth_end, 5) #By default
    n_estimators = n_estimators #n_estimator
    n_jobs = n_jobs #no_of_CPU
    myClassifier = myOptimizer(estimator=myClassifiers.RF(random_state=0), cv=cv, param_grid=dict(n_estimators=n_estimators, max_depth=max_depth), n_jobs=n_jobs, scoring='f1')
    myClassifier.fit(X_train, y_train)

    #Let's look at the best estimator that was found after optimization
    if verbosity > 0:
        print "Best Estimator: \n"
        print myClassifier.best_estimator_ , "\n"
    return myClassifier.best_estimator_.max_depth, myClassifier.best_estimator_.n_estimators

""" Performs Parameter Optimisation Support Vector Machine Classifier"""
def findParamatersSVM(cv, X_train, y_train, param_grid, n_jobs, verbosity):
    n_jobs = n_jobs #no_of_CPU
    myClassifier = myOptimizer(estimator=myClassifiers.svm(), cv=cv, param_grid=param_grid, n_jobs=n_jobs, scoring='f1')
    myClassifier.fit(X_train, y_train)
    #Let's look at the best estimator that was found after optimization
    if verbosity > 0:
        print "Best Estimator: \n"
        print myClassifier.best_estimator_ , "\n"
    return myClassifier.best_estimator_.C, myClassifier.best_estimator_.gamma

""" Plots the Learning Curve """
def plotLearningCurve(estimator, title, X_train, y_train, cv, verbosity):
    ylim = None
    n_jobs = 1
    train_sizes=np.linspace(0.1, 1.0, 5)
    if verbosity > 0:
        print "Cross Validation Value is ", cv
    myPlot.figure()
    myPlot.title(title)
    if ylim is not None:
        myPlot.ylim(*ylim)
    myPlot.xlabel("Training")
    myPlot.ylabel("Score")
    train_sizes, train_scores, test_scores = myLearningCurve(estimator, X_train, y_train, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, scoring='f1')
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    myPlot.grid()
    myPlot.fill_between(train_sizes, train_scores_mean - train_scores_std,train_scores_mean + train_scores_std,alpha=0.1,color="r")
    myPlot.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="g")
    myPlot.plot(train_sizes, train_scores_mean, 'o-', color="r",label="Training score")
    myPlot.plot(train_sizes, test_scores_mean, 'o-', color="g",label="Cross-validation score")
    myPlot.legend(loc="best")
    return myPlot

""" Plots the ROC Curve """
def plotROC(estimator, X_test, y_test, y_pred, verbosity):
    y_score = estimator.predict_proba(X_test)
    y_score = np.around(y_score, decimals=2)

    if verbosity > 0:
        accuracy = myScores.accuracy_score(y_test, y_pred)
        print "Accuracy Complete Dataset: ", accuracy

    #Generate ROC curve for each cross-validation
    fpr, tpr, thresholds = myScores.roc_curve(y_test, y_score[:,1], pos_label = 1)  #Pos lebel for positive class
    random_mean_auc = myScores.auc(fpr, tpr)
    myPlot.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Standard')
    myPlot.plot(fpr, tpr, 'k--',label='Random Forest (area = %0.2f)' % random_mean_auc, lw=2, color=(0.45, 0.42, 0.18))
    myPlot.xlim([-0.05, 1.05])
    myPlot.ylim([-0.05, 1.05])
    myPlot.xlabel('False Positive Rate')
    myPlot.ylabel('True Positive Rate')
    myPlot.title('Receiver Operating Characteristic Curve')
    myPlot.legend(loc="lower right")
    return myPlot

""" Sort and Cluster the coordinates """
padding = 0
def sortCoordinate(d):
    coords = []
    i = 0
    for coord in d:
        coords.append(('s',coord[0] - padding,i))
        coords.append(('e',coord[1] + padding))
        i += 1
    coords.sort(key = lambda x : x[0], reverse = True)
    coords.sort(key = lambda x : x[1])
    return coords

def clusterByOverlap(c):
    count = 0
    posA = 0
    out = []
    currentData = []
    for pos in c:
        if count == 0:
            posA = pos[1]
        if pos[0] == 's':
            count += 1
            currentData.append(pos[2])
        if pos[0] == 'e':
            count -=1
        if count == 0:
            out.append((posA + padding, pos[1] - padding, currentData))
            currentData = []
    return out

