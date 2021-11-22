#include "algorithm"
#include "databasetools.h"
#include "logregtools.h"
#include "threadpool.hpp"
#include "seal/seal.h"
#include "examples.h"
#include <iostream>

using namespace std;
using namespace seal;

int main(){

	// create the set of parameters
	const auto &parameter_set = ParameterPack(6, 50, 40, 18);	
	EncryptionParameters parms(scheme_type::ckks);
	size_t poly_modulus_degree = 32768;
	parms.set_poly_modulus_degree(poly_modulus_degree);

	vector<int> mod(parameter_set.number_of_primes + 2,
			parameter_set.middle_prime_length);
	mod[0] = parameter_set.sentinel_prime_length;
	mod[parameter_set.number_of_primes + 1] = parameter_set.sentinel_prime_length;
	parms.set_coeff_modulus(CoeffModulus::Create(poly_modulus_degree, mod));
	SEALContext context(parms);

	KeyGenerator keygen(context);
	auto skey = keygen.secret_key();
	PublicKey pkey;
	keygen.create_public_key(pkey);
	RelinKeys rkey;
	keygen.create_relin_keys(rkey);

	Encryptor encryptor(context, pkey);
	Decryptor decryptor(context, skey);
	Evaluator evaluator(context);
	CKKSEncoder encoder(context);

	double scale = pow(2.0, 40);

	// reciprocal of a
	int a;
	cout << "Calculate reciprocal of a : ";
	cin >> a;

	vector<double> x, va;
	x.push_back(0.01);  // initial value X_0
	va.push_back(a);    // N

	Plaintext plain_x, plain_a;
	encoder.encode(x, scale, plain_x);
	encoder.encode(va, scale, plain_a);

	Ciphertext cipher_x, cipher_a;
	encryptor.encrypt(plain_x, cipher_x);
	encryptor.encrypt(plain_a, cipher_a);
	
	// Newton Raphson Method : Xn+1 = 2Xn - aXn^2

	// negate : cipher_a = -a
	evaluator.negate_inplace(cipher_a);

    	for(int i=0; i<9; i++){
	    // first double and store the result
	    // cipher_x1 = 2Xn
            Ciphertext cipher_x1;
            evaluator.add(cipher_x, cipher_x, cipher_x1);
 
	    // square the current value, relin and rescale
	    // cipher_x2 = Xn^2
	    Ciphertext cipher_x2;
	    evaluator.square(cipher_x, cipher_x2);
	    evaluator.relinearize_inplace(cipher_x2, rkey);
	    evaluator.rescale_to_next_inplace(cipher_x2);
	    
	    // mod switch down our stored value cipher_a, and multiply
	    // cipher_x2 = -aXn^2
	    evaluator.mod_switch_to_inplace(cipher_a, cipher_x2.parms_id()); 
	    evaluator.multiply_inplace(cipher_x2, cipher_a);
	    evaluator.relinearize_inplace(cipher_x2, rkey);
	    evaluator.rescale_to_next_inplace(cipher_x2);
     
	    // modify scale of cipher_x1, mod switch down, and add
	    cipher_x1.scale() = cipher_x2.scale();
	    evaluator.mod_switch_to_inplace(cipher_x1, cipher_x2.parms_id());
	    evaluator.add(cipher_x1, cipher_x2, cipher_x);
                
	    // decrypt
	    Plaintext plain_result;
	    decryptor.decrypt(cipher_x, plain_result);
    
	    // decode
	    vector<double> result;
            encoder.decode(plain_result, result);
 
	    cout << result[0] << endl;
    	}
        return 0;
}
