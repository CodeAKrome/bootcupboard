import fitz

# pip install PyMuPDF

def extract_pdf_fields(pdf_file_path):
    # Initialize the PDF document
    pdf_document = fitz.open(pdf_file_path)

    # Initialize an empty dictionary to store the fields and their values
    pdf_fields = {}

    # Iterate through the pages of the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        
        # Get the page's annotations (form fields)
        annotations = page.annots()

        # Iterate through the annotations (form fields)
        for annotation in annotations:
            field_name = annotation.get('T', '')  # Field name
            field_value = annotation.get('V', '')  # Field value

            # Add the field name and value to the dictionary
            pdf_fields[field_name] = field_value

    # Close the PDF document
    pdf_document.close()

    return pdf_fields

# Example usage:
pdf_file_path = 'sample.pdf'  # Replace with the path to your PDF file
fields_dict = extract_pdf_fields(pdf_file_path)

# Print the extracted fields and their values
for field, value in fields_dict.items():
    print(f'Field: {field}, Value: {value}')
