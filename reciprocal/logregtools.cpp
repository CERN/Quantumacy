#include "logregtools.h"
#include <iostream>
#include <string>
#include <vector>
#include <numeric>
#include <fstream>
#include <sstream>
#include "math.h"
#include "databasetools.h"



double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}
//define one iteration of logistic regression with preprocessing
int LR_iteration(dMat Matrix, dVec& weights, double learning_rate, int n, int nfeatures) {
    //temp grad vector
    dVec grad(nfeatures, 0);
    ////loop over the entries
    for (int i = 0; i < n; i++) {
        //find the value of the sigmoid function
        double sig = sigmoid(-std::inner_product(Matrix[i].cbegin(), Matrix[i].cend(), weights.cbegin(), 0.0));
        //loop over the features, adding to the grad vector:
        for (int j = 0; j < nfeatures; j++) grad[j] += sig * Matrix[i][j];
    }
    //add to the weight vector
    for (int i = 0; i < nfeatures; i++) weights[i] += learning_rate * grad[i] / (1.0 * n);
    return 0;
}
//function combining import & plaintext logistic regression, writing resulting weights to a vector
int LR(dMat Matrix, dVec& weights, int max_iter, double learning_rate) {
    //extract number of records
    int n = Matrix.size();
    //extract number of weights needed (remember we need a constant weight as well)
    int nfeatures = Matrix[0].size();
    //iterate 
    for (int i = 0; i < max_iter; i++) {
        LR_iteration(Matrix, weights, learning_rate, n, nfeatures);
    }
    return 0;
}


int predict_LR(dVec weights, dVec sample, double divisor, double threshold) {
    //calculate a prediction {1,-1} for weights (b0,b1,b2..,) and a sample (z0/div,z1/div,z2/div,...,) 
    //compute probability
    double prob = sigmoid(divisor * divisor * sample[0] * std::inner_product(weights.cbegin(), weights.cend(), sample.cbegin(), 0.0));
    //compare to threshold
    if (prob > threshold) return 1;
    else return -1;
}

double accuracy_LR(dVec weights, dMat test, double divisor,double threshold) {
    double score = 0;
    for (unsigned i = 0; i < test.size(); i++) {
        if (predict_LR(weights, test[i], divisor, threshold) == divisor * test[i][0])score++;
    }
    return 100 * score / test.size();
}

double getAUC(dVec theta, dMat zTest,double divisor) {
    //calculates the AUC when the test set is given by entries of the form (z10/div,z11/div,...,z1d/div)

    dVec xtheta_y1;
    dVec xtheta_y0;

    xtheta_y1.reserve(zTest.size()/2);
    xtheta_y0.reserve(zTest.size()/2);
    
    for (unsigned i = 0; i < zTest.size(); i++) {
        if (divisor * zTest[i][0] == 1.0) {
            xtheta_y1.push_back(divisor * divisor * zTest[i][0] * std::inner_product(zTest[i].cbegin(), zTest[i].cend(), theta.cbegin(), 0.0));
        }
        else {
            xtheta_y0.push_back(divisor * divisor * zTest[i][0] * std::inner_product(zTest[i].cbegin(), zTest[i].cend(), theta.cbegin(), 0.0));
        }
    }
    double auc = 0.0;
    for (unsigned i = 0; i < xtheta_y1.size(); ++i) {
        for (unsigned j = 0; j < xtheta_y0.size(); ++j) {
                if (xtheta_y0[j] <= xtheta_y1[i]) auc++;
            }
        }
    auc /= xtheta_y1.size();
    auc /=xtheta_y0.size();
        
    return auc;

    
}


//one iteration of Nesterov's gradient descent: not great to be extracting dimensions each time? 
int LR_NV_iteration(dMat train, dVec& beta, dVec& v, double alpha, double gamma, int n, int nfeatures) {
    //first find J(v), since this is the only time we need the whole training set:
    dVec J(nfeatures, 0);
    double sig;
    for (int i = 0; i < n; i++) {
        //find the value of the sigmoid function
        sig = sigmoid(-std::inner_product(train[i].cbegin(), train[i].cend(), v.cbegin(), 0.0));/*1 / 2 - 1.20096 * inner_prod(train[i], v) / 8 + 0.81562 * pow(inner_prod(train[i], v) / 8, 3)*/;
        sig /= n;
        //loop over the features, adding to the grad vector:
        for (int l = 0; l < nfeatures; l++) J[l] += sig * train[i][l];
    }
    dVec temp(nfeatures, 0);
    for (int i = 0; i < nfeatures; i++) {

        temp[i] = v[i] + alpha * J[i];
        v[i] = (1 - gamma) * temp[i] + gamma * beta[i];

    }
    beta = temp;
    return 0;
}

int LR_NV(dMat train, dVec& beta, dVec& v, int max_iter) {
    int n = train.size();
    int nfeatures = train[0].size();
    double t = 1.;
    double T, theta;
    for (int i = 0; i < max_iter; i++) {
        T = updatet(t);
        theta = -(t - 1) / T;
        LR_NV_iteration(train, beta, v, 10 / (i + 1), theta, n, nfeatures);
    }
    return 0;
}

//this function calculates t(k+1) from tk. Recall gammat = -(t(k)-1)/t(k+1)
double updatet(double t) {
    double T = (1. + sqrt(1. + 4 * t * t)) / 2.;
    return T;
}

double T1(double X) {
    return 8 * (X + 1) / (X * X + 6 * X + 1);
}

double T2(double X) {
    return (-1.*8) / (X * X + 6 * X + 1);
}

int LR_iteration_lowdeg(dMat Matrix, dVec& weights, double learning_rate, int n, int nfeatures) {
    //temp grad vector
    dVec grad(nfeatures, 0);
    ////loop over the entries
    for (int i = 0; i < n; i++) {
        //find the value of the low degree sigmoid approximation, 
        double sig = 0.5 - 0.15625 * std::inner_product(Matrix[i].cbegin(), Matrix[i].cend(), weights.cbegin(), 0.0);
        //loop over the features, adding to the grad vector:
        for (int j = 0; j < nfeatures; j++) grad[j] += sig * Matrix[i][j];
    }
    //add to the weight vector
    for (int i = 0; i < nfeatures; i++) weights[i] += learning_rate * grad[i] / (1.0 * n);
    return 0;
}

