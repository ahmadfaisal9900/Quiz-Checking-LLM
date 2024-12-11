import os
import base64
import google.generativeai as genai
from API_Key import gen_api_key
API_KEY = gen_api_key()
# Configure the Google Generative AI API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Hidden prompt
hidden_prompt = "Check each quiz and say which are right and which are wrong. Each question is worth one mark, and tell obtained marks at the end for each quiz."

# Function to process all images in a directory
def process_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: The specified path {directory} is not a directory.")
        return

    image_files = [f for f in os.listdir(directory) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not image_files:
        print("No image files found in the directory.")
        return

    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        print(f"Processing {image_file}...")
        try:
            with open(image_path, "rb") as img_file:
                image_content = img_file.read()

            # Call the AI model
            response = model.generate_content([
                {
                    'mime_type': 'image/jpeg',
                    'data': base64.b64encode(image_content).decode('utf-8')
                },
                hidden_prompt
            ])

            print(f"Result for {image_file}:")
            print(response.text)
            print("-" * 50)

        except Exception as e:
            print(f"Error processing {image_file}: {e}")

# Example usage
def main():
    directory = input("Enter the directory path containing the quiz images: ").strip()
    process_directory(directory)

if __name__ == "__main__":
    main()

    