//----------------------------------------------------------------------------
// Created By  : José Cabrero-Holgueras
// Created Date: 01/2022
// Copyright: CERN
// License: MIT
// version ='1.0'
// ---------------------------------------------------------------------------

package he


import (
	"image"
	"os"
	"log"
	_ "image/png"
)

func GetImageFromFilePath(filePath string) (image.Image) {
	// Since nobody is going to read the comments, I just put this.
    f, err := os.Open(filePath)
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()
    image, _, err := image.Decode(f)
	if err != nil {
		log.Fatal(err)
	}
    return image
}