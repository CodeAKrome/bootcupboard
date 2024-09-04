package main

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

var mediaExtensions = map[string][]string{
	"video": {".mp4", ".avi", ".mov", ".mkv", ".wmv"},
	"audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
	"image": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
}

func main() {
	if len(os.Args) < 5 {
		fmt.Println("Usage: go run main.go <directory> <max_depth> <max_errors> <media_type1> [media_type2] ...")
		fmt.Println("Media types: video, audio, image")
		fmt.Println("<max_depth>: Maximum directory depth to traverse (0 for unlimited)")
		fmt.Println("<max_errors>: Maximum number of errors before exiting (0 for unlimited)")
		os.Exit(1)
	}

	directory := os.Args[1]
	maxDepth, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Println("Invalid max_depth. Please provide a non-negative integer.")
		os.Exit(1)
	}

	maxErrors, err := strconv.Atoi(os.Args[3])
	if err != nil {
		fmt.Println("Invalid max_errors. Please provide a non-negative integer.")
		os.Exit(1)
	}

	mediaTypes := make(map[string]bool)
	for _, arg := range os.Args[4:] {
		mediaType := strings.ToLower(arg)
		if _, ok := mediaExtensions[mediaType]; !ok {
			fmt.Printf("Warning: Invalid media type: %s. Choose from: video, audio, image\n", mediaType)
			continue
		}
		mediaTypes[mediaType] = true
	}

	if len(mediaTypes) == 0 {
		fmt.Println("No valid media types specified. Exiting.")
		os.Exit(1)
	}

	var filesFound, errorsEncountered int

	err = filepath.WalkDir(directory, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			fmt.Printf("Error accessing %s: %v\n", path, err)
			errorsEncountered++
			if maxErrors > 0 && errorsEncountered >= maxErrors {
				return fmt.Errorf("maximum number of errors (%d) reached", maxErrors)
			}
			return nil // Continue walking
		}

		relPath, _ := filepath.Rel(directory, path)
		depth := strings.Count(relPath, string(os.PathSeparator))

		if maxDepth > 0 && depth > maxDepth {
			if d.IsDir() {
				return filepath.SkipDir
			}
			return nil
		}

		if !d.IsDir() {
			ext := strings.ToLower(filepath.Ext(path))
			for mediaType := range mediaTypes {
				for _, validExt := range mediaExtensions[mediaType] {
					if ext == validExt {
						fmt.Printf("[%s] %s\n", mediaType, path)
						filesFound++
						break
					}
				}
			}
		}
		return nil
	})

	if err != nil {
		if err.Error() == fmt.Sprintf("maximum number of errors (%d) reached", maxErrors) {
			fmt.Println(err)
		} else {
			fmt.Printf("Error walking directory: %v\n", err)
		}
		errorsEncountered++
	}

	fmt.Printf("\nSummary:\n")
	fmt.Printf("Files found: %d\n", filesFound)
	fmt.Printf("Errors encountered: %d\n", errorsEncountered)
	if maxDepth > 0 {
		fmt.Printf("Maximum depth traversed: %d\n", maxDepth)
	} else {
		fmt.Println("Depth: Unlimited")
	}
	if maxErrors > 0 {
		fmt.Printf("Maximum errors allowed: %d\n", maxErrors)
	} else {
		fmt.Println("Error limit: Unlimited")
	}
}
