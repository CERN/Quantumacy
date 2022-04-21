//----------------------------------------------------------------------------
// Created By  : José Cabrero-Holgueras
// Created Date: 01/2022
// Copyright: CERN
// License: MIT
// version ='1.0'
// ---------------------------------------------------------------------------

package he

import (
	"log"
	"os"
	"github.com/sbinet/npyio/npy"
)

func OpenModel()([]float32, float32){

	var bias float32 = -0.05991028
	f, err := os.Open("data/model/w.npy")
	if err != nil{
		log.Fatal(err)
	}
	var weights []float32
	err = npy.Read(f, &weights)
	if err != nil {
		log.Fatal(err)
	}
	
	return  weights, bias
}