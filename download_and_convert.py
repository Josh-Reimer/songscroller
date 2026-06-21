import os
import subprocess
import fitz  # PyMuPDF

pdf_url = "https://archive.org/download/christianhymnalc00chur/christianhymnalc00chur.pdf"
pdf_filename = "christianhymnalc00chur.pdf"
img_dir = "img"

def main():
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        print(f"Created directory: {img_dir}")

    if not os.path.exists(pdf_filename):
        print(f"Downloading {pdf_url} ...")
        subprocess.run(["curl", "-L", "-o", pdf_filename, pdf_url], check=True)
        print("Download complete.")
    else:
        print("PDF already exists.")

    print("Converting PDF pages to JPG...")
    doc = fitz.open(pdf_filename)
    total_pages = len(doc)
    print(f"Total pages: {total_pages}")
    
    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        # Save as songscroller{page_num}.jpg
        # Let's 1-index them to match some convention or 0-index. 
        # The js script assumes 11 to 590, so the numbers don't strictly matter as long as they are sequential.
        # But we'll just use page_num.
        output_filename = os.path.join(img_dir, f"songscroller{page_num}.jpg")
        pix.save(output_filename)
        if page_num % 50 == 0:
            print(f"Converted {page_num}/{total_pages} pages...")

    print("Conversion complete.")

if __name__ == "__main__":
    main()
