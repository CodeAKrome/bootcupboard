package main

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
)

var mediaExtensions = map[string][]string{
	"video": {".mp4", ".avi", ".mov", ".mkv", ".wmv"},
	"audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
	"image": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: go run main.go <directory> <media_type1> [media_type2] ...")
		fmt.Println("Media types: video, audio, image")
		os.Exit(1)
	}

	directory := os.Args[1]
	mediaTypes := make(map[string]bool)

	for _, arg := range os.Args[2:] {
		mediaType := strings.ToLower(arg)
		if _, ok := mediaExtensions[mediaType]; !ok {
			fmt.Printf("Invalid media type: %s. Choose from: video, audio, image\n", mediaType)
			os.Exit(1)
		}
		mediaTypes[mediaType] = true
	}

	err := filepath.WalkDir(directory, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if !d.IsDir() {
			ext := strings.ToLower(filepath.Ext(path))
			for mediaType := range mediaTypes {
				for _, validExt := range mediaExtensions[mediaType] {
					if ext == validExt {
						fmt.Printf("[%s] %s\n", mediaType, path)
						break
					}
				}
			}
		}
		return nil
	})

	if err != nil {
		fmt.Printf("Error walking through directory: %v\n", err)
		os.Exit(1)
	}
}
