
import sys
# Try pypdf first if installed (user likely has it if python env is used for other stuff)
# Otherwise fall back to a dumb read if it's text based, but PDFs are binary.
# Since we can't install new system packages easily, we check if we can just read it.
# Actually, let's just ask the User to copy paste or use python to read it if pypdf exists.

try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not installed. Please run: pip install pypdf")
    sys.exit(1)

try:
    reader = PdfReader(r"c:\Users\moras\Documents\GitHub\TRAVO\AI_Model_API_Usage_Guide_v2.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open("pdf_final_output.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("PDF content written to pdf_final_output.txt")
except Exception as e:
    import traceback
    traceback.print_exc()
