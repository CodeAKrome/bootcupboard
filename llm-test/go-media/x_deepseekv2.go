package main

import (
    "fmt"
    "io/fs"
    "log"
    "os"
    "path/filepath"

    "github.com/spf13/cobra"
)

func mediaFileTypes(mediaType string) []string {
    var fileExtensions []string

    switch mediaType {
    case "video":
        fileExtensions = []string{".mp4", ".mkv", ".mov", ".avi"}
    case "audio":
        fileExtensions = []string{".mp3", ".wav", ".aac"}
    case "image":
        fileExtensions = []string{".jpg", ".jpeg", ".png"}
    default:
        log.Fatal("Invalid media type")
    }

    return fileExtensions
}

func findMediaFiles(cmd *cobra.Command, args []string) ([]string, error) {
    var files []string

    directory := cmd.Flag("directory").Value.String()
    depth, _ := cmd.Flags().GetInt("depth")
    maxErrors, _ := cmd.Flags().GetInt("max-errors")

    mediaTypes := args

    // Get the list of supported file extensions for all given media types
    var allFileExtensions []string
    for _, mediaType := range mediaTypes {
        allFileExtensions = append(allFileExtensions, mediaFileTypes(mediaType)...)
    }

    errorCount := 0
    err := filepath.WalkDir(directory,
        func(path string, entry fs.DirEntry, err error) error {
            if err != nil {
                log.Printf("Error processing %s: %v", path, err)
                errorCount++
                if errorCount >= maxErrors {
                    return &fs.SkipAllError{Err: fmt.Errorf("maximum number of errors reached")}
                }
                return fs.SkipDir
            }

            // Limit the depth traversed
            relPath, err := filepath.Rel(directory, path)
            if err != nil {
                log.Printf("Error getting relative path for %s: %v", path, err)
                errorCount++
                if errorCount >= maxErrors {
                    return &fs.SkipAllError{Err: fmt.Errorf("maximum number of errors reached")}
                }
                return fs.SkipDir
            }
            dirDepth := len(filepath.SplitList(relPath))
            if dirDepth > depth {
                return fs.SkipDir
            }

            if !entry.IsDir() {
                for _, extension := range allFileExtensions {
                    if filepath.Ext(entry.Name()) == extension {
                        files = append(files, path)
                    }
                }
            }
            return nil
        })

    return files, err
}

func main() {
    rootCmd := &cobra.Command{
        Use: "media_finder",
        RunE: func(cmd *cobra.Command, args []string) error {
            if len(args) == 0 {
                return fmt.Errorf("at least one media type must be specified")
            }
            files, err := findMediaFiles(cmd, args)
            if err != nil && !os.IsNotExist(err) {
                return err
            } else if os.IsNotExist(err) {
                log.Printf("Directory does not exist: %s", cmd.Flag("directory").Value.String())
            }

            // Print the list of media files
            for _, file := range files {
                fmt.Println(file)
            }
            return nil
        },
    }

    rootCmd.Flags().StringP("directory", "d", "", "Directory to search for media files")
    if err := rootCmd.MarkFlagRequired("directory"); err != nil {
        log.Fatal(err)
    }

    rootCmd.Flags().IntP("depth", "p", -1, "Maximum depth to traverse (default: unlimited)")
    rootCmd.Flags().IntP("max-errors", "m", 10, "Maximum number of errors before exiting (default: 10)")

    if err := rootCmd.Execute(); err != nil {
        log.Fatal(err)
    }
}