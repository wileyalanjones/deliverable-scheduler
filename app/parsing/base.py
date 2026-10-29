from . import pdf, docx, eml

class ParsingError(Exception):
    ...


def extract_text(data: bytes, file_type: str) -> str:
    match file_type:
        case "pdf":
            return pdf.extract(data)
        case "docx":
            return docx.extract(data)
        case "eml":
            return eml.extract(data)
        case _:
            raise ParsingError(f"unsupported file type: {file_type}")