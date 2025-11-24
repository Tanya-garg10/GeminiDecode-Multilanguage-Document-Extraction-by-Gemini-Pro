from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import tempfile

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini Pro Vision API
def get_gemini_response(file_path, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    # Pass file path as input
    response = model.generate_content([file_path, prompt])
    return response.text

# Streamlit app
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
st.markdown(
    "<span style='font-family: serif;'>"
    "Utilizing Gemini Pro AI, this project effortlessly extracts vital information "
    "from diverse multilingual documents, transcending language barriers with precision "
    "and efficiency for enhanced productivity and decision-making."
    "</span>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    input_prompt = """
    You are an expert in understanding invoices.
    We will upload an image as an invoice and you will have to answer any questions based on the uploaded image.
    """

    if st.button("Tell me about the document"):
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name

        # Call Gemini API with file path
        response = get_gemini_response(tmp_file_path, input_prompt)
        st.subheader("The response is:")
        st.write(response)
