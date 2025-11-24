import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Vision Model (working & supported)
MODEL_NAME = "models/gemini-pro-latest"


# Convert PDF to images
def pdf_to_images(uploaded_pdf):
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    images = []
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images


# Get Gemini response
def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel(MODEL_NAME)

    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)

    return response.text


# Streamlit UI
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction")

st.title("📄 GeminiDecode — Multilanguage Document Extraction")
st.write("Extract text, insights & structured information from PDFs and Images using Gemini Pro Vision.")

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "jpg", "jpeg", "png"])
prompt = st.text_area("Enter Instruction", 
                      "Extract all important information from this document in structured format.")

if st.button("Process Document"):
    if not uploaded_file:
        st.warning("Please upload a file.")
        st.stop()

    file_type = uploaded_file.name.split(".")[-1].lower()

    with st.spinner("Processing… Please wait 🚀"):
        
        # For PDF
        if file_type == "pdf":
            st.write("📘 Converting PDF pages into images...")
            images = pdf_to_images(uploaded_file)

            full_output = ""
            for i, img in enumerate(images):
                st.image(img, caption=f"Page {i+1}")
                text = get_gemini_response(prompt, img)
                full_output += f"\n\n### Page {i+1}\n{text}\n"

            st.success("Extraction Completed!")
            st.markdown(full_output)

        else:
            # For images (jpg/png)
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
            output = get_gemini_response(prompt, image)
            st.success("Extraction Completed!")
            st.markdown(output)

