import os
import requests
import argparse
from pathlib import Path
import time
import sys

class LocalSpeechToText:
    def __init__(self, lm_studio_api_url="http://localhost:1234/v1"):
        """
        Initialize the Speech-to-Text converter using local models through LM-Studio.
        
        Args:
            lm_studio_api_url: URL for the LM-Studio API (default is localhost:1234)
        """
        self.lm_studio_api_url = lm_studio_api_url
        
        # Check if LM-Studio is running
        try:
            response = requests.get(f"{self.lm_studio_api_url}/models")
            if response.status_code == 200:
                print("✓ Successfully connected to LM-Studio")
                models = response.json()
                if models:
                    print(f"✓ Available models: {[model['name'] for model in models]}")
                else:
                    print("⚠ No models loaded in LM-Studio. Please load a speech model like Whisper.")
            else:
                print(f"⚠ LM-Studio returned status code {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to LM-Studio. Make sure it's running at", self.lm_studio_api_url)
            print("   Start LM-Studio and ensure the local server is enabled in settings.")
            sys.exit(1)
    
    def transcribe_wav(self, wav_path, model_name="whisper-large-v3", output_file=None):
        """
        Transcribe a WAV file using a local model through LM-Studio.
        
        Args:
            wav_path: Path to the WAV file
            model_name: Name of the model to use for transcription
            output_file: Optional path to save the transcription
            
        Returns:
            Transcribed text
        """
        wav_path = Path(wav_path)
        if not wav_path.exists():
            print(f"❌ File not found: {wav_path}")
            return None
            
        if wav_path.suffix.lower() != ".wav":
            print(f"⚠ Warning: File {wav_path} doesn't have a .wav extension. The file should be in WAV format.")
        
        file_size_mb = os.path.getsize(wav_path) / (1024 * 1024)
        print(f"✓ Processing WAV file: {wav_path} ({file_size_mb:.2f} MB)")
        print(f"✓ Using model: {model_name}")
        
        # Start timer
        start_time = time.time()
        
        # Read audio file
        with open(wav_path, "rb") as audio_file:
            audio_data = audio_file.read()
        
        # Prepare the API request
        url = f"{self.lm_studio_api_url}/audio/transcriptions"
        files = {
            "file": (wav_path.name, audio_data, "audio/wav")
        }
        data = {
            "model": model_name
        }
        
        try:
            print("⏳ Transcribing audio... (this may take a while for larger files)")
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                transcription = result.get("text", "")
                
                # Calculate elapsed time
                elapsed_time = time.time() - start_time
                
                print(f"✓ Transcription completed in {elapsed_time:.2f} seconds")
                
                # Save transcription to file if requested
                if output_file:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(transcription)
                    print(f"✓ Transcription saved to: {output_file}")
                
                return transcription
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"❌ Exception during transcription: {e}")
            return None

def process_directory(directory, model_name, output_dir=None):
    """Process all WAV files in a directory"""
    stt = LocalSpeechToText()
    directory = Path(directory)
    
    if not directory.exists() or not directory.is_dir():
        print(f"❌ Directory not found: {directory}")
        return
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
    
    wav_files = list(directory.glob("*.wav"))
    if not wav_files:
        print(f"❌ No WAV files found in {directory}")
        return
    
    print(f"Found {len(wav_files)} WAV file(s) to process")
    
    for i, wav_file in enumerate(wav_files, 1):
        print(f"\n[{i}/{len(wav_files)}] Processing {wav_file.name}")
        
        if output_dir:
            output_file = output_dir / f"{wav_file.stem}.txt"
        else:
            output_file = wav_file.with_suffix(".txt")
        
        transcription = stt.transcribe_wav(wav_file, model_name=model_name, output_file=output_file)
        
        if transcription:
            print(f"Transcript: {transcription[:100]}{'...' if len(transcription) > 100 else ''}")

def main():
    parser = argparse.ArgumentParser(description="Transcribe WAV files using LM-Studio local models")
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", type=str, help="Path to WAV file to transcribe")
    input_group.add_argument("--dir", type=str, help="Directory containing WAV files to transcribe")
    
    # Other options
    parser.add_argument("--model", type=str, default="whisper-large-v3", help="Model name to use for transcription")
    parser.add_argument("--output", type=str, default=None, help="Output file or directory for transcriptions")
    
    args = parser.parse_args()
    
    if args.file:
        # Process single file
        stt = LocalSpeechToText()
        transcript = stt.transcribe_wav(args.file, model_name=args.model, output_file=args.output)
        
        if transcript:
            print("\nTranscription:")
            print(transcript)
    
    elif args.dir:
        # Process directory
        process_directory(args.dir, args.model, args.output)

if __name__ == "__main__":
    main()
