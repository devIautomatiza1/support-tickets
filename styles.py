# ============================================================================
# CONFIGURACIÓN DE ESTILOS Y TEMAS - VERSIÓN FINAL
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
    radius_xxl: str = "1.25rem"  # 20px
    radius_full: str = "9999px"
    
    # Shadows
    shadow_sm: str = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    shadow_md: str = "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
    shadow_lg: str = "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
    shadow_xl: str = "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
    shadow_hover: str = "0 25px 50px -12px rgba(59, 130, 246, 0.3)"
    
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
# GENERADOR DE CSS MODERNO - VERSIÓN COMPLETA
# ----------------------------------------------------------------------------

def generate_global_styles(theme: str = "dark") -> str:
    """Genera CSS moderno con todos los estilos optimizados"""
    
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
            --radius-xxl: {TOKENS.radius_xxl};
            --radius-full: {TOKENS.radius_full};
            
            /* Shadows */
            --shadow-sm: {TOKENS.shadow_sm};
            --shadow-md: {TOKENS.shadow_md};
            --shadow-lg: {TOKENS.shadow_lg};
            --shadow-xl: {TOKENS.shadow_xl};
            --shadow-hover: {TOKENS.shadow_hover};
            
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
           GRID DE TARJETAS
        ------------------------------------------------------------------ */
        div.row-widget.stHorizontal {{
            gap: 0.75rem;
            flex-wrap: wrap;
        }}
        
        /* ------------------------------------------------------------------
           TARJETAS COMPACTAS
        ------------------------------------------------------------------ */
        .ticket-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 0.85rem;
            transition: var(--transition-base);
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        .ticket-card:hover {{
            border-color: var(--border-hover);
            box-shadow: 0 6px 16px rgba(0,0,0,0.4);
            transform: translateY(-2px);
            background: linear-gradient(145deg, var(--bg-card), #1A1E24);
        }}
        
        .ticket-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.4rem;
        }}
        
        .ticket-number {{
            font-family: var(--font-mono);
            font-size: 0.65rem;
            font-weight: 500;
            color: var(--text-tertiary);
            letter-spacing: 0.02em;
        }}
        
        .ticket-title {{
            font-size: 0.8rem;
            font-weight: 450;
            color: var(--text-primary);
            line-height: 1.3;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 2rem;
        }}
        
        /* ------------------------------------------------------------------
           BADGES MINIMALISTAS
        ------------------------------------------------------------------ */
        .badge {{
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
        }}
        
        .badge-new {{ 
            background: rgba(239,68,68,0.08); 
            color: #F87171; 
            border-color: rgba(239,68,68,0.2); 
        }}
        
        .badge-progress {{ 
            background: rgba(245,158,11,0.08); 
            color: #FBBF24; 
            border-color: rgba(245,158,11,0.2); 
        }}
        
        .badge-won {{ 
            background: rgba(16,185,129,0.08); 
            color: #34D399; 
            border-color: rgba(16,185,129,0.2); 
        }}
        
        .badge-closed {{ 
            background: rgba(107,114,128,0.08); 
            color: #9CA3AF; 
            border-color: rgba(107,114,128,0.2); 
        }}
        
        /* ------------------------------------------------------------------
           MODAL CENTRADO
        ------------------------------------------------------------------ */
        div[data-testid="stDialog"] {{
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 1rem 0 !important;
        }}
        
        div[data-testid="stDialog"] > div {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 20px !important;
            padding: 1.5rem 1.75rem !important;
            box-shadow: var(--shadow-xl) !important;
            max-width: 600px !important;
            width: 100% !important;
            margin: 0 auto !important;
            max-height: 90vh !important;
            overflow-y: auto !important;
        }}
        
        div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2 {{
            display: none !important;
        }}
        
        /* ------------------------------------------------------------------
           MODAL HEADER
        ------------------------------------------------------------------ */
        .modal-header {{
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.75rem;
        }}
        
        .modal-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text-primary);
            line-height: 1.3;
            letter-spacing: -0.02em;
        }}
        
        .modal-date {{
            font-size: 0.75rem;
            color: var(--text-tertiary);
            font-family: var(--font-mono);
            background: var(--bg-secondary);
            padding: 0.2rem 0.6rem;
            border-radius: 16px;
            border: 1px solid var(--border);
        }}
        
        /* ------------------------------------------------------------------
           DESCRIPCIÓN
        ------------------------------------------------------------------ */
        .section-title {{
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .description-box {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.9rem 1rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
            line-height: 1.5;
            white-space: pre-wrap;
        }}
        
        /* ------------------------------------------------------------------
           ESTADO Y PRIORIDAD
        ------------------------------------------------------------------ */
        .status-priority-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .info-card {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 0.9rem;
            border: 1px solid var(--border);
        }}
        
        .info-label {{
            font-size: 0.6rem;
            font-weight: 600;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
        }}
        
        .current-value {{
            display: inline-block;
            padding: 0.2rem 0.75rem;
            border-radius: 16px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }}
        
        .select-label {{
            font-size: 0.6rem;
            color: var(--text-tertiary);
            margin-bottom: 0.2rem;
        }}
        
        /* ------------------------------------------------------------------
           SELECT BOXES
        ------------------------------------------------------------------ */
        .stSelectbox {{
            margin-bottom: 0.25rem !important;
        }}
        
        .stSelectbox [data-baseweb="select"] {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            min-height: 2rem !important;
            transition: var(--transition-base) !important;
        }}
        
        .stSelectbox [data-baseweb="select"]:hover {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px {TOKENS.primary_500}20 !important;
        }}
        
        /* ------------------------------------------------------------------
           TEXT AREA
        ------------------------------------------------------------------ */
        .stTextArea {{
            margin-top: 0.25rem;
        }}
        
        .stTextArea textarea {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            font-size: 0.8rem !important;
            line-height: 1.5 !important;
            padding: 0.75rem !important;
            min-height: 120px !important;
            max-height: 150px !important;
            font-family: var(--font-mono) !important;
            transition: var(--transition-base) !important;
        }}
        
        .stTextArea textarea:hover {{
            border-color: var(--border-hover) !important;
        }}
        
        .stTextArea textarea:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px {TOKENS.primary_500}20 !important;
        }}
        
        /* ------------------------------------------------------------------
           BOTONES CON HOVER MEJORADOS
        ------------------------------------------------------------------ */
        .stButton > button {{
            border-radius: 8px !important;
            font-size: 0.75rem !important;
            padding: 0.35rem 0.75rem !important;
            transition: var(--transition-base) !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            width: 100% !important;
            background: transparent !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border) !important;
            position: relative !important;
            overflow: hidden !important;
        }}
        
        .stButton > button:hover {{
            background: var(--primary-soft) !important;
            border-color: var(--primary) !important;
            color: var(--primary) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px {TOKENS.primary_500}30 !important;
        }}
        
        .stButton > button:active {{
            transform: translateY(0) !important;
        }}
        
        /* Botón ACTUALIZAR */
        .stButton > button[key*="ACTUALIZAR"] {{
            background: transparent !important;
            border: 1px solid var(--border) !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.8rem !important;
        }}
        
        .stButton > button[key*="ACTUALIZAR"]:hover {{
            background: var(--primary) !important;
            border-color: var(--primary) !important;
            color: white !important;
            box-shadow: 0 4px 12px {TOKENS.primary_500}40 !important;
        }}
        
        /* Botón Guardar (primario) */
        .stButton > button[kind="primary"] {{
            background: var(--primary) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 2px 8px {TOKENS.primary_500}30 !important;
        }}
        
        .stButton > button[kind="primary"]:hover {{
            background: var(--primary-hover) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px {TOKENS.primary_500}50 !important;
        }}
        
        /* Botón Cancelar */
        .stButton > button:not([kind="primary"]) {{
            background: transparent !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border) !important;
        }}
        
        .stButton > button:not([kind="primary"]):hover {{
            background: var(--bg-secondary) !important;
            border-color: var(--border-hover) !important;
            color: var(--text-primary) !important;
        }}
        
        /* ------------------------------------------------------------------
           MÉTRICAS
        ------------------------------------------------------------------ */
        [data-testid="metric-container"] {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.6rem;
            transition: var(--transition-base) !important;
        }}
        
        [data-testid="metric-container"]:hover {{
            border-color: var(--border-hover) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        }}
        
        [data-testid="metric-container"] label {{
            color: var(--text-tertiary) !important;
            font-size: 0.6rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        [data-testid="metric-container"] [data-testid="metric-value"] {{
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }}
        
        /* ------------------------------------------------------------------
           EXPANDER
        ------------------------------------------------------------------ */
        .streamlit-expanderHeader {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            transition: var(--transition-base) !important;
        }}
        
        .streamlit-expanderHeader:hover {{
            border-color: var(--border-hover) !important;
            background: var(--bg-secondary) !important;
        }}
        
        /* ------------------------------------------------------------------
           DIVIDER
        ------------------------------------------------------------------ */
        hr {{
            border: none;
            height: 1px;
            background: var(--border);
            margin: 1rem 0;
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
# FUNCIÓN PRINCIPAL DE INICIALIZACIÓN
# ----------------------------------------------------------------------------

def init_design_system(theme: str = "dark") -> None:
    """
    Inicializa el sistema de diseño completo
    """
    st.markdown(generate_global_styles(theme), unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# COMPONENTES REUTILIZABLES (OPCIONALES - Comenta si no los usas)
# ----------------------------------------------------------------------------

class StatusBadge:
    """Componente de badge de estado"""
    
    STATUS_CONFIG = {
        "new": {"class": "badge-new", "label": "NUEVO", "icon": ""},
        "in_progress": {"class": "badge-progress", "label": "PROGRESO", "icon": ""},
        "won": {"class": "badge-won", "label": "GANADO", "icon": ""},
        "closed": {"class": "badge-closed", "label": "CERRADO", "icon": ""},
    }
    
    @classmethod
    def render(cls, status: str) -> str:
        config = cls.STATUS_CONFIG.get(status, cls.STATUS_CONFIG["new"])
        return f'<span class="badge {config["class"]}">{config["label"]}</span>'


class PriorityIndicator:
    """Indicador de prioridad minimalista"""
    
    PRIORITY_CONFIG = {
        "High": {"color": "#F87171", "label": "Alta"},
        "Medium": {"color": "#FBBF24", "label": "Media"},
        "Low": {"color": "#34D399", "label": "Baja"},
    }
    
    @classmethod
    def render(cls, priority: str) -> str:
        config = cls.PRIORITY_CONFIG.get(priority, cls.PRIORITY_CONFIG["Medium"])
        return f'<span style="color: {config["color"]}; font-weight: 600;">{config["label"]}</span>'