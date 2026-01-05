#!/usr/bin/env python
import sys
import re
import os
import json
import argparse
from pathlib import Path
from kokoro_onnx import Kokoro
import soundfile as sf
import numpy as np

def clean_text(text):
    """Remove problematic characters from text."""
    return re.sub(r'[^\w\s.,!?;:\'"()\-]', '', text)

def generate_audio_for_sentence(kokoro, text, output_path, voice='af_heart'):
    """Generate audio for a single sentence and save to file."""
    # Clean the text
    cleaned_text = clean_text(text)
    
    if not cleaned_text.strip():
        print(f"Warning: Empty text after cleaning, skipping", file=sys.stderr)
        return None
    
    # Generate audio with kokoro-onnx
    try:
        samples, sample_rate = kokoro.create(cleaned_text, voice=voice, speed=1.0)
        
        if samples is None or len(samples) == 0:
            print(f"Warning: No audio generated for text: {text}", file=sys.stderr)
            return None
        
        # Save audio file
        sf.write(output_path, samples, sample_rate)
        
        return output_path
    except Exception as e:
        print(f"Error generating audio: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Generate audio files from sentences and output JSON for video generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From file, one sentence per line
  ./ttskokoro.py input.txt -o audio_output -b segment
  
  # From stdin
  cat sentences.txt | ./ttskokoro.py - -o audio_output -b clip
  
  # With custom voice
  ./ttskokoro.py input.txt -o audio -b audio --voice af_bella
        """
    )
    
    parser.add_argument(
        'input',
        help='Input file path or "-" for stdin (one sentence per line)'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='audio_output',
        help='Output directory for audio files (default: audio_output)'
    )
    parser.add_argument(
        '-b', '--basename',
        default='audio',
        help='Base name for output files (default: audio)'
    )
    parser.add_argument(
        '--voice',
        default='af_heart',
        help='Voice to use for TTS (default: af_heart). Options: af (female), am (male), bf, bm, af_heart, etc.'
    )
    parser.add_argument(
        '--format',
        choices=['wav', 'mp3'],
        default='wav',
        help='Audio format (default: wav)'
    )
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read sentences
    if args.input == '-':
        print("Reading sentences from stdin (one per line, Ctrl+D to finish)...", file=sys.stderr)
        lines = sys.stdin.readlines()
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    # Filter empty lines
    sentences = [line.strip() for line in lines if line.strip()]
    
    if not sentences:
        print("Error: No sentences found in input", file=sys.stderr)
        sys.exit(1)
    
    print(f"Processing {len(sentences)} sentences...", file=sys.stderr)
    
    # Initialize Kokoro once
    print("Initializing Kokoro TTS...", file=sys.stderr)

    kokoro = Kokoro()
    
    # Process each sentence
    json_entries = []
    for i, sentence in enumerate(sentences, 1):
        # Generate output filename
        audio_filename = f"{args.basename}_{i:03d}.{args.format}"
        audio_path = output_dir / audio_filename
        
        print(f"Processing sentence {i}/{len(sentences)}: {sentence[:50]}...", file=sys.stderr)
        
        # Generate audio
        result_path = generate_audio_for_sentence(
            kokoro, 
            sentence, 
            str(audio_path),
            voice=args.voice
        )
        
        if result_path:
            # Create JSON entry
            json_entry = {
                "text": sentence,
                "audio": str(audio_path)
            }
            json_entries.append(json_entry)
            
            # Output JSON line immediately (streaming output)
            print(json.dumps(json_entry))
            sys.stdout.flush()
        else:
            print(f"Skipping sentence {i} due to generation failure", file=sys.stderr)
    
    print(f"\nSuccessfully generated {len(json_entries)} audio files in {output_dir}", file=sys.stderr)
    print(f"JSON output complete", file=sys.stderr)

if __name__ == '__main__':
    main()
