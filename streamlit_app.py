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
# SISTEMA DE DISEÑO MODERNO (CSS puro)
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
        --shadow: 0 4px 20px rgba(0,0,0,0.5);
        --transition: all 0.2s ease;
    }

    [data-testid="stAppViewContainer"] { background: var(--bg-primary); }
    [data-testid="stSidebar"] { background: var(--bg-secondary); border-right: 1px solid var(--border); }

    /* ===== GRID DE TARJETAS ===== */
    div.row-widget.stHorizontal {
        gap: 1rem;
        flex-wrap: wrap;
    }

    /* ===== TARJETA MODERNA ===== */
    .ticket-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        transition: var(--transition);
        height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
    }
    .ticket-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow);
        transform: translateY(-2px);
    }

    /* Cabecera con número y badge */
    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.75rem;
    }
    .ticket-number {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        color: var(--accent);
        background: var(--accent-soft);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        border: 1px solid transparent;
    }
    .badge-new { background: rgba(239,68,68,0.1); color: #FCA5A5; border-color: rgba(239,68,68,0.3); }
    .badge-progress { background: rgba(245,158,11,0.1); color: #FCD34D; border-color: rgba(245,158,11,0.3); }
    .badge-won { background: rgba(16,185,129,0.1); color: #6EE7B7; border-color: rgba(16,185,129,0.3); }
    .badge-closed { background: rgba(107,114,128,0.1); color: #D1D5DB; border-color: rgba(107,114,128,0.3); }

    /* Título */
    .ticket-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
        line-height: 1.4;
    }

    /* Descripción recortada */
    .ticket-description {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 1rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* Metadatos en grid 2x2 */
    .meta-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-bottom: 1rem;
        background: rgba(0,0,0,0.2);
        padding: 0.75rem;
        border-radius: var(--radius-md);
    }
    .meta-item {
        display: flex;
        flex-direction: column;
    }
    .meta-label {
        color: var(--text-tertiary);
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .meta-value {
        color: var(--text-primary);
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Notas (truncadas) */
    .ticket-notes {
        background: rgba(0,0,0,0.2);
        padding: 0.75rem;
        border-radius: var(--radius-md);
        margin-top: auto;
    }
    .notes-label {
        color: var(--text-tertiary);
        font-size: 0.7rem;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .notes-preview {
        color: var(--text-secondary);
        font-size: 0.8rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* Botón de acción principal */
    .detail-button {
        width: 100%;
        margin-top: 1rem;
        background: var(--accent-soft);
        color: var(--accent);
        border: 1px solid rgba(59,130,246,0.3);
        border-radius: var(--radius-md);
        padding: 0.5rem;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        transition: var(--transition);
        text-align: center;
    }
    .detail-button:hover {
        background: rgba(59,130,246,0.2);
        border-color: var(--accent);
    }

    /* ===== MODAL PERSONALIZADO (diálogo nativo) ===== */
    div[data-testid="stDialog"] > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 2rem !important;
    }

    /* ===== MÉTRICAS ===== */
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CREDENCIALES Y FUNCIONES SUPABASE (sin cambios, solo optimización)
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
# MODAL DE DETALLE COMPLETO Y EDICIÓN
# ============================================================================
@st.dialog("🎫 Detalle del Ticket", width="large")
def ticket_detail_modal(ticket: Dict[str, Any]):
    """Muestra toda la información del ticket y permite editar campos clave."""
    
    # Preparar datos
    ticket_id = ticket.get("id")
    ticket_num = ticket.get("ticket_number", "N/A")
    title = ticket.get("title", "Sin título")
    description = ticket.get("description", "").strip()
    status = ticket.get("status", "new")
    priority = ticket.get("priority", "Medium")
    notes = ticket.get("notes", "") or ""
    created_at = ticket.get("created_at", "")[:10] if ticket.get("created_at") else "N/A"
    recording_id = ticket.get("recording_id", "N/A")
    
    # --- SECCIÓN INFORMACIÓN (no editable) ---
    st.markdown(f"### #{ticket_num} - {title}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📅 Creado:** {created_at}")
        st.markdown(f"**🎙️ Grabación ID:** `{recording_id}`")
    with col2:
        st.markdown(f"**📌 Estado actual:** {status}")
        st.markdown(f"**⚡ Prioridad actual:** {priority}")
    
    st.markdown("---")
    
    # --- DESCRIPCIÓN COMPLETA ---
    st.markdown("#### 📝 Descripción")
    st.markdown(f"<div style='background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px; color: var(--text-secondary);'>{description or '_Sin descripción_'}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- SECCIÓN EDICIÓN ---
    st.markdown("#### ✏️ Editar Ticket")
    
    status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
    priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
    
    col1, col2 = st.columns(2)
    with col1:
        status_display = st.selectbox(
            "Estado",
            list(status_map.keys()),
            index=["new", "in_progress", "closed", "won"].index(status) if status in ["new", "in_progress", "closed", "won"] else 0,
            key=f"modal_status_{ticket_id}"
        )
        new_status = status_map[status_display]
    with col2:
        priority_display = st.selectbox(
            "Prioridad",
            list(priority_map.keys()),
            index=["Low", "Medium", "High"].index(priority) if priority in ["Low", "Medium", "High"] else 1,
            key=f"modal_priority_{ticket_id}"
        )
        new_priority = priority_map[priority_display]
    
    # Notas completas (con altura suficiente)
    new_notes = st.text_area(
        "📋 Notas",
        value=notes,
        height=150,
        key=f"modal_notes_{ticket_id}",
        placeholder="Agrega notas o actualizaciones..."
    )
    
    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Guardar Cambios", use_container_width=True, type="primary"):
            if update_ticket(ticket_id, new_status, new_notes, new_priority):
                st.success("✅ Ticket actualizado correctamente")
                st.rerun()
            else:
                st.error("❌ Error al actualizar")
    with col3:
        if st.button("❌ Cerrar", use_container_width=True):
            st.rerun()

# ============================================================================
# FUNCIÓN PARA RENDERIZAR UNA TARJETA EN UNA COLUMNA
# ============================================================================
def render_ticket_card(ticket: Dict[str, Any], column):
    """Dibuja una tarjeta dentro de una columna de Streamlit."""
    with column:
        # Extraer datos
        ticket_num = ticket.get("ticket_number", "N/A")
        title = ticket.get("title", "Sin título")
        description = ticket.get("description", "").strip()
        status = ticket.get("status", "new").lower()
        priority = ticket.get("priority", "Medium")
        notes = (ticket.get("notes", "") or "").strip()
        created_date = ticket.get("created_at", "")[:10] if ticket.get("created_at") else "N/A"
        recording_id = str(ticket.get("recording_id", "N/A"))[:8]
        
        # Configurar badge de estado
        badge_class = {
            "new": "badge-new",
            "in_progress": "badge-progress",
            "won": "badge-won",
            "closed": "badge-closed"
        }.get(status, "badge-new")
        status_label = {
            "new": "NUEVO",
            "in_progress": "PROGRESO",
            "won": "GANADO",
            "closed": "CERRADO"
        }.get(status, status.upper())
        
        # Prioridad texto
        priority_text = {"Low": "Baja", "Medium": "Media", "High": "Alta"}.get(priority, priority)
        
        # Notas preview
        notes_preview = notes[:80] + "..." if len(notes) > 80 else notes
        if not notes_preview:
            notes_preview = "Sin notas"
        
        # Construir HTML de la tarjeta
        card_html = f"""
        <div class="ticket-card">
            <div class="ticket-header">
                <span class="ticket-number">#{ticket_num}</span>
                <span class="badge {badge_class}">{status_label}</span>
            </div>
            <div class="ticket-title">{title}</div>
            <div class="ticket-description">{description[:120]}{'...' if len(description) > 120 else ''}</div>
            
            <div class="meta-grid">
                <div class="meta-item">
                    <span class="meta-label">Prioridad</span>
                    <span class="meta-value">{priority_text}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Creado</span>
                    <span class="meta-value">{created_date}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Grabación</span>
                    <span class="meta-value">{recording_id}...</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Ticket</span>
                    <span class="meta-value">#{ticket_num}</span>
                </div>
            </div>
            
            <div class="ticket-notes">
                <div class="notes-label">📌 Notas</div>
                <div class="notes-preview">{notes_preview}</div>
            </div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Botón "Ver detalles" que abre el modal
        if st.button("🔍 Ver detalles", key=f"view_{ticket.get('id')}", use_container_width=True):
            st.session_state.selected_ticket = ticket
            st.rerun()

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================
st.title("🎫 Dashboard de Tickets")
st.markdown("##### Gestión de oportunidades • *Haz clic en cualquier ticket para ver detalles*")
st.divider()

# --- SIDEBAR: FILTROS Y ESTADÍSTICAS ---
with st.sidebar:
    st.markdown("## Filtros")
    all_tickets = fetch_tickets()
    
    # Filtros
    status_filter = st.selectbox(
        "Estado",
        ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
        key="sidebar_status"
    )
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
    
    if st.button("🔄 Actualizar", use_container_width=True):
        st.rerun()
    
    st.divider()
    st.markdown("## Estadísticas")
    if not all_tickets.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", len(all_tickets))
        col2.metric("Nuevos", len(all_tickets[all_tickets["status"] == "new"]))
        col3.metric("Ganados", len(all_tickets[all_tickets["status"] == "won"]))
    else:
        st.info("No hay datos")

# --- CONTENIDO PRINCIPAL: GRID DE TARJETAS ---
tickets = fetch_tickets(
    status_filter=selected_status if selected_status != "Todos" else None,
    priority_filter=selected_priority if selected_priority != "Todos" else None
)

if tickets.empty:
    st.info("No hay tickets con los filtros seleccionados.")
else:
    st.markdown(f"### Mostrando {len(tickets)} tickets")
    
    # Configuración de grid: 3 columnas en desktop, 2 en tablet, 1 en móvil
    num_columns = 3
    columns = st.columns(num_columns)
    
    for idx, (_, ticket) in enumerate(tickets.iterrows()):
        col = columns[idx % num_columns]
        render_ticket_card(ticket.to_dict(), col)
    
    # --- MODAL DE DETALLE (si hay ticket seleccionado) ---
    if "selected_ticket" in st.session_state and st.session_state.selected_ticket is not None:
        ticket_detail_modal(st.session_state.selected_ticket)
        # Limpiar después de cerrar el modal (se ejecuta cuando se rerun)
        st.session_state.selected_ticket = None

# ============================================================================
# DEBUG (expandible)
# ============================================================================
with st.expander("🔧 Diagnóstico del sistema", expanded=False):
    success, msg, count = test_connection()
    if success:
        st.success(f"{msg} — {count} registros")
    else:
        st.error(msg)
    st.caption(f"URL: {SUPABASE_URL[:25]}... | Key: {SUPABASE_KEY[:15]}...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Ver muestra de opportunities"):
            client = get_supabase_connection()
            if client:
                data = client.table("opportunities").select("*").limit(3).execute().data
                st.dataframe(pd.DataFrame(data))
    with col2:
        if st.button("🎙️ Ver muestra de recordings"):
            client = get_supabase_connection()
            if client:
                data = client.table("recordings").select("*").limit(3).execute().data
                st.dataframe(pd.DataFrame(data))