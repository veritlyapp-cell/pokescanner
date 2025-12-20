import streamlit as st
from PIL import Image
import utils
import json
import os

# --- Page Config ---
st.set_page_config(
    page_title="PokéScanner",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Mobile-Responsive CSS ---
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .type-badge {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        font-size: 14px;
    }
    
    /* Larger touch targets for mobile */
    .stButton button {
        width: 100%;
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    /* Responsive images */
    img {
        max-width: 100%;
        height: auto;
    }
    
    /* Better spacing on mobile */
    @media (max-width: 768px) {
        .stColumn {
            padding: 5px !important;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        .type-badge {
            font-size: 12px;
            padding: 6px 12px;
        }
    }
    
    /* Hide Streamlit branding on mobile */
    @media (max-width: 768px) {
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🔴 PokéScanner")
st.markdown("*Identifica Pokémon con IA*")

# --- Favorites Persistence ---
FAVORITES_FILE = "favorites.json"

def load_favorites():
    """Load favorites from JSON file"""
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_favorites(favorites):
    """Save favorites to JSON file"""
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error guardando favoritos: {e}")

# --- Initialize Session State ---
if 'selected_pokemon' not in st.session_state:
    st.session_state.selected_pokemon = None
if 'favorites' not in st.session_state:
    st.session_state.favorites = load_favorites()
if 'last_scan' not in st.session_state:
    st.session_state.last_scan = None

# --- Sidebar: Favorites Only ---
with st.sidebar:
    st.header("⭐ Pokémon Guardados")
    
    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            if st.button(f"#{fav['id']:03d} {fav['name'].capitalize()}", key=f"fav_{fav['name']}", use_container_width=True):
                st.session_state.selected_pokemon = fav['name']
                st.rerun()
    else:
        st.info("Aún no has guardado ningún Pokémon")

# --- Get API Keys from secrets (supports multiple keys) ---
api_keys = []

# Try to load multiple API keys
for i in range(1, 6):  # Support up to 5 API keys
    key_name = f"GOOGLE_API_KEY_{i}" if i > 1 else "GOOGLE_API_KEY"
    key = st.secrets.get(key_name, "")
    if key:
        api_keys.append(key)

if not api_keys:
    st.error("⚠️ API Key no configurada. Agrega GOOGLE_API_KEY en .streamlit/secrets.toml")
    st.stop()

# Show how many API keys are loaded (for debugging)
if len(api_keys) > 1:
    st.sidebar.caption(f"🔑 {len(api_keys)} API Keys configuradas")

# --- Input Section ---
if not st.session_state.selected_pokemon:
    st.subheader("📸 Toma una Foto")
    camera_img = st.camera_input("Usa tu cámara para identificar un Pokémon")
    
    if camera_img and api_keys:
        img = Image.open(camera_img)
        
        if st.button("🔍 Identificar Pokémon", use_container_width=True):
            with st.spinner("Analizando con Gemini AI..."):
                try:
                    gemini_data = utils.identify_pokemon_with_gemini(api_keys, img, "models/gemini-2.5-flash")
                    
                    if "error" in gemini_data:
                        error_msg = gemini_data['error'].lower()
                        
                        # Check for quota errors - includes the QUOTA_EXCEEDED flag from rotation
                        if "quota" in error_msg or "resource_exhausted" in error_msg or "429" in error_msg or error_msg == "quota_exceeded":
                            st.warning("⏰ **Has usado demasiado el Pokédex**")
                            st.info("🔄 Vuelve en **1-2 minutos** y podrás seguir identificando Pokémon")
                            st.caption("💡 La versión gratuita tiene un límite de 15 búsquedas por minuto")
                            # Show debug info if multiple keys configured
                            if len(api_keys) > 1:
                                st.caption(f"⚠️ Todas las {len(api_keys)} API Keys han alcanzado el límite diario")
                        elif "api_key" in error_msg or "invalid" in error_msg:
                            st.error("🔑 **API Key no válida**")
                            st.info("Verifica que tu API Key esté correctamente configurada")
                        else:
                            st.error(f"❌ Error: {gemini_data['error']}")
                    else:
                        nombre_ingles = gemini_data.get('nombre_ingles')
                        if nombre_ingles:
                            st.session_state.selected_pokemon = nombre_ingles
                            st.session_state.last_scan = gemini_data.get('anime_debut', 'Información no disponible')
                            st.rerun()
                        else:
                            st.error("🤔 No se pudo identificar el Pokémon. Intenta con mejor iluminación.")
                except Exception as e:
                    error_str = str(e).lower()
                    
                    # Check for quota errors in exception
                    if "quota" in error_str or "resource_exhausted" in error_str or "429" in error_str:
                        st.warning("⏰ **Has usado demasiado el Pokédex**")
                        st.info("🔄 Vuelve en **1-2 minutos** y podrás seguir identificando Pokémon")
                        st.caption("💡 La versión gratuita tiene un límite de 15 búsquedas por minuto")
                    else:
                        st.error(f"❌ Error inesperado: {str(e)}")
    elif camera_img and not api_keys:
        st.warning("⚠️ Por favor configura tu API Key")
    
# --- Display Pokemon ---
if st.session_state.selected_pokemon and api_keys:
    nombre_ingles = st.session_state.selected_pokemon
    anime_debut = st.session_state.last_scan or "De la línea evolutiva"
    
    # Fetch Pokemon data
    poke_data = utils.get_pokemon_data(nombre_ingles)
    
    if not poke_data:
        st.error(f"No se encontraron datos en PokeAPI para: {nombre_ingles}")
        if st.button("← Volver"):
            st.session_state.selected_pokemon = None
            st.session_state.last_scan = None
            st.rerun()
    else:
        # Parse data
        pokemon_id = poke_data['id']
        official_image = poke_data['sprites']['other']['official-artwork']['front_default']
        types = utils.translate_types(poke_data['types'])
        height = poke_data['height']
        weight = poke_data['weight']
        
        species_url = poke_data['species']['url']
        species_data = utils.get_species_data(species_url)
        
        description = "Un Pokémon misterioso."
        if species_data and 'flavor_text_entries' in species_data:
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'es':
                    description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                    break
        
        audio_bytes = utils.generate_pokedex_audio(nombre_ingles, pokemon_id, description, height, weight)
        
        # --- Header ---
        st.markdown("---")
        col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
        
        with col_h1:
            st.markdown(f"## #{pokemon_id:03d} {nombre_ingles.capitalize()}")
        
        with col_h2:
            is_favorite = any(f['name'] == nombre_ingles for f in st.session_state.favorites)
            if not is_favorite:
                if st.button("⭐ Guardar"):
                    st.session_state.favorites.append({'name': nombre_ingles, 'id': pokemon_id})
                    save_favorites(st.session_state.favorites)  # Save to file
                    st.rerun()
            else:
                st.success("✅ Guardado")
        
        with col_h3:
            if st.button("← Volver"):
                st.session_state.selected_pokemon = None
                st.session_state.last_scan = None
                st.rerun()
        
        # --- Main Info ---
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if official_image:
                st.image(official_image, width=300)
            else:
                st.warning("No hay arte oficial disponible.")
        
        with col2:
            st.markdown(f"**🎬 Debut en Anime:** {anime_debut}")
            st.markdown("**Tipos:**")
            for t in types:
                st.markdown(f'<span class="type-badge">{t}</span>', unsafe_allow_html=True)
            
            height_m = height / 10
            weight_kg = weight / 10
            st.markdown(f"**📏 Altura:** {height_m:.1f}m | **⚖️ Peso:** {weight_kg:.1f}kg")
        
        # --- Audio ---
        st.markdown("### 🔊 Escucha la Pokédex")
        if audio_bytes:
            st.audio(audio_bytes, format='audio/mp3')
        else:
            st.warning("No se pudo generar el audio.")
        
        # --- Description ---
        st.markdown("### 📖 Descripción")
        st.info(description)
        
        # --- Evolution Chain ---
        st.markdown("### 🧬 Línea Evolutiva")
        if species_data:
            evo_chain_url = species_data['evolution_chain']['url']
            evo_chain_data = utils.get_species_data(evo_chain_url)
            
            if evo_chain_data:
                chain = evo_chain_data['chain']
                evolutions = utils.flatten_evolution_chain(chain, nombre_ingles)
                
                past_evos = [e for e in evolutions if e['evolution_type'] == 'past']
                current_evo = [e for e in evolutions if e['evolution_type'] == 'current']
                future_evos = [e for e in evolutions if e['evolution_type'] == 'future']
                
                if past_evos:
                    st.markdown("#### ⬅️ Evoluciones Previas")
                    cols = st.columns(len(past_evos))
                    for idx, evo in enumerate(past_evos):
                        with cols[idx]:
                            st.image(evo['image_url'], width=120)
                            st.caption(f"#{int(evo['pokemon_id']):03d}")
                            st.caption(evo['name'].capitalize())
                            if st.button(f"Ver", key=f"past_{idx}"):
                                st.session_state.selected_pokemon = evo['name']
                                st.session_state.last_scan = None
                                st.rerun()
                
                if current_evo:
                    st.markdown("#### ✨ Actual")
                    st.image(current_evo[0]['image_url'], width=150)
                    st.caption(f"**#{int(current_evo[0]['pokemon_id']):03d} {current_evo[0]['name'].capitalize()}**")
                
                if future_evos:
                    st.markdown("#### ➡️ Evoluciones Futuras")
                    cols = st.columns(len(future_evos))
                    for idx, evo in enumerate(future_evos):
                        with cols[idx]:
                            st.image(evo['image_url'], width=120)
                            st.caption(f"#{int(evo['pokemon_id']):03d}")
                            st.caption(evo['name'].capitalize())
                            if st.button(f"Ver", key=f"future_{idx}"):
                                st.session_state.selected_pokemon = evo['name']
                                st.session_state.last_scan = None
                                st.rerun()
        else:
            st.warning("No se pudo cargar la cadena evolutiva.")
