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


func runtime(ciphertext_file, result_ciphertext_file, params_file, evaluation_key_file, rotation_key_file string){
	//fmt.Println("This is my image", img)
	params := he.ParamsFromFile(params_file)
	rlk := he.EvaluationKeyFromFile(evaluation_key_file)
	gks := he.RotationKeyFromFile(rotation_key_file)
	ct := he.CiphertextFromFile(ciphertext_file)
	
	weights, bias := he.OpenModel()
	encoded_weights := he.EncodeVector(weights, params)

	result := he.LR(ct, encoded_weights,bias, params, rlk, gks)
	he.CiphertextToFile(result_ciphertext_file, result)
}
func main() {
	var ciphertext_file = flag.String("ic", "data/he/img.enc", "Input Image Ciphertext File")
	var result_ciphertext_file = flag.String("oc", "data/he/result.enc", "Output Result Ciphertext")
	var params_file = flag.String("p", "data/he/parameters.params", "Encryption Parameters File")
	var evaluation_key_file = flag.String("rlk", "data/he/key.rlk", "Evaluation Key File")
	var rotation_key_file = flag.String("gks", "data/he/key.gks", "Rotation Key File")
	flag.Parse()
	fmt.Println(*ciphertext_file, *result_ciphertext_file, *params_file, *evaluation_key_file, *rotation_key_file )
	runtime(*ciphertext_file, *result_ciphertext_file, *params_file, *evaluation_key_file, *rotation_key_file )

}
