import google.generativeai as genai
import requests
from PIL import Image
import json
from gtts import gTTS
import io
import streamlit as st

# Mapeo de tipos a español
TYPE_TRANSLATIONS = {
    "normal": "Normal",
    "fighting": "Lucha",
    "flying": "Volador",
    "poison": "Veneno",
    "ground": "Tierra",
    "rock": "Roca",
    "bug": "Bicho",
    "ghost": "Fantasma",
    "steel": "Acero",
    "fire": "Fuego",
    "water": "Agua",
    "grass": "Planta",
    "electric": "Eléctrico",
    "psychic": "Psíquico",
    "ice": "Hielo",
    "dragon": "Dragón",
    "dark": "Siniestro",
    "fairy": "Hada"
}

def get_available_models(api_key):
    """
    Lists available Gemini models for the provided API key.
    """
    try:
        genai.configure(api_key=api_key)
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        return models
    except:
        return []

def identify_pokemon_with_gemini(api_key, image, model_name='models/gemini-2.5-flash'):
    """
    Identifies a Pokemon from an image using the specified Gemini model.
    Returns: dict with 'nombre_ingles' and 'anime_debut'.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = (
            "Identifica este pokemon. "
            "Devuelve SOLO un JSON válido con este formato exacto (usa comillas dobles): "
            '{"nombre_ingles": "pikachu", "anime_debut": "Temporada 1"}'
        )
        
        response = model.generate_content([prompt, image])
        
        # Clean response text
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        # Try to parse directly first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # If it fails, try replacing single quotes with double quotes
            text = text.replace("'", '"')
            return json.loads(text)
            
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_pokemon_data(name):
    """
    Fetches Pokemon data from PokeAPI.
    Cached to avoid redundant API calls.
    """
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching Pokemon data: {e}")
        return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_species_data(url):
    """
    Fetches species or evolution chain data from a given URL.
    Cached to avoid redundant API calls.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()
    except:
        return None

def generate_pokedex_audio(pokemon_name, pokemon_id, description, height, weight):
    """
    Generates Pokédex-style voice narration using TTS.
    Returns audio bytes with fast, robotic voice.
    """
    try:
        # Convert height from decimeters to meters, weight from hectograms to kg
        height_m = height / 10
        weight_kg = weight / 10
        
        # Format ultra-corto y robótico - cada número/palabra separada
        script = (
            f"{pokemon_name.capitalize()}. "
            f"Número. {pokemon_id}. "
            f"{description}. "
            f"Altura. {height_m}. metros. "
            f"Peso. {weight_kg}. kilos."
        )
        
        # Generate TTS - tld com.mx para voz clara y rápida
        tts = gTTS(text=script, lang='es', slow=False, tld='com.mx')
        
        # Return as bytes
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.read()
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def flatten_evolution_chain(chain_link, current_pokemon_name, evolutions=None, is_past=True):
    """
    Recursively flattens the evolution chain and marks each as past/current/future.
    """
    if evolutions is None:
        evolutions = []
    
    # Get current pokemon details
    species_name = chain_link['species']['name']
    pokemon_id = get_id_from_url(chain_link['species']['url'])
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    
    # Determine evolution type
    if species_name.lower() == current_pokemon_name.lower():
        evolution_type = "current"
        is_past = False  # Found current, next ones are future
    elif is_past:
        evolution_type = "past"
    else:
        evolution_type = "future"
    
    evolutions.append({
        "name": species_name,
        "image_url": image_url,
        "pokemon_id": pokemon_id,
        "evolution_type": evolution_type
    })
    
    # Recursively process next evolutions
    if chain_link['evolves_to']:
        for next_link in chain_link['evolves_to']:
            flatten_evolution_chain(next_link, current_pokemon_name, evolutions, is_past)
            
    return evolutions


def get_id_from_url(url):
    """Helper to extract Pokemon ID from species URL"""
    return url.split('/')[-2]

def translate_types(types_list):
    """Translates a list of type dictionaries to Spanish"""
    translated = []
    for t in types_list:
        type_name = t['type']['name']
        translated.append(TYPE_TRANSLATIONS.get(type_name, type_name.capitalize()))
    return translated
