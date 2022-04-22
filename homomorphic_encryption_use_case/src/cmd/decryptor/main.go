//----------------------------------------------------------------------------
// Created By  : José Cabrero-Holgueras
// Created Date: 01/2022
// Copyright: CERN
// License: MIT
// version ='1.0'
// ---------------------------------------------------------------------------

package main 

import(
	"fmt"
	"pifs/qkd/internal/he"
	"flag"
	"os"
)


func decrypt(result_ciphertext_file, params_file, secret_key_file string) (int){

	params := he.ParamsFromFile(params_file)
	sk := he.SecretKeyFromFile(secret_key_file)
	result := he.CiphertextFromFile(result_ciphertext_file)
	pt := he.DecryptResult(result, sk, params)
	fmt.Println("RESULT:", pt)
	if pt < 0.5 {
		return 0
	} else {
		return 1
	}

}
func main() {
	var result_ciphertext_file = flag.String("oc", "data/he/result.enc", "Output Result Ciphertext")
	var params_file = flag.String("p", "data/he/parameters.params", "Encryption Parameters File")
	var secret_key_file = flag.String("sk", "data/he/key.sk", "Secret Key File")
	flag.Parse()
	os.Exit(decrypt(*result_ciphertext_file, *params_file, *secret_key_file))

}
