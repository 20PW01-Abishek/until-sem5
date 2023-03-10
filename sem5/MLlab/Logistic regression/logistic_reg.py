import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def getCols(df):
    l = LabelEncoder()
    l.fit(df['diagnosis'])
    df['diagnosis'] = l.transform(df['diagnosis'])
    X = df.drop(['id', 'diagnosis'], axis=1)
    Y = df['diagnosis'].values
    return X,Y

def removeMulticollinearity(X,Y):
    Xnames = X.columns
    final_features = [x for x in Xnames]
    p = df[Xnames].corr().values.tolist()
    for i in range(len(p)):
        for j in range(i+1, len(p)):
            if abs(p[i][j]) > 0.7 and Xnames[i] in final_features:
                final_features.remove(Xnames[i])
    print("\n\nFeatures before removing multicollinearity:\n", Xnames)
    print("\n\nFeatures after removing multicollinearity:\n", final_features)
    return final_features

def outlier_treatment(df, feature):
    q1, q3 = np.percentile(df[feature], [25, 75])
    IQR = q3 - q1 
    lower_range = q1 - (1.5 * IQR) 
    upper_range = q3 + (1.5 * IQR)
    to_drop = df[(df[feature]<lower_range)|(df[feature]>upper_range)]
    df.drop(to_drop.index, inplace=True)

df = pd.read_csv("bc.csv")
print(df.describe())
X,Y=getCols(df)
final_features=removeMulticollinearity(X, Y)
for i in final_features:
    outlier_treatment(df, i)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

def sigmoid(Z):
    Z = np.array(Z, dtype='float64')
    return 1/(1 + np.exp(-Z))

def logisticRegression(X, Y, learningRate, iterations):
    X = np.vstack((np.ones((X.shape[0],)), X.T)).T
    print(X)
    wT=np.zeros((X.shape[1], 1)).T
    costs = []
    for i in range(iterations):
        wTx = np.dot(wT, X.T)
        A = sigmoid(wTx)
        wPred = np.array([1 if x >= 0.5 else 0 for x in A[0]])
        costs.append(np.sum(np.square(wPred - Y)))
        dW = np.dot(X.T, (wPred - Y)) / (Y.size) 
        wT = wT - learningRate * dW
    return wT, np.array(costs)

W, costs = logisticRegression(X_train, Y_train, 0.000001,10000)
print(W)

def predict(X, Y, W):
    X = np.vstack((np.ones((X.shape[0],)), X.T)).T
    wTx = np.dot(W, X.T)
    A = sigmoid(wTx)
    wPred = np.array([1 if x >= 0.5 else 0 for x in A[0]])
    print("Accuracy: ", np.sum(wPred == Y)/Y.size)
    print("Precision for 0: ", np.sum(wPred == 0)/np.sum(Y == 0))
    print("Precision for 1: ", np.sum(wPred == 1)/np.sum(Y == 1))
    wPred = ['Malignant' if i==0 else 'Benign' for i in wPred]
    return wPred
dP = predict(X_test, Y_test, W)
print(dP)
