import os
from pathlib import Path

class FileMatcher:
    def __init__(self, directories, extensions):
        self.directories = directories
        # Convert all extensions to lowercase
        self.extensions = [ext.lower() for ext in extensions]

    def get_matching_filesold(self):
        matching_files = []
        for directory in self.directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in self.extensions):
                        matching_files.append(os.path.join(root, file))
        return matching_files

    def get_matching_files(self):
        matching_files = []
        for directory in self.directories:
            for ext in self.extensions:
                matching_files.extend(
                    file for file in Path(directory).rglob('*')
                    if file.is_file() and file.suffix.lower() == ext
                )
        return [str(file) for file in matching_files]

if __name__ == "__main__":
    matcher = FileMatcher(("."), (".jpg",".jpeg",".tiff",".png",".gif"))
    for file in matcher.get_matching_files():
        print(file)
