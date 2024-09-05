package main

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"
)

var (
	maxDepth   int
	maxErrors  int
	mediaTypes []string
)

var mediaExtensions = map[string][]string{
	"video": {".mp4", ".avi", ".mov", ".mkv", ".wmv"},
	"audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".aif"},
	"image": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
	"book":  {".pdf", ".epub", ".mobi", ".azw"},
	"text":  {".txt", ".md", ".html"},
	"comic": {".cbz", ".cbr"},
}

var rootCmd = &cobra.Command{
	Use:   "media-lister [directory]",
	Short: "List media files in a directory",
	Long: `A flexible media file lister that can search for various types of media files
in a specified directory, with options to limit search depth and error tolerance.`,
	Args: cobra.ExactArgs(1),
	Run:  listMediaFiles,
}

func init() {
	rootCmd.Flags().IntVar(&maxDepth, "max-depth", 0, "Maximum directory depth to traverse (0 for unlimited)")
	rootCmd.Flags().IntVar(&maxErrors, "max-errors", 0, "Maximum number of errors before exiting (0 for unlimited)")
	
	// Create a dynamic list of media types based on the keys of mediaExtensions
	defaultMediaTypes := make([]string, 0, len(mediaExtensions))
	for mediaType := range mediaExtensions {
		defaultMediaTypes = append(defaultMediaTypes, mediaType)
	}
	
	rootCmd.Flags().StringSliceVar(&mediaTypes, "types", defaultMediaTypes, "Media types to search for")
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func listMediaFiles(cmd *cobra.Command, args []string) {
	directory := args[0]
	validMediaTypes := validateMediaTypes(mediaTypes)

	if len(validMediaTypes) == 0 {
		fmt.Println("Error: No valid media types specified")
		cmd.Usage()
		os.Exit(1)
	}

	var filesFound, errorsEncountered int

	err := filepath.WalkDir(directory, func(path string, d fs.DirEntry, err error) error {
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
			for _, mediaType := range validMediaTypes {
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

	printSummary(filesFound, errorsEncountered)
}

func validateMediaTypes(types []string) []string {
	validTypes := []string{}
	for _, t := range types {
		if _, ok := mediaExtensions[strings.ToLower(t)]; ok {
			validTypes = append(validTypes, strings.ToLower(t))
		} else {
			fmt.Printf("Warning: Invalid media type '%s' ignored\n", t)
		}
	}
	return validTypes
}

func printSummary(filesFound, errorsEncountered int) {
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
	fmt.Printf("Media types searched: %v\n", mediaTypes)
}
