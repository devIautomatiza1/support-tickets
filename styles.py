# ============================================================================
# CONFIGURACIÓN DE ESTILOS Y TEMAS - VERSIÓN 2025
# ============================================================================

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import streamlit as st

# ----------------------------------------------------------------------------
# SISTEMA DE DISEÑO TOKEN-BASED (Moderno y Escalable)
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class DesignTokens:
    """Sistema de tokens de diseño - Single source of truth"""
    
    # Colores base - Paleta neutral profesional
    gray_0: str = "#FFFFFF"
    gray_50: str = "#FAFAFA"
    gray_100: str = "#F5F5F5"
    gray_200: str = "#E5E5E5"
    gray_300: str = "#D4D4D4"
    gray_400: str = "#A3A3A3"
    gray_500: str = "#737373"
    gray_600: str = "#525252"
    gray_700: str = "#404040"
    gray_800: str = "#262626"
    gray_900: str = "#171717"
    gray_950: str = "#0A0A0A"
    
    # Colores primarios - Azul profesional
    primary_50: str = "#EFF6FF"
    primary_100: str = "#DBEAFE"
    primary_200: str = "#BFDBFE"
    primary_300: str = "#93C5FD"
    primary_400: str = "#60A5FA"
    primary_500: str = "#3B82F6"
    primary_600: str = "#2563EB"
    primary_700: str = "#1D4ED8"
    primary_800: str = "#1E40AF"
    primary_900: str = "#1E3A8A"
    
    # Colores semánticos
    success: str = "#059669"
    warning: str = "#D97706"
    danger: str = "#DC2626"
    info: str = "#2563EB"
    
    # Tipografía
    font_family: str = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    font_family_mono: str = "'JetBrains Mono', 'SF Mono', Monaco, Consolas, monospace"
    
    # Espaciado (8px grid system)
    space_1: str = "0.25rem"  # 4px
    space_2: str = "0.5rem"   # 8px
    space_3: str = "0.75rem"  # 12px
    space_4: str = "1rem"     # 16px
    space_5: str = "1.25rem"  # 20px
    space_6: str = "1.5rem"   # 24px
    space_8: str = "2rem"     # 32px
    space_10: str = "2.5rem"  # 40px
    space_12: str = "3rem"    # 48px
    
    # Radii
    radius_sm: str = "0.375rem"  # 6px
    radius_md: str = "0.5rem"    # 8px
    radius_lg: str = "0.75rem"   # 12px
    radius_xl: str = "1rem"      # 16px
    radius_full: str = "9999px"
    
    # Shadows
    shadow_sm: str = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    shadow_md: str = "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
    shadow_lg: str = "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
    shadow_xl: str = "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
    
    # Transitions
    transition_base: str = "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)"
    
    # Z-index
    z_dropdown: int = 1000
    z_modal: int = 1100
    z_tooltip: int = 1200


# Instancia global de tokens
TOKENS = DesignTokens()


# ----------------------------------------------------------------------------
# TEMAS (Dark/Light mode ready)
# ----------------------------------------------------------------------------

@dataclass
class Theme:
    """Tema dinámico con soporte para modo claro/oscuro"""
    
    @staticmethod
    def dark() -> Dict[str, str]:
        return {
            "bg_primary": TOKENS.gray_950,
            "bg_secondary": TOKENS.gray_900,
            "bg_tertiary": TOKENS.gray_800,
            "bg_card": TOKENS.gray_900,
            "bg_card_hover": TOKENS.gray_800,
            "bg_sidebar": TOKENS.gray_900,
            "border": TOKENS.gray_800,
            "border_hover": TOKENS.gray_700,
            "text_primary": TOKENS.gray_50,
            "text_secondary": TOKENS.gray_300,
            "text_tertiary": TOKENS.gray_400,
            "text_disabled": TOKENS.gray_600,
            "primary": TOKENS.primary_500,
            "primary_hover": TOKENS.primary_600,
            "primary_soft": f"{TOKENS.primary_500}10",
        }
    
    @staticmethod
    def light() -> Dict[str, str]:
        return {
            "bg_primary": TOKENS.gray_50,
            "bg_secondary": TOKENS.gray_100,
            "bg_tertiary": TOKENS.gray_200,
            "bg_card": TOKENS.gray_0,
            "bg_card_hover": TOKENS.gray_50,
            "bg_sidebar": TOKENS.gray_100,
            "border": TOKENS.gray_200,
            "border_hover": TOKENS.gray_300,
            "text_primary": TOKENS.gray_900,
            "text_secondary": TOKENS.gray_600,
            "text_tertiary": TOKENS.gray_500,
            "text_disabled": TOKENS.gray_400,
            "primary": TOKENS.primary_600,
            "primary_hover": TOKENS.primary_700,
            "primary_soft": f"{TOKENS.primary_600}10",
        }


