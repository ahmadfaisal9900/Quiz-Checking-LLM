import streamlit as st
import google.generativeai as genai
import base64
import os
from API_Key import gen_api_key
API_KEY = gen_api_key()
# Configure the Google Generative AI API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Function to process the image and generate content
def process_image_with_prompt(image_path, prompt):
    try:
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()

        response = model.generate_content([
            {
                'mime_type': 'image/jpeg',
                'data': base64.b64encode(image_content).decode('utf-8')
            },
            prompt
        ])
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Set the page layout
st.set_page_config(page_title="Quiz Checker", layout="centered")

st.title("LLM Quiz Checker")

st.subheader("Upload a Handwritten Quiz and Provide a Prompt")
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Prompt input
user_prompt = st.text_area(
    "Enter your prompt (e.g., 'Check each quiz and say which are right and which are wrong.')",
    placeholder="Type your prompt here...",
    height=150
)

# Process and display the result
if st.button("Submit"):
    if uploaded_file and user_prompt.strip():
        # Save the uploaded image temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as temp_file:
            temp_file.write(uploaded_file.read())
        
        # Process the image with the prompt
        result = process_image_with_prompt(temp_path, user_prompt.strip())

        # Clean up the temporary file
        os.remove(temp_path)

        # Display the result in the main area
        st.success("Response from AI:")
        st.write(result)
    else:
        st.error("Please upload an image and provide a prompt before submitting.")
