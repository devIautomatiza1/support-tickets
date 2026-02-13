"""
Sistema de diseño profesional para el Dashboard de Tickets.
Gestiona temas, colores y componentes de UI de forma centralizada.
"""

import streamlit as st
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple


# ============================================================================
# DEFINICIÓN DE TEMAS Y COLORES
# ============================================================================

class ColorScheme:
    """Esquema de colores del dashboard"""
    
    # Fondos
    BG_PRIMARY = "#0A0C10"
    BG_SECONDARY = "#111316"
    BG_CARD = "#16181C"
    
    # Bordes
    BORDER = "#2A2C30"
    BORDER_HOVER = "#404448"
    
    # Texto
    TEXT_PRIMARY = "#E8E9EA"
    TEXT_SECONDARY = "#8B8E94"
    TEXT_TERTIARY = "#5E6269"
    
    # Estados
    ACCENT = "#3B82F6"
    ACCENT_SOFT = "rgba(59, 130, 246, 0.1)"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    
    # Componentes
    BADGE_NEW = "rgba(239,68,68,0.08)"
    BADGE_NEW_TEXT = "#F87171"
    BADGE_PROGRESS = "rgba(245,158,11,0.08)"
    BADGE_PROGRESS_TEXT = "#FBBF24"
    BADGE_WON = "rgba(16,185,129,0.08)"
    BADGE_WON_TEXT = "#34D399"
    BADGE_CLOSED = "rgba(107,114,128,0.08)"
    BADGE_CLOSED_TEXT = "#9CA3AF"


@dataclass
class StatusColor:
    """Colores para estados de tickets"""
    bg: str
    color: str
    border: str = None
    
    def __post_init__(self):
        if self.border is None:
            self.border = "rgba(0, 0, 0, 0.2)"


class StatusColors:
    """Paleta de colores para estados"""
    
    NEW = StatusColor(
        bg="rgba(239,68,68,0.08)",
        color="#F87171",
        border="rgba(239,68,68,0.2)"
    )
    IN_PROGRESS = StatusColor(
        bg="rgba(245,158,11,0.08)",
        color="#FBBF24",
        border="rgba(245,158,11,0.2)"
    )
    WON = StatusColor(
        bg="rgba(16,185,129,0.08)",
        color="#34D399",
        border="rgba(16,185,129,0.2)"
    )
    CLOSED = StatusColor(
        bg="rgba(107,114,128,0.08)",
        color="#9CA3AF",
        border="rgba(107,114,128,0.2)"
    )


class PriorityColors:
    """Paleta de colores para prioridades"""
    
    LOW = StatusColor(
        bg="rgba(16,185,129,0.08)",
        color="#34D399",
        border="rgba(16,185,129,0.2)"
    )
    MEDIUM = StatusColor(
        bg="rgba(245,158,11,0.08)",
        color="#FBBF24",
        border="rgba(245,158,11,0.2)"
    )
    HIGH = StatusColor(
        bg="rgba(239,68,68,0.08)",
        color="#F87171",
        border="rgba(239,68,68,0.2)"
    )


# ============================================================================
# GESTIÓN DE ESTILOS CSS
# ============================================================================

class CSSTokens:
    """Tokens de diseño centralizados"""
    
    RADIUS_LG = "16px"
    RADIUS_MD = "12px"
    RADIUS_SM = "8px"
    
    SHADOW = "0 20px 40px -12px rgba(0,0,0,0.4)"
    SHADOW_HOVER = "0 25px 50px -12px rgba(59,130,246,0.3)"
    
    TRANSITION = "all 0.2s ease"


