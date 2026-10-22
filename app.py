import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(page_title="EstudiaMás AI", page_icon="📚", layout="centered")

st.title("📚 EstudiaMás AI - Tu profesor de bolsillo")
st.write("Sube una foto de un problema o tus apuntes y deja que la IA te ayude paso a paso.")

st.sidebar.header("🔑 Configuración")
api_key = st.sidebar.text_input("Introduce tu OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)
    modo = st.sidebar.radio("¿Qué deseas hacer?", ["Resolver un problema paso a paso", "Resumir apuntes o texto"])
    tipo_entrada = st.radio("¿Cómo quieres aportar la imagen?", ["Subir imagen desde el archivo", "Usar la cámara del dispositivo"])

    imagen_cargada = None
    if tipo_entrada == "Subir imagen desde el archivo":
        imagen_cargada = st.file_uploader("Sube una foto clara (PNG, JPG)", type=["png", "jpg", "jpeg"])
    else:
        imagen_cargada = st.camera_input("Haz una foto al problema o texto")

    if imagen_cargada is not None:
        st.image(imagen_cargada, caption="Imagen cargada", use_column_width=True)
        
        if st.button("🚀 Analizar y Resolver"):
            with st.spinner("Analizando la imagen..."):
                try:
                    image_bytes = imagen_cargada.getvalue()
                    base64_image = base64.b64encode(image_bytes).decode("utf-8")
                    
                    if modo == "Resolver un problema paso a paso":
                        prompt_sistema = (
                            "Eres un profesor experto en ciencias y matemáticas. "
                            "Analiza la imagen del problema detalladamente: "
                            "1. Identifica los datos. "
                            "2. Explica el planteamiento. "
                            "3. Desarrolla la solución paso a paso. "
                            "4. Da el resultado final."
                        )
                    else:
                        prompt_sistema = (
                            "Eres un asistente de estudio. "
                            "Analiza la imagen y proporciona: "
                            "- Conceptos clave. "
                            "- Resumen esquemático. "
                            "- 2 preguntas de autoevaluación."
                        )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_sistema},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        },
                                    },
                                ],
                            }
                        ],
                        max_tokens=1200,
                    )
                    
                    resultado_ia = response.choices[0].message.content
                    st.success("¡Análisis completado!")
                    st.markdown("### 📝 Solución / Explicación:")
                    st.markdown(resultado_ia)
                    
                except Exception as e:
                    st.error(f"Error al procesar: {e}")
else:
    st.info("👈 Introduce tu API Key de OpenAI en la barra lateral para empezar.")
