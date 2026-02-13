import streamlit as st
import pandas as pd
from datetime import datetime
import traceback
from typing import Optional, Dict, Any
from dataclasses import dataclass

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
st.set_page_config(
    page_title="Dashboard de Tickets",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SISTEMA DE DISEÑO MODERNO - ICONOS MINIMALISTAS
# ============================================================================
st.markdown("""
<style>
    /* ===== TOKENS ===== */
    :root {
        --bg-primary: #0A0C10;
        --bg-secondary: #111316;
        --bg-card: #16181C;
        --border: #2A2C30;
        --border-hover: #404448;
        --text-primary: #E8E9EA;
        --text-secondary: #8B8E94;
        --text-tertiary: #5E6269;
        --accent: #3B82F6;
        --accent-soft: rgba(59, 130, 246, 0.1);
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --radius-lg: 12px;
        --radius-md: 8px;
        --radius-sm: 6px;
        --shadow: 0 4px 20px rgba(0,0,0,0.5);
        --transition: all 0.2s ease;
    }

    [data-testid="stAppViewContainer"] { 
        background: var(--bg-primary); 
    }
    
    [data-testid="stSidebar"] { 
        background: var(--bg-secondary); 
        border-right: 1px solid var(--border); 
    }

    /* ===== GRID DE TARJETAS ===== */
    div.row-widget.stHorizontal {
        gap: 0.75rem;
        flex-wrap: wrap;
    }

    /* ===== TARJETA MODERNA ===== */
    .ticket-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1rem;
        transition: var(--transition);
        height: 100%;
        display: flex;
        flex-direction: column;
        margin-bottom: 0.25rem;
    }
    
    .ticket-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow);
        transform: translateY(-1px);
    }

    /* Header con número y badge */
    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .ticket-number {
        font-family: 'SF Mono', 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        color: var(--text-tertiary);
        letter-spacing: 0.02em;
    }

    /* Badges minimalistas - SIN EMOJIS */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.65rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        border: 1px solid transparent;
        white-space: nowrap;
    }
    
    .badge-new { 
        background: rgba(239,68,68,0.08); 
        color: #F87171; 
        border-color: rgba(239,68,68,0.2); 
    }
    
    .badge-progress { 
        background: rgba(245,158,11,0.08); 
        color: #FBBF24; 
        border-color: rgba(245,158,11,0.2); 
    }
    
    .badge-won { 
        background: rgba(16,185,129,0.08); 
        color: #34D399; 
        border-color: rgba(16,185,129,0.2); 
    }
    
    .badge-closed { 
        background: rgba(107,114,128,0.08); 
        color: #9CA3AF; 
        border-color: rgba(107,114,128,0.2); 
    }

    /* Título compacto */
    .ticket-title {
        font-size: 0.85rem;
        font-weight: 450;
        color: var(--text-primary);
        line-height: 1.4;
        margin: 0.25rem 0 0.5rem 0;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 2.2rem;
    }

    /* Botón de editar - diseño limpio */
    .stButton > button {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        font-size: 0.7rem !important;
        font-weight: 400 !important;
        padding: 0.2rem 0.5rem !important;
        width: 100% !important;
        transition: var(--transition) !important;
        letter-spacing: 0.02em !important;
    }
    
    .stButton > button:hover {
        background: var(--bg-secondary) !important;
        border-color: var(--text-tertiary) !important;
        color: var(--text-primary) !important;
    }

    /* Métricas - diseño limpio */
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 0.75rem;
    }
    
    [data-testid="metric-container"] label {
        color: var(--text-tertiary) !important;
        font-size: 0.65rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-primary) !important;
        font-size: 1.1rem !important;
        font-weight: 450 !important;
    }

    /* Modal styling - minimalista */
    div[data-testid="stDialog"] > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.5rem !important;
    }
    
    div[data-testid="stDialog"] h1, 
    div[data-testid="stDialog"] h2, 
    div[data-testid="stDialog"] h3 {
        color: var(--text-primary) !important;
        font-weight: 450 !important;
    }

    /* Info box */
    .info-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 0.75rem;
        color: var(--text-secondary);
        font-size: 0.8rem;
        line-height: 1.5;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1rem 0;
    }

    /* Select boxes */
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 4px;
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 450;
        letter-spacing: -0.01em;
    }

    h1 {
        font-size: 1.5rem;
    }

    h3 {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CREDENCIALES Y FUNCIONES SUPABASE
# ============================================================================
SUPABASE_URL = "https://euqtlsheickstdtcfhfi.supabase.co"
SUPABASE_KEY = "sb_publishable_cVoObJObqnsKxRIXgcft4g_ejb6VJnC"
GEMINI_API_KEY = "AIzaSyBBD6CoJl2n2--7DWRTrdLxZMYcr_Mzk0I"

def get_supabase_connection():
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        return None

def test_connection():
    try:
        client = get_supabase_connection()
        if not client:
            return False, "No se pudo inicializar", None
        response = client.table("opportunities").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        return True, "Conexión exitosa", count
    except Exception as e:
        return False, f"Error de conexión", None

def fetch_tickets(status_filter=None, priority_filter=None):
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
    except:
        return pd.DataFrame()

def update_ticket(ticket_id: int, status: str, notes: str, priority: str = None) -> bool:
    try:
        client = get_supabase_connection()
        if not client:
            return False
        
        data = {"status": status, "notes": notes}
        if priority:
            data["priority"] = priority
            
        client.table("opportunities").update(data).eq("id", ticket_id).execute()
        return True
    except:
        return False

# ============================================================================
# MODAL DE EDICIÓN - MODERNO Y LIMPIO
# ============================================================================
@st.dialog("Editar ticket", width="large")
def edit_ticket_modal(ticket_dict: Dict[str, Any]):
    """Modal para editar ticket con diseño minimalista"""
    
    ticket_id = ticket_dict.get("id")
    ticket_num = ticket_dict.get("ticket_number", "N/A")
    title = ticket_dict.get("title", "Sin título")
    description = ticket_dict.get("description", "").strip()
    status = ticket_dict.get("status", "new").lower()
    priority = ticket_dict.get("priority", "Medium")
    notes = ticket_dict.get("notes", "") or ""
    created_at = ticket_dict.get("created_at", "")[:10] if ticket_dict.get("created_at") else "N/A"
    recording_id = ticket_dict.get("recording_id", "N/A")
    
    # Header minimalista
    st.markdown(f"### #{ticket_num}")
    st.markdown(f"**{title}**")
    
    # Info en grid limpio
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<span style='color: var(--text-tertiary); font-size: 0.7rem;'>CREADO</span><br><span style='color: var(--text-primary);'>{created_at}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: var(--text-tertiary); font-size: 0.7rem;'>GRABACIÓN</span><br><span style='color: var(--text-primary); font-family: monospace;'>{recording_id[:12]}...</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<span style='color: var(--text-tertiary); font-size: 0.7rem;'>ESTADO</span><br><span style='color: var(--text-primary);'>{status}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: var(--text-tertiary); font-size: 0.7rem;'>PRIORIDAD</span><br><span style='color: var(--text-primary);'>{priority}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Descripción
    st.markdown("#### Descripción")
    st.markdown(f"<div class='info-box'>{description if description else 'Sin descripción'}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Formulario de edición
    with st.form(key=f"edit_form_{ticket_id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            status_options = ["Nuevo", "En progreso", "Cerrado", "Ganado"]
            status_idx = ["new", "in_progress", "closed", "won"].index(status) if status in ["new", "in_progress", "closed", "won"] else 0
            new_status = st.selectbox("Estado", status_options, index=status_idx)
            status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
        
        with col2:
            priority_options = ["Baja", "Media", "Alta"]
            priority_idx = ["Low", "Medium", "High"].index(priority) if priority in ["Low", "Medium", "High"] else 1
            new_priority = st.selectbox("Prioridad", priority_options, index=priority_idx)
            priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
        
        new_notes = st.text_area(
            "Notas",
            value=notes,
            height=100,
            placeholder="Agregar notas..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            saved = st.form_submit_button("Guardar cambios", use_container_width=True)
        with col3:
            cancelled = st.form_submit_button("Cancelar", use_container_width=True)
        
        if saved:
            if update_ticket(ticket_id, status_map[new_status], new_notes, priority_map[new_priority]):
                st.success("Actualizado")
                st.rerun()
        
        if cancelled:
            st.rerun()

# ============================================================================
# GRID DE TARJETAS - SIN EMOJIS, SOLO TEXTO
# ============================================================================
@st.fragment
def render_ticket_grid(tickets_df: pd.DataFrame):
    """Grid de tickets con diseño minimalista"""
    
    if tickets_df.empty:
        st.info("No hay tickets disponibles")
        return
    
    num_columns = 3
    columns = st.columns(num_columns, gap="small")
    
    for idx, (_, ticket) in enumerate(tickets_df.iterrows()):
        with columns[idx % num_columns]:
            ticket_dict = ticket.to_dict()
            
            ticket_num = ticket_dict.get("ticket_number", "N/A")
            title = ticket_dict.get("title", "Sin título")[:60]
            status = ticket_dict.get("status", "new").lower()
            
            # Badge sin emojis
            badge_map = {
                "new": {"class": "badge-new", "label": "NUEVO"},
                "in_progress": {"class": "badge-progress", "label": "PROGRESO"},
                "won": {"class": "badge-won", "label": "GANADO"},
                "closed": {"class": "badge-closed", "label": "CERRADO"}
            }
            badge = badge_map.get(status, badge_map["new"])
            
            # Tarjeta limpia
            card_html = f"""
            <div class="ticket-card">
                <div class="ticket-header">
                    <span class="ticket-number">#{ticket_num}</span>
                    <span class="badge {badge['class']}">{badge['label']}</span>
                </div>
                <div class="ticket-title">{title}</div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Botón de editar
            if st.button("EDITAR", key=f"edit_{ticket_dict.get('id')}", use_container_width=True):
                st.session_state.edit_ticket = ticket_dict
                st.rerun()

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================
st.title("Dashboard de Tickets")
st.markdown("<h3>Gestión de oportunidades</h3>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## Filtros")
    
    all_tickets = fetch_tickets()
    
    status_filter = st.selectbox(
        "Estado",
        ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
        key="status_filter"
    )
    
    priority_filter = st.selectbox(
        "Prioridad",
        ["Todos", "Baja", "Media", "Alta"],
        key="priority_filter"
    )
    
    status_map = {
        "Todos": "Todos", "Nuevo": "new", "En progreso": "in_progress", 
        "Cerrado": "closed", "Ganado": "won"
    }
    priority_map = {
        "Todos": "Todos", "Baja": "Low", "Media": "Medium", "Alta": "High"
    }
    
    selected_status = status_map[status_filter]
    selected_priority = priority_map[priority_filter]
    
    if st.button("ACTUALIZAR", use_container_width=True):
        st.rerun()
    
    st.divider()
    
    # Estadísticas
    st.markdown("## Estadísticas")
    if not all_tickets.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", len(all_tickets))
        with col2:
            st.metric("Nuevos", len(all_tickets[all_tickets["status"] == "new"]))
        with col3:
            st.metric("Ganados", len(all_tickets[all_tickets["status"] == "won"]))
    else:
        st.info("Sin datos")

# --- GRID DE TICKETS ---
tickets = fetch_tickets(
    status_filter=selected_status if selected_status != "Todos" else None,
    priority_filter=selected_priority if selected_priority != "Todos" else None
)

if tickets.empty:
    st.info("No hay tickets con los filtros seleccionados.")
else:
    st.markdown(f"#### {len(tickets)} tickets encontrados")
    render_ticket_grid(tickets)

# --- MODAL ---
if "edit_ticket" in st.session_state and st.session_state.edit_ticket:
    edit_ticket_modal(st.session_state.edit_ticket)
    st.session_state.edit_ticket = None

# ============================================================================
# DIAGNÓSTICO
# ============================================================================
with st.expander("Diagnóstico del sistema", expanded=False):
    success, msg, count = test_connection()
    
    if success:
        st.success(f"{msg} — {count} registros")
    else:
        st.error(msg)
    
    st.caption(f"URL: {SUPABASE_URL[:20]}...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ver opportunities"):
            client = get_supabase_connection()
            if client:
                data = client.table("opportunities").select("*").limit(3).execute().data
                if data:
                    st.dataframe(pd.DataFrame(data))
    with col2:
        if st.button("Ver recordings"):
            client = get_supabase_connection()
            if client:
                data = client.table("recordings").select("*").limit(3).execute().data
                if data:
                    st.dataframe(pd.DataFrame(data))