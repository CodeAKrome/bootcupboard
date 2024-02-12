#!env python
from pypdf import PdfReader
import fire

def extract_text(pdf_file, mode:str="default"):
    reader = PdfReader(pdf_file)
    
    for page in reader.pages:
        match mode:
            case "default":
                print(f"->{page.extract_text()}<-")
            case "layout":
                print(page.extract_text(extraction_mode="layout"))
            case "no vertical space":
                print(page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))
            case "adjust horizontal spacing":
                print(page.extract_text(extraction_mode="layout", layout_mode_scale_weight=1.0))
            case _:
                raise ValueError("Invalid mode, please choose from 'layout', 'no vertical space' or 'adjust horizontal spacing'")

if __name__ == "__main__":
    fire.Fire(extract_text)