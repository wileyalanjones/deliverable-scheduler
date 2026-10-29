from email import policy 
from email.parser import BytesParser


def extract(data: bytes) -> str:
    msg = BytesParser(policy=policy.default).parsebytes(data)
    body = msg.get_body(preferencelist=("plain", "html"))
    if body is None:
        return ""
    return body.get_content()