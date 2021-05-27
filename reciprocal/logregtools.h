#pragma once
#include "databasetools.h"

double sigmoid(double x);
int LR_iteration(dMat Matrix, dVec& weights, double learning_rate, int n, int nfeatures);
int LR(dMat Matrix, dVec& weights, int max_iter, double learning_rate);
double getAUC(dVec theta, dMat zTest, double divisor = 1.0);
int predict_LR(dVec weights, dVec sample, double divisor = 1.0, double threshold = 0.5);
double accuracy_LR(dVec weights, dMat test, double divisor = 1.0, double threshold = 0.5);
int LR_NV_iteration(dMat train, dVec& beta, dVec& v, double alpha, double gamma, int n, int nfeatures);
int LR_NV(dMat train, dVec& beta, dVec& v, int max_iter);
double updatet(double t);
double T1(double X);
double T2(double X);
int LR_iteration_lowdeg(dMat Matrix, dVec& weights, double learning_rate, int n, int nfeatures);
