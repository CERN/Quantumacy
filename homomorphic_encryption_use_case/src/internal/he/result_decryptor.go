//----------------------------------------------------------------------------
// Created By  : José Cabrero-Holgueras
// Created Date: 01/2022
// Copyright: CERN
// License: MIT
// version ='1.0'
// ---------------------------------------------------------------------------


package he

import (
	"fmt"
	"math"
	"github.com/ldsec/lattigo/v2/ckks"
)

func DecryptResult(ct *ckks.Ciphertext, sk *ckks.SecretKey, params *ckks.Parameters) (float64){
	var encoder ckks.Encoder = ckks.NewEncoder(params)
	var decryptor ckks.Decryptor = ckks.NewDecryptor(params, sk)
	pt := encoder.Decode(decryptor.DecryptNew(ct), params.LogSlots())
	res := 1.0 / (1.0 + math.Exp(real(pt[0])))
	fmt.Println("Plaintext:", real(pt[0]))
	return res
}