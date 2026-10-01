import fitz  # PyMuPDF
import os

pdf_files = [
    "offer_letter.pdf",
    "Ifso_certificate.pdf",
    "Employer Feedback Form.pdf"
]

def extract_first_page_as_image(pdf_path, output_image_path):
    if not os.path.exists(pdf_path):
        print(f"[-] Error: File not found - {pdf_path}")
        return False
        
    try:
        # Open the document
        doc = fitz.open(pdf_path)
        # Load the first page (index 0)
        page = doc.load_page(0)
        
        # Increase the resolution (matrix) for a high-quality image
        zoom = 2.0  # e.g. 2.0 = 200% zoom
        mat = fitz.Matrix(zoom, zoom)
        
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(output_image_path)
        
        print(f"[+] Successfully extracted {pdf_path} to {output_image_path}")
        return True
    except Exception as e:
        print(f"[-] Failed to process {pdf_path}: {e}")
        return False

if __name__ == "__main__":
    success_count = 0
    for pdf in pdf_files:
        image_name = os.path.splitext(pdf)[0] + ".png"
        if extract_first_page_as_image(pdf, image_name):
            success_count += 1
            
    print(f"[*] Extracted {success_count} out of {len(pdf_files)} PDF pages.")
