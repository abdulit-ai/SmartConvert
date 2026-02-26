import streamlit as st
from PIL import Image
import easyocr
from io import BytesIO
from docx import Document
from pdf2docx import Converter
import fitz  # PyMuPDF
import pandas as pd
from pptx import Presentation

st.set_page_config(page_title="Smart Document Converter", layout="wide")

# ---------- UI Styling ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
}
.block-container {
    padding: 3rem;
}
h1 {
    font-size: 45px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar Navigation ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Image to Text", "Image to Word", "Image to PDF",
     "PDF to Word", "PDF to Excel", "PDF to Slides"]
)

# ---------- Homepage ----------
if page == "Home":
    st.title("Smart Document Converter")
    st.write("""
    Convert files instantly with high accuracy.

    ### Features:
    - Image → Text
    - Image → Word
    - Image → PDF
    - PDF → Word
    - PDF → Excel
    - PDF → Slides
    """)

    st.info("Select a tool from the sidebar to start.")

# ---------- OCR Loader ----------
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'], gpu=False)

# ---------- Image to Text ----------
elif page == "Image to Text":
    st.header("Image to Text")

    uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image)

        reader = load_ocr()
        result = reader.readtext(image)

        text_output = " ".join([res[1] for res in result])

        st.text_area("Extracted Text", text_output, height=300)

# ---------- Image to Word ----------
elif page == "Image to Word":
    st.header("Image to Word")

    uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        reader = load_ocr()
        result = reader.readtext(image)

        text_output = "\n".join([res[1] for res in result])

        doc = Document()
        doc.add_paragraph(text_output)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            "Download Word Document",
            buffer,
            file_name="converted.docx"
        )

# ---------- Image to PDF ----------
elif page == "Image to PDF":
    st.header("Image to PDF")

    uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded:
        image = Image.open(uploaded)
        buffer = BytesIO()
        image.save(buffer, format="PDF")
        buffer.seek(0)

        st.download_button(
            "Download PDF",
            buffer,
            file_name="converted.pdf"
        )

# ---------- PDF to Word ----------
elif page == "PDF to Word":
    st.header("PDF to Word")

    uploaded = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded.read())

        cv = Converter("temp.pdf")
        cv.convert("converted.docx", start=0, end=None)
        cv.close()

        with open("converted.docx", "rb") as f:
            st.download_button(
                "Download Word File",
                f,
                file_name="converted.docx"
            )

# ---------- PDF to Excel ----------
elif page == "PDF to Excel":
    st.header("PDF to Excel")

    uploaded = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded:
        pdf = fitz.open(stream=uploaded.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()

        df = pd.DataFrame({"Extracted Text": [text]})
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            "Download Excel",
            buffer,
            file_name="converted.xlsx"
        )

# ---------- PDF to Slides ----------
elif page == "PDF to Slides":
    st.header("PDF to Slides")

    uploaded = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded:
        pdf = fitz.open(stream=uploaded.read(), filetype="pdf")
        prs = Presentation()

        for page in pdf:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            text = page.get_text()
            slide.placeholders[1].text = text[:1000]

        buffer = BytesIO()
        prs.save(buffer)
        buffer.seek(0)

        st.download_button(
            "Download Slides",
            buffer,
            file_name="converted.pptx"
        )
