import streamlit as st
from PIL import Image
import io

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="SmartConvert",
    page_icon="🔄",
    layout="wide"
)

# ----------------------------
# CUSTOM CLEAN UI
# ----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------
st.title("SmartConvert")
st.markdown("### Convert Anything. Edit Everything.")

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
page = st.sidebar.selectbox(
    "Choose Conversion Type",
    [
        "Home",
        "Image to Text",
        "Image to PDF",
        "PDF to Word",
        "PDF to Excel",
        "PDF to Slides"
    ]
)

# ==================================================
# HOME
# ==================================================
if page == "Home":
    st.markdown("## Welcome 👋")
    st.write("""
    SmartConvert allows you to:
    
    • Convert Image → Text  
    • Convert Image → PDF  
    • Convert PDF → Word  
    • Convert PDF → Excel  
    • Convert PDF → Slides  
    
    Select a tool from the sidebar to begin.
    """)

# ==================================================
# IMAGE TO TEXT
# ==================================================
elif page == "Image to Text":
    st.header("Image to Text")

    uploaded = st.file_uploader(
        "Upload an Image (PNG, JPG)",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.info("OCR functionality can be added with pytesseract.")

# ==================================================
# IMAGE TO PDF
# ==================================================
elif page == "Image to PDF":
    st.header("Image to PDF")

    uploaded = st.file_uploader(
        "Upload an Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:
        image = Image.open(uploaded).convert("RGB")

        pdf_bytes = io.BytesIO()
        image.save(pdf_bytes, format="PDF")
        pdf_bytes.seek(0)

        st.success("Converted Successfully!")

        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="converted.pdf",
            mime="application/pdf"
        )

# ==================================================
# PDF TO WORD
# ==================================================
elif page == "PDF to Word":
    st.header("PDF to Word")

    uploaded = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded:
        st.info("PDF to Word conversion requires python-docx and pdf processing libraries.")

# ==================================================
# PDF TO EXCEL
# ==================================================
elif page == "PDF to Excel":
    st.header("PDF to Excel")

    uploaded = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded:
        st.info("PDF to Excel conversion requires table extraction libraries like camelot or tabula.")

# ==================================================
# PDF TO SLIDES
# ==================================================
elif page == "PDF to Slides":
    st.header("PDF to Slides")

    uploaded = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded:
        st.info("PDF to Slides conversion can be implemented using python-pptx.")
