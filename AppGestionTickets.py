import streamlit as st
import supabase
import requests
import pandas as pd
import datetime
import os

# --- CONFIGURACIÓN (USAR VARIABLES DE ENTORNO) ---
# NUNCA incluyas claves directamente en el código
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL"))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY"))
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

# Validar que las claves estén configuradas
if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY]):
    st.error("""
    ⚠️ Error de configuración: Faltan credenciales.
    
    Por favor, configura las siguientes variables de entorno o secrets:
    - SUPABASE_URL
    - SUPABASE_KEY  
    - GEMINI_API_KEY
    """)
    st.stop()

# --- CONEXIÓN SUPABASE ---
try:
    client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error conectando a Supabase: {str(e)}")
    st.stop()

# --- FUNCIONES ---
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_all_opportunities():
    with st.spinner("Cargando tickets de oportunidad..."):
        try:
            query = (
                client.table("opportunities")
                .select("id, recording_id, title, description, created_at, status, priority, ticket_number, notes, updated_at, recordings(filename, transcription)")
                .order("created_at", desc=True)
            )
            data = query.execute()
            df = pd.DataFrame(data.data)
            if df.empty:
                st.info("No hay tickets disponibles")
            return df
        except Exception as e:
            st.error(f"Error cargando tickets: {str(e)}")
            return pd.DataFrame()

def traducir_estado(status_en):
    """Traduce estado de inglés a español"""
    traducciones = {"Open": "Abierto", "In Progress": "En progreso", "Closed": "Cerrado"}
    return traducciones.get(status_en, status_en)

def traducir_prioridad(priority_en):
    """Traduce prioridad de inglés a español"""
    traducciones = {"High": "Alta", "Medium": "Media", "Low": "Baja"}
    return traducciones.get(priority_en, priority_en)

def estado_a_ingles(status_es):
    """Traduce estado de español a inglés"""
    traducciones = {"Abierto": "Open", "En progreso": "In Progress", "Cerrado": "Closed"}
    return traducciones.get(status_es, status_es)

def prioridad_a_ingles(priority_es):
    """Traduce prioridad de español a inglés"""
    traducciones = {"Alta": "High", "Media": "Medium", "Baja": "Low"}
    return traducciones.get(priority_es, priority_es)

# --- DASHBOARD ---
st.set_page_config(page_title="AppGestionTickets", page_icon="📝", layout="wide")
st.title("📝 AppGestionTickets - Gestión de Tickets")

st.markdown(
    """
    <style>
    .glass {
        background: rgba(255,255,255,0.2);
        box-shadow: 0 4px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(7px);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.3);
        padding: 1.5em;
        margin-bottom: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FILTROS ---
st.sidebar.header("Filtros avanzados")
status_filter = st.sidebar.selectbox("Estado", ["Todos", "Abierto", "En progreso", "Cerrado"])
priority_filter = st.sidebar.selectbox("Prioridad", ["Todas", "Alta", "Media", "Baja"])

# --- DATOS ---
df = get_all_opportunities()

if not df.empty:
    # Aplicar filtros
    if status_filter != "Todos":
        status_en = estado_a_ingles(status_filter)
        df = df[df["status"] == status_en]
    if priority_filter != "Todas":
        priority_en = prioridad_a_ingles(priority_filter)
        df = df[df["priority"] == priority_en]

    # --- TABLERO ---
    st.subheader("Tickets de Oportunidad")
    
    if df.empty:
        st.info("No hay tickets que coincidan con los filtros seleccionados")
    else:
        for idx, row in df.iterrows():
            with st.container():
                st.markdown(f'<div class="glass">', unsafe_allow_html=True)
                
                # Mostrar información del ticket
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Ticket #{row['ticket_number']}** | {row['title']}")
                with col2:
                    st.write(f"Creado: {row['created_at'][:10] if row['created_at'] else 'N/D'}")
                
                st.write(f"**Estado:** {traducir_estado(row['status'])} | **Prioridad:** {traducir_prioridad(row['priority'])}")
                
                # Transcripción
                if row['recordings']:
                    st.write(f"**Archivo:** {row['recordings'].get('filename', 'N/D')}")
                    transcription = row['recordings'].get('transcription', '')
                    if transcription:
                        st.write(f"**Transcripción:** {transcription[:200]}...")
                    else:
                        st.write("*Sin transcripción disponible*")
                else:
                    st.write("*Sin grabación asociada*")
                
                st.write(f"**Descripción:** {row['description'] if row['description'] else 'Sin descripción'}")
                
                if row['notes']:
                    st.write(f"**Notas:** {row['notes']}")
                
                # --- EDICIÓN ---
                with st.expander("✏️ Editar Ticket"):
                    new_title = st.text_input("Título", value=row['title'] or "", key=f"title_{row['id']}")
                    new_desc = st.text_area("Descripción", value=row['description'] or "", key=f"desc_{row['id']}")
                    
                    estados_list = ["Abierto", "En progreso", "Cerrado"]
                    prioridades_list = ["Alta", "Media", "Baja"]
                    
                    new_status = st.selectbox(
                        "Estado", 
                        estados_list, 
                        index=estados_list.index(traducir_estado(row['status'])), 
                        key=f"status_{row['id']}"
                    )
                    
                    new_priority = st.selectbox(
                        "Prioridad", 
                        prioridades_list, 
                        index=prioridades_list.index(traducir_prioridad(row['priority'])), 
                        key=f"priority_{row['id']}"
                    )
                    
                    new_notes = st.text_area("Notas", value=row['notes'] or "", key=f"notes_{row['id']}")
                    
                    if st.button("💾 Guardar cambios", key=f"save_{row['id']}"):
                        try:
                            client.table("opportunities").update({
                                "title": new_title,
                                "description": new_desc,
                                "status": estado_a_ingles(new_status),
                                "priority": prioridad_a_ingles(new_priority),
                                "notes": new_notes,
                                "updated_at": datetime.datetime.now().isoformat()
                            }).eq("id", row['id']).execute()
                            st.success("✅ Ticket actualizado correctamente")
                            st.cache_data.clear()  # Limpiar caché
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error actualizando ticket: {str(e)}")
                
                # --- GEMINI ---
                if st.button("🤖 Re-analizar con Gemini", key=f"gemini_{row['id']}"):
                    transcription = row['recordings']['transcription'] if row.get('recordings') else ''
                    if transcription:
                        with st.spinner("Analizando con Gemini..."):
                            try:
                                response = requests.post(
                                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
                                    json={
                                        "contents": [{
                                            "parts": [{
                                                "text": f"Analiza esta transcripción de un ticket de soporte y proporciona: 1) Resumen del problema, 2) Posible solución, 3) Prioridad sugerida:\n\n{transcription[:2000]}"
                                            }]
                                        }]
                                    },
                                    timeout=30
                                )
                                if response.status_code == 200:
                                    result = response.json()
                                    analysis = result['candidates'][0]['content']['parts'][0]['text']
                                    st.info(analysis)
                                else:
                                    st.error(f"Error al consultar Gemini: {response.status_code}")
                            except Exception as e:
                                st.error(f"Error en la conexión con Gemini: {str(e)}")
                    else:
                        st.warning("⚠️ No hay transcripción disponible para analizar.")
                
                st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("No se pudieron cargar los datos. Verifica la conexión con Supabase.")