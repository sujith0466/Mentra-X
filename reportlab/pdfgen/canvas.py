from __future__ import annotations


class Canvas:
    def __init__(self, buffer, pagesize=(595.27, 841.89)):
        self.buffer = buffer
        self.pagesize = pagesize
        self.title = ""
        self.lines = []

    def setTitle(self, title):
        self.title = title

    def setLineWidth(self, width):
        return None

    def rect(self, *args, **kwargs):
        return None

    def drawImage(self, *args, **kwargs):
        return None

    def setFont(self, *args, **kwargs):
        return None

    def drawCentredString(self, x, y, text):
        self.lines.append(str(text))

    def save(self):
        content = "\n".join(self.lines) if self.lines else (self.title or "Mentra Certificate")
        pdf_bytes = (
            b"%PDF-1.4\n"
            + content.encode("utf-8", errors="ignore")
            + b"\n%%EOF"
        )
        self.buffer.write(pdf_bytes)
