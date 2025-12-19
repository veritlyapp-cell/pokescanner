# PokéScanner

🔴 **Identifica Pokémon con IA y consulta la Pokédex**

Una aplicación web que usa Google Gemini AI para identificar Pokémon desde fotos y proporciona información completa desde PokeAPI, incluyendo audio narrado en español.

## 🌟 Características

- 📸 **Identificación con cámara** - Toma fotos directamente desde tu dispositivo
- 🤖 **IA de Google Gemini** - Reconocimiento preciso de Pokémon
- 🔊 **Voz robótica** - Audio TTS en español estilo Pokédex
- 🧬 **Navegación evolutiva** - Explora familias evolutivas completas
- ⭐ **Favoritos persistentes** - Guarda tus Pokémon favoritos
- 📱 **100% Mobile-Responsive** - Diseñado para celulares
- ⚡ **Optimizado** - Caché para carga rápida

## 🚀 Demo

**URL de la app:** [Tu URL de Streamlit Cloud aquí]

## 📋 Requisitos

- Python 3.8+
- Google AI API Key (gratis en [aistudio.google.com](https://aistudio.google.com))

## 🛠️ Instalación Local

```bash
# Clona el repositorio
git clone https://github.com/TU_USUARIO/pokescanner.git
cd pokescanner

# Instala dependencias
pip install -r requirements.txt

# Configura tu API Key
# Crea .streamlit/secrets.toml y agrega:
# GOOGLE_API_KEY = "tu-api-key-aqui"

# Ejecuta la app
streamlit run app.py
```

## 📱 Uso en Móvil

### Red Local
1. Ejecuta la app en tu PC
2. En tu celular (misma WiFi), ve a: `http://TU-IP:8501`
3. Agrega a pantalla de inicio como PWA

### Streamlit Cloud (Recomendado)
1. Haz fork de este repo
2. Deploy en [share.streamlit.io](https://share.streamlit.io)
3. Configura `GOOGLE_API_KEY` en Secrets
4. Accede desde cualquier dispositivo

## 📁 Estructura del Proyecto

```
pokescanner/
├── app.py              # Aplicación principal
├── utils.py            # Funciones auxiliares
├── requirements.txt    # Dependencias
├── .gitignore         # Archivos ignorados
├── favorites.json     # Favoritos guardados (generado automáticamente)
└── .streamlit/
    └── secrets.toml   # API Keys (no incluido en Git)
```

## 🎯 Tecnologías

- **Streamlit** - Framework web
- **Google Gemini AI** - Identificación de Pokémon
- **PokeAPI** - Datos de Pokémon
- **gTTS** - Text-to-Speech
- **Python** - Backend

## 📖 Cómo Usar

1. **Abre la app** en tu navegador
2. **Toma una foto** de un Pokémon (juguete, carta, pantalla)
3. **Haz clic en "Identificar"**
4. **Explora** la información completa:
   - Nombre y número
   - Tipos y estadísticas
   - Audio en español
   - Evoluciones clickeables
5. **Guarda favoritos** con el botón ⭐
6. **Navega evoluciones** haciendo clic en "Ver"

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - siéntete libre de usar este proyecto

## 🙏 Agradecimientos

- [Google Generative AI](https://ai.google.dev/) - API de Gemini
- [PokeAPI](https://pokeapi.co/) - Datos de Pokémon
- [Streamlit](https://streamlit.io/) - Framework web
- Comunidad Pokémon

## 📧 Contacto

¿Preguntas o sugerencias? Abre un issue en GitHub

---

Hecho con ❤️ para fans de Pokémon
