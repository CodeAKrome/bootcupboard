import os
import re
import docx2txt
import pdfplumber
from bs4 import BeautifulSoup

def convert_to_plain_text(input_file_path):
    file_extension = os.path.splitext(input_file_path)[-1].lower()

    if file_extension == '.txt':
        with open(input_file_path, 'r', encoding='utf-8') as file:
            return file.read()

    elif file_extension == '.md':
        with open(input_file_path, 'r', encoding='utf-8') as file:
            return file.read()

    elif file_extension == '.docx':
        return docx2txt.process(input_file_path)

    elif file_extension == '.pdf':
        text = ''
        with pdfplumber.open(input_file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    elif file_extension == '.html':
        with open(input_file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return re.sub(r'\n+', '\n', soup.get_text())

    else:
        return f"Unsupported file format: {file_extension}"

def main():
    input_file_path = 'input_file.pdf'  # Replace with the path to your input file
    converted_text = convert_to_plain_text(input_file_path)

    output_file_path = 'output.txt'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(converted_text)

if __name__ == '__main__':
    main()
