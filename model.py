#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:17:23 2021

@author: ismaellopezbahena
"""
#first we import pandas 
import pandas as pd
#let's read the csv of data analysis
df = pd.read_csv('data-eda.csv')
#description
df.describe()
#info
df.info()
#drop the unnecessary
df = df.drop(['name', 'location', 'link', 'divisa', 'Delegacion'], axis=1) 
#get dumies
df_model = pd.get_dummies(df)

#models

#lets split our data in X and y
X = df_model.drop(['price MP'], axis=1).values
y = df_model['price MP'].values


#if we want to scale our data
from sklearn.preprocessing import scale
X = scale(X)
y = scale(y)

#split our train and test data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#1st model: Linear Regresison
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

lr = LinearRegression()

lr.fit(X_train, y_train)

lr.score(X_test, y_test)

#let's try croos validation with 5 folds and take the mean
import numpy as np

np.mean(cross_val_score(lr, X_train, y_train, scoring = 'neg_mean_squared_error', cv=5))


# 2nd model: Ridge Regression
from sklearn.linear_model import Ridge

ridge = Ridge(random_state=0)

ridge.fit(X_train, y_train)

ridge.score(X_test, y_test)

np.mean(cross_val_score(ridge, X_train, y_train, scoring = 'neg_mean_squared_error', cv=5))

#3rd model: Lasso Regression
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt

lasso= Lasso(random_state=0)

lasso.fit(X_train, y_train)

lasso.score(X_test, y_test)

np.mean(cross_val_score(lasso, X_train, y_train, scoring='neg_mean_squared_error' , cv=5))

#best alpha
alpha=[]
error=[]

for i in np.linspace(0,1,11):
    alpha.append(i)
    lasso=Lasso(alpha=i)
    error.append(np.mean(cross_val_score(lasso, X_train, y_train, scoring='neg_mean_squared_error' , cv=5)))
    
plt.plot(alpha, error)

#4th model: Gradient Boosting Reegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error as MSE

gbr = GradientBoostingRegressor(random_state=0)

gbr.fit(X_train, y_train)

gbr.score(X_test, y_test)

np.mean(cross_val_score(gbr, X_train, y_train, scoring='neg_mean_squared_error' , cv=5))


#Hyperparameter tuning

from sklearn.model_selection import GridSearchCV 

#ridge choosing alpha
param_grid = {'alpha':  np.linspace(0,1,11), 'fit_intercept':[True, False], 'normalize': [True, False]}

ridge_cv = GridSearchCV(ridge, param_grid= param_grid, scoring='neg_mean_squared_error', cv=5)
result_ridge=ridge_cv.fit(X_train, y_train)
print('Best Score: %s' % result_ridge.best_score_)
print('Best Hyperparameters: %s' % result_ridge.best_params_)

#we discart lasso
#lasso_cv = GridSearchCV(lasso, param_grid= param_grid, scoring='neg_mean_squared_error', cv=5)
#result_lasso=lasso_cv.fit(X_train, y_train)
#print('Best Score: %s' % result_lasso.best_score_)
#print('Best Hyperparameters: %s' % result_lasso.best_params_)

#Gradient Boosting Reegressor
param_gbr = {'n_estimators':[100,300,500], 'max_depth':[2,3,4], 'max_features':[ 'sqrt', 'log2']}

gbr_cv = GridSearchCV(gbr, param_grid= param_gbr, scoring='neg_mean_squared_error', cv=5 )
result_gbr = gbr_cv.fit(X_train, y_train)
print('Best Score: %s' % result_gbr.best_score_)
print('Best Hyperparameters: %s' % result_gbr.best_params_)


#evalueting each model
ypred_lr = lr.predict(X_test)
ypred_rid = ridge_cv.best_estimator_.predict(X_test)
#ypred_lasso = lasso.predict(X_test)
ypred_gbr = gbr_cv.best_estimator_.predict(X_test)

print("Tuned Linear Regression RMSE: {}".format(MSE(y_test, ypred_lr)**(1/2)))

print("Tuned Ridge Regression RMSE: {}".format(MSE(y_test, ypred_rid)**(1/2)))

#print("Tuned Lasso Regression RMSE: {}".format(MSE(y_test, ypred_lasso)**(1/2)))

print("Tuned Gradient Boosting Reegressor RMSE: {}".format(MSE(y_test, ypred_gbr)**(1/2)))

