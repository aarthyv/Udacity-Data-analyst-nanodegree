#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedShuffleSplit
from feature_format import featureFormat, targetFeatureSplit
from time import time
import numpy as np
np.random.seed(42)
import pandas
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV
from sklearn import preprocessing 
import tester

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi". 
### making feature list. poi is the label. Chose features that are likely to matter for pois, including financial and email related features. "email address" was not chosen since it is descriptive and "other" was not chosen as it is ill- defined
features_list = ['poi', 'salary', 'total_payments', 'exercised_stock_options', 'bonus', 'total_stock_value', 'long_term_incentive', 'shared_receipt_with_poi', 'from_this_person_to_poi', 'from_poi_to_this_person', 'restricted_stock', 'restricted_stock_deferred', 'deferred_income', 'director_fees', 'expenses']
## There are financial and email related features of which total_payments and total_stock_value are aggregate features
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
## Exploring data , getting outliers
print "There are", len(data_dict), "entries in the enron email file"
## Names in the enron email file
print data_dict.keys()
## There is one outlier, THE TRAVEL AGENCY IN THE PARK, which is clearly not a name. Removing it
data_dict.pop("THE TRAVEL AGENCY IN THE PARK")
## Total number of features per person
all_features =  data_dict['METTS MARK'].keys()
print "There are", len(data_dict['METTS MARK']), "features for each person in the enron email datafile and they are"
print all_features
## Exploring the names in data_dict wro poi
count_poi = 0
poi_list = []
for user in data_dict:
    if data_dict[user]["poi"] == True:
        count_poi+=1
        poi_list.append(user)
print "There are", count_poi, "pois in the datafile and they are", poi_list
## Looking for persons with NaNs in salary, bonus, total payments and exercised stock options as these are important features
for user in data_dict:
        if data_dict[user]["salary"] == 'NaN' and data_dict[user]["bonus"] == 'NaN' and data_dict[user]["total_payments"] == 'NaN' and data_dict[user]["exercised_stock_options"] == 'NaN' and data_dict[user]["total_stock_value"]:
            print user, "have NaN for salary, bonus, total payments and exercised stock options"
## 6 names had a bunch of NaN values for the major feaures chosen. Exploring all six for all features           
print "Features and values for Chan Ronnie are", data_dict["CHAN RONNIE"]   
print "Features and values for Kenneth Cline are", data_dict["CLINE KENNETH W"]           
print "Features and values for William Powers are", data_dict["POWERS WILLIAM"]           
print "Features and values for Jim Piro are", data_dict["PIRO JIM"]           
print "Features and values for Eugene Lockhart are", data_dict["LOCKHART EUGENE E"]           
print "Features and values for Roderick Hayslett are", data_dict["HAYSLETT RODERICK J"]
## Apart from Eugene Lockhart, all others have large values for restricted stocks, director's fees and deferred payments. Eugene Lockhart has NaN for all feaures and thus qualifies as an outlier.
## Cleaning data to reflect this
data_dict.pop("LOCKHART EUGENE E")
## More analysis of bivariate relationships in data_dict, using salary and bonus
## Analysing for users with high salary and bonus
high_salary_bonus_list = []
for user in data_dict:
    if data_dict[user]["salary"] != 'NaN' and data_dict[user]["salary"] >= 1000000 and data_dict[user]["bonus"] != 'NaN' and data_dict[user]["bonus"] >= 5000000:
        high_salary_bonus_list.append(user)
