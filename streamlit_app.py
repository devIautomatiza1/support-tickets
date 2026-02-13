import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import traceback
from typing import Optional, List

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    page_title="Dashboard - Tickets de Soporte",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar tema minimalista profesional moderno
st.markdown("""
<style>
    /* Colores profesionales */
    :root {
        --primary: #3D63FF;
        --secondary: #6B7280;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --bg-dark: #0F172A;
        --bg-light: #1E293B;
        --border: #334155;
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
    }
    
    /* Fondo limpio y moderno */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #0F172A, #1a1f35);
    }
    
    /* Sidebar profesional */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: 1px solid #334155;
    }
    
    /* Tarjetas minimalistas */
    .ticket-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    
    .ticket-card:hover {
        border-color: #64748B;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    .ticket-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 14px 16px;
        border-bottom: 1px solid #334155;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .ticket-body {
        padding: 16px;
    }
    
    .ticket-footer {
        background: #0F172A;
        padding: 12px 16px;
        border-top: 1px solid #334155;
        font-size: 0.85em;
    }
    
    .ticket-title {
        font-size: 1.1em;
        font-weight: 600;
        color: #F1F5F9;
        margin: 0 0 8px 0;
    }
    
    .ticket-description {
        color: #CBD5E1;
        font-size: 0.95em;
        line-height: 1.5;
        margin: 0 0 12px 0;
    }
    
    .ticket-meta {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        font-size: 0.85em;
        margin-bottom: 0;
    }
    
    .meta-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .meta-label {
        color: #94A3B8;
        font-weight: 500;
    }
    
    .meta-value {
        color: #F1F5F9;
        font-weight: 500;
    }
    
    /* Container debug */
    .debug-container {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        margin-top: 16px;
    }
    
    /* Tipografía profesional */
    h1, h2, h3 {
        color: #F1F5F9;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 2em;
        margin-bottom: 4px;
    }
    
    h2 {
        font-size: 1.5em;
        margin-top: 16px;
        margin-bottom: 12px;
    }
    
    h3 {
        font-size: 1.1em;
        margin: 0;
    }
    
    /* Texto general */
    body, p, span, div {
        color: #F1F5F9;
    }
    
    /* Status badges - Minimalistas */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.8em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-open {
        background-color: rgba(239, 68, 68, 0.1);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .status-progress {
        background-color: rgba(245, 158, 11, 0.1);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .status-closed {
        background-color: rgba(16, 185, 129, 0.1);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* Prioridades */
    .priority-high {
        color: #FCA5A5;
        font-weight: 600;
    }
    
    .priority-medium {
        color: #FCD34D;
        font-weight: 600;
    }
    
    .priority-low {
        color: #6EE7B7;
        font-weight: 600;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 1px solid #334155;
        margin: 12px 0;
    }
    
    /* Selectboxes y inputs */
    .stSelectbox, .stTextArea {
        background-color: #1E293B !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #1E293B;
        border-color: #334155;
    }
    
    /* Botones */
    .stButton > button {
        background-color: #3D63FF;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 8px 16px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #4F46E5;
        box-shadow: 0 4px 12px rgba(61, 99, 255, 0.4);
    }
    
    /* Botón editar (color secundario) */
    button[key*="btn_edit_"] {
        background-color: #64748B !important;
    }
    
    button[key*="btn_edit_"]:hover {
        background-color: #475569 !important;
    }
    
    /* Métricas */
    [data-testid="metric-container"] {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: rgba(61, 99, 255, 0.1) !important;
        border: 1px solid #3D63FF !important;
        border-radius: 6px !important;
    }
    
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid #10B981 !important;
        border-radius: 6px !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid #EF4444 !important;
        border-radius: 6px !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid #F59E0B !important;
        border-radius: 6px !important;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 6px;
        color: #F1F5F9;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CREDENCIALES DE SUPABASE
# ============================================================================

SUPABASE_URL = "https://euqtlsheickstdtcfhfi.supabase.co"
SUPABASE_KEY = "sb_publishable_cVoObJObqnsKxRIXgcft4g_ejb6VJnC"
GEMINI_API_KEY = "AIzaSyBBD6CoJl2n2--7DWRTrdLxZMYcr_Mzk0I"

# ============================================================================
# FUNCIONES DE CONEXIÓN A SUPABASE
# ============================================================================

def get_supabase_connection():
    """Obtiene la conexión a Supabase"""
    try:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return client
    except Exception as e:
        return None

def test_connection() -> tuple[bool, str, Optional[int]]:
    """Prueba la conexión a Supabase y retorna (éxito, mensaje, count)"""
    try:
        client = get_supabase_connection()
        if not client:
            return False, "❌ No se pudo inicializar el cliente de Supabase", None
        
        # Intentar obtener conteo de registros
        response = client.table("opportunities").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        
        return True, "✅ Conexión exitosa a Supabase", count
    except Exception as e:
        return False, f"❌ Error de conexión: {str(e)}", None

def fetch_tickets(status_filter: Optional[str] = None, priority_filter: Optional[str] = None) -> pd.DataFrame:
    """Obtiene los tickets de Supabase con filtros opcionales"""
    try:
        client = get_supabase_connection()
        if not client:
            return pd.DataFrame()
        
        # Query base
        query = client.table("opportunities").select(
            "id, ticket_number, title, description, status, priority, notes, created_at, recording_id"
        )
        
        # Aplicar filtros
        if status_filter and status_filter != "Todos":
            query = query.eq("status", status_filter)
        
        if priority_filter and priority_filter != "Todos":
            query = query.eq("priority", priority_filter)
        
        response = query.execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            # Normalizar nombres de columnas y datos
            df.columns = df.columns.str.lower()
            return df
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error al obtener tickets: {str(e)}")
        return pd.DataFrame()

def fetch_recording_name(recording_id: Optional[str]) -> str:
    """Obtiene el nombre de la grabación por ID"""
    if not recording_id:
        return "N/A"
    
    try:
        client = get_supabase_connection()
        if not client:
            return "N/A"
        
        response = client.table("recordings").select("name").eq("id", recording_id).execute()
        if response.data:
            return response.data[0].get("name", "N/A")
        return "N/A"
    except:
        return "N/A"

def update_ticket(ticket_id: int, status: str, notes: str) -> bool:
    """Actualiza un ticket en Supabase"""
    try:
        client = get_supabase_connection()
        if not client:
            return False
        
        response = client.table("opportunities").update({
            "status": status,
            "notes": notes
        }).eq("id", ticket_id).execute()
        
        return True
    except Exception as e:
        st.error(f"Error al actualizar ticket: {str(e)}")
        return False

@st.dialog("Editar Ticket")
def edit_ticket_modal(ticket):
    """Modal para editar ticket"""
    status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
    priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_status_label = {"new": "Nuevo", "in_progress": "En progreso", "closed": "Cerrado", "won": "Ganado"}.get(ticket.get('status', 'new'), "Nuevo")
        status_display = st.selectbox(
            "Estado",
            list(status_map.keys()),
            index=list(status_map.keys()).index(current_status_label) if current_status_label in status_map.keys() else 0,
            key=f"modal_status_{ticket.get('id')}"
        )
        new_status = status_map[status_display]
    
    with col2:
        current_priority_label = {"Low": "Baja", "Medium": "Media", "High": "Alta"}.get(ticket.get('priority', 'Medium'), "Media")
        priority_display = st.selectbox(
            "Prioridad",
            list(priority_map.keys()),
            index=list(priority_map.keys()).index(current_priority_label) if current_priority_label in priority_map.keys() else 0,
            key=f"modal_priority_{ticket.get('id')}"
        )
        new_priority = priority_map[priority_display]
    
    new_notes = st.text_area(
        "Notas",
        value=ticket.get('notes', '') or '',
        key=f"modal_notes_{ticket.get('id')}",
        height=100
    )
    
    col1, col2 = st.columns([0.7, 0.3])
    with col2:
        if st.button("Guardar", key=f"modal_save_{ticket.get('id')}", width='stretch'):
            if update_ticket(ticket.get('id'), new_status, new_notes):
                st.success("Actualizado correctamente")
                st.rerun()
            else:
                st.error("Error al actualizar")

# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================

# Título principal
st.title("🎫 Dashboard de Tickets")
st.markdown("_Gestión de oportunidades de negocio_")
st.markdown("")

# ============================================================================
# BARRA LATERAL - FILTROS
# ============================================================================

st.sidebar.title("Filtros")
st.sidebar.markdown("")

# Obtener tickets para estadísticas
all_tickets = fetch_tickets()

# Definir todos los estados y prioridades posibles
status_options = ["Todos", "new", "in_progress", "closed", "won"]
priority_options = ["Todos", "Low", "Medium", "High"]

# Mapeo para mostrar en español
status_display_map = {
    "Todos": "Todos",
    "new": "Nuevo",
    "in_progress": "En progreso",
    "closed": "Cerrado",
    "won": "Ganado"
}

priority_display_map = {
    "Todos": "Todos",
    "Low": "Baja",
    "Medium": "Media",
    "High": "Alta"
}

# Selectores con display en español
status_display = st.sidebar.selectbox(
    "Estado",
    [status_display_map[s] for s in status_options],
    key="status_filter"
)

priority_display = st.sidebar.selectbox(
    "Prioridad",
    [priority_display_map[p] for p in priority_options],
    key="priority_filter"
)

# Mapear de vuelta a valores de Supabase
selected_status = [k for k, v in status_display_map.items() if v == status_display][0]
selected_priority = [k for k, v in priority_display_map.items() if v == priority_display][0]

# Botón de actualizar
if st.sidebar.button("Actualizar", width='stretch'):
    st.rerun()

st.sidebar.markdown("")
st.sidebar.divider()
st.sidebar.markdown("")

# Mostrar estadísticas
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.metric("Total", len(all_tickets) if not all_tickets.empty else 0)

if not all_tickets.empty:
    nuevos = len(all_tickets[all_tickets["status"] == "new"])
    en_progreso = len(all_tickets[all_tickets["status"] == "in_progress"])
    ganados = len(all_tickets[all_tickets["status"] == "won"])
    
    with col2:
        st.metric("Nuevos", nuevos)
    with col3:
        st.metric("Ganados", ganados)

# ============================================================================
# CONTENIDO PRINCIPAL - VISTA DE TARJETAS
# ============================================================================

# Inicializar session state para modal
if 'edit_ticket_id' not in st.session_state:
    st.session_state.edit_ticket_id = None

# Obtener tickets con filtros
tickets = fetch_tickets(
    status_filter=selected_status if selected_status != "Todos" else None,
    priority_filter=selected_priority if selected_priority != "Todos" else None
)

if tickets.empty:
    st.info("No hay tickets disponibles con los filtros seleccionados.")
else:
    st.subheader(f"Tickets ({len(tickets)})")
    st.markdown("")
    
    # Definir estilos reutilizables
    CARD_STYLES = {
        "container": "background: #1E293B; border: 2px solid #334155; border-radius: 12px; overflow: hidden; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);",
        "header": "background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 16px; border-bottom: 2px solid #334155; display: flex; justify-content: space-between; align-items: center; gap: 12px;",
        "ticket_num": "font-weight: 700; font-size: 1.1em; color: #3D63FF; letter-spacing: 1px;",
        "body": "padding: 18px;",
        "title": "font-size: 1.15em; font-weight: 700; color: #F1F5F9; margin: 0 0 10px 0; word-break: break-word;",
        "description": "color: #CBD5E1; font-size: 0.95em; line-height: 1.6; margin: 0 0 16px 0; word-break: break-word;",
        "meta_grid": "display: grid; grid-template-columns: 1fr 1fr; gap: 14px; padding: 14px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; border-left: 3px solid #3D63FF;",
        "meta_item": "display: flex; flex-direction: column; gap: 6px;",
        "meta_label": "color: #94A3B8; font-weight: 600; font-size: 0.85em;",
        "meta_value": "color: #F1F5F9; font-weight: 600;",
        "footer": "background: #0F172A; padding: 14px 18px; border-top: 2px solid #334155; font-size: 0.9em;",
        "notes_label": "color: #94A3B8; font-weight: 600;",
        "notes_value": "color: #CBD5E1;",
    }
    
    # Crear contenedor para tarjetas
    for idx, ticket in tickets.iterrows():
        # Determinar color de estado
        status_value = str(ticket.get("status", "")).lower()
        if status_value == "new":
            status_class = "status-open"
            status_label = "NUEVO"
        elif status_value == "in_progress":
            status_class = "status-progress"
            status_label = "EN PROGRESO"
        elif status_value == "closed":
            status_class = "status-closed"
            status_label = "CERRADO"
        elif status_value == "won":
            status_class = "status-closed"
            status_label = "GANADO"
        else:
            status_class = "status-open"
            status_label = status_value.upper()
        
        # Determinar prioridad
        priority_value = str(ticket.get("priority", "")).lower()
        if priority_value == "high":
            priority_label = "ALTA"
        elif priority_value == "medium":
            priority_label = "MEDIA"
        elif priority_value == "low":
            priority_label = "BAJA"
        else:
            priority_label = priority_value.upper()
        
        # Limpiar datos
        desc = ticket.get('description', '').replace('"', '').strip()
        notes = (ticket.get('notes', '') or '').replace('\n', ' | ')
        if len(notes) > 200:
            notes = notes[:200] + '...'
        
        ticket_num = ticket.get('ticket_number', 'N/A')
        title = ticket.get('title', 'Sin título')
        created_date = ticket.get('created_at', 'N/A')[:10]
        recording_id = str(ticket.get('recording_id', 'N/A'))[:10]
        ticket_id = ticket.get('id')
        
        # Determinar estilos de estado
        status_colors = {
            "status-open": {
                "bg": "rgba(239, 68, 68, 0.15)",
                "border": "rgba(239, 68, 68, 0.4)",
                "text": "#FCA5A5"
            },
            "status-progress": {
                "bg": "rgba(245, 158, 11, 0.15)",
                "border": "rgba(245, 158, 11, 0.4)",
                "text": "#FCD34D"
            },
            "status-closed": {
                "bg": "rgba(16, 185, 129, 0.15)",
                "border": "rgba(16, 185, 129, 0.4)",
                "text": "#6EE7B7"
            }
        }
        
        colors = status_colors.get(status_class, status_colors["status-open"])
        
        # Construir HTML con estilos separados
        card_html = f'''<div style="{CARD_STYLES['container']}">
  <div style="{CARD_STYLES['header']}">
    <div style="{CARD_STYLES['ticket_num']}">#{ticket_num}</div>
    <div style="background-color: {colors['bg']}; border: 1px solid {colors['border']}; color: {colors['text']}; padding: 6px 14px; border-radius: 8px; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; white-space: nowrap;">{status_label}</div>
  </div>
  <div style="{CARD_STYLES['body']}">
    <div style="{CARD_STYLES['title']}">{title}</div>
    <div style="{CARD_STYLES['description']}">{desc}</div>
    <div style="{CARD_STYLES['meta_grid']}">
      <div style="{CARD_STYLES['meta_item']}">
        <span style="{CARD_STYLES['meta_label']}">ESTADO</span>
        <span style="{CARD_STYLES['meta_value']}">{status_label.title()}</span>
      </div>
      <div style="{CARD_STYLES['meta_item']}">
        <span style="{CARD_STYLES['meta_label']}">PRIORIDAD</span>
        <span style="{CARD_STYLES['meta_value']}">{priority_label.title()}</span>
      </div>
      <div style="{CARD_STYLES['meta_item']}">
        <span style="{CARD_STYLES['meta_label']}">CREADO</span>
        <span style="{CARD_STYLES['meta_value']}">{created_date}</span>
      </div>
      <div style="{CARD_STYLES['meta_item']}">
        <span style="{CARD_STYLES['meta_label']}">GRABACIÓN</span>
        <span style="{CARD_STYLES['meta_value']}; cursor: pointer;" title="{ticket.get('recording_id', 'N/A')}">{recording_id}...</span>
      </div>
    </div>
  </div>
  <div style="{CARD_STYLES['footer']}">
    <span style="{CARD_STYLES['notes_label']}">Notas:</span> 
    <span style="{CARD_STYLES['notes_value']}">{notes if notes else '—'}</span>
  </div>
</div>'''
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Botón Editar usando Streamlit nativo
        col1, col2, col3 = st.columns([0.70, 0.15, 0.15])
        with col3:
            if st.button("Editar", key=f"btn_edit_{ticket_id}", width='stretch'):
                st.session_state.edit_ticket_id = ticket_id
                st.rerun()
    
    # Mostrar modal si hay ticket seleccionado
    if st.session_state.edit_ticket_id:
        matching_tickets = tickets[tickets['id'] == st.session_state.edit_ticket_id]
        if not matching_tickets.empty:
            selected_ticket = matching_tickets.iloc[0].to_dict()
            edit_ticket_modal(selected_ticket)
            st.session_state.edit_ticket_id = None

# ============================================================================
# PANEL DE DIAGNÓSTICO - DEBUG
# ============================================================================

st.markdown("")
st.divider()

with st.expander("🔧 Debug & Conexión", expanded=False):
    debug_col1, debug_col2 = st.columns(2)
    
    with debug_col1:
        st.subheader("📡 Verificación de Conexión")
        
        # Intentar conectar
        success, message, count = test_connection()
        
        if success:
            st.success(message)
            st.info(f"📊 Total de registros en 'opportunities': **{count}**")
        else:
            st.error(message)
    
    with debug_col2:
        st.subheader("🔑 Credenciales Configuradas")
        st.info(f"""
        **URL Supabase:** `{SUPABASE_URL[:30]}...`
        
        **API Key:** `{SUPABASE_KEY[:20]}...`
        
        **Gemini API:** `{GEMINI_API_KEY[:20]}...`
        """)
    
    st.markdown("---")
    
    st.subheader("🧪 Pruebas de Diagnóstico")
    
    if st.button("🔍 Verificar Tabla 'opportunities'"):
        try:
            client = get_supabase_connection()
            if client:
                response = client.table("opportunities").select("*").limit(3).execute()
                if response.data:
                    st.success("✅ Tabla 'opportunities' accesible")
                    st.dataframe(pd.DataFrame(response.data), width='stretch')
                else:
                    st.warning("⚠️ La tabla está vacía o no contiene datos")
            else:
                st.error("❌ No se pudo inicializar cliente Supabase")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.code(traceback.format_exc(), language="python")
    
    if st.button("🔍 Verificar Tabla 'recordings'"):
        try:
            client = get_supabase_connection()
            if client:
                response = client.table("recordings").select("*").limit(3).execute()
                if response.data:
                    st.success("✅ Tabla 'recordings' accesible")
                    st.dataframe(pd.DataFrame(response.data), width='stretch')
                else:
                    st.warning("⚠️ La tabla está vacía o no contiene datos")
            else:
                st.error("❌ No se pudo inicializar cliente Supabase")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.code(traceback.format_exc(), language="python")
    
    if st.button("📋 Listar Todas las Tablas"):
        try:
            client = get_supabase_connection()
            if client:
                # Intentar obtener información del esquema
                response = client.table("information_schema.tables").select("table_name").eq("table_schema", "public").execute()
                if response.data:
                    tables = [row["table_name"] for row in response.data]
                    st.success("✅ Tablas disponibles:")
                    for table in tables:
                        st.write(f"  • {table}")
                else:
                    st.info("No se pudo obtener listado de tablas del esquema")
            else:
                st.error("❌ No se pudo inicializar cliente Supabase")
        except Exception as e:
            st.warning("⚠️ Esquema information_schema puede requerir permisos especiales")
            st.code(str(e), language="text")