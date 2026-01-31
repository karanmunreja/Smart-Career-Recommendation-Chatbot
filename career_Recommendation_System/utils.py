import pdfplumber
import docx

def extractTextFromPdf(file):
    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text

def extractTextFromDocx(file):
    doc=docx.Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def extractResumeText(file):
    if file.type=="application/pdf":
        return extractTextFromPdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extractTextFromDocx(file)
    return ""

