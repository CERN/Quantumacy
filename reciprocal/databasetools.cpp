#include <iostream>
#include <string>
#include <vector>
#include <stdio.h>
#include <fstream>
#include <iomanip>
#include <sstream>

#include "math.h"
#include "seal/seal.h"
#include "time.h"
#include "databasetools.h"

using namespace std;
using namespace seal;

enum ErrorPos {
    NO_ERROR = 0,
    UNABLE_TO_OPEN_FILE = 1,
    UNABLE_TO_READ_FILE = 2,
    FILE_DIMENSION_ERROR = 3,
};

const static std::string  ErrorMessage[4] = {"No error reported.",
                                         "Unable to open the file. Please check the file path and make sure that it is correct.", 
                                         "Unable to read the file. Is the first line malformed?", 
                                         "The number of columns in your file appears to be inconsistent."};


void ImportData(dMat& Matrix, string filename) {
	//open file
	ifstream inFile;
	inFile.open(filename);
	//check file is open
	if (!inFile) {
		cout << ErrorMessage[ErrorPos::UNABLE_TO_OPEN_FILE];
		exit(ErrorPos::UNABLE_TO_OPEN_FILE);
	}

	string line;
	char split_char = '\t';
	unsigned ncolumns{};
	//process first row, moving class to the front and extracting number of columns
	if (getline(inFile, line)) {
		istringstream split(line);
		vector<string> record;
		for (string entry; getline(split, entry, split_char); 
        record.emplace_back(entry));
		ncolumns = record.size();
		vector<double> entry1;
        entry1.reserve(ncolumns);
		entry1.push_back(stod(record[ncolumns - 1]) * 2 - 1);
		for (unsigned i = 0; i < ncolumns - 1; i++) 
            entry1.emplace_back(stod(record[i]));
		//add to matrix
		Matrix.push_back(entry1);
	} else {
		cout << ErrorMessage[ErrorPos::UNABLE_TO_READ_FILE];
        exit(ErrorPos::UNABLE_TO_READ_FILE);
	}
	//process rest of the data
	while (getline(inFile, line)) {
		istringstream split(line);
		vector<string> record;
		for (string entry; getline(split, entry, split_char); record.push_back(entry));
		//record should have the same number of features
		if (record.size() != ncolumns) {
			cout << ErrorMessage[ErrorPos::FILE_DIMENSION_ERROR];
            exit(ErrorPos::FILE_DIMENSION_ERROR);
		}
		//define a new entry
		vector<double> entryi;
        entryi.reserve(ncolumns);
		entryi.push_back(stod(record[ncolumns - 1]) * 2 - 1);
		for (unsigned i = 0; i < ncolumns - 1; i++) entryi.push_back(stod(record[i]));
		//add it to the matrix
		Matrix.push_back(entryi);
	}
}

void AllSum(const Ciphertext& encrypted, Ciphertext& allsum, const unsigned slot_count, shared_ptr<SEALContext> context, const GaloisKeys& gal_keys) {
	Evaluator evaluator(context);
	allsum = encrypted;
	Ciphertext temp = encrypted;
	for (unsigned j = 1; j < slot_count; j++) {
		evaluator.rotate_vector(temp, 1, gal_keys, temp);
		evaluator.add(allsum, temp, allsum);
	}
}


void ImportDataLR(dMat& Matrix, const string& filename, bool first,  double divisor, char split_char) {
	//This function imports data from a .txt file with the following adjustments: changes classification
	//from {0,1} to {-1,1}; moves the classification to the first (0th) column if it is not there; 
	//multiplies each entry 1 - d by the classification; divides all entries by the divisor.
	//first = true: classification is in the first column of the .txt file
	//split_char is the character that splits up entries in the .txt file: default is tab

	//open file

	ifstream inFile;
	inFile.open(filename);
	//check file is open
	if (!inFile) {
		cout << ErrorMessage[ErrorPos::UNABLE_TO_OPEN_FILE];
		exit(ErrorPos::UNABLE_TO_OPEN_FILE);
	}

	string line;
    unsigned ncolumns, j;
	//process first row, moving class to the front and extracting number of columns
	if (getline(inFile, line)) {
		istringstream split(line);
		vector<string> record;
		for (string entry; getline(split, entry, split_char); record.push_back(entry));
		ncolumns = record.size();
		//if the classification is at the beginning, set j = 0. Otherwise, set j= ncolumns-1
		j = first ? 0 : (ncolumns - 1);

		vector<double> entry1;
		//change classification from {0,1} to {-1,1}, and divide entry by divisor
		entry1.push_back((stod(record[j]) * 2 - 1) / (1. * divisor));
		//preprocessing for logistic regression
		if (first) {
			for (unsigned i = 1; i < ncolumns; i++) entry1.push_back(stod(record[i]) * entry1[0]);
		}
		else {
			for (unsigned i = 0; i < ncolumns - 1; i++) entry1.push_back(stod(record[i]) * entry1[0]);
		}
		
		//add to matrix
		Matrix.push_back(entry1);
	}
	else {
		cout << ErrorMessage[ErrorPos::UNABLE_TO_READ_FILE];
        exit(ErrorPos::UNABLE_TO_READ_FILE);
	}
	//process rest of the data
	while (getline(inFile, line)) {
		istringstream split(line);
		vector<string> record;
		for (string entry; getline(split, entry, split_char); record.emplace_back(entry));
		//record should have the same number of features
		if (record.size() != ncolumns) {
		    cout << ErrorMessage[ErrorPos::FILE_DIMENSION_ERROR];
            exit(ErrorPos::FILE_DIMENSION_ERROR);
        }
		//define a new entry
		vector<double> entryi;
		entryi.push_back((stod(record[j]) * 2 - 1)/(1.*divisor));
		if (first) {
			for (unsigned i = 1; i < ncolumns; i++) entryi.push_back(stod(record[i]) * entryi[0]);
		}
		else {
			for (unsigned i = 0; i < ncolumns - 1; i++) entryi.push_back(stod(record[i]) * entryi[0]);
		}
		//add it to the matrix
		Matrix.push_back(entryi);
	}
}


bool is_number(const std::string& s) {
	return !s.empty() && std::all_of(s.begin(), s.end(), ::isdigit);
}

void CVrandomSampling(dMatMat& CVtrain, dMatMat& CVtest, dMat data) {
	/*srand(time(NULL));*/
	dMat train, test;
	int n = data.size();
	int m = floor(n / 5);

	int n_test[5];
	n_test[0] = m;
	n_test[1] = m;
	n_test[2] = m;
	n_test[3] = m;
	n_test[4] = n - 4 * m;

	//label all pieces of vector as "unchosen"
	dVec sort(n, -1);

	//decide where each record will go
	for (int i = 0; i < 5; i++) {
		//start a counter
		int counter = 0;
		while (counter < n_test[i]) {
			//sample a random number from [data.size()]
			int j = rand() % data.size();
			//if it's unchosen, add it to the fold
			if (sort[j] == -1) {
				sort[j] += 1 * (i + 1);
				//now add record to testing fold
				test.push_back(data[j]);
				counter++;
			}		}
		CVtest.push_back(test);
		test.clear();
	}
	//form the training sets. 
	for (int m = 0; m < 5; m++) {
		for (int l = m + 1; l < 5; l++) {
			for (int i = 0; i < n_test[l]; i++) {
				train.push_back(CVtest[l][i]);
			}
		}
		for (int l = 0; l < m; l++) {
			for (int i = 0; i < n_test[l]; i++) {
				train.push_back(CVtest[l][i]);
			}
		}
		CVtrain.push_back(train);
		train.clear();
	}
}
