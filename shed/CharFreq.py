import sys
from collections import Counter

def main0():
    text = sys.stdin.read()  # read input from stdin
    
    char_counts = Counter(text)  # count the occurrences of each character
    
    for char, count in char_counts.most_common():
        print(f"{char}: {count}")

def main():
    text = sys.stdin.read()  # read input from stdin
    
    char_counts = Counter(text)  # count the occurrences of each character
    
    for char, count in char_counts.most_common():
        if ord(char) < 32 or (ord(char) >= 127 and ord(char) <= 159):  # non-printable characters
            symbolic_name = f"[{ord(char)}]"
        elif char == "\r":
            symbolic_name = "[CR]"
        elif char == "\n":
            symbolic_name = "[LF]"
        else:
            symbolic_name = char
            
        print(f"{symbolic_name}: {count}")

if __name__ == "__main__":
    main() 
