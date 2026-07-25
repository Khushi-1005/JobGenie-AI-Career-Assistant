import google.generativeai as genai

from config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load the model
model = genai.GenerativeModel("gemini-2.5-flash")

# Ask a question
response = model.generate_content(
    "Explain Agentic AI in simple words."
)

print(response.text)