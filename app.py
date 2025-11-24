### Health Management APP
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini Pro Vision API
def get_gemini_response(input_image, prompt):
    """
    input_image: list containing PIL Image object(s)
    prompt: string
    """
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_image[0], prompt])
    return response.text

# Streamlit page configuration
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

# Description text
text = (
    "Utilizing Gemini Pro AI, this project effortlessly extracts vital information "
    "from diverse multilingual documents, transcending language barriers with precision "
    "and efficiency for enhanced productivity and decision-making."
)
styled_text = f"<span style='font-family: serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# File uploader for image
uploaded_file = st.file_uploader("Choose an image of the document: ", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
else:
    image = None

# Input prompt for Gemini Pro
input_prompt = """
You are an expert in understanding invoices.
We will upload an image as an invoice and you will have to answer any questions based on the uploaded image.
"""

# Submit button
submit = st.button("Tell me about the document")

# If submit button is clicked
if submit:
    if uploaded_file is None:
        st.warning("Please upload an image first.")
    else:
        # Call Gemini Pro API with uploaded image and prompt
        response = get_gemini_response([image], input_prompt)
        st.subheader("The response is")
        st.write(response)