# ----------------------------------------------------------------------------
# GENERADOR DE CSS MODERNO
# ----------------------------------------------------------------------------

def generate_global_styles(theme: str = "dark") -> str:
    """Genera CSS moderno con variables CSS y diseño system-ui"""
    
    colors = Theme.dark() if theme == "dark" else Theme.light()
    
    return f"""
    <style>
        /* ------------------------------------------------------------------
           DESIGN SYSTEM - TOKENS
        ------------------------------------------------------------------ */
        :root {{
            --font-sans: {TOKENS.font_family};
            --font-mono: {TOKENS.font_family_mono};
            
            /* Spacing */
            --space-1: {TOKENS.space_1};
            --space-2: {TOKENS.space_2};
            --space-3: {TOKENS.space_3};
            --space-4: {TOKENS.space_4};
            --space-5: {TOKENS.space_5};
            --space-6: {TOKENS.space_6};
            --space-8: {TOKENS.space_8};
            --space-10: {TOKENS.space_10};
            --space-12: {TOKENS.space_12};
            
            /* Radii */
            --radius-sm: {TOKENS.radius_sm};
            --radius-md: {TOKENS.radius_md};
            --radius-lg: {TOKENS.radius_lg};
            --radius-xl: {TOKENS.radius_xl};
            --radius-full: {TOKENS.radius_full};
            
            /* Shadows */
            --shadow-sm: {TOKENS.shadow_sm};
            --shadow-md: {TOKENS.shadow_md};
            --shadow-lg: {TOKENS.shadow_lg};
            --shadow-xl: {TOKENS.shadow_xl};
            
            /* Transitions */
            --transition-base: {TOKENS.transition_base};
        }}
        
        /* ------------------------------------------------------------------
           TEMA ACTIVO (Dark/Light)
        ------------------------------------------------------------------ */
        :root {{
            --bg-primary: {colors['bg_primary']};
            --bg-secondary: {colors['bg_secondary']};
            --bg-tertiary: {colors['bg_tertiary']};
            --bg-card: {colors['bg_card']};
            --bg-card-hover: {colors['bg_card_hover']};
            --bg-sidebar: {colors['bg_sidebar']};
            --border: {colors['border']};
            --border-hover: {colors['border_hover']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --text-tertiary: {colors['text_tertiary']};
            --text-disabled: {colors['text_disabled']};
            --primary: {colors['primary']};
            --primary-hover: {colors['primary_hover']};
            --primary-soft: {colors['primary_soft']};
            --success: {TOKENS.success};
            --warning: {TOKENS.warning};
            --danger: {TOKENS.danger};
            --info: {TOKENS.info};
        }}
        
        /* ------------------------------------------------------------------
           RESET Y BASE
        ------------------------------------------------------------------ */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            font-size: 16px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        body, [data-testid="stAppViewContainer"] {{
            font-family: var(--font-sans);
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
        }}
        
        /* ------------------------------------------------------------------
           SIDEBAR MODERNO
        ------------------------------------------------------------------ */
        [data-testid="stSidebar"] {{
            background: var(--bg-sidebar);
            border-right: 1px solid var(--border);
        }}
        
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
            padding: var(--space-4) 0;
        }}
        
        /* ------------------------------------------------------------------
           TIPOGRAFÍA
        ------------------------------------------------------------------ */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-sans);
            color: var(--text-primary);
            font-weight: 600;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        h1 {{
            font-size: 2rem;
            margin-bottom: var(--space-2);
        }}
        
        h2 {{
            font-size: 1.5rem;
            margin-bottom: var(--space-4);
        }}
        
        h3 {{
            font-size: 1.25rem;
            margin-bottom: var(--space-3);
        }}
        
        p {{
            color: var(--text-secondary);
            line-height: 1.6;
        }}
        
        /* ------------------------------------------------------------------
           TARJETAS MODERNAS - GLASSMORPHISM
        ------------------------------------------------------------------ */
        .ticket-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            margin-bottom: var(--space-4);
            transition: var(--transition-base);
            backdrop-filter: blur(8px);
        }}
        
        .ticket-card:hover {{
            border-color: var(--border-hover);
            box-shadow: var(--shadow-lg);
            background: var(--bg-card-hover);
        }}
        
        .ticket-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--space-4);
            border-bottom: 1px solid var(--border);
            background: linear-gradient(to right, var(--bg-tertiary), transparent);
        }}
        
        .ticket-number {{
            font-family: var(--font-mono);
            font-weight: 600;
            color: var(--primary);
            letter-spacing: -0.01em;
        }}
        
        .ticket-body {{
            padding: var(--space-4);
        }}
        
        .ticket-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: var(--space-2);
        }}
        
        .ticket-description {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: var(--space-4);
        }}
        
        /* ------------------------------------------------------------------
           GRID DE METADATOS
        ------------------------------------------------------------------ */
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: var(--space-4);
            background: var(--bg-tertiary);
            border-radius: var(--radius-md);
            padding: var(--space-4);
            margin-bottom: var(--space-4);
        }}
        
        .meta-item {{
            display: flex;
            flex-direction: column;
            gap: var(--space-1);
        }}
        
        .meta-label {{
            color: var(--text-tertiary);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .meta-value {{
            color: var(--text-primary);
            font-weight: 500;
            font-size: 0.9rem;
        }}
        
        /* ------------------------------------------------------------------
           BADGES MINIMALISTAS
        ------------------------------------------------------------------ */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: var(--space-1) var(--space-3);
            border-radius: var(--radius-full);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            white-space: nowrap;
            border: 1px solid transparent;
        }}
        
        .badge-new {{
            background: {TOKENS.danger}10;
            color: {TOKENS.danger};
            border-color: {TOKENS.danger}20;
        }}
        
        .badge-progress {{
            background: {TOKENS.warning}10;
            color: {TOKENS.warning};
            border-color: {TOKENS.warning}20;
        }}
        
        .badge-won {{
            background: {TOKENS.success}10;
            color: {TOKENS.success};
            border-color: {TOKENS.success}20;
        }}
        
        .badge-closed {{
            background: {TOKENS.gray_500}10;
            color: var(--text-tertiary);
            border-color: {TOKENS.gray_500}20;
        }}
        
        /* ------------------------------------------------------------------
           BOTONES MODERNOS
        ------------------------------------------------------------------ */
        .stButton > button {{
            font-family: var(--font-sans);
            font-weight: 500;
            font-size: 0.9rem;
            padding: var(--space-2) var(--space-4);
            border-radius: var(--radius-md);
            background: var(--primary);
            color: white;
            border: none;
            transition: var(--transition-base);
            box-shadow: var(--shadow-sm);
        }}
        
        .stButton > button:hover {{
            background: var(--primary-hover);
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Botón secundario */
        .stButton > button[kind="secondary"] {{
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid var(--border);
        }}
        
        .stButton > button[kind="secondary"]:hover {{
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border-color: var(--border-hover);
        }}
        
        /* ------------------------------------------------------------------
           MÉTRICAS
        ------------------------------------------------------------------ */
        [data-testid="metric-container"] {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: var(--space-4);
            transition: var(--transition-base);
        }}
        
        [data-testid="metric-container"]:hover {{
            border-color: var(--border-hover);
            box-shadow: var(--shadow-md);
        }}
        
        [data-testid="metric-container"] label {{
            color: var(--text-tertiary) !important;
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        [data-testid="metric-container"] [data-testid="metric-value"] {{
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-size: 1.5rem !important;
        }}
        
        /* ------------------------------------------------------------------
           INPUTS Y SELECTS
        ------------------------------------------------------------------ */
        .stSelectbox [data-baseweb="select"] {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            transition: var(--transition-base);
        }}
        
        .stSelectbox [data-baseweb="select"]:hover {{
            border-color: var(--border-hover);
        }}
        
        .stSelectbox [data-baseweb="select"]:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 2px {TOKENS.primary_500}20;
        }}
        
        /* ------------------------------------------------------------------
           EXPANDER
        ------------------------------------------------------------------ */
        .streamlit-expanderHeader {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-weight: 500;
            transition: var(--transition-base);
        }}
        
        .streamlit-expanderHeader:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-hover);
        }}
        
        /* ------------------------------------------------------------------
           DIVIDER
        ------------------------------------------------------------------ */
        hr {{
            border: none;
            border-top: 1px solid var(--border);
            margin: var(--space-6) 0;
        }}
        
        /* ------------------------------------------------------------------
           ANIMACIONES
        ------------------------------------------------------------------ */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .ticket-card {{
            animation: fadeIn 0.3s ease-out;
        }}
    </style>
    """


