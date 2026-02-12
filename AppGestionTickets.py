import streamlit as st
import supabase
import requests
import pandas as pd
import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://euqtlsheickstdtcfhfi.supabase.co"
SUPABASE_KEY = "sb_publishable_cVoObJObqnsKxRIXgcft4g_ejb6VJnC"
GEMINI_API_KEY = "AIzaSyBBD6CoJl2n2--7DWRTrdLxZMYcr_Mzk0I"

# --- CONEXIÓN SUPABASE ---
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNCIONES ---
def get_all_opportunities():
    with st.spinner("Cargando tickets de oportunidad..."):
        query = (
            client.table("opportunities")
            .select("id, recording_id, title, description, created_at, status, priority, ticket_number, notes, updated_at, recordings(filename, transcription)")
            .order("created_at", desc=True)
        )
        data = query.execute()
        return pd.DataFrame(data.data)

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
if status_filter != "Todos":
    estados = {"Abierto": "Open", "En progreso": "In Progress", "Cerrado": "Closed"}
    df = df[df["status"] == estados[status_filter]]
if priority_filter != "Todas":
    prioridades = {"Alta": "High", "Media": "Medium", "Baja": "Low"}
    df = df[df["priority"] == prioridades[priority_filter]]

# --- TABLERO ---
st.subheader("Tickets de Oportunidad")
for idx, row in df.iterrows():
    with st.container():
        st.markdown(f'<div class="glass">', unsafe_allow_html=True)
        st.write(f"Ticket #{row['ticket_number']} | {row['title']}")
        estado_es = {"Open": "Abierto", "In Progress": "En progreso", "Closed": "Cerrado"}
        prioridad_es = {"High": "Alta", "Medium": "Media", "Low": "Baja"}
        st.write(f"Estado: {estado_es.get(row['status'], row['status'])} | Prioridad: {prioridad_es.get(row['priority'], row['priority'])}")
        st.write(f"Creado: {row['created_at']}")
        st.write(f"Archivo: {row['recordings']['filename'] if row['recordings'] else 'N/D'}")
        st.write(f"Transcripción: {row['recordings']['transcription'][:120] if row['recordings'] and row['recordings']['transcription'] else 'N/D'}...")
        st.write(f"Descripción: {row['description']}")
        st.write(f"Notas: {row['notes'] if row['notes'] else ''}")
        # --- EDICIÓN ---
        with st.expander("Editar Ticket"):
            new_title = st.text_input("Título", value=row['title'], key=f"title_{row['id']}")
            new_desc = st.text_area("Descripción", value=row['description'], key=f"desc_{row['id']}")
            estados_list = ["Abierto", "En progreso", "Cerrado"]
            prioridades_list = ["Alta", "Media", "Baja"]
            new_status = st.selectbox("Estado", estados_list, index=estados_list.index(estado_es.get(row['status'], row['status'])), key=f"status_{row['id']}")
            new_priority = st.selectbox("Prioridad", prioridades_list, index=prioridades_list.index(prioridad_es.get(row['priority'], row['priority'])), key=f"priority_{row['id']}")
            new_notes = st.text_area("Notas", value=row['notes'] if row['notes'] else '', key=f"notes_{row['id']}")
            if st.button("Guardar cambios", key=f"save_{row['id']}"):
                estados_inv = {"Abierto": "Open", "En progreso": "In Progress", "Cerrado": "Closed"}
                prioridades_inv = {"Alta": "High", "Media": "Medium", "Baja": "Low"}
                client.table("opportunities").update({
                    "title": new_title,
                    "description": new_desc,
                    "status": estados_inv[new_status],
                    "priority": prioridades_inv[new_priority],
                    "notes": new_notes,
                    "updated_at": datetime.datetime.now().isoformat()
                }).eq("id", row['id']).execute()
                st.success("Ticket actualizado correctamente")
        # --- GEMINI ---
        if st.button("Re-analizar con Gemini", key=f"gemini_{row['id']}"):
            transcription = row['recordings']['transcription'] if row['recordings'] else ''
            if transcription:
                with st.spinner("Analizando con Gemini..."):
                    response = requests.post(
                        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                        headers={"x-goog-api-key": GEMINI_API_KEY},
                        json={"contents": [{"parts": [{"text": transcription}]}]}
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.info(result['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error("Error al consultar Gemini")
            else:
                st.warning("No hay transcripción disponible.")
        st.markdown('</div>', unsafe_allow_html=True)
