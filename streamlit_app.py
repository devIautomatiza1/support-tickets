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
# SISTEMA DE DISEÑO MODERNO (CSS optimizado para tarjetas compactas)
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

    /* ===== TARJETA COMPACTA ===== */
    .ticket-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 0.85rem;
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

    /* Badge compacto */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        border: 1px solid transparent;
        white-space: nowrap;
    }
    
    .badge-new { 
        background: rgba(239,68,68,0.1); 
        color: #FCA5A5; 
        border-color: rgba(239,68,68,0.3); 
    }
    
    .badge-progress { 
        background: rgba(245,158,11,0.1); 
        color: #FCD34D; 
        border-color: rgba(245,158,11,0.3); 
    }
    
    .badge-won { 
        background: rgba(16,185,129,0.1); 
        color: #6EE7B7; 
        border-color: rgba(16,185,129,0.3); 
    }
    
    .badge-closed { 
        background: rgba(107,114,128,0.1); 
        color: #D1D5DB; 
        border-color: rgba(107,114,128,0.3); 
    }

    /* Número de ticket */
    .ticket-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-tertiary);
    }

    /* Título compacto */
    .ticket-title-compact {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-primary);
        line-height: 1.3;
        margin: 0.25rem 0 0.5rem 0;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 2.2rem;
    }

    /* Botón de editar dentro de la tarjeta */
    .edit-button-container {
        margin-top: 0.25rem;
        width: 100%;
    }
    
    .stButton > button {
        background: var(--accent-soft) !important;
        color: var(--accent) !important;
        border: 1px solid rgba(59,130,246,0.3) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        padding: 0.25rem 0.5rem !important;
        width: 100% !important;
        transition: var(--transition) !important;
    }
    
    .stButton > button:hover {
        background: rgba(59,130,246,0.2) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    /* Métricas */
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 0.75rem;
    }
    
    [data-testid="metric-container"] label {
        color: var(--text-tertiary) !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-primary) !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }

    /* Modal styling */
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
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1rem 0;
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
            return False, "❌ No se pudo inicializar", None
        response = client.table("opportunities").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        return True, "✅ Conexión exitosa", count
    except Exception as e:
        return False, f"❌ Error: {str(e)}", None

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
# MODAL DE EDICIÓN
# ============================================================================
@st.dialog("✏️ Editar Ticket", width="large")
def edit_ticket_modal(ticket_dict: Dict[str, Any]):
    """Modal para editar ticket con todos los datos"""
    
    # Extraer datos
    ticket_id = ticket_dict.get("id")
    ticket_num = ticket_dict.get("ticket_number", "N/A")
    title = ticket_dict.get("title", "Sin título")
    description = ticket_dict.get("description", "").strip()
    status = ticket_dict.get("status", "new").lower()
    priority = ticket_dict.get("priority", "Medium")
    notes = ticket_dict.get("notes", "") or ""
    created_at = ticket_dict.get("created_at", "")[:10] if ticket_dict.get("created_at") else "N/A"
    recording_id = ticket_dict.get("recording_id", "N/A")
    
    # Encabezado del modal
    st.markdown(f"### #{ticket_num} - {title}")
    
    # Información no editable en dos columnas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📅 Creado:** {created_at}")
        st.markdown(f"**🎙️ Grabación:** `{recording_id[:12]}...`" if recording_id != "N/A" else "**🎙️ Grabación:** N/A")
    with col2:
        st.markdown(f"**📌 Estado actual:** {status}")
        st.markdown(f"**⚡ Prioridad actual:** {priority}")
    
    st.markdown("---")
    
    # Descripción completa
    st.markdown("#### 📝 Descripción")
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px; color: var(--text-secondary);">
        {description if description else '<em>Sin descripción</em>'}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Formulario de edición
    with st.form(key=f"modal_edit_form_{ticket_id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            status_options = ["Nuevo", "En progreso", "Cerrado", "Ganado"]
            status_idx = ["new", "in_progress", "closed", "won"].index(status) if status in ["new", "in_progress", "closed", "won"] else 0
            new_status_display = st.selectbox("Estado", status_options, index=status_idx)
            status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
            new_status = status_map[new_status_display]
        
        with col2:
            priority_options = ["Baja", "Media", "Alta"]
            priority_idx = ["Low", "Medium", "High"].index(priority) if priority in ["Low", "Medium", "High"] else 1
            new_priority_display = st.selectbox("Prioridad", priority_options, index=priority_idx)
            priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
            new_priority = priority_map[new_priority_display]
        
        new_notes = st.text_area(
            "📋 Notas",
            value=notes,
            height=120,
            placeholder="Agregar notas o actualizaciones..."
        )
        
        # Botones
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("💾 Guardar Cambios", use_container_width=True, type="primary")
        with col3:
            cancel = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        if submitted:
            if update_ticket(ticket_id, new_status, new_notes, new_priority):
                st.success("✅ Ticket actualizado correctamente")
                st.rerun()
            else:
                st.error("❌ Error al actualizar el ticket")
        
        if cancel:
            st.rerun()

# ============================================================================
# FUNCIÓN COMPACTA CON FRAGMENT - Grid de 3 columnas
# ============================================================================
@st.fragment
def render_ticket_grid(tickets_df: pd.DataFrame):
    """
    Renderiza tickets en grid de 3 columnas con tarjetas ultra-compactas.
    Cada tarjeta tiene badge de estado + título y un botón para abrir modal.
    """
    if tickets_df.empty:
        st.info("🎫 No hay tickets disponibles")
        return
    
    num_columns = 3
    columns = st.columns(num_columns, gap="small")
    
    for idx, (_, ticket) in enumerate(tickets_df.iterrows()):
        with columns[idx % num_columns]:
            ticket_dict = ticket.to_dict()
            
            # Extraer datos mínimos
            ticket_id = ticket_dict.get("id")
            ticket_num = ticket_dict.get("ticket_number", "N/A")
            title = ticket_dict.get("title", "Sin título")[:60]
            status = ticket_dict.get("status", "new").lower()
            
            # Configuración de badge
            badge_config = {
                "new": {"class": "badge-new", "icon": "🆕", "label": "NUEVO"},
                "in_progress": {"class": "badge-progress", "icon": "⚡", "label": "PROGRESO"},
                "won": {"class": "badge-won", "icon": "🎯", "label": "GANADO"},
                "closed": {"class": "badge-closed", "icon": "✅", "label": "CERRADO"}
            }
            config = badge_config.get(status, badge_config["new"])
            
            # Tarjeta compacta
            card_html = f"""
            <div class="ticket-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="ticket-number">#{ticket_num}</span>
                    <span class="badge {config['class']}">
                        {config['icon']} {config['label']}
                    </span>
                </div>
                <div class="ticket-title-compact">{title}</div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Botón de editar dentro de la tarjeta (NO expander)
            if st.button("✏️ Editar", key=f"edit_btn_{ticket_id}", use_container_width=True):
                st.session_state.ticket_to_edit = ticket_dict
                st.rerun()

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================
st.title("🎫 Dashboard de Tickets")
st.markdown("##### Gestión de oportunidades")
st.divider()

# --- SIDEBAR: FILTROS Y ESTADÍSTICAS ---
with st.sidebar:
    st.markdown("## Filtros")
    
    # Obtener tickets para estadísticas
    all_tickets = fetch_tickets()
    
    # Filtros de estado
    status_filter = st.selectbox(
        "Estado",
        ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
        key="sidebar_status"
    )
    
    # Filtros de prioridad
    priority_filter = st.selectbox(
        "Prioridad",
        ["Todos", "Baja", "Media", "Alta"],
        key="sidebar_priority"
    )
    
    # Mapeo a valores internos
    status_map_filter = {
        "Todos": "Todos",
        "Nuevo": "new",
        "En progreso": "in_progress",
        "Cerrado": "closed",
        "Ganado": "won"
    }
    priority_map_filter = {
        "Todos": "Todos",
        "Baja": "Low",
        "Media": "Medium",
        "Alta": "High"
    }
    
    selected_status = status_map_filter[status_filter]
    selected_priority = priority_map_filter[priority_filter]
    
    # Botón actualizar
    if st.button("🔄 Actualizar", use_container_width=True):
        st.rerun()
    
    st.divider()
    
    # Estadísticas
    st.markdown("## Estadísticas")
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

# --- CONTENIDO PRINCIPAL: GRID DE TARJETAS COMPACTAS ---
tickets = fetch_tickets(
    status_filter=selected_status if selected_status != "Todos" else None,
    priority_filter=selected_priority if selected_priority != "Todos" else None
)

if tickets.empty:
    st.info("🎫 No hay tickets con los filtros seleccionados.")
else:
    st.markdown(f"### 🎟️ {len(tickets)} tickets encontrados")
    render_ticket_grid(tickets)

# --- MODAL DE EDICIÓN (se activa cuando hay un ticket seleccionado) ---
if "ticket_to_edit" in st.session_state and st.session_state.ticket_to_edit is not None:
    edit_ticket_modal(st.session_state.ticket_to_edit)
    st.session_state.ticket_to_edit = None

# ============================================================================
# PANEL DE DIAGNÓSTICO
# ============================================================================
with st.expander("🔧 Diagnóstico del sistema", expanded=False):
    success, msg, count = test_connection()
    
    if success:
        st.success(f"✅ {msg} — {count} registros en opportunities")
    else:
        st.error(f"❌ {msg}")
    
    st.caption(f"**URL:** `{SUPABASE_URL[:25]}...`")
    st.caption(f"**API Key:** `{SUPABASE_KEY[:15]}...`")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Ver muestra de opportunities", use_container_width=True):
            client = get_supabase_connection()
            if client:
                data = client.table("opportunities").select("*").limit(3).execute().data
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True)
                else:
                    st.warning("No hay datos")
    
    with col2:
        if st.button("🎙️ Ver muestra de recordings", use_container_width=True):
            client = get_supabase_connection()
            if client:
                data = client.table("recordings").select("*").limit(3).execute().data
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True)
                else:
                    st.warning("No hay datos")