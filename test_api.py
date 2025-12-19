import utils
import streamlit as st
from PIL import Image
import io

# Create a small dummy image for testing
dummy_img = Image.new('RGB', (100, 100), color = 'red')

# Try to load key from secrets
try:
    key = st.secrets["GOOGLE_API_KEY"]
    print(f"Testing with Key: {key[:5]}...{key[-5:]}")
    
    print("Calling Gemini...")
    result = utils.identify_pokemon_with_gemini(key, dummy_img)
    print("Result:")
    print(result)
    
except Exception as e:
    print(f"Setup Error: {e}")
