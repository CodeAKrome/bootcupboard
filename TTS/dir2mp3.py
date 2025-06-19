import os
from gtts import gTTS

def say(text: str, file: str):
    tts = gTTS(text)
    tts.save(file)

def process_directory(directory_path: str):
    # Check if directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        return
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        # Process only .txt files
        if filename.endswith('.txt'):
            input_path = os.path.join(directory_path, filename)
            # Create output filename by replacing .txt with .mp3
            output_filename = os.path.splitext(filename)[0] + '.mp3'
            output_path = os.path.join(directory_path, output_filename)
            
            try:
                # Read the text file
                with open(input_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                # Convert text to speech and save as MP3
                say(text, output_path)
                print(f"Successfully converted {filename} to {output_filename}")
            
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python tts_directory.py <directory_path>")
    else:
        process_directory(sys.argv[1])