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
)


func encryptor(input_file, ciphertext_file, public_key_file, params_file string){

	img := he.GetImageFromFilePath(input_file)
	params := he.ParamsFromFile(params_file)
	pk := he.PublicKeyFromFile(public_key_file)


	ct := he.EncryptImage(img, params, pk)
	he.CiphertextToFile(ciphertext_file, ct)
}
func main() {
	var input_file = flag.String("i", "data/img/frontal.png", "Input Image File")
	var ciphertext_file = flag.String("c", "data/he/img.enc", "Output Encrypted Image")
	var public_key_file = flag.String("pk", "data/he/key.pk", "Public Key File")
	var params_file = flag.String("p", "data/he/parameters.params", "Encryption Parameters File")
	flag.Parse()
	
	fmt.Println(*input_file, *ciphertext_file, *public_key_file, *params_file)
	encryptor(*input_file, *ciphertext_file, *public_key_file, *params_file)
}
