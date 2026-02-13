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
# SISTEMA DE DISEÑO MODERNO - VERSIÓN PROFESIONAL
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
        --shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
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

    /* ===== TARJETA COMPACTA ===== */
    .ticket-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1rem;
        transition: var(--transition);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .ticket-card:hover {
        border-color: var(--border-hover);
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        transform: translateY(-1px);
    }

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

    /* Badges minimalistas */
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

    .ticket-title {
        font-size: 0.85rem;
        font-weight: 450;
        color: var(--text-primary);
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 2.2rem;
    }

    /* ===== MODAL CENTRADO PROFESIONAL ===== */
    div[data-testid="stDialog"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div[data-testid="stDialog"] > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: var(--shadow) !important;
        max-width: 700px !important;
        width: 100% !important;
        margin: 0 auto !important;
        position: relative !important;
    }
    
    /* Ocultar título por defecto */
    div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2 {
        display: none !important;
    }

    /* Header del modal */
    .modal-header {
        margin-bottom: 1.5rem;
        text-align: left;
    }
    
    .modal-title {
        font-size: 1.35rem;
        font-weight: 450;
        color: var(--text-primary);
        line-height: 1.4;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.01em;
    }
    
    .modal-divider {
        height: 2px;
        width: 50px;
        background: var(--accent);
        opacity: 0.5;
        margin: 0.75rem 0 0 0;
    }

    /* Grid de 2 columnas para info */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 1.25rem;
    }
    
    .info-item {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .info-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-tertiary);
        font-weight: 600;
    }
    
    .info-value {
        font-size: 0.9rem;
        color: var(--text-primary);
        font-weight: 400;
    }
    
    .info-value-mono {
        font-family: 'SF Mono', 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    /* Descripción */
    .description-section {
        margin: 1.5rem 0;
    }
    
    .section-title {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-tertiary);
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .description-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.25rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    /* Formulario */
    .form-card {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    /* Select boxes */
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--border-hover) !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.1) !important;
    }

    /* Botones */
    .stButton > button {
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        padding: 0.5rem 1rem !important;
        transition: var(--transition) !important;
        font-weight: 500 !important;
    }
    
    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #2563EB !important;
        transform: translateY(-1px);
    }
    
    .stButton > button:not([kind="primary"]) {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border) !important;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        background: var(--bg-card) !important;
        border-color: var(--border-hover) !important;
        color: var(--text-primary) !important;
    }

    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.5rem 0;
        opacity: 0.7;
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
# MODAL DE EDICIÓN - SIN DUPLICIDAD, CENTRADO
# ============================================================================
@st.dialog("", width="large")
def edit_ticket_modal(ticket_dict: Dict[str, Any]):
    """Modal profesional sin información duplicada"""
    
    # Extraer datos
    ticket_id = ticket_dict.get("id")
    ticket_num = ticket_dict.get("ticket_number", "N/A")
    title = ticket_dict.get("title", "Sin título")
    description = ticket_dict.get("description", "").strip()
    current_status = ticket_dict.get("status", "new").lower()
    current_priority = ticket_dict.get("priority", "Medium")
    notes = ticket_dict.get("notes", "") or ""
    created_at = ticket_dict.get("created_at", "")[:10] if ticket_dict.get("created_at") else "N/A"
    recording_id = ticket_dict.get("recording_id", "N/A")
    
    # === HEADER - SOLO TÍTULO ===
    st.markdown(f"""
    <div class="modal-header">
        <div class="modal-title">{title}</div>
        <div class="modal-divider"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # === INFO GRID - SIN DUPLICAR ESTADO/PRIORIDAD ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 10px; height: 100%;">
            <div style="margin-bottom: 1rem;">
                <span style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-tertiary); font-weight: 600;">📅 CREADO</span><br>
                <span style="font-size: 0.95rem; color: var(--text-primary); font-weight: 400;">{created_at}</span>
            </div>
            <div>
                <span style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-tertiary); font-weight: 600;">🎙️ GRABACIÓN</span><br>
                <span style="font-size: 0.8rem; color: var(--text-secondary); font-family: monospace;">{recording_id[:12]}...{recording_id[-6:] if len(recording_id) > 12 else ''}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Badge de estado
        status_colors = {
            "new": {"bg": "rgba(239,68,68,0.08)", "color": "#F87171", "label": "NUEVO"},
            "in_progress": {"bg": "rgba(245,158,11,0.08)", "color": "#FBBF24", "label": "EN PROGRESO"},
            "won": {"bg": "rgba(16,185,129,0.08)", "color": "#34D399", "label": "GANADO"},
            "closed": {"bg": "rgba(107,114,128,0.08)", "color": "#9CA3AF", "label": "CERRADO"}
        }
        status_style = status_colors.get(current_status, status_colors["new"])
        
        # Badge de prioridad
        priority_colors = {
            "Low": {"bg": "rgba(16,185,129,0.08)", "color": "#34D399", "label": "BAJA"},
            "Medium": {"bg": "rgba(245,158,11,0.08)", "color": "#FBBF24", "label": "MEDIA"},
            "High": {"bg": "rgba(239,68,68,0.08)", "color": "#F87171", "label": "ALTA"}
        }
        priority_style = priority_colors.get(current_priority, priority_colors["Medium"])
        
        st.markdown(f"""
        <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 10px; height: 100%;">
            <div style="margin-bottom: 1rem;">
                <span style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-tertiary); font-weight: 600;">📌 ESTADO</span><br>
                <span style="display: inline-block; padding: 0.25rem 0.75rem; margin-top: 0.25rem; background: {status_style['bg']}; border: 1px solid rgba(239,68,68,0.2); border-radius: 20px; font-size: 0.7rem; color: {status_style['color']}; text-transform: uppercase; font-weight: 500;">
                    {status_style['label']}
                </span>
            </div>
            <div>
                <span style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-tertiary); font-weight: 600;">⚡ PRIORIDAD</span><br>
                <span style="display: inline-block; padding: 0.25rem 0.75rem; margin-top: 0.25rem; background: {priority_style['bg']}; border: 1px solid rgba(16,185,129,0.2); border-radius: 20px; font-size: 0.7rem; color: {priority_style['color']}; font-weight: 500;">
                    {priority_style['label']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # === DESCRIPCIÓN ===
    st.markdown("""
    <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-tertiary); font-weight: 600; margin-bottom: 0.75rem;">
        📝 DESCRIPCIÓN
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6; margin-bottom: 1.5rem;">
        {description if description else 'Sin descripción'}
    </div>
    """, unsafe_allow_html=True)
    
    # === FORMULARIO DE EDICIÓN (ÚNICO LUGAR PARA EDITAR) ===
    st.markdown("""
    <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-tertiary); font-weight: 600; margin-bottom: 1rem;">
        ✏️ EDITAR TICKET
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(key=f"edit_modal_form_{ticket_id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            status_options = ["Nuevo", "En progreso", "Cerrado", "Ganado"]
            status_idx = ["new", "in_progress", "closed", "won"].index(current_status) if current_status in ["new", "in_progress", "closed", "won"] else 0
            new_status = st.selectbox("Cambiar estado", status_options, index=status_idx)
            status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
        
        with col2:
            priority_options = ["Baja", "Media", "Alta"]
            priority_idx = ["Low", "Medium", "High"].index(current_priority) if current_priority in ["Low", "Medium", "High"] else 1
            new_priority = st.selectbox("Cambiar prioridad", priority_options, index=priority_idx)
            priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
        
        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        
        new_notes = st.text_area(
            "Notas",
            value=notes,
            height=150,
            placeholder="Agregar notas, enlaces o actualizaciones..."
        )
        
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            saved = st.form_submit_button(
                "Guardar cambios", 
                use_container_width=True,
                type="primary"
            )
        
        with col3:
            cancelled = st.form_submit_button(
                "Cancelar", 
                use_container_width=True
            )
        
        if saved:
            if update_ticket(
                ticket_id, 
                status_map[new_status], 
                new_notes, 
                priority_map[new_priority]
            ):
                st.success("✓ Ticket actualizado correctamente")
                st.rerun()
            else:
                st.error("Error al actualizar el ticket")
        
        if cancelled:
            st.rerun()

# ============================================================================
# GRID DE TARJETAS
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
            
            badge_map = {
                "new": {"class": "badge-new", "label": "NUEVO"},
                "in_progress": {"class": "badge-progress", "label": "PROGRESO"},
                "won": {"class": "badge-won", "label": "GANADO"},
                "closed": {"class": "badge-closed", "label": "CERRADO"}
            }
            badge = badge_map.get(status, badge_map["new"])
            
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
            
            if st.button("EDITAR", key=f"edit_{ticket_dict.get('id')}", use_container_width=True):
                st.session_state.edit_ticket = ticket_dict
                st.rerun()

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================
st.title("Dashboard de Tickets")
st.markdown("<h3 style='color: var(--text-secondary); font-weight: 400; margin-top: -0.5rem;'>Gestión de oportunidades</h3>", unsafe_allow_html=True)
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