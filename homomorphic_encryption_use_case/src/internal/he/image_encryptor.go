//----------------------------------------------------------------------------
// Created By  : José Cabrero-Holgueras
// Created Date: 01/2022
// Copyright: CERN
// License: MIT
// version ='1.0'
// ---------------------------------------------------------------------------

package he

import (
	//"fmt"
	"log"
	"image"
	"image/color"
	"github.com/ldsec/lattigo/v2/ckks"
)

func rgba_to_gray(img image.Image)(image.Image){
	b := img.Bounds()
	imgSet := image.NewRGBA(b)
	for y := 0; y < b.Max.Y; y++ {
		for x := 0; x < b.Max.X; x++ {
		  oldPixel := img.At(x, y)
		  r, g, b, _ := oldPixel.RGBA()
		  t := 0.299*float64(r) + 0.587*float64(g) + 0.114*float64(b)
		  pixel := color.Gray{uint8(t / 256)}
		  imgSet.Set(x, y, pixel)
		}
	}
	return imgSet 
}

func EncryptImage(img image.Image, params *ckks.Parameters, pk *ckks.PublicKey)(*ckks.Ciphertext){
	log.Println("Encrypting Image")
	var plaintext *ckks.Plaintext
	var encoder ckks.Encoder = ckks.NewEncoder(params)
	var encryptor ckks.Encryptor = ckks.NewEncryptorFromPk(params, pk)
	
	
	bounds := img.Bounds()
    w, h := bounds.Max.X, bounds.Max.Y

	values := make([]complex128, h * w)
	for i := 0; i < h; i++ {
		for j := 0; j < w; j++ {
	
			color , _ := img.At(j, i).(color.Gray)

			pixel := float32(color.Y) / 255.0

			values[i * w + j] = complex128(complex(float32(pixel), 0))
		}

	}
	plaintext = encoder.EncodeNew(values, params.LogSlots())
	var ciphertext *ckks.Ciphertext = &ckks.Ciphertext{Element:&ckks.Element{}}
	ciphertext = encryptor.EncryptNew(plaintext)
	return ciphertext

}
