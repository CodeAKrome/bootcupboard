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

func printHelp() {
	fmt.Println("Usage: go run main.go <directory> <max_depth> <max_errors> <media_type1> [media_type2] ...")
	fmt.Println("  or   go run main.go --help")
	fmt.Println("\nArguments:")
	fmt.Println("  <directory>   : Path to the directory to search")
	fmt.Println("  <max_depth>   : Maximum directory depth to traverse (0 for unlimited)")
	fmt.Println("  <max_errors>  : Maximum number of errors before exiting (0 for unlimited)")
	fmt.Println("  <media_type>  : One or more media types to search for (video, audio, image)")
	fmt.Println("\nExample:")
	fmt.Println("  go run main.go /home/user/media 3 5 video image")
	fmt.Println("\nThis will search for video and image files in /home/user/media,")
	fmt.Println("up to 3 levels deep, and will stop if it encounters 5 errors.")
}

func parseArgs() (string, int, int, map[string]bool, error) {
	if len(os.Args) == 2 && (os.Args[1] == "--help" || os.Args[1] == "-h") {
		printHelp()
		os.Exit(0)
	}

	if len(os.Args) < 5 {
		return "", 0, 0, nil, fmt.Errorf("insufficient arguments")
	}

	directory := os.Args[1]
	maxDepth, err := strconv.Atoi(os.Args[2])
	if err != nil || maxDepth < 0 {
		return "", 0, 0, nil, fmt.Errorf("invalid max_depth: must be a non-negative integer")
	}

	maxErrors, err := strconv.Atoi(os.Args[3])
	if err != nil || maxErrors < 0 {
		return "", 0, 0, nil, fmt.Errorf("invalid max_errors: must be a non-negative integer")
	}

	mediaTypes := make(map[string]bool)
	for _, arg := range os.Args[4:] {
		mediaType := strings.ToLower(arg)
		if _, ok := mediaExtensions[mediaType]; !ok {
			return "", 0, 0, nil, fmt.Errorf("invalid media type: %s", mediaType)
		}
		mediaTypes[mediaType] = true
	}

	if len(mediaTypes) == 0 {
		return "", 0, 0, nil, fmt.Errorf("no valid media types specified")
	}

	return directory, maxDepth, maxErrors, mediaTypes, nil
}

func main() {
	directory, maxDepth, maxErrors, mediaTypes, err := parseArgs()
	if err != nil {
		fmt.Printf("Error: %v\n\n", err)
		printHelp()
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
