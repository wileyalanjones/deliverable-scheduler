from docx import Document
from io import BytesIO

def extract(data: bytes) -> str:
    doc = Document(BytesIO(data))
    paragraph_text = "\n".join(p.text for p in doc.paragraphs)
    table_text_list = []
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    table_text_list.append(p.text)
    table_text = "\n".join(table_text_list)

    return paragraph_text + "\n" + table_text
    