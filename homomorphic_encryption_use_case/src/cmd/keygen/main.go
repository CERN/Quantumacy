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
	"flag" // For cmdline args
)


func keygen(params_file, public_key_file, secret_key_file, evaluation_key_file, rotation_key_file string){
	//fmt.Println("This is my image", img)
	params := he.GenRLWEParameters()
	sk, pk, rlk, gks := he.GenKeys(params)
	
	he.ParamsToFile(params_file, params)	
	he.SecretKeyToFile(secret_key_file, sk)
	he.PublicKeyToFile(public_key_file, pk)
	he.EvaluationKeyToFile(evaluation_key_file, rlk)
	he.RotationKeyToFile(rotation_key_file, gks)
}
func main() {
	var params_file = flag.String("p", "data/he/parameters.params", "Encryption Parameters File")
	var public_key_file = flag.String("pk", "data/he/key.pk", "Public Key File")
	var secret_key_file = flag.String("sk", "data/he/key.sk", "Secret Key File")
	var evaluation_key_file = flag.String("rlk", "data/he/key.rlk", "Evaluation Key File")
	var rotation_key_file = flag.String("gks", "data/he/key.gks", "Rotation Key File")
	flag.Parse()
	fmt.Println(*params_file, *public_key_file, *secret_key_file, *evaluation_key_file, *rotation_key_file)
	keygen(*params_file, *public_key_file, *secret_key_file, *evaluation_key_file, *rotation_key_file)

}
