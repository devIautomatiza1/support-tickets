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
# DISEÑO MINIMALISTA PROFESIONAL - MEJORADO
# ============================================================================

st.markdown("""
<style>
    /* Variables y Reset */
    :root {
        --bg-primary: #0A0C10;
        --bg-secondary: #111316;
        --bg-card: #16181C;
        --border: #2A2C30;
        --text-primary: #E8E9EA;
        --text-secondary: #8B8E94;
        --text-tertiary: #5E6269;
        --accent: #3B82F6;
        --accent-soft: rgba(59, 130, 246, 0.1);
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
    }
    
    /* Estructura base */
    [data-testid="stAppViewContainer"] {
        background: var(--bg-primary);
    }
    
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    /* Tipografía refinada */
    h1, h2, h3, h4, p, span {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    h1 {
        font-size: 1.875rem;
        font-weight: 500;
        letter-spacing: -0.025em;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    h2 {
        font-size: 1.25rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    
    /* Subtítulo */
    .subtitle {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
    }
    
    /* Tarjetas - diseño limpio */
    .ticket-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease;
    }
    
    .ticket-card:hover {
        border-color: var(--text-tertiary);
    }
    
    /* Cabecera de tarjeta */
    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .ticket-title {
        font-size: 1rem;
        font-weight: 500;
        color: var(--text-primary);
        margin: 0;
        line-height: 1.5;
    }
    
    .ticket-id {
        color: var(--text-tertiary);
        font-size: 0.875rem;
        font-weight: 400;
        margin-left: 0.5rem;
    }
    
    /* Badges minimalistas */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.025em;
        background: var(--accent-soft);
        color: var(--accent);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .badge-new { background: rgba(239, 68, 68, 0.1); color: #FCA5A5; border-color: rgba(239, 68, 68, 0.2); }
    .badge-progress { background: rgba(245, 158, 11, 0.1); color: #FCD34D; border-color: rgba(245, 158, 11, 0.2); }
    .badge-won { background: rgba(16, 185, 129, 0.1); color: #6EE7B7; border-color: rgba(16, 185, 129, 0.2); }
    .badge-closed { background: rgba(107, 114, 128, 0.1); color: #D1D5DB; border-color: rgba(107, 114, 128, 0.2); }
    
    /* Grid de información */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
        padding: 0.75rem 0;
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
    }
    
    .info-item {
        display: flex;
        flex-direction: column;
    }
    
    .info-label {
        color: var(--text-tertiary);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .info-value {
        color: var(--text-primary);
        font-size: 0.875rem;
        font-weight: 400;
    }
    
    /* Sección de notas */
    .notes-section {
        background: var(--bg-secondary);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 0.5rem;
    }
    
    .notes-title {
        color: var(--text-tertiary);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .notes-content {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.6;
        margin: 0;
        max-height: 100px;
        overflow-y: auto;
    }
    
    /* Métricas compactas */
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
    }
    
    [data-testid="metric-container"] > div {
        margin: 0;
    }
    
    [data-testid="metric-container"] label {
        color: var(--text-tertiary) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-primary) !important;
        font-size: 1.5rem !important;
        font-weight: 500 !important;
    }
    
    /* Divider refinado */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid var(--border);
    }
    
    /* Botones */
    .stButton > button {
        background: var(--accent-soft);
        color: var(--accent);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: rgba(59, 130, 246, 0.15);
        border-color: var(--accent);
    }
    
    /* Select boxes */
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-card);
        border-color: var(--border);
        border-radius: 8px;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--text-tertiary);
    }
    
    /* Panel de debug */
    .debug-panel {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    /* Estado vacío */
    .empty-state {
        text-align: center;
        padding: 3rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    
    .empty-state p {
        color: var(--text-tertiary);
        margin: 0;
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-tertiary);
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
            return False, "No se pudo inicializar el cliente de Supabase", None
        
        response = client.table("opportunities").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        
        return True, "Conexión exitosa", count
    except Exception as e:
        return False, f"Error de conexión", None

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
        return False

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def get_badge_class(status: str) -> str:
    """Retorna la clase CSS para el badge de estado"""
    status_map = {
        "new": "badge-new",
        "in_progress": "badge-progress",
        "won": "badge-won",
        "closed": "badge-closed"
    }
    return status_map.get(status.lower(), "badge")

def format_date(date_str: str) -> str:
    """Formatea la fecha de manera legible"""
    if not date_str or date_str == "N/A":
        return "N/A"
    try:
        date_obj = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")
    except:
        return date_str[:10]

# ============================================================================
# INTERFAZ DE USUARIO - HEADER
# ============================================================================

col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("<h1 style='font-size: 2rem; margin-bottom: 0;'>🎫</h1>", unsafe_allow_html=True)
with col2:
    st.title("Tickets")
    st.markdown('<p class="subtitle">Gestión de oportunidades y seguimiento</p>', unsafe_allow_html=True)

# ============================================================================
# BARRA LATERAL - FILTROS Y ESTADÍSTICAS
# ============================================================================

with st.sidebar:
    st.markdown("### Filtros")
    
    # Obtener tickets para estadísticas
    all_tickets = fetch_tickets()
    
    # Definir opciones
    status_options = {
        "Todos": "Todos",
        "new": "Nuevo",
        "in_progress": "En progreso",
        "closed": "Cerrado",
        "won": "Ganado"
    }
    
    priority_options = {
        "Todos": "Todos",
        "Low": "Baja",
        "Medium": "Media",
        "High": "Alta"
    }
    
    # Selectores
    selected_status_display = st.selectbox(
        "Estado",
        list(status_options.values()),
        key="sidebar_status"
    )
    
    selected_priority_display = st.selectbox(
        "Prioridad",
        list(priority_options.values()),
        key="sidebar_priority"
    )
    
    # Mapear de vuelta
    selected_status = [k for k, v in status_options.items() if v == selected_status_display][0]
    selected_priority = [k for k, v in priority_options.items() if v == selected_priority_display][0]
    
    # Botón actualizar
    if st.button("Actualizar", use_container_width=True):
        st.rerun()
    
    st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Estadísticas compactas
    st.markdown("### Resumen")
    
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
    <div class="empty-state">
        <p style='font-size: 1.25rem; margin-bottom: 0.5rem;'>🎫 No hay tickets</p>
        <p style='color: var(--text-tertiary);'>No se encontraron tickets con los filtros seleccionados</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Contador de resultados
    st.markdown(f"### Mostrando {len(tickets)} tickets")
    
    # Iterar tickets
    for _, ticket in tickets.iterrows():
        
        # Determinar badge de estado
        status = str(ticket.get("status", "")).lower()
        status_labels = {
            "new": "NUEVO",
            "in_progress": "PROGRESO",
            "won": "GANADO",
            "closed": "CERRADO"
        }
        status_label = status_labels.get(status, status.upper())
        badge_class = get_badge_class(status)
        
        # Prioridad
        priority = str(ticket.get("priority", "")).lower()
        priority_icon = {"high": "⚠️", "medium": "●", "low": "○"}.get(priority, "●")
        priority_color = {
            "high": "var(--danger)",
            "medium": "var(--warning)",
            "low": "var(--success)"
        }.get(priority, "var(--text-secondary)")
        
        # HTML de la tarjeta
        card_html = f"""
        <div class="ticket-card">
            <div class="ticket-header">
                <div>
                    <span class="ticket-title">
                        {ticket.get('title', 'Sin título')}
                        <span class="ticket-id">#{ticket.get('ticket_number', 'N/A')}</span>
                    </span>
                </div>
                <span class="badge {badge_class}">{status_label}</span>
            </div>
            
            <p style="color: var(--text-secondary); font-size: 0.875rem; margin: 0 0 1rem 0; line-height: 1.6;">
                {ticket.get('description', 'Sin descripción').replace('"', '').strip()[:200]}{'...' if len(str(ticket.get('description', ''))) > 200 else ''}
            </p>
            
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Fecha</span>
                    <span class="info-value">{format_date(ticket.get('created_at', 'N/A'))}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Prioridad</span>
                    <span class="info-value" style="color: {priority_color};">{priority_icon} {priority.upper() if priority else 'MEDIA'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Grabación</span>
                    <span class="info-value">{str(ticket.get('recording_id', 'N/A'))[:8]}...</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Última actualización</span>
                    <span class="info-value">{format_date(ticket.get('created_at', 'N/A'))}</span>
                </div>
            </div>
            
            <div class="notes-section">
                <div class="notes-title">Notas</div>
                <div class="notes-content">
                    {ticket.get('notes', '').replace('"', '').strip() or '<span style="color: var(--text-tertiary); font-style: italic;">Sin notas registradas</span>'}
                </div>
            </div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Expander para edición
        with st.expander("✏️ Editar ticket", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                edit_status = st.selectbox(
                    "Estado",
                    ["Nuevo", "En progreso", "Cerrado", "Ganado"],
                    index=["new", "in_progress", "closed", "won"].index(status) if status in ["new", "in_progress", "closed", "won"] else 0,
                    key=f"edit_status_{ticket['id']}"
                )
                
                status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
            
            with col2:
                edit_priority = st.selectbox(
                    "Prioridad",
                    ["Baja", "Media", "Alta"],
                    index=["low", "medium", "high"].index(priority) if priority in ["low", "medium", "high"] else 1,
                    key=f"edit_priority_{ticket['id']}"
                )
                
                priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
            
            edit_notes = st.text_area(
                "Notas",
                value=ticket.get('notes', ''),
                key=f"edit_notes_{ticket['id']}",
                placeholder="Agregar notas sobre el ticket..."
            )
            
            if st.button("Guardar cambios", key=f"save_{ticket['id']}"):
                if update_ticket(ticket['id'], status_map[edit_status], edit_notes):
                    st.success("✅ Ticket actualizado correctamente")
                    st.rerun()
                else:
                    st.error("❌ Error al actualizar el ticket")
        
        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

# ============================================================================
# PANEL DE DIAGNÓSTICO
# ============================================================================

with st.expander("🔧 Diagnóstico del sistema", expanded=False):
    st.markdown('<div class="debug-panel">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Estado de conexión")
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
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Ver opportunities", use_container_width=True):
            try:
                client = get_supabase_connection()
                if client:
                    response = client.table("opportunities").select("*").limit(5).execute()
                    if response.data:
                        st.dataframe(
                            pd.DataFrame(response.data),
                            use_container_width=True,
                            hide_index=True
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("🔍 Ver recordings", use_container_width=True):
            try:
                client = get_supabase_connection()
                if client:
                    response = client.table("recordings").select("*").limit(5).execute()
                    if response.data:
                        st.dataframe(
                            pd.DataFrame(response.data),
                            use_container_width=True,
                            hide_index=True
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)