print "Top 3 persons based on salary and bonus are:", high_salary_bonus_list
## Only 3 users have a salary> 1000000 and bonus > 5000000. Of these 'Total" does not seem to be a real person and is possibly an outlier.
## It could be a data entry error. If so, the values for 'Total" will be orders variant from the 2 next highest users. Verifying this
print "Salary and bonus for Total are", data_dict["TOTAL"]["salary"], "and", data_dict["TOTAL"]["bonus"]
print "Salary and bonus for Kenneth Lay are", data_dict["LAY KENNETH L"]["salary"], "and", data_dict["LAY KENNETH L"]["bonus"]
print "Salary and bonus for Jeffrey Skilling are", data_dict["SKILLING JEFFREY K"]["salary"], "and", data_dict["SKILLING JEFFREY K"]["bonus"]
## Clearly, Total seems to be a calculation and data processing error as it is many magnitudes higher than the next 2 hihest values. Remonving Total
data_dict.pop("TOTAL", 0)
print "There are", len(data_dict), "users in the enron datafile after removing the outliers"
## More analysis of bivariate relationships in data_dict, this time using the aggregate features, total payments  and total stock value
## Analysing for users with high total payments and stock value
high_payment_stock_list = []
for user in data_dict:
    if data_dict[user]["total_payments"] != 'NaN' and data_dict[user]["total_payments"] >= 2500000 and data_dict[user]["total_stock_value"] != 'NaN' and data_dict[user]["total_stock_value"] >= 5000000:
        high_payment_stock_list.append(user)
print"There are", len(high_payment_stock_list), "persons who received total payments > 2500000 and total stock options > 5000000. They are", high_payment_stock_list
## The names on this list look real. No outliers here.
## Now checking how high salary, bonus and total stock options correlate with poi status
high_salary_list = []
high_bonus_list = []
high_total_stock_list = []
for user in data_dict:
    if data_dict[user]["salary"] != 'NaN' and data_dict[user]["salary"] >= 500000:
        high_salary_list.append((user, int(data_dict[user]["salary"])))       
print "People with the highest salary are", high_salary_list
high_salary_list_poi = []
for user in high_salary_list:
    if data_dict[user[0]]["poi"] == True:
        high_salary_list_poi. append(user[0])
print "These", len(high_salary_list_poi),"people making a salary >500000 are also pois", high_salary_list_poi
## 2 of the people with highest salary are also pois.
## Repeating the same for bonus and total stock options
for user in data_dict:
    if data_dict[user]["bonus"] != 'NaN' and data_dict[user]["bonus"] >= 3000000:
        high_bonus_list.append((user, int(data_dict[user]["bonus"])))       
print "People with the highest bonus are", high_bonus_list
high_bonus_list_poi = []
for user in high_bonus_list:
    if data_dict[user[0]]["poi"] == True:
        high_bonus_list_poi. append(user[0])
print "These", len(high_bonus_list_poi), "people making a bonus >3000000 are also pois", high_bonus_list_poi 
for user in data_dict:
    if data_dict[user]["total_stock_value"] != 'NaN' and data_dict[user]["total_stock_value"] >= 5000000:
        high_total_stock_list.append((user, int(data_dict[user]["total_stock_value"])))       
print "People with the highest total stock value are", high_total_stock_list
high_total_stock_list_poi = []
for user in high_total_stock_list:
    if data_dict[user[0]]["poi"] == True:
        high_total_stock_list_poi. append(user[0])
print "These", len(high_total_stock_list_poi), "people holding a total stock value >5000000 are also pois", high_total_stock_list_poi
## Cleaned data is ready for storing data-dict as my_dataset as required for grader
### Task 3: Create new feature(s)
## making a new feature which combines fraction of emails from and to poi and the user
## function to derive fraction of messages from or to poi over all messages
def email_fraction(email_poi, email_all):
    fraction_of_messages = 0.
    if email_poi == 'NaN' or email_poi == 'NaNNaN':
        email_poi == 0
    if email_all == 'NaN' or email_all == 'NaNNaN':
        return fraction_of_messages
    fraction_of_messages = float(email_poi)/float(email_all)
    return fraction_of_messages
## computing fraction of emails from and to poi
## creating a new key:value pair to denote the total fraction of emails from and to pois
for user in data_dict:   
    all_emails = (data_dict[user]["to_messages"]) + (data_dict[user]["from_messages"])
    all_poi = (data_dict[user]["from_poi_to_this_person"]) + (data_dict[user]["from_this_person_to_poi"])
    fraction_to_from_poi = email_fraction(all_poi, all_emails)
    data_dict[user]["fraction_to_from_poi"] = fraction_to_from_poi
## checking whether the addition worked. 
print "The fraction of emails for Jim Piro to and from pois is", data_dict["PIRO JIM"]["fraction_to_from_poi"]
print "The fraction of emails for Ken Lay to and from pois is", data_dict["LAY KENNETH L"]["fraction_to_from_poi"]
## It worked!! Now is this even significant?
poi_email_fraction_count = 0
for user in data_dict:
    if data_dict[user]["fraction_to_from_poi"] != 0:
        poi_email_fraction_count += 1