# ----------------------------------------------------------------------------
# COMPONENTES REUTILIZABLES
# ----------------------------------------------------------------------------

class StatusBadge:
    """Componente de badge de estado"""
    
    STATUS_CONFIG = {
        "new": {"class": "badge-new", "label": "Nuevo", "icon": "🆕"},
        "in_progress": {"class": "badge-progress", "label": "En progreso", "icon": "⚡"},
        "won": {"class": "badge-won", "label": "Ganado", "icon": "🎯"},
        "closed": {"class": "badge-closed", "label": "Cerrado", "icon": "✅"},
    }
    
    @classmethod
    def render(cls, status: str) -> str:
        config = cls.STATUS_CONFIG.get(status, cls.STATUS_CONFIG["new"])
        return f'<span class="badge {config["class"]}">{config["icon"]} {config["label"]}</span>'


class PriorityIndicator:
    """Indicador de prioridad minimalista"""
    
    PRIORITY_CONFIG = {
        "High": {"color": "#DC2626", "dot": "🔴", "label": "Alta"},
        "Medium": {"color": "#D97706", "dot": "🟡", "label": "Media"},
        "Low": {"color": "#059669", "dot": "🟢", "label": "Baja"},
    }
    
    @classmethod
    def render(cls, priority: str) -> str:
        config = cls.PRIORITY_CONFIG.get(priority, cls.PRIORITY_CONFIG["Medium"])
        return f'<span style="display: flex; align-items: center; gap: 4px;"><span style="color: {config["color"]};">{config["dot"]}</span> {config["label"]}</span>'


