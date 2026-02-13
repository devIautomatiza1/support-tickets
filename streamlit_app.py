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

# ============================================================================
# CSS MEJORADO - Tarjetas con botón integrado
# ============================================================================

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
        --text-tertiary: #94A3B8;
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
    
    /* Tarjetas - Estilo exacto como la imagen */
    .ticket-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 20px;
        transition: all 0.2s ease;
        position: relative;
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
    
    .ticket-header-left {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .ticket-number {
        font-weight: 700;
        font-size: 1em;
        color: #F1F5F9;
    }
    
    .ticket-body {
        padding: 16px;
    }
    
    .ticket-footer {
        background: #0F172A;
        padding: 12px 16px;
        border-top: 1px solid #334155;
        font-size: 0.85em;
        display: flex;
        justify-content: space-between;
        align-items: center;
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
        margin: 0 0 16px 0;
    }
    
    .ticket-meta {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        font-size: 0.85em;
    }
    
    .meta-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .meta-label {
        color: #94A3B8;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .meta-value {
        color: #F1F5F9;
        font-weight: 500;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.75em;
        font-weight: 700;
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
    
    .status-won {
        background-color: rgba(16, 185, 129, 0.1);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* Botón de editar - Estilo secundario */
    .edit-button {
        background-color: #64748B;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85em;
        padding: 6px 16px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .edit-button:hover {
        background-color: #475569;
        box-shadow: 0 4px 12px rgba(100, 116, 139, 0.3);
    }
    
    /* Notas */
    .notes-label {
        color: #94A3B8;
        font-weight: 600;
        margin-right: 8px;
    }
    
    .notes-text {
        color: #CBD5E1;
    }
    
    /* Ocultar elementos duplicados de Streamlit */
    .stButton {
        display: none;
    }
    
    /* Ajustes de tipografía */
    h1, h2, h3, p, span, div {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Métricas */
    [data-testid="metric-container"] {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
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
    """Prueba la conexión a Supabase"""
    try:
        client = get_supabase_connection()
        if not client:
            return False, "❌ No se pudo inicializar el cliente de Supabase", None
        
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
        
        query = client.table("opportunities").select(
            "id, ticket_number, title, description, status, priority, notes, created_at, recording_id"
        )
        
        if status_filter and status_filter != "Todos":
            query = query.eq("status", status_filter)
        
        if priority_filter and priority_filter != "Todos":
            query = query.eq("priority", priority_filter)
        
        response = query.execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            df.columns = df.columns.str.lower()
            return df
        return pd.DataFrame()
    
    except Exception as e:
        return pd.DataFrame()

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
        return False

# ============================================================================
# MODAL DE EDICIÓN
# ============================================================================

@st.dialog("✏️ Editar Ticket")
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
            index=list(status_map.keys()).index(current_status_label) if current_status_label in status_map.keys() else 0
        )
        new_status = status_map[status_display]
    
    with col2:
        current_priority_label = {"Low": "Baja", "Medium": "Media", "High": "Alta"}.get(ticket.get('priority', 'Medium'), "Media")
        priority_display = st.selectbox(
            "Prioridad",
            list(priority_map.keys()),
            index=list(priority_map.keys()).index(current_priority_label) if current_priority_label in priority_map.keys() else 0
        )
        new_priority = priority_map[priority_display]
    
    new_notes = st.text_area(
        "Notas",
        value=ticket.get('notes', '') or '',
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Guardar Cambios", use_container_width=True):
            if update_ticket(ticket.get('id'), new_status, new_notes):
                st.success("✅ Ticket actualizado correctamente")
                st.rerun()
            else:
                st.error("❌ Error al actualizar el ticket")
    with col3:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()

# ============================================================================
# FUNCIÓN PARA RENDERIZAR TARJETA CON BOTÓN INTEGRADO
# ============================================================================

def render_ticket_card(ticket, edit_callback):
    """Renderiza una tarjeta de ticket con botón de edición integrado"""
    
    # Determinar estado
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
        status_class = "status-won"
        status_label = "GANADO"
    else:
        status_class = "status-open"
        status_label = status_value.upper()
    
    # Determinar prioridad
    priority_value = str(ticket.get("priority", "")).lower()
    priority_label = {
        "high": "ALTA",
        "medium": "MEDIA",
        "low": "BAJA"
    }.get(priority_value, priority_value.upper())
    
    # Limpiar datos
    desc = ticket.get('description', '').replace('"', '').strip()
    notes = (ticket.get('notes', '') or '').replace('\n', ' | ')
    if len(notes) > 150:
        notes = notes[:150] + '...'
    
    ticket_num = ticket.get('ticket_number', 'N/A')
    title = ticket.get('title', 'Sin título')
    created_date = ticket.get('created_at', 'N/A')[:10]
    recording_id_full = str(ticket.get('recording_id', 'N/A'))
    recording_id_short = recording_id_full[:10]
    
    # Generar ID único para el botón
    button_id = f"edit_btn_{ticket.get('id')}"
    
    # HTML de la tarjeta con botón integrado
    card_html = f'''
    <div class="ticket-card">
        <div class="ticket-header">
            <div class="ticket-header-left">
                <span class="ticket-number">#{ticket_num}</span>
            </div>
            <div class="status-badge {status_class}">{status_label}</div>
        </div>
        
        <div class="ticket-body">
            <div class="ticket-title">{title}</div>
            <div class="ticket-description">{desc}</div>
            
            <div class="ticket-meta">
                <div class="meta-item">
                    <span class="meta-label">Estado</span>
                    <span class="meta-value">{status_label.title()}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Prioridad</span>
                    <span class="meta-value">{priority_label.title()}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Creado</span>
                    <span class="meta-value">{created_date}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Grabación</span>
                    <span class="meta-value" title="{recording_id_full}">{recording_id_short}...</span>
                </div>
            </div>
        </div>
        
        <div class="ticket-footer">
            <div>
                <span class="notes-label">Notas:</span>
                <span class="notes-text">{notes if notes else '<em>Sin notas</em>'}</span>
            </div>
            <button class="edit-button" onclick="document.querySelector('#{button_id}').click()">✏️ Editar</button>
        </div>
    </div>
    '''
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Botón invisible de Streamlit que se activa con el botón HTML
    if st.button("Editar", key=button_id, on_click=edit_callback, args=(ticket,), type="secondary"):
        pass

# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================

# Título principal
st.title("🎫 Dashboard de Tickets")
st.markdown("##### Gestión de oportunidades de negocio")
st.markdown("")

# ============================================================================
# BARRA LATERAL - FILTROS Y ESTADÍSTICAS
# ============================================================================

with st.sidebar:
    st.markdown("## Filtros")
    st.markdown("")
    
    # Obtener tickets para estadísticas
    all_tickets = fetch_tickets()
    
    # Definir opciones
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
    
    # Selectores
    status_display = st.selectbox(
        "Estado",
        [status_display_map[s] for s in status_options],
        key="sidebar_status_filter"
    )
    
    priority_display = st.selectbox(
        "Prioridad",
        [priority_display_map[p] for p in priority_options],
        key="sidebar_priority_filter"
    )
    
    # Mapear de vuelta
    selected_status = [k for k, v in status_display_map.items() if v == status_display][0]
    selected_priority = [k for k, v in priority_display_map.items() if v == priority_display][0]
    
    # Botón actualizar
    if st.button("🔄 Actualizar", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.markdown("## Estadísticas")
    
    # Métricas
    if not all_tickets.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total", len(all_tickets))
        
        with col2:
            nuevos = len(all_tickets[all_tickets["status"] == "new"])
            st.metric("Nuevos", nuevos)
        
        with col3:
            ganados = len(all_tickets[all_tickets["status"] == "won"])
            st.metric("Ganados", ganados)
    else:
        st.info("No hay datos disponibles")

# ============================================================================
# CONTENIDO PRINCIPAL - LISTA DE TICKETS
# ============================================================================

# Obtener tickets con filtros
tickets = fetch_tickets(
    status_filter=selected_status if selected_status != "Todos" else None,
    priority_filter=selected_priority if selected_priority != "Todos" else None
)

if tickets.empty:
    st.markdown("""
    <div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 40px; text-align: center;">
        <h3 style="color: #CBD5E1; margin-bottom: 8px;">🎫 No hay tickets disponibles</h3>
        <p style="color: #94A3B8;">No se encontraron tickets con los filtros seleccionados</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Contador de resultados
    st.markdown(f"### Mostrando {len(tickets)} tickets")
    st.markdown("")
    
    # Renderizar tarjetas
    for idx, ticket in tickets.iterrows():
        render_ticket_card(ticket, edit_ticket_modal)

# ============================================================================
# PANEL DE DIAGNÓSTICO
# ============================================================================

st.markdown("---")

with st.expander("🔧 Diagnóstico del Sistema", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Estado de Conexión")
        success, message, count = test_connection()
        
        if success:
            st.success(f"✅ {message}")
            st.caption(f"Registros disponibles: {count}")
        else:
            st.error(f"❌ {message}")
    
    with col2:
        st.markdown("##### Configuración")
        st.caption(f"**URL:** `{SUPABASE_URL[:25]}...`")
        st.caption(f"**API Key:** `{SUPABASE_KEY[:15]}...`")
        st.caption(f"**Gemini:** `{GEMINI_API_KEY[:15]}...`")