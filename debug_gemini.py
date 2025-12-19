import google.generativeai as genai
from PIL import Image
import toml

try:
    # Read key manually
    with open(".streamlit/secrets.toml", "r") as f:
        content = f.read()
        # Parse simple TOML manually or use lib if available. 
        # Content is: GOOGLE_API_KEY = "..."
        key = content.split('=')[1].strip().strip('"')
    
    print(f"Key loaded: {key[:5]}...{key[-5:]}")
    
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    img = Image.new('RGB', (100, 100), color = 'red')
    
    print("Sending request to Gemini...")
    response = model.generate_content(["Describe this image", img])
    
    print("Response received!")
    print(response.text)

except Exception as e:
    print(f"ERROR OCCURRED: {type(e).__name__}: {e}")
