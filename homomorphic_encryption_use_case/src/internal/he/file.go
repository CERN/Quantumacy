//----------------------------------------------------------------------------
// Created By  : José Cabrero-Holgueras
// Created Date: 01/2022
// Copyright: CERN
// License: MIT
// version ='1.0'
// ---------------------------------------------------------------------------

package he

import(
	"os"
	"log"
	"github.com/ldsec/lattigo/v2/ckks"
)

func BytesToFile(filename string, bytes []byte){
	file, err := os.Create(filename)
	defer file.Close()
	if err != nil {
		log.Fatal(err)
	} 

	_, err2 := file.Write(bytes)

	if err2 != nil {
		log.Fatal(err2)
	}
}

func BytesFromFile(filename string) (bytes []byte){
	bytes, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	return bytes
}
func CiphertextToFile(filename string, ciphertext *ckks.Ciphertext) {
	bin_buf, err1 := ciphertext.MarshalBinary() // Little Endian
	if err1 != nil {
		log.Fatal(err1)
	}

	BytesToFile(filename, bin_buf)

}

func CiphertextFromFile(filename string) (*ckks.Ciphertext) {
	var ciphertext *ckks.Ciphertext = &ckks.Ciphertext{}
	bytes := BytesFromFile(filename)

	ciphertext.UnmarshalBinary(bytes)

	return ciphertext
}

func ParamsToFile(filename string, params *ckks.Parameters){
	bin_buf, err1 := params.MarshalBinary() // Little Endian
	if err1 != nil {
		log.Fatal(err1)
	}

	BytesToFile(filename, bin_buf)


}
func ParamsFromFile(filename string) (*ckks.Parameters){
	var params *ckks.Parameters = &ckks.Parameters{}
	bytes := BytesFromFile(filename)

	params.UnmarshalBinary(bytes)

	return params
}


func PublicKeyToFile(filename string, pk *ckks.PublicKey) {
	bin_buf, err1 := pk.MarshalBinary() // Little Endian
	if err1 != nil {
		log.Fatal(err1)
	}

	BytesToFile(filename, bin_buf)
}

func PublicKeyFromFile(filename string) (*ckks.PublicKey) {
	var pk *ckks.PublicKey = &ckks.PublicKey{}
	bytes := BytesFromFile(filename)

	pk.UnmarshalBinary(bytes)

	return pk
}

func SecretKeyToFile(filename string, sk *ckks.SecretKey) {
	bin_buf, err1 := sk.MarshalBinary() // Little Endian
	if err1 != nil {
		log.Fatal(err1)
	}

	BytesToFile(filename, bin_buf)
}

func SecretKeyFromFile(filename string) (*ckks.SecretKey) {
	var sk *ckks.SecretKey = &ckks.SecretKey{}
	bytes := BytesFromFile(filename)

	sk.UnmarshalBinary(bytes)

	return sk
}

func EvaluationKeyToFile(filename string, rlk *ckks.EvaluationKey) {
	bin_buf, err1 := rlk.MarshalBinary() // Little Endian
	if err1 != nil {
		log.Fatal(err1)
	}

	BytesToFile(filename, bin_buf)
}

func EvaluationKeyFromFile(filename string) (*ckks.EvaluationKey) {
	var rlk *ckks.EvaluationKey = &ckks.EvaluationKey{}
	bytes := BytesFromFile(filename)

	rlk.UnmarshalBinary(bytes)

	return rlk
}

func RotationKeyToFile(filename string, gks *ckks.RotationKeys) {
	bin_buf, err1 := gks.MarshalBinary() // Little Endian
	if err1 != nil {
		log.Fatal(err1)
	}

	BytesToFile(filename, bin_buf)
}

func RotationKeyFromFile(filename string) (*ckks.RotationKeys) {
	var gks *ckks.RotationKeys = &ckks.RotationKeys{}
	bytes := BytesFromFile(filename)

	gks.UnmarshalBinary(bytes)

	return gks
}