# ----------------------------------------------------------------------------
# FACTORY DE TARJETAS
# ----------------------------------------------------------------------------

class TicketCardFactory:
    """Factory para crear tarjetas de tickets"""
    
    @staticmethod
    def create(
        ticket_num: str,
        title: str,
        description: str,
        status: str,
        priority: str,
        created_at: str,
        recording_id: str,
        notes: str = ""
    ) -> str:
        """Crea una tarjeta de ticket moderna"""
        
        # Sanitizar y truncar
        description = (description or "").replace('"', '&quot;').strip()
        if len(description) > 200:
            description = description[:200] + "..."
            
        notes = (notes or "").replace('"', '&quot;').strip()
        if len(notes) > 150:
            notes = notes[:150] + "..."
        
        # Formatear fecha
        created_date = created_at[:10] if created_at else "N/A"
        
        # Truncar ID de grabación
        recording_short = str(recording_id)[:8] if recording_id else "N/A"
        
        # Generar componentes
        status_badge = StatusBadge.render(status)
        priority_indicator = PriorityIndicator.render(priority)
        
        return f"""
        <div class="ticket-card">
            <div class="ticket-header">
                <span class="ticket-number">#{ticket_num}</span>
                {status_badge}
            </div>
            
            <div class="ticket-body">
                <div class="ticket-title">{title}</div>
                <div class="ticket-description">{description}</div>
                
                <div class="meta-grid">
                    <div class="meta-item">
                        <span class="meta-label">Prioridad</span>
                        <span class="meta-value">{priority_indicator}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Creado</span>
                        <span class="meta-value">{created_date}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Grabación</span>
                        <span class="meta-value" title="{recording_id}">{recording_short}...</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Ticket ID</span>
                        <span class="meta-value">#{ticket_num}</span>
                    </div>
                </div>
                
                <div style="margin-top: var(--space-3); padding-top: var(--space-3); border-top: 1px solid var(--border);">
                    <span style="color: var(--text-tertiary); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Notas</span>
                    <p style="color: var(--text-secondary); font-size: 0.85rem; margin-top: var(--space-2); line-height: 1.6;">
                        {notes if notes else '<span style="color: var(--text-disabled);">Sin notas registradas</span>'}
                    </p>
                </div>
            </div>
        </div>
        """


# ----------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE INICIALIZACIÓN
# ----------------------------------------------------------------------------

def init_design_system(theme: str = "dark") -> None:
    """
    Inicializa el sistema de diseño completo
    """
    st.markdown(generate_global_styles(theme), unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# EJEMPLO DE USO
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    # Ejemplo de cómo usar en Streamlit
    st.set_page_config(page_title="Dashboard Moderno", layout="wide")
    
    # Inicializar diseño
    init_design_system(theme="dark")
    
    # Título
    st.title("Dashboard de Tickets")
    
    # Ejemplo de tarjeta
    card = TicketCardFactory.create(
        ticket_num="479",
        title="[IA] Infraestructura - Jaime",
        description="Estimamos que necesitamos unos $75,000 para invertir en nuevas herramientas en software.",
        status="new",
        priority="Low",
        created_at="2026-02-13",
        recording_id="39856553-09d2-46f8-9b88-04fde06cc561",
        notes="hola | ✨ Tema: Infraestructura | 🏠 Descripción: Recursos tecnológicos, herramientas, sistemas"
    )
    
    st.markdown(card, unsafe_allow_html=True)