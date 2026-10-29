import fitz 

def extract(data: bytes) -> str:
    doc = fitz.open(stream=data, filetype="pdf")
    try:
        pages = []
        for page in doc:
            page_text = page.get_text("text")
            pages.append(page_text)
        return "\n".join(pages)
    finally:
        doc.close()