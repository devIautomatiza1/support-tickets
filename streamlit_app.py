import streamlit as st
import pandas as pd
from typing import Any, Dict, Optional, Tuple

# =============================================================================
# CONFIG APP
# =============================================================================
st.set_page_config(
    page_title="Dashboard de Tickets",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CONSTANTES (UI/DB MAPS)
# =============================================================================
STATUS_DB = ["new", "in_progress", "closed", "won"]
STATUS_UI = ["Nuevo", "En progreso", "Cerrado", "Ganado"]
STATUS_UI_TO_DB = dict(zip(STATUS_UI, STATUS_DB))
STATUS_DB_TO_UI = dict(zip(STATUS_DB, STATUS_UI))

PRIORITY_DB = ["Low", "Medium", "High"]
PRIORITY_UI = ["Baja", "Media", "Alta"]
PRIORITY_UI_TO_DB = dict(zip(PRIORITY_UI, PRIORITY_DB))
PRIORITY_DB_TO_UI = dict(zip(PRIORITY_DB, PRIORITY_UI))

BADGE_MAP = {
    "new": {"class": "badge-new", "label": "NUEVO"},
    "in_progress": {"class": "badge-progress", "label": "PROGRESO"},
    "won": {"class": "badge-won", "label": "GANADO"},
    "closed": {"class": "badge-closed", "label": "CERRADO"},
}

STATUS_STYLE = {
    "new": {"bg": "rgba(239,68,68,0.1)", "color": "#F87171", "label": "Nuevo"},
    "in_progress": {"bg": "rgba(245,158,11,0.1)", "color": "#FBBF24", "label": "En progreso"},
    "closed": {"bg": "rgba(107,114,128,0.1)", "color": "#9CA3AF", "label": "Cerrado"},
    "won": {"bg": "rgba(16,185,129,0.1)", "color": "#34D399", "label": "Ganado"},
}

PRIORITY_STYLE = {
    "Low": {"bg": "rgba(16,185,129,0.1)", "color": "#34D399", "label": "Baja"},
    "Medium": {"bg": "rgba(245,158,11,0.1)", "color": "#FBBF24", "label": "Media"},
    "High": {"bg": "rgba(239,68,68,0.1)", "color": "#F87171", "label": "Alta"},
}

# =============================================================================
# CSS
# =============================================================================
def load_css() -> None:
    st.markdown(
        """
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
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
        --shadow: 0 20px 40px -12px rgba(0,0,0,0.4);
        --shadow-hover: 0 25px 50px -12px rgba(59,130,246,0.3);
        --transition: all 0.2s ease;
    }

    [data-testid="stAppViewContainer"] { 
        background: var(--bg-primary); 
    }
    
    [data-testid="stSidebar"] { 
        background: var(--bg-secondary); 
        border-right: 1px solid var(--border); 
    }

    div.row-widget.stHorizontal {
        gap: 0.75rem;
        flex-wrap: wrap;
    }

    .ticket-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 0.85rem;
        transition: var(--transition);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .ticket-card:hover {
        border-color: var(--border-hover);
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
        transform: translateY(-2px);
        background: linear-gradient(145deg, var(--bg-card), #1A1E24);
    }

    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    
    .ticket-number {
        font-family: 'SF Mono', 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 500;
        color: var(--text-tertiary);
        letter-spacing: 0.02em;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.6rem;
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
        font-size: 0.8rem;
        font-weight: 450;
        color: var(--text-primary);
        line-height: 1.3;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 2rem;
    }

    div[data-testid="stDialog"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 1rem 0 !important;
    }
    
    div[data-testid="stDialog"] > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 1.5rem 1.75rem !important;
        box-shadow: var(--shadow) !important;
        max-width: 600px !important;
        width: 100% !important;
        margin: 0 auto !important;
        max-height: 90vh !important;
        overflow-y: auto !important;
    }
    
    div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2 {
        display: none !important;
    }

    .modal-header {
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        flex-wrap: wrap;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.75rem;
    }
    
    .modal-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.3;
        letter-spacing: -0.02em;
    }
    
    .modal-date {
        font-size: 0.75rem;
        color: var(--text-tertiary);
        font-family: 'SF Mono', 'JetBrains Mono', monospace;
        background: var(--bg-secondary);
        padding: 0.2rem 0.6rem;
        border-radius: 16px;
        border: 1px solid var(--border);
    }

    .section-title {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .description-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.9rem 1rem;
        color: var(--text-secondary);
        font-size: 0.85rem;
        line-height: 1.5;
        white-space: pre-wrap;
    }

    .info-card {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 0.9rem;
        border: 1px solid var(--border);
    }
    
    .info-label {
        font-size: 0.6rem;
        font-weight: 600;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    
    .current-value {
        display: inline-block;
        padding: 0.2rem 0.75rem;
        border-radius: 16px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    .select-label {
        font-size: 0.6rem;
        color: var(--text-tertiary);
        margin-bottom: 0.2rem;
    }

    .stSelectbox {
        margin-bottom: 0.25rem !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        min-height: 2rem !important;
        transition: var(--transition) !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
        background: var(--bg-card) !important;
    }

    .stTextArea textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-size: 0.8rem !important;
        line-height: 1.5 !important;
        padding: 0.75rem !important;
        min-height: 120px !important;
        max-height: 150px !important;
        font-family: 'SF Mono', 'JetBrains Mono', monospace !important;
        transition: var(--transition) !important;
    }

    .stButton > button {
        border-radius: 8px !important;
        font-size: 0.75rem !important;
        padding: 0.35rem 0.75rem !important;
        transition: var(--transition) !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        width: 100% !important;
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        background: var(--accent-soft) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.2) !important;
    }

    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(59,130,246,0.2) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #2563EB !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59,130,246,0.4) !important;
    }

    hr {
        border: none;
        height: 1px;
        background: var(--border);
        margin: 1rem 0;
    }
    
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.6rem;
        transition: var(--transition) !important;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: var(--border-hover) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# SUPABASE
# =============================================================================
@st.cache_resource(show_spinner=False)
def get_supabase_client():
    try:
        from supabase import create_client
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error conectando a Supabase: {e}")
        return None


def fetch_tickets(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
) -> pd.DataFrame:
    client = get_supabase_client()
    if not client:
        return pd.DataFrame()

    try:
        q = client.table("opportunities").select(
            "id, ticket_number, title, description, status, priority, notes, created_at, recording_id"
        )

        if status_filter:
            q = q.eq("status", status_filter)
        if priority_filter:
            q = q.eq("priority", priority_filter)

        res = q.execute()
        data = res.data or []
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df.columns = df.columns.str.lower()
        
        # ✅ Filtrar registros con ID válido
        df = df.dropna(subset=["id"])
        df = df[df["id"].astype(str).str.strip() != ""]
        
        return df

    except Exception as e:
        st.error(f"Error fetching tickets: {e}")
        return pd.DataFrame()


def update_ticket(ticket_id: int, status: str, notes: str, priority: Optional[str] = None) -> bool:
    client = get_supabase_client()
    if not client:
        return False

    try:
        payload: Dict[str, Any] = {"status": status, "notes": notes}
        if priority is not None:
            payload["priority"] = priority

        client.table("opportunities").update(payload).eq("id", ticket_id).execute()
        return True
    except Exception as e:
        st.error(f"Error actualizando ticket: {e}")
        return False


def test_connection() -> Tuple[bool, str, Optional[int]]:
    client = get_supabase_client()
    if not client:
        return False, "No se pudo inicializar Supabase (revisa secrets / dependencia)", None
    try:
        res = client.table("opportunities").select("id", count="exact").limit(1).execute()
        count = getattr(res, "count", None)
        return True, "Conexión exitosa", count
    except Exception as e:
        return False, f"Error de conexión: {e}", None


# =============================================================================
# HELPERS UI
# =============================================================================
def clean_description(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return "\n".join([line for line in text.split("\n") if line.strip()])


def ui_filters_to_db(status_ui: str, priority_ui: str) -> Tuple[Optional[str], Optional[str]]:
    status_db = None if status_ui == "Todos" else STATUS_UI_TO_DB.get(status_ui)
    priority_db = None if priority_ui == "Todos" else PRIORITY_UI_TO_DB.get(priority_ui)
    return status_db, priority_db


def safe_get_ticket_id(ticket: Dict[str, Any]) -> Optional[int]:
    """Convierte de forma segura cualquier formato de ID a entero"""
    raw_id = ticket.get("id")
    
    # Caso 1: No existe el campo
    if raw_id is None:
        return None
    
    # Caso 2: String vacío
    if isinstance(raw_id, str) and not raw_id.strip():
        return None
    
    # Caso 3: Convertir a entero
    try:
        return int(float(raw_id))
    except (ValueError, TypeError):
        return None


# =============================================================================
# MODAL - CORREGIDO CON VALIDACIÓN DE ID
# =============================================================================
@st.dialog("Editar ticket", width="large")
def edit_ticket_modal(ticket: Dict[str, Any]) -> None:
    # ===== VALIDACIÓN ROBUSTA DEL ID =====
    ticket_id = safe_get_ticket_id(ticket)
    
    if ticket_id is None:
        st.error("❌ Error: Ticket sin identificador válido")
        st.stop()
    
    # Si llegamos aquí, ticket_id es un int válido
    title = ticket.get("title") or "Sin título"
    description = clean_description(ticket.get("description") or "")
    created_at = (ticket.get("created_at") or "")[:10] or "N/A"
    
    current_status = (ticket.get("status") or "new").lower()
    current_priority = ticket.get("priority") or "Medium"
    notes = ticket.get("notes") or ""

    # Header
    st.markdown(
        f"""
        <div class="modal-header">
            <div><span class="modal-title">{title}</span></div>
            <span class="modal-date">{created_at}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Descripción
    st.markdown('<div class="section-title">DESCRIPCIÓN</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="description-box">
            {description if description else 'Sin descripción'}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin-top: 1.25rem; margin-bottom: 0.75rem;">
            <span class="section-title">ESTADO Y PRIORIDAD</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    # Estado
    with col1:
        style = STATUS_STYLE.get(current_status, STATUS_STYLE["new"])
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">ESTADO ACTUAL</div>
                <span class="current-value" style="background: {style['bg']}; color: {style['color']};">
                    {style['label']}
                </span>
                <div class="select-label">CAMBIAR A</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        status_ui_default = STATUS_DB_TO_UI.get(current_status, "Nuevo")
        status_idx = STATUS_UI.index(status_ui_default) if status_ui_default in STATUS_UI else 0
        new_status_ui = st.selectbox(
            "",
            STATUS_UI,
            index=status_idx,
            key=f"status_{ticket_id}",
            label_visibility="collapsed",
        )
        new_status_db = STATUS_UI_TO_DB[new_status_ui]

    # Prioridad
    with col2:
        pstyle = PRIORITY_STYLE.get(current_priority, PRIORITY_STYLE["Medium"])
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">PRIORIDAD ACTUAL</div>
                <span class="current-value" style="background: {pstyle['bg']}; color: {pstyle['color']};">
                    {pstyle['label']}
                </span>
                <div class="select-label">CAMBIAR A</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        priority_ui_default = PRIORITY_DB_TO_UI.get(current_priority, "Media")
        pr_idx = PRIORITY_UI.index(priority_ui_default) if priority_ui_default in PRIORITY_UI else 1
        new_priority_ui = st.selectbox(
            "",
            PRIORITY_UI,
            index=pr_idx,
            key=f"priority_{ticket_id}",
            label_visibility="collapsed",
        )
        new_priority_db = PRIORITY_UI_TO_DB[new_priority_ui]

    # Notas (form)
    st.markdown(
        """
        <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
            <span class="section-title">NOTAS</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(key=f"edit_modal_form_{ticket_id}"):
        new_notes = st.text_area(
            "",
            value=notes,
            height=120,
            placeholder="⭐️ Tema / 📌 Descripción / 👤 Mencionado / 💬 Contexto / 📊 Confianza",
            key=f"notes_{ticket_id}",
            label_visibility="collapsed",
        )

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])

        with c2:
            saved = st.form_submit_button("Guardar cambios", use_container_width=True, type="primary")
        with c3:
            cancelled = st.form_submit_button("Cancelar", use_container_width=True)

        if saved:
            ok = update_ticket(ticket_id, new_status_db, new_notes, new_priority_db)
            if ok:
                st.success("✓ Ticket actualizado correctamente")
                st.rerun()
            else:
                st.error("❌ Error al actualizar en Supabase")

        if cancelled:
            st.rerun()


# =============================================================================
# GRID - CORREGIDO CON VALIDACIÓN DE ID
# =============================================================================
@st.fragment
def render_ticket_grid(df: pd.DataFrame, num_columns: int = 3) -> None:
    if df.empty:
        st.info("No hay tickets disponibles")
        return

    cols = st.columns(num_columns, gap="small")
    for idx, (_, row) in enumerate(df.iterrows()):
        with cols[idx % num_columns]:
            t = row.to_dict()
            
            # ✅ Validar que el ticket tiene ID válido
            ticket_id = safe_get_ticket_id(t)
            if ticket_id is None:
                continue  # Saltar tickets sin ID válido
            
            ticket_num = t.get("ticket_number", "N/A")
            title = (t.get("title") or "Sin título")[:60]
            status = (t.get("status") or "new").lower()

            badge = BADGE_MAP.get(status, BADGE_MAP["new"])
            st.markdown(
                f"""
                <div class="ticket-card">
                    <div class="ticket-header">
                        <span class="ticket-number">#{ticket_num}</span>
                        <span class="badge {badge['class']}">{badge['label']}</span>
                    </div>
                    <div class="ticket-title">{title}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("EDITAR", key=f"edit_{ticket_id}", use_container_width=True):
                st.session_state.edit_ticket = t
                st.rerun()


# =============================================================================
# MAIN
# =============================================================================
load_css()

st.title("Dashboard")
st.markdown(
    "<h3 style='color: var(--text-secondary); font-weight: 400; margin-top: -0.5rem;'>Gestión de oportunidades</h3>",
    unsafe_allow_html=True,
)
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("## Filtros")

    all_tickets = fetch_tickets()

    status_ui = st.selectbox("Estado", ["Todos"] + STATUS_UI, key="status_filter")
    priority_ui = st.selectbox("Prioridad", ["Todos"] + PRIORITY_UI, key="priority_filter")

    status_db, priority_db = ui_filters_to_db(status_ui, priority_ui)

    if st.button("ACTUALIZAR", key="ACTUALIZAR", use_container_width=True):
        st.rerun()

    st.divider()
    st.markdown("## Estadísticas")
    if not all_tickets.empty and "status" in all_tickets.columns:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total", len(all_tickets))
        with c2:
            st.metric("Nuevos", int((all_tickets["status"] == "new").sum()))
        with c3:
            st.metric("Ganados", int((all_tickets["status"] == "won").sum()))
    else:
        st.info("Sin datos")

# Data grid
tickets = fetch_tickets(status_filter=status_db, priority_filter=priority_db)

if tickets.empty:
    st.info("No hay tickets con los filtros seleccionados.")
else:
    st.markdown(f"#### {len(tickets)} tickets encontrados")
    render_ticket_grid(tickets)

# Modal
if st.session_state.get("edit_ticket"):
    edit_ticket_modal(st.session_state.edit_ticket)
    st.session_state.edit_ticket = None

# Diagnóstico
with st.expander("Diagnóstico del sistema", expanded=False):
    ok, msg, count = test_connection()
    if ok:
        st.success(f"{msg} — {count if count is not None else 'N/A'} registros")
    else:
        st.error(msg)

    st.caption("URL: Configurada en secrets")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Ver opportunities", key="ver_opp"):
            client = get_supabase_client()
            if client:
                data = client.table("opportunities").select("*").limit(3).execute().data
                if data:
                    st.dataframe(pd.DataFrame(data))
    with col2:
        if st.button("🎙️ Ver recordings", key="ver_rec"):
            client = get_supabase_client()
            if client:
                data = client.table("recordings").select("*").limit(3).execute().data
                if data:
                    st.dataframe(pd.DataFrame(data))