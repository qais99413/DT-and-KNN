# -*- coding: utf-8 -*-
"""QAIS413.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UD0mj9lSXABMxFY4LOcfNLCuEJ-Qfed7
"""

# import necessary packages.
import numpy as np  
import matplotlib.pyplot as plt
import pandas as pd

#here, we set our dataset
Mydata= pd.read_csv('heart.csv')
Mydata

# here, we declare cloumns types.
Mydata.dtypes

Mydata.size

Mydata["target"].value_counts()

Mydata.isnull().sum()

Mydata.describe().T

heart_dataset = Mydata.copy(deep = True)

heart_dataset[['age','sex','cp','chol', 'exang', 'ca', 'target']] = heart_dataset[['age','sex','cp','chol', 'exang', 'ca', 'target']].replace(0,np.NaN)

## showing the count of Nans
print(heart_dataset.isnull().sum())

p = Mydata.hist(figsize = (30,30))

from sklearn.model_selection import train_test_split #training and testing data split

X=Mydata[['age','sex','cp','chol', 'exang', 'ca']]
y=Mydata["target"]

train_X,test_X,train_Y,test_Y=train_test_split(X,y,test_size=0.3,random_state=0)

train_X,val_X,train_Y,val_Y=train_test_split(train_X,train_Y,test_size=0.3,random_state=0)

len(train_X), len(train_Y), len(test_X), len(test_Y)

train_X.fillna(0)

train_Y.fillna(0)

train_X.head()

#the train data 
train_Y.head()

test_Y.head()

test_X.head()

#Decision Tree

from sklearn.tree import DecisionTreeClassifier 
dt=DecisionTreeClassifier()

train_Y=train_Y.fillna(0)
train_X=train_X.fillna(0)
test_X=test_X.fillna(0)
test_Y=test_Y.fillna(0)

dt=dt.fit(train_X,train_Y)

heart_dataset.isnull().sum()

# also, here we use mean method as another solution to handle null values.
heart_dataset['age'].fillna(heart_dataset['age'].mean(), inplace = True) 
heart_dataset['sex'].fillna(heart_dataset['sex'].mean(), inplace = True) 
heart_dataset['cp'].fillna(heart_dataset['cp'].mean(), inplace = True) 
heart_dataset['chol'].fillna(heart_dataset['chol'].mean(), inplace = True)
heart_dataset['exang'].fillna(heart_dataset['exang'].mean(), inplace = True)
heart_dataset['ca'].fillna(heart_dataset['ca'].mean(), inplace = True)
heart_dataset['target'].fillna(heart_dataset['target'].mean(), inplace = True)

heart_dataset.isnull().sum()

#accuracy
# Predicting results using testing  data set
## dt.score(test_X,train_Y)

pred = dt.predict(test_X)

# Accuracy score
from sklearn.metrics import accuracy_score
accuracy_score(pred,test_Y)

#accuracy
# Predicting results using training data set
pred = dt.predict(train_X)
accuracy_score(pred,train_Y)

# confusion_matrix
import seaborn as sns
sns.set()
from sklearn.metrics import confusion_matrix
from sklearn import metrics

print("\n")
y_pred = dt.predict(test_X)

cnf_matrix = metrics.confusion_matrix(test_Y, y_pred)

p = sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score
def model_evaluation(test_Y, y_pred, model_name):
    acc = accuracy_score(test_Y, y_pred)
    prec = precision_score(test_Y, y_pred)
    rec = recall_score(test_Y, y_pred)
    f1 = f1_score(test_Y, y_pred)
    f2 = fbeta_score(test_Y, y_pred, beta = 2.0)

    results = pd.DataFrame([[model_name, acc, prec, rec, f1, f2]], 
                       columns = ["Model", "Accuracy", "Precision", "Recall",
                                 "F1 SCore", "F2 Score"])
    results = results.sort_values(["Precision", "Recall", "F2 Score"], ascending = False)
    return results

print("\n")

model_evaluation(test_Y, y_pred, "DecisionTree")

from sklearn.metrics import classification_report

val_accuracy = accuracy_score(test_Y, y_pred)
print("\n")
print(f'Accuracy Validation for the Decision Tree is: {val_accuracy}')
print("\n")
target_names = ['no 0', 'yes 1']
print(classification_report(test_Y, y_pred, target_names=target_names))
print("\n")

from sklearn.metrics import auc, roc_auc_score, roc_curve, precision_recall_curve

