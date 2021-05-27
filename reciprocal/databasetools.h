#pragma once
#ifndef DATABASE_TOOLS
#define DATABASE_TOOLS

#include <vector>
#include <iostream>
#include <string>

#include <fstream>
#include <sstream>
#include <stdio.h>
#include <cstdlib>
#include "math.h"
#include"seal/seal.h"

using namespace std;
using namespace seal;

typedef vector<double> dVec;
typedef vector<vector<double>> dMat;
typedef vector<Ciphertext> cVec;
typedef vector<Plaintext> pVec;
typedef vector<dMat> dMatMat;

/**
 * ParameterPack. As opposed to hardcoding in the values of each parameter, we allow the each method
 * to create a local map containing their supported parameters. 
 */
struct ParameterPack {
    public:
        // This is the number of training iterations for each method
        const unsigned int number_of_iterations;
        // This is the bit length of both the first and last prime in the basis
        const unsigned int sentinel_prime_length;
        // This is the bit length of the middle primes in the basis
        const unsigned int middle_prime_length;
        // This is the number of primes in the middle of the basis. Final basis size is number_of_primes + 2
        const unsigned int number_of_primes;
     ParameterPack(const unsigned int number_of_iterations,
                   const unsigned int sentinel_prime_length,
                    const unsigned int middle_prime_length,
                    const unsigned int number_of_primes)
        : number_of_iterations{number_of_iterations},
            sentinel_prime_length{sentinel_prime_length},
            middle_prime_length{middle_prime_length}, number_of_primes{number_of_primes} {}
};
void AllSum(const Ciphertext& encrypted, Ciphertext& allsum, const unsigned slot_count, shared_ptr<SEALContext> context, const GaloisKeys& gal_keys); 
void ImportData(dMat& Z, string filename);
void CVrandomSampling(dMatMat& CVtrain, dMatMat& CVtest, dMat data);
void ImportDataLR(dMat& Matrix, const string& filename, bool first,  double divisor = 1, char split_char = '\t');
bool is_number(const std::string& s);
#endif
