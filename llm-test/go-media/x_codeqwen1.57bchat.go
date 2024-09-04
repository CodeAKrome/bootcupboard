package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"
)

var (
	rootCmd    = &cobra.Command{Use: "media-list"}
	errLimit   int
	depthLimit int
	types      []string
)

func init() {
	rootCmd.Flags().StringArrayVar(&types, "type", []string{}, "Type of media (video, audio, image), can specify multiple types")
	rootCmd.Flags().IntVar(&errLimit, "error-limit", 0, "Maximum number of errors before exiting")
	rootCmd.Flags().IntVar(&depthLimit, "max-depth", 10, "Maximum depth to traverse (default is 10)")

}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
}

func runCommand(cmd *cobra.Command, args []string) error {
	if len(types) == 0 {
		return fmt.Errorf("No media type specified")
	}

	errCount := 0

	walkdir.WalkDirs("/path/to/directory", func(path string, d os.FileInfo, err error) error {
		if err != nil {
			errCount++
			if errLimit > 0 && errCount >= errLimit {
				return fmt.Errorf("Exceeded maximum number of errors")
			}
			fmt.Printf("Error: %s\n", err)
			return nil
		}

		depth, _ := walkdir.Depth(path)
		if depth > depthLimit {
			return filepath.SkipDir
		}

		ext := strings.ToLower(filepath.Ext(path))

		for _, mediaType := range types {
			switch mediaType {
			case "video":
				if strings.HasPrefix(ext, ".mp4") || strings.HasPrefix(ext, ".avi") || strings.HasPrefix(ext, ".mkv") {
					fmt.Println(path)
				}
			case "audio":
				if strings.HasPrefix(ext, ".mp3") || strings.HasPrefix(ext, ".wav") || strings.HasPrefix(ext, ".ogg") {
					fmt.Println(path)
				}
			case "image":
				if strings.HasPrefix(ext, ".jpg") || strings.HasPrefix(ext, ".jpeg") || strings.HasPrefix(ext, ".png") {
					fmt.Println(path)
				}
			default:
				return fmt.Errorf("Invalid media type: %s", mediaType)
			}
		}

		return nil
	})

	return nil
}

// go run main.go -type video -type image /path/to/directory
