"""
Sistema de diseño profesional para el Dashboard de Tickets.
Gestiona temas, colores y componentes de UI de forma centralizada.
Integración con Bootstrap 5 y estilos avanzados de nivel enterprise.
"""

import streamlit as st
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple
import json


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
    @st.cache_data
    def get_advanced_css() -> str:
        """Estilos avanzados con diseño profesional de nivel enterprise"""
        return """
        <style>
            /* ===== ANIMACIONES ===== */
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes glow {
                0%, 100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.5); }
                50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.8); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.8; }
            }

            /* ===== CONTEXTO GENERAL ===== */
            * {
                scrollbar-width: thin;
                scrollbar-color: var(--accent) var(--bg-secondary);
            }
            
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--bg-secondary);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--accent);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--accent-soft);
            }

            /* ===== ENHANCED CARD STYLES ===== */
            .ticket-card {
                animation: slideIn 0.3s ease-out;
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
            }
            
            .ticket-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255, 255, 255, 0.1),
                    transparent
                );
                transition: left 0.5s;
            }
            
            .ticket-card:hover::before {
                left: 100%;
            }

            /* ===== BADGE ENHANCEMENTS ===== */
            .badge {
                animation: fadeIn 0.3s ease-out;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                backdrop-filter: blur(8px);
            }
            
            .badge-new {
                box-shadow: 0 0 15px rgba(240, 113, 113, 0.3) !important;
            }
            
            .badge-progress {
                box-shadow: 0 0 15px rgba(250, 190, 36, 0.3) !important;
            }
            
            .badge-won {
                box-shadow: 0 0 15px rgba(52, 211, 153, 0.3) !important;
            }
            
            .badge-closed {
                box-shadow: 0 0 15px rgba(156, 163, 175, 0.3) !important;
            }

            /* ===== PROFESSIONAL SHADOWS ===== */
            .menu-item {
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            
            .profile-section {
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            }

            /* ===== ENHANCED MODALS ===== */
            div[data-testid="stDialog"] > div {
                animation: slideIn 0.3s ease-out;
                backdrop-filter: blur(20px);
                background: linear-gradient(135deg, var(--bg-card), rgba(22, 24, 28, 0.8));
            }
            
            .modal-header {
                background: linear-gradient(90deg, var(--bg-secondary), var(--bg-card));
                border-radius: 12px 12px 0 0;
                margin: -1.5rem -1.75rem 1rem;
                padding: 1rem 1.75rem;
                border-bottom: 2px solid var(--accent);
            }
            
            .modal-title {
                background: linear-gradient(90deg, var(--text-primary), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
            }

            /* ===== ENHANCED INFO CARDS ===== */
            .info-card {
                transition: var(--transition);
                border-left: 3px solid var(--accent);
                background: linear-gradient(135deg, var(--bg-secondary), rgba(22, 24, 28, 0.5));
            }
            
            .info-card:hover {
                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
                transform: translateX(4px);
            }

            /* ===== ENHANCED INPUTS ===== */
            .stSelectbox [data-baseweb="select"] {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            }
            
            .stSelectbox [data-baseweb="select"]:focus-within {
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25), 
                            0 4px 12px rgba(59, 130, 246, 0.15) !important;
                transform: translateY(-2px);
            }
            
            .stTextArea textarea {
                transition: all 0.3s ease !important;
                resize: vertical !important;
            }
            
            .stTextArea textarea:focus {
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25),
                            0 8px 16px rgba(59, 130, 246, 0.15) !important;
            }

            /* ===== ENHANCED BUTTONS ===== */
            .stButton > button {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                position: relative;
                overflow: hidden;
            }
            
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.1);
                transition: left 0.5s;
                z-index: 0;
            }
            
            .stButton > button:hover::before {
                left: 100%;
            }
            
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, var(--accent), #2563EB) !important;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
            }
            
            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #2563EB, #1d4ed8) !important;
                box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important;
                transform: translateY(-3px) !important;
            }
            
            .stButton > button[kind="primary"]:active {
                transform: translateY(-1px) !important;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
            }

            /* ===== ENHANCED METRICS ===== */
            [data-testid="metric-container"] {
                background: linear-gradient(135deg, var(--bg-card), rgba(22, 24, 28, 0.5));
                border-left: 3px solid var(--accent);
                transition: all 0.3s ease;
            }
            
            [data-testid="metric-container"]:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 32px rgba(59, 130, 246, 0.2) !important;
            }

            /* ===== DIVIDER ENHANCEMENT ===== */
            hr {
                background: linear-gradient(90deg, transparent, var(--border), transparent);
                opacity: 0.6;
                margin: 1.5rem 0;
            }

            /* ===== TITLE ENHANCEMENTS ===== */
            [data-testid="stMarkdownContainer"] h1 {
                background: linear-gradient(90deg, var(--text-primary), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
                letter-spacing: -0.02em;
            }
            
            [data-testid="stMarkdownContainer"] h3 {
                font-weight: 500;
                letter-spacing: -0.01em;
            }

            /* ===== SIDEBAR ENHANCEMENTS ===== */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
            }

            /* ===== EXPANDER ENHANCEMENT ===== */
            .streamlit-expanderHeader {
                background: linear-gradient(90deg, var(--bg-card), rgba(22, 24, 28, 0.5));
                transition: all 0.3s ease;
            }
            
            .streamlit-expanderHeader:hover {
                background: linear-gradient(90deg, var(--bg-card), var(--bg-secondary)) !important;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
            }

            /* ===== PROFESSIONAL TEXT STYLES ===== */
            .section-title {
                letter-spacing: 0.1em;
                font-weight: 600;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .description-box {
                background: linear-gradient(135deg, var(--bg-secondary), rgba(22, 24, 28, 0.3));
                border-left: 3px solid var(--accent);
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            /* ===== RESPONSIVE DESIGN ===== */
            @media (max-width: 768px) {
                .ticket-card {
                    padding: 0.6rem;
                }
                
                .modal-title {
                    font-size: 1rem;
                }
                
                [data-testid="metric-container"] {
                    padding: 0.5rem !important;
                }
            }

            /* ===== ACCESSIBILITY ===== */
            button:focus-visible,
            input:focus-visible,
            select:focus-visible,
            textarea:focus-visible {
                outline: 2px solid var(--accent);
                outline-offset: 2px;
            }

            /* ===== TRANSITION SMOOTHNESS ===== */
            * {
                transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
            }
        </style>
        """
        """Inyecta todos los estilos CSS incluyendo Bootstrap y estilos avanzados"""
        # Bootstrap 5 CDN
        st.markdown("""
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        """, unsafe_allow_html=True)
        
        css_parts = [
            StyleManager.get_base_css(),
            StyleManager.get_card_css(),
            StyleManager.get_badge_css(),
            StyleManager.get_modal_css(),
            StyleManager.get_input_css(),
            StyleManager.get_button_css(),
            StyleManager.get_metric_css(),
            StyleManager.get_advanced_css(),
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
        """Renderiza un badge de estado profesional"""
        badge_classes = {
            "new": "badge-new",
            "in_progress": "badge-progress",
            "won": "badge-won",
            "closed": "badge-closed"
        }
        badge_class = badge_classes.get(status, "badge-new")
        icons = {
            "new": "🆕",
            "in_progress": "⏳",
            "won": "✅",
            "closed": "🔒"
        }
        icon = icons.get(status, "")
        return f'<span class="badge {badge_class}">{icon} {label}</span>'
    
    @staticmethod
    def render_colored_value(bg: str, color: str, text: str) -> str:
        """Renderiza un valor con colores personalizados y efectos"""
        return f'''
        <span class="current-value" style="
            background: {bg}; 
            color: {color};
            box-shadow: 0 2px 8px {bg};
            font-weight: 600;
        ">{text}</span>
        '''
    
    @staticmethod
    def render_info_card(label: str, content: str, icon: str = "ℹ️") -> str:
        """Renderiza una tarjeta de información profesional"""
        return f"""
        <div class="info-card">
            <div class="info-label">
                <span style="margin-right: 0.5rem;">{icon}</span>{label}
            </div>
            {content}
        </div>
        """
    
    @staticmethod
    def render_stat_card(title: str, value: str, change: str = "", 
                        trend_positive: bool = True) -> str:
        """Renderiza una tarjeta de estadística profesional"""
        trend_icon = "📈" if trend_positive else "📉"
        trend_color = "#34D399" if trend_positive else "#F87171"
        
        return f"""
        <div style="
            background: linear-gradient(135deg, var(--bg-card), rgba(22, 24, 28, 0.5));
            border-radius: 12px;
            padding: 1.2rem;
            border-left: 4px solid var(--accent);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
        " onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 12px 32px rgba(59, 130, 246, 0.2)';"
           onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none';">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.75rem; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                        {title}
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary);">
                        {value}
                    </div>
                </div>
                <div style="font-size: 1.5rem; color: {trend_color}; opacity: 0.8;">
                    {trend_icon}
                </div>
            </div>
            {f'<div style="margin-top: 0.75rem; font-size: 0.85rem; color: {trend_color};">{change}</div>' if change else ''}
        </div>
        """
    
    @staticmethod
    def render_section_label(label: str, icon: str = "▪") -> str:
        """Renderiza un label de sección profesional"""
        return f"""
        <div style="
            padding: 0.75rem 1rem;
            background: linear-gradient(90deg, var(--accent), transparent);
            border-radius: 8px;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        ">
            <span style="
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: var(--text-primary);
            ">{icon} {label}</span>
        </div>
        """

    @staticmethod
    def render_gradient_separator() -> str:
        """Renderiza un separador con gradiente"""
        return """
        <div style="
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            margin: 1.5rem 0;
            border-radius: 1px;
        "></div>
        """


class ThemeManager:
    """Gestor de temas intercambiables"""
    
    @staticmethod
    def get_dark_theme() -> Dict[str, str]:
        """Tema oscuro (predeterminado)"""
        return {
            "primary": ColorScheme.ACCENT,
            "background": ColorScheme.BG_PRIMARY,
            "surface": ColorScheme.BG_CARD,
            "text_primary": ColorScheme.TEXT_PRIMARY,
            "text_secondary": ColorScheme.TEXT_SECONDARY,
        }
    
    @staticmethod
    def apply_theme(theme_name: str = "dark"):
        """Aplica un tema"""
        themes = {
            "dark": ThemeManager.get_dark_theme(),
        }
        return themes.get(theme_name, themes["dark"])


class BootstrapIntegration:
    """Utilidades para integrar Bootstrap 5"""
    
    @staticmethod
    def button_primary(text: str) -> str:
        """Genera un botón Bootstrap primario"""
        return f'<button class="btn btn-primary" style="width: 100%;">{text}</button>'
    
    @staticmethod
    def button_secondary(text: str) -> str:
        """Genera un botón Bootstrap secundario"""
        return f'<button class="btn btn-outline-secondary" style="width: 100%;">{text}</button>'
    
    @staticmethod
    def alert_success(message: str, icon: str = "✓") -> str:
        """Alerta de éxito con Bootstrap"""
        return f"""
        <div class="alert alert-success alert-dismissible fade show" role="alert" style="
            border-left: 4px solid #34D399;
            background: rgba(52, 211, 153, 0.1);
            color: #34D399;
        ">
            <strong>{icon} Éxito:</strong> {message}
        </div>
        """
    
    @staticmethod
    def alert_error(message: str, icon: str = "✕") -> str:
        """Alerta de error con Bootstrap"""
        return f"""
        <div class="alert alert-danger alert-dismissible fade show" role="alert" style="
            border-left: 4px solid #F87171;
            background: rgba(248, 113, 113, 0.1);
            color: #F87171;
        ">
            <strong>{icon} Error:</strong> {message}
        </div>
        """
    
    @staticmethod
    def card(title: str, content: str, footer: str = "") -> str:
        """Tarjeta Bootstrap profesional"""
        footer_html = f'<div class="card-footer">{footer}</div>' if footer else ''
        return f"""
        <div class="card" style="
            border: 1px solid var(--border);
            background: var(--bg-card);
            color: var(--text-primary);
        ">
            <div class="card-header" style="
                background: linear-gradient(90deg, var(--bg-secondary), var(--bg-card));
                border-bottom: 2px solid var(--accent);
            ">
                <h5 class="card-title" style="margin: 0; color: var(--text-primary);">{title}</h5>
            </div>
            <div class="card-body">
                {content}
            </div>
            {footer_html}
        </div>
        """