# Decision Tree
modelTree=DecisionTreeClassifier()
modelTree.fit(train_X,train_Y)
y_pred_prob_Tree = modelTree.predict_proba(test_X)[:,1]
fpr_Tree, tpr_Tree, thresholds_Tree = roc_curve(test_Y, y_pred_prob_Tree)
roc_auc_Tree = auc(fpr_Tree, tpr_Tree)
precision_Tree, recall_Tree, th_Tree = precision_recall_curve(test_Y, y_pred_prob_Tree)

print("\n")

plt.plot([0, 1], [0, 1], 'k--')
 
plt.plot(fpr_Tree, tpr_Tree, label='Tree (area = %0.3f)' % roc_auc_Tree)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curves for DecisionTreeClassifier')
plt.legend(loc='best')
plt.show()
print("\n")

"""# KNN implementation """

from sklearn.neighbors import KNeighborsClassifier

train_scores = []
test_scores = []

for i in range(1,15):
    knn = KNeighborsClassifier(i)
    knn.fit(train_X,train_Y)
    train_scores.append(knn.score(train_X,train_Y))
    test_scores.append(knn.score(train_X,train_Y))

##accuracy
# Predicting results using testing  data set
pred = knn.predict(test_X)
accuracy_score(pred,test_Y)

# Running KNN for various values of n_neighbors and storing results
knn_r_acc = []
for i in range(1,17,1):
    knn = KNeighborsClassifier(n_neighbors=i)
    
    knn.fit(train_X,train_Y)
    
    test_score = knn.score(test_X, test_Y)
    train_score = knn.score(train_X, train_Y)
    
    knn_r_acc.append((i, test_score ,train_score))
df = pd.DataFrame(knn_r_acc , columns=['K','Accuracy Test Score','Accuracy Train Score'])
print("\n")
print(df)
print("\n")

## score that comes from testing  
max_test_score = max(test_scores)
test_scores_ind = [i for i, v in enumerate(test_scores) if v == max_test_score]
print('Max test score {} % and k = {}'.format(max_test_score*100,list(map(lambda x: x+1, test_scores_ind))))

##Visualizing KNN
plt.figure(figsize=(10,5))
p = sns.lineplot( train_scores,marker='*',label='Train Score')
p = sns.lineplot( test_scores,marker='o',label='Test Score')

#  confusion_matrix
import seaborn as sns
sns.set()
from sklearn.metrics import confusion_matrix
from sklearn import metrics
print("\n")
y_pred = knn.predict(test_X)
cnf_matrix = metrics.confusion_matrix(test_Y, y_pred)
p = sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score
def model_evaluation(test_Y, y_pred, model_name):
    acc = accuracy_score(test_Y, y_pred)
    prec = precision_score(test_Y, y_pred)
    rec = recall_score(test_Y, y_pred)
    f1 = f1_score(test_Y, y_pred)
    f2 = fbeta_score(test_Y, y_pred, beta = 2.0)

    results = pd.DataFrame([[model_name, acc, prec, rec, f1, f2]], 
                       columns = ["Model", "Accuracy", "Precision", "Recall",
                                 "F1 SCore", "F2 Score"])
    results = results.sort_values(["Precision", "Recall", "F2 Score"], ascending = False)
    return results


print("\n")
model_evaluation(test_Y, y_pred, "KNN")

from sklearn.metrics import classification_report
val_accuracy = accuracy_score(test_Y, y_pred)
print("\n")
print(f'Accuracy Validation for the KNN is: {val_accuracy}')
print("\n")
target_names = ['no 0', 'yes 1']
print(classification_report(test_Y, y_pred, target_names=target_names))

knn_5 = KNeighborsClassifier(n_neighbors=7)

# fit the model to the training set
knn_5.fit(train_X,train_Y)

# predict on the test-set
y_pred_5 = knn_5.predict(test_X)

print('Model accuracy score with k=7: {0:0.4f}'. format(accuracy_score(test_Y, y_pred_5)))

from sklearn.metrics import auc, roc_auc_score, roc_curve, precision_recall_curve

# Decision Tree
modelKNN = KNeighborsClassifier(n_neighbors=7)
modelKNN.fit(train_X,train_Y)

y_pred_prob_KNN = modelKNN.predict_proba(test_X)[:,1]
fpr_KNN, tpr_KNN, thresholds_KNN = roc_curve(test_Y, y_pred_prob_KNN)
roc_auc_KNN = auc(fpr_KNN, tpr_KNN)
precision_KNN, recall_KNN, th_KNN = precision_recall_curve(test_Y, y_pred_prob_KNN)

print("\n")
plt.plot([0, 1], [0, 1], 'k--')
 
plt.plot(fpr_KNN, tpr_KNN, label='KNN (area = %0.3f)' % roc_auc_KNN)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curves for KNN')
plt.legend(loc='best')
plt.show()