class StyleManager:
    """Gestor centralizado de estilos CSS"""
    
    @staticmethod
    @st.cache_data
    def get_base_css() -> str:
        """CSS base del aplicación"""
        return f"""
        <style>
            :root {{
                --bg-primary: {ColorScheme.BG_PRIMARY};
                --bg-secondary: {ColorScheme.BG_SECONDARY};
                --bg-card: {ColorScheme.BG_CARD};
                --border: {ColorScheme.BORDER};
                --border-hover: {ColorScheme.BORDER_HOVER};
                --text-primary: {ColorScheme.TEXT_PRIMARY};
                --text-secondary: {ColorScheme.TEXT_SECONDARY};
                --text-tertiary: {ColorScheme.TEXT_TERTIARY};
                --accent: {ColorScheme.ACCENT};
                --accent-soft: {ColorScheme.ACCENT_SOFT};
                --success: {ColorScheme.SUCCESS};
                --warning: {ColorScheme.WARNING};
                --danger: {ColorScheme.DANGER};
                --radius-lg: {CSSTokens.RADIUS_LG};
                --radius-md: {CSSTokens.RADIUS_MD};
                --radius-sm: {CSSTokens.RADIUS_SM};
                --shadow: {CSSTokens.SHADOW};
                --shadow-hover: {CSSTokens.SHADOW_HOVER};
                --transition: {CSSTokens.TRANSITION};
            }}

            [data-testid="stAppViewContainer"] {{ 
                background: var(--bg-primary); 
            }}
            
            [data-testid="stSidebar"] {{ 
                background: var(--bg-secondary); 
                border-right: 1px solid var(--border); 
            }}

            div.row-widget.stHorizontal {{
                gap: 0.75rem;
                flex-wrap: wrap;
            }}

            hr {{
                border: none;
                height: 1px;
                background: var(--border);
                margin: 1rem 0;
            }}
        </style>
        """
    
    @staticmethod
    @st.cache_data
    def get_card_css() -> str:
        """CSS para tarjetas"""
        return """
        <style>
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
        </style>
        """
    
    @staticmethod
    @st.cache_data
    def get_badge_css() -> str:
        """CSS para badges"""
        return """
        <style>
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
        </style>
        """
    
    @staticmethod
    @st.cache_data
    def get_modal_css() -> str:
        """CSS para modales"""
        return """
        <style>
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

            .description-section {
                margin-bottom: 1.25rem;
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

            .status-priority-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin-bottom: 1.25rem;
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
        </style>
        """
    
    @staticmethod
    @st.cache_data
    def get_input_css() -> str:
        """CSS para inputs y controles"""
        return """
        <style>
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
            
            .stTextArea {
                margin-top: 0.25rem;
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
            
            .stTextArea textarea:hover {
                border-color: var(--border-hover) !important;
            }
            
            .stTextArea textarea:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
            }
        </style>
        """
    
    @staticmethod
    @st.cache_data
    def get_button_css() -> str:
        """CSS para botones"""
        return """
        <style>
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
            
            .stButton > button:active {
                transform: translateY(0) !important;
            }
            
            .stButton > button[key*="ACTUALIZAR"] {
                background: transparent !important;
                border: 1px solid var(--border) !important;
                padding: 0.5rem 1rem !important;
                font-size: 0.8rem !important;
            }
            
            .stButton > button[key*="ACTUALIZAR"]:hover {
                background: var(--accent) !important;
                border-color: var(--accent) !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
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
            
            .stButton > button[kind="primary"]:active {
                transform: translateY(0) !important;
                box-shadow: 0 2px 8px rgba(59,130,246,0.2) !important;
            }
            
            .stButton > button:not([kind="primary"]) {
                background: transparent !important;
                color: var(--text-secondary) !important;
                border: 1px solid var(--border) !important;
            }
            
            .stButton > button:not([kind="primary"]):hover {
                background: var(--bg-secondary) !important;
                border-color: var(--border-hover) !important;
                color: var(--text-primary) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
            }
        </style>
        """
    
    @staticmethod
    @st.cache_data
    def get_metric_css() -> str:
        """CSS para métricas"""
        return """
        <style>
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
            
            [data-testid="metric-container"] label {
                font-size: 0.6rem !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-value"] {
                font-size: 1.1rem !important;
            }

            .streamlit-expanderHeader {
                background: var(--bg-card) !important;
                border: 1px solid var(--border) !important;
                border-radius: 8px !important;
                transition: var(--transition) !important;
            }
            
            .streamlit-expanderHeader:hover {
                border-color: var(--border-hover) !important;
                background: var(--bg-secondary) !important;
            }
        </style>
        """
    
    @staticmethod
    def inject_all():
        """Inyecta todos los estilos CSS"""
        css_parts = [
            StyleManager.get_base_css(),
            StyleManager.get_card_css(),
            StyleManager.get_badge_css(),
            StyleManager.get_modal_css(),
            StyleManager.get_input_css(),
            StyleManager.get_button_css(),
            StyleManager.get_metric_css(),
        ]
        
        for css in css_parts:
            st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# UTILIDADES DE ESTILO
# ============================================================================

class ComponentStyles:
    """Estilos predefinidos para componentes específicos"""
    
    @staticmethod
    def render_status_badge(status: str, label: str) -> str:
        """Renderiza un badge de estado"""
        badge_classes = {
            "new": "badge-new",
            "in_progress": "badge-progress",
            "won": "badge-won",
            "closed": "badge-closed"
        }
        badge_class = badge_classes.get(status, "badge-new")
        return f'<span class="badge {badge_class}">{label}</span>'
    
    @staticmethod
    def render_colored_value(bg: str, color: str, text: str) -> str:
        """Renderiza un valor con colores personalizados"""
        return f'<span class="current-value" style="background: {bg}; color: {color};">{text}</span>'
    
    @staticmethod
    def render_info_card(label: str, content: str) -> str:
        """Renderiza una tarjeta de información"""
        return f"""
        <div class="info-card">
            <div class="info-label">{label}</div>
            {content}
        </div>
        """
