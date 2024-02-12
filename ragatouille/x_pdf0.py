from pypdf import PdfReader

def extract_text(pdf_file, mode:str="default"):
    reader = PdfReader(pdf_file)
    
    for page in reader.pages:
        match mode:
            case "default":
                text = page.extract_text()
            case "layout":
                text = page.extract_text(extraction_mode="layout")
            case "no vertical space":
                text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
            case "adjust horizontal spacing":
                text = page.extract_text(extraction_mode="layout", layout_mode_scale_weight=1.0)
            case _:
                raise ValueError("Invalid mode, please choose from 'layout', 'no vertical space' or 'adjust horizontal spacing'")
        
        yield text  # yield the extracted text for each page

for text in extract_text('hand.pdf'):  # replace layout with no vertical space, adjust horizontal spacing as needed
    print(text)