import os
import sys
from PyPDF2 import PdfReader, PdfWriter
import subprocess
import sys

# 自動安裝機制
try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("正在安裝必要的套件 (PyPDF2)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    from PyPDF2 import PdfReader, PdfWriter
    print("安裝完成！\n")

def extract_pages(pdf_path, page_range_str):
    """
    Extracts a range of pages from a PDF and saves them as a new file.
    page_range_str can be a single number "5" or a range "5~15" or "5-15".
    """
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        # Parse range
        if '~' in page_range_str:
            parts = page_range_str.split('~')
        elif '-' in page_range_str:
             parts = page_range_str.split('-')
        else:
            parts = [page_range_str]
            
        if len(parts) == 1:
            start_page = int(parts[0])
            end_page = start_page
        elif len(parts) == 2:
            start_page = int(parts[0])
            end_page = int(parts[1])
        else:
            print("Invalid format. Please use 'Start~End' (e.g., 5~15) or a single page number.")
            return

        # Validate range
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            print(f"Error: Invalid page range {start_page}~{end_page}. The document has {total_pages} pages.")
            return

        writer = PdfWriter()
        # Convert 1-based page numbers to 0-based index and extract
        for p in range(start_page, end_page + 1):
            writer.add_page(reader.pages[p - 1])

        if start_page == end_page:
            output_filename = f"extracted_page_{start_page}.pdf"
        else:
            output_filename = f"extracted_pages_{start_page}_to_{end_page}.pdf"
            
        output_path = os.path.join(os.path.dirname(pdf_path), output_filename)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        print(f"Success! Pages {start_page}~{end_page} saved to: {output_path}")

    except ValueError:
        print("Error: Invalid number format.")
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_pdfs(directory):
    pdfs = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    return pdfs

def main():
    print("--- PDF Page Extractor ---")
    
    target_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = None

    # Check if file path is provided as command line argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        if os.path.exists(target_dir):
            pdfs = list_pdfs(target_dir)
            if pdfs:
                print(f"Found {len(pdfs)} PDF(s) in {target_dir}:")
                for i, pdf in enumerate(pdfs, 1):
                    print(f"{i}. {pdf}")
                
                while True:
                    selection = input("\nEnter the number of the PDF to use (or path, or 'q' to quit): ").strip()
                    if selection.lower() == 'q':
                        return
                    
                    if selection.isdigit():
                        idx = int(selection)
                        if 1 <= idx <= len(pdfs):
                            pdf_path = os.path.join(target_dir, pdfs[idx-1])
                            break
                        else:
                            print("Invalid selection.")
                    else:
                        # Maybe they typed a path manually
                        pdf_path = selection.strip('"') 
                        break
            else:
                 print(f"No PDFs found in {target_dir}.")
                 pdf_path = input("Enter the path to the PDF file: ").strip().strip('"')
        else:
            print(f"Directory not found: {target_dir}")
            pdf_path = input("Enter the path to the PDF file: ").strip().strip('"')

    if not pdf_path or not os.path.exists(pdf_path):
        print("Error: The file does not exist. Please check the path and try again.")
        return

    print(f"\nSelected: {pdf_path}")

    while True:
        page_input = input("Enter the page range to extract (e.g. 5~15 or 5) (or 'q' to quit): ").strip()
        if page_input.lower() == 'q':
            break
        
        extract_pages(pdf_path, page_input)
        print("\n")

if __name__ == "__main__":
    main()
