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
	//"os"
	//"log"
	"pifs/qkd/internal/he"
	"image"
	"time"
	//"math"
	//"flag" // For cmdline args
)


func process_image(img image.Image){
	//fmt.Println("This is my image", img)
	a := time.Now()
	params := he.GenRLWEParameters()
	ea := time.Since(a)
	he.ParamsToFile("data/he/parameters.params", params)
	params = he.ParamsFromFile("data/he/parameters.params")

	b := time.Now()
	sk, pk, rlk, gks := he.GenKeys(params)
	eb := time.Since(b)

	he.SecretKeyToFile("data/he/key.sk", sk)
	sk = he.SecretKeyFromFile("data/he/key.sk")

	he.PublicKeyToFile("data/he/key.pk", pk)
	pk = he.PublicKeyFromFile("data/he/key.pk")

	he.EvaluationKeyToFile("data/he/key.rlk", rlk)
	rlk = he.EvaluationKeyFromFile("data/he/key.rlk")

	he.RotationKeyToFile("data/he/key.gks", gks)
	gks = he.RotationKeyFromFile("data/he/key.gks")
	
	c := time.Now()
	ct := he.EncryptImage(img, params, pk)
	ec := time.Since(c)
	
	he.CiphertextToFile("data/he/img.enc", ct)
	ct = he.CiphertextFromFile("data/he/img.enc")
	
	weights, bias := he.OpenModel()
	fmt.Println("WEIGHTS:", weights[0:9])
	encoded_weights := he.EncodeVector(weights, params)
	
	d := time.Now()
	result := he.LR(ct, encoded_weights,bias, params, rlk, gks)
	ed := time.Since(d)

	fmt.Println(result)
	
	e := time.Now()
	pt := he.DecryptResult(result, sk, params)
	ee := time.Since(e)

	fmt.Println(pt)
	fmt.Println("**************")
	fmt.Println("SUMMARY:")
	fmt.Println("PARAM GENERATION: ", ea)
	fmt.Println("KEY GENERATION: ", eb)
	fmt.Println("ENCRYPTION: ", ec)
	fmt.Println("EVALUATION: ", ed)
	fmt.Println("DECRYPTION: ", ee)
	fmt.Println("**************")
	
	he.Use(params, sk, pk, rlk, gks, ct, weights, bias)
}
func main() {
	
	fmt.Println("FRONTAL: 0")
	img := he.GetImageFromFilePath("data/img/frontal.png")
	process_image(img)
	fmt.Println("LATERAL: 1")
	img2 := he.GetImageFromFilePath("data/img/lateral.png")
	process_image(img2)	

}
