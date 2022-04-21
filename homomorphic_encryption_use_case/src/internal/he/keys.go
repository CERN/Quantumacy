//----------------------------------------------------------------------------
// Created By  : José Cabrero-Holgueras
// Created Date: 01/2022
// Copyright: CERN
// License: MIT
// version ='1.0'
// ---------------------------------------------------------------------------

package he

import (
	"github.com/ldsec/lattigo/v2/ckks"
)


func GenKeyPair(keygen ckks.KeyGenerator)(sk *ckks.SecretKey, pk *ckks.PublicKey){
	sk, pk = keygen.GenKeyPair()
	return
}

func GenRelinKeys(keygen ckks.KeyGenerator, sk *ckks.SecretKey)(rlk *ckks.EvaluationKey){
	rlk = keygen.GenRelinKey(sk)
	return
}

func GenGaloisKeys(keygen ckks.KeyGenerator, sk *ckks.SecretKey)(gks *ckks.RotationKeys){
	gks = keygen.GenRotationKeysPow2(sk)
	return
}

func GenKeys(params *ckks.Parameters) (sk *ckks.SecretKey, pk *ckks.PublicKey, rlk *ckks.EvaluationKey, gks *ckks.RotationKeys) {
	keygen := ckks.NewKeyGenerator(params)
	sk, pk = GenKeyPair(keygen)
	rlk = GenRelinKeys(keygen, sk)
	gks = GenGaloisKeys(keygen, sk)
	return 
}