print "There are", poi_email_fraction_count, "users with a positive fraction of emails to and from pois"
## Correlation with pois using a simple scatter plot to see if the the fraction_to_from_poi is distinct for pis and non-pois
import matplotlib.pyplot
for user in data_dict:
    poi = data_dict[user]["poi"]
    fraction_to_from_poi = data_dict[user]["fraction_to_from_poi"]
    if poi == True:
        matplotlib.pyplot.scatter(poi, fraction_to_from_poi, color = "b")
    else:
        matplotlib.pyplot.scatter(poi, fraction_to_from_poi, color = "r")
matplotlib.pyplot.xlabel("poi label")
matplotlib.pyplot.ylabel("Fraction of emails to and from pois")
matplotlib.pyplot.show()
## Seems like the two data sets are distinct, though significance is hard to interpret. Will use feature selection and ranking to understand significance
## Adding the new feature to features_list to see if that improves the decision tree
features_list.append('fraction_to_from_poi')
print features_list
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
### Extract features and labels from my_dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)   
folds = 1000
cv = StratifiedShuffleSplit(labels, folds, random_state= 42)  
## Setting up 3 classifiers with feature scaling
## Gaussian NB
print "Gaussian NB classifier output:"
NB_clf = Pipeline(steps =[('scaling', preprocessing.MinMaxScaler()), ('classifier', GaussianNB())])
t0 = time()
tester.test_classifier(NB_clf,my_dataset,features_list)
print "Gaussian NB run time:", round(time ()- t0, 3),"s"

## KMeans
print "KMeans classifier output:"
KM_clf = Pipeline(steps =[('scaling', preprocessing.MinMaxScaler()), ('classifier', KMeans(n_clusters = 2))])
t0 = time()
tester.test_classifier(KM_clf,my_dataset,features_list)
print "KMeans run time:", round(time ()- t0, 3),"s"

## Decision tree
print "Decision Tree classifier output:"
DT_clf = Pipeline(steps =[('scaling', preprocessing.MinMaxScaler()), ('classifier', DecisionTreeClassifier())])
t0 = time()
tester.test_classifier(DT_clf,my_dataset,features_list)
print "Decision Tree run time:", round(time ()- t0, 3),"s"
## Accuracy is higher than the other algorithms,  F1 score,precision and recall are moderate 
## Getting feature rankings for all except label to see how they stack
importances = DT_clf.steps[-1][1].feature_importances_
indices = np.argsort(importances)[::-1]
print "Feature Ranking"
for i in range(10):
    print "{} {}: {}". format(i+1, features_list[1:][indices[i]], importances[indices[i]])
### The new feature created is 4th in the importances, it must be of some significance. DT_clf has better overall evaluation metrics than NB_clf. Needs tuning
## Will use k-best algorithm to select features
from sklearn.feature_selection import SelectKBest
select = SelectKBest(k = 10)
## Removinf poi as a feature for k best
features_list_k = features_list[1:]
kbest_features = select.fit(features, labels)
kbest_scores = kbest_features.scores_
kbest_feature_score = zip(features_list_k[1:], kbest_scores)
## converting to array for sorting by score
selected_features = pandas.DataFrame(kbest_feature_score, columns =['Feature', 'Score'])
selected_features = selected_features.sort_values(by ='Score', ascending = False)
print "The top 10 KBest features selected from features_list are"
print selected_features.to_string(index = False)
## KBest features will be used with Decision tree, again, the new features created 
features_list = ['poi', 'bonus', 'long_term_incentive', 'total_stock_value', 'total_payments', 'director_fees', 'shared_receipt_with_poi', 'restricted_stock_deferred', 'exercised_stock_options', 'from_this_person_to_poi', 'fraction_to_from_poi', 'restricted_stock', 'from_poi_to_this_person', 'expenses', 'deferred_income']
print "Decision Tree classifier with KBest features output:"
DT_K_clf = Pipeline(steps =[('scaling', preprocessing.MinMaxScaler()), ('classifier', DecisionTreeClassifier(random_state = None))])
t0 = time()
tester.test_classifier(DT_K_clf,my_dataset,features_list)
print "Decision Tree run time:", round(time ()- t0, 3),"s"
##  KBest features do not really change the metrics much. Will tune the DT algorithm and bost to see if metrics improve
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
## Tuning Gaussian NB with PCA ti reduce dimensions. Grid Search CV has no parameters to set for NB
print "Gaussian NB classifier with PCA output:"
NB_PCA_clf = Pipeline(steps =[('scaling', preprocessing.MinMaxScaler()),('pca', PCA(copy = True, n_components = 0.95, whiten = False)), ('gaussian', GaussianNB())])
t0 = time()
tester.test_classifier(NB_PCA_clf,my_dataset,features_list)
print "Gaussian NB with PCA run time:", round(time ()- t0, 3),"s"
## PCA drastically improves the performance of the Gaussian NB algorithm!!

