from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Google Gemini Pro Vision API
def get_gemini_response(input_image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    # Pass the uploaded file directly along with the prompt
    response = model.generate_content([input_image, prompt])
    return response.text

# Streamlit app configuration
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

# File uploader for documents
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    input_prompt = """
    You are an expert in understanding invoices.
    We will upload an image as an invoice and you will have to answer any questions based on the uploaded image.
    """

    if st.button("Tell me about the document"):
        # Call Gemini Pro API directly with the uploaded file
        response = get_gemini_response(uploaded_file, input_prompt)
        st.subheader("The response is:")
        st.write(response)
