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
        --radius-lg: 20px;
        --radius-md: 14px;
        --radius-sm: 10px;
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
        transform: translateY(-2px);
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
        border-radius: 6px;
        font-size: 0.65rem;
        font-weight: 600;
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

    /* ===== MODAL CENTRADO - CON MÁS MARGEN ===== */
    div[data-testid="stDialog"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 2rem 0 !important;  /* ← MÁS MARGEN SUPERIOR/INFERIOR */
    }
    
    div[data-testid="stDialog"] > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 28px !important;  /* ← MÁS REDONDEADO */
        padding: 2.5rem 2.5rem !important;  /* ← MÁS PADDING INTERNO */
        box-shadow: var(--shadow) !important;
        max-width: 750px !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    
    /* Ocultar título por defecto */
    div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2 {
        display: none !important;
    }

    /* Header del modal - SIN LÍNEA AZUL */
    .modal-header {
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        flex-wrap: wrap;
        border-bottom: 1px solid var(--border);  /* ← LÍNEA SUTIL GRIS */
        padding-bottom: 1.25rem;
    }
    
    .modal-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.4;
        letter-spacing: -0.02em;
    }
    
    .modal-date {
        font-size: 0.85rem;
        color: var(--text-tertiary);
        font-family: 'SF Mono', 'JetBrains Mono', monospace;
        background: var(--bg-secondary);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        border: 1px solid var(--border);
    }

    /* Descripción */
    .description-section {
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }
    
    .description-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* Estado y Prioridad */
    .status-priority-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .info-card {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid var(--border);
    }
    
    .info-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .current-value {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .select-label {
        font-size: 0.7rem;
        color: var(--text-tertiary);
        margin-bottom: 0.25rem;
    }

    /* Select boxes */
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--border-hover) !important;
    }
    
    /* Text area - GRANDE */
    .stTextArea {
        margin-top: 0.5rem;
    }
    
    .stTextArea textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
        padding: 1.25rem !important;
        min-height: 250px !important;
        font-family: 'SF Mono', 'JetBrains Mono', monospace !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
    }

    /* Botones */
    .stButton > button {
        border-radius: 12px !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.5rem !important;
        transition: var(--transition) !important;
        font-weight: 600 !important;
    }
    
    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #2563EB !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59,130,246,0.3) !important;
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
        height: 1px;
        background: var(--border);
        margin: 1.5rem 0;
    }
    
    /* Métricas */
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CREDENCIALES Y FUNCIONES SUPABASE - USANDO SECRETS
# ============================================================================

def get_supabase_connection():
    try:
        from supabase import create_client
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
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
# MODAL DE EDICIÓN - CON MÁS MARGEN Y SIN LÍNEAS AZULES
# ============================================================================
@st.dialog("Editar ticket", width="large")
def edit_ticket_modal(ticket_dict: Dict[str, Any]):
    """Modal profesional - CON MÁS ESPACIO Y SIN LÍNEAS AZULES"""
    
    # Extraer datos
    ticket_id = ticket_dict.get("id")
    title = ticket_dict.get("title", "Sin título")
    description = ticket_dict.get("description", "").strip()
    current_status = ticket_dict.get("status", "new").lower()
    current_priority = ticket_dict.get("priority", "Medium")
    notes = ticket_dict.get("notes", "") or ""
    created_at = ticket_dict.get("created_at", "")[:10] if ticket_dict.get("created_at") else "N/A"
    
    # === HEADER CON BORDE GRIS (SIN AZUL) ===
    st.markdown(f"""
    <div class="modal-header">
        <div>
            <span class="modal-title">{title}</span>
        </div>
        <span class="modal-date">{created_at}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # === DESCRIPCIÓN ===
    st.markdown("""
    <div class="section-title">DESCRIPCIÓN</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="description-box">
        {description if description else 'Sin descripción'}
    </div>
    """, unsafe_allow_html=True)
    
    # === ESTADO Y PRIORIDAD ===
    st.markdown("""
    <div style="margin-top: 2rem; margin-bottom: 1rem;">
        <span class="section-title">ESTADO Y PRIORIDAD</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Estado actual
        status_colors = {
            "new": {"bg": "rgba(239,68,68,0.1)", "color": "#F87171", "label": "Nuevo"},
            "in_progress": {"bg": "rgba(245,158,11,0.1)", "color": "#FBBF24", "label": "En progreso"},
            "closed": {"bg": "rgba(107,114,128,0.1)", "color": "#9CA3AF", "label": "Cerrado"},
            "won": {"bg": "rgba(16,185,129,0.1)", "color": "#34D399", "label": "Ganado"}
        }
        status_style = status_colors.get(current_status, status_colors["new"])
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">ESTADO ACTUAL</div>
            <span class="current-value" style="background: {status_style['bg']}; color: {status_style['color']};">
                {status_style['label']}
            </span>
            <div class="select-label">CAMBIAR A</div>
        </div>
        """, unsafe_allow_html=True)
        
        status_options = ["Nuevo", "En progreso", "Cerrado", "Ganado"]
        status_idx = ["new", "in_progress", "closed", "won"].index(current_status) if current_status in ["new", "in_progress", "closed", "won"] else 0
        new_status = st.selectbox("", status_options, index=status_idx, key=f"status_{ticket_id}", label_visibility="collapsed")
        status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
    
    with col2:
        # Prioridad actual
        priority_colors = {
            "Low": {"bg": "rgba(16,185,129,0.1)", "color": "#34D399", "label": "Baja"},
            "Medium": {"bg": "rgba(245,158,11,0.1)", "color": "#FBBF24", "label": "Media"},
            "High": {"bg": "rgba(239,68,68,0.1)", "color": "#F87171", "label": "Alta"}
        }
        priority_style = priority_colors.get(current_priority, priority_colors["Medium"])
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">PRIORIDAD ACTUAL</div>
            <span class="current-value" style="background: {priority_style['bg']}; color: {priority_style['color']};">
                {priority_style['label']}
            </span>
            <div class="select-label">CAMBIAR A</div>
        </div>
        """, unsafe_allow_html=True)
        
        priority_options = ["Baja", "Media", "Alta"]
        priority_idx = ["Low", "Medium", "High"].index(current_priority) if current_priority in ["Low", "Medium", "High"] else 1
        new_priority = st.selectbox("", priority_options, index=priority_idx, key=f"priority_{ticket_id}", label_visibility="collapsed")
        priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
    
    # === NOTAS Y COMENTARIOS ===
    st.markdown("""
    <div style="margin-top: 2rem; margin-bottom: 1rem;">
        <span class="section-title">NOTAS Y COMENTARIOS</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(key=f"edit_modal_form_{ticket_id}"):
        new_notes = st.text_area(
            "",
            value=notes,
            height=250,
            placeholder="""⭐️ Tema: Infraestructura
📌 Descripción: Recursos tecnológicos, herramientas, sistemas, equipos
👤 Mencionado por: Jaime
💬 Contexto: Estimamos que necesitamos unos $75,000...
📊 Confianza: 85%

Agrega aquí más notas, enlaces o actualizaciones...""",
            key=f"notes_{ticket_id}",
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        
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
    
    st.caption(f"URL: Configurada en secrets")
    
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