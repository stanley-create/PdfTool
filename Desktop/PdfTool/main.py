import os
import sys
import subprocess

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("偵測到缺少必要組件，正在為您自動配置 (pypdf)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
        from pypdf import PdfReader, PdfWriter
        print("配置完成！\n")
    except Exception as e:
        print(f"自動配置失敗，請手動輸入 'pip install pypdf'。錯誤原因: {e}")
        sys.exit(1)

def extract_pages(pdf_path, page_range_str):
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        separator = '~' if '~' in page_range_str else '-'
        parts = page_range_str.split(separator) if separator in page_range_str else [page_range_str]
            
        if len(parts) == 1:
            start_page = end_page = int(parts[0])
        elif len(parts) == 2:
            start_page, end_page = int(parts[0]), int(parts[1])
        else:
            print("格式錯誤。請使用 '開始~結束' (如 5~15) 或單一頁碼。")
            return

        if start_page < 1 or end_page > total_pages or start_page > end_page:
            print(f"錯誤：無效頁碼。該文件共 {total_pages} 頁。")
            return

        writer = PdfWriter()
        for p in range(start_page, end_page + 1):
            writer.add_page(reader.pages[p - 1])

        output_filename = f"extracted_{start_page}.pdf" if start_page == end_page else f"extracted_{start_page}_to_{end_page}.pdf"
        output_path = os.path.join(os.path.dirname(pdf_path), output_filename)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        print(f"成功！已儲存至: {output_path}")

    except ValueError:
        print("錯誤：請輸入正確的數字格式。")
    except Exception as e:
        print(f"發生錯誤: {e}")

def list_pdfs(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]

def main():
    print("--- PDF 頁面提取工具 (AI 協作版) ---")
    
    target_dir = os.path.dirname(os.path.abspath(__file__))
    
    pdfs = list_pdfs(target_dir)
    if not pdfs:
        print(f"在 {target_dir} 中找不到 PDF 檔案。")
        pdf_path = input("請輸入 PDF 的完整路徑: ").strip().strip('"')
    else:
        print(f"在目錄中找到 {len(pdfs)} 個檔案：")
        for i, pdf in enumerate(pdfs, 1):
            print(f"{i}. {pdf}")
        
        choice = input("\n請輸入編號選擇檔案 (或按 q 退出): ").strip()
        if choice.lower() == 'q': return
        
        if choice.isdigit() and 1 <= int(choice) <= len(pdfs):
            pdf_path = os.path.join(target_dir, pdfs[int(choice)-1])
        else:
            pdf_path = choice.strip('"')

    if not os.path.exists(pdf_path):
        print("錯誤：檔案不存在。")
        return

    while True:
        page_input = input("\n請輸入要提取的頁碼範圍 (例如 5~15 或 5) (按 q 退出): ").strip()
        if page_input.lower() == 'q': break
        extract_pages(pdf_path, page_input)

if __name__ == "__main__":
    main()