## Using PCA and Gridsearch CV to tune decision tree
print "Decision Tree classifier with PCA output:"
DT_PCA_clf = Pipeline(steps =[('scaling', preprocessing.MinMaxScaler()), ('pca', PCA(copy = True, n_components = 0.95, whiten = False)), ('classifier', DecisionTreeClassifier(random_state = None))])
t0 = time()
tester.test_classifier(DT_PCA_clf,my_dataset,features_list)
print "Decision Tree run time:", round(time ()- t0, 3),"s"
## PCA reduces the effectiveness of the DT classifier.
## Tuning with Grid Search CV
## Cut out to save time
param_grid = [{'classifier__min_samples_split': [2, 4],
          'classifier__max_depth': [None, 3, 10],
          'classifier__max_features': [None, 'auto', 'log2'],
          'classifier__criterion': ['gini', 'entropy'],
          'classifier__splitter': ['best', 'random'],
          'classifier__min_weight_fraction_leaf': [0, 0.1],
          'classifier__class_weight': [{1: 1, 0: 0.5}, {1: 0.8, 0: 0.3}]
    }]
DT_grid_clf = Pipeline(steps =[('scaling', preprocessing.MinMaxScaler()), ('classifier', DecisionTreeClassifier(random_state = None))])
DT_grid = GridSearchCV(DT_grid_clf, param_grid, cv=cv, scoring = 'f1')
DT_grid.fit(features, labels)
print "Decision Tree tuning by GridSearchCV"
print "Best parameters:", DT_grid.best_params_, "and Best score:", DT_grid.best_score_
## Running decision tree algorithm with best features
DT_best_clf = DT_K_clf.set_params(**DT_grid.best_params_)
t0 = time()
tester.test_classifier(DT_best_clf,my_dataset,features_list)
print "Decision Tree run time:", round(time ()- t0, 3),"s"
### Do not hit the precision and recall desired. Will boost this with Adaboost
DT_best_params = DT_best_clf.steps[-1][1].get_params()
## Using these parameters, do a grid serachCV for best Adaboost params
AB_params = [{'classifier__base_estimator': [DecisionTreeClassifier(**DT_best_params)],
'classifier__n_estimators': [5, 10, 50, 70],
'classifier__learning_rate': [0.5, 1, 2]
}]
AB_grid_clf = Pipeline(steps = [('scaling', preprocessing.MinMaxScaler()), ('classifier', AdaBoostClassifier(random_state = None))])
AB_grid = GridSearchCV(AB_grid_clf, AB_params, cv = cv, scoring = 'f1')
AB_grid.fit(features, labels)
print "AdaBoost tuning of Decision Tree by GridSearchCV"
print "Best parameters:", AB_grid.best_params_, "and Best score:", AB_grid.best_score_
## Running decision tree algorithm with best features
AB_best_clf = AB_grid_clf.set_params(**AB_grid.best_params_)
t0 = time()
tester.test_classifier(AB_best_clf,my_dataset,features_list)
print "AdaBoost run time:", round(time ()- t0, 3),"s"
## AdaBoosting does not help improve the tuned Decision tree 
## I will choose the GridSearchCV tuned  Decision Tree, which gave the best performance as my best classifier
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
dump_classifier_and_data(DT_best_clf, my_dataset, features_list)