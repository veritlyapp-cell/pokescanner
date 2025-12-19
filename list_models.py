import google.generativeai as genai
import toml

try:
    with open(".streamlit/secrets.toml", "r") as f:
        content = f.read()
        key = content.split('=')[1].strip().strip('"')
    
    genai.configure(api_key=key)
    
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

except Exception as e:
    print(f"Error: {e}")
