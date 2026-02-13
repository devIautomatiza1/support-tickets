# ============================================================================
# CONFIGURACIÓN DE ESTILOS Y TEMAS
# ============================================================================

# Paleta de colores profesional
COLORS = {
    "primary": "#3D63FF",
    "secondary": "#6B7280",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "bg_dark": "#0F172A",
    "bg_light": "#1E293B",
    "border": "#334155",
    "text_primary": "#F1F5F9",
    "text_secondary": "#CBD5E1",
    "gray_dark": "#64748B",
    "gray_light": "#94A3B8",
}

# Estilos CSS globales
GLOBAL_STYLES = """
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
"""

# Estilos de tarjetas de tickets
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

# Estados de tickets con colores
STATUS_COLORS = {
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

# Mapeos de estado
STATUS_MAP_SPANISH = {
    "new": "Nuevo",
    "in_progress": "En progreso",
    "closed": "Cerrado",
    "won": "Ganado"
}

PRIORITY_MAP_SPANISH = {
    "Low": "Baja",
    "Medium": "Media",
    "High": "Alta"
}

# Función para obtener color de estado
def get_status_colors(status_class: str) -> dict:
    """Retorna los colores para un estado específico"""
    return STATUS_COLORS.get(status_class, STATUS_COLORS["status-open"])

# Función para generar HTML de tarjeta
def generate_ticket_card_html(
    ticket_num: str,
    status_label: str,
    status_class: str,
    title: str,
    desc: str,
    status_display: str,
    priority_display: str,
    created_date: str,
    recording_id: str,
    recording_id_full: str,
    notes: str
) -> str:
    """Genera el HTML para una tarjeta de ticket con estilos inline"""
    
    colors = get_status_colors(status_class)
    
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
        <span style="{CARD_STYLES['meta_value']}">{status_display}</span>
      </div>
      <div style="{CARD_STYLES['meta_item']}">
        <span style="{CARD_STYLES['meta_label']}">PRIORIDAD</span>
        <span style="{CARD_STYLES['meta_value']}">{priority_display}</span>
      </div>
      <div style="{CARD_STYLES['meta_item']}">
        <span style="{CARD_STYLES['meta_label']}">CREADO</span>
        <span style="{CARD_STYLES['meta_value']}">{created_date}</span>
      </div>
      <div style="{CARD_STYLES['meta_item']}">
        <span style="{CARD_STYLES['meta_label']}">GRABACIÓN</span>
        <span style="{CARD_STYLES['meta_value']}; cursor: pointer;" title="{recording_id_full}">{recording_id}...</span>
      </div>
    </div>
  </div>
  <div style="{CARD_STYLES['footer']}">
    <span style="{CARD_STYLES['notes_label']}">Notas:</span> 
    <span style="{CARD_STYLES['notes_value']}">{notes if notes else '—'}</span>
  </div>
</div>'''
    
    return card_html
