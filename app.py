from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import tempfile

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini Pro Vision API
def get_gemini_response(file_path, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([file_path, prompt])
    return response.text

# Streamlit app setup
st.set_page_config(page_title="GeminiDecode: Multilingual Document Extraction")
st.header("GeminiDecode: Multilingual Document Extraction by Gemini Pro")
st.markdown(
    "<span style='font-family: serif;'>"
    "Upload a document image and Gemini Pro will extract key information, "
    "answer questions, and provide insights from it."
    "</span>",
    unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Prompt for Gemini
    input_prompt = """
    You are an expert in understanding invoices.
    Answer any questions based on the uploaded image.
    """

    if st.button("Tell me about the document"):
        # Save uploaded file temporarily for Gemini API
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        # Call Gemini Pro Vision API
        try:
            response = get_gemini_response(tmp_path, input_prompt)
            st.subheader("The response is:")
            st.write(response)
        except Exception as e:
            st.error(f"Error while calling Gemini API: {e}")
