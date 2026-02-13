"""
Sistema de estilos HERMOSO - Diseño SaaS Premium tipo Linear/Vercel.
"""

import streamlit as st


class StyleManager:
    """Gestor maestro de estilos - Diseño premium"""
    
    @staticmethod
    @st.cache_data
    def inject_all():
        """Inyecta CSS HERMOSO y profesional"""
        st.markdown("""
        <link href="https://cdn.tailwindcss.com" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --bg-dark: #0a0c12;
                --bg-secondary: #0f1117;
                --bg-tertiary: #1a1c23;
                --accent: #3b82f6;
                --accent-light: #60a5fa;
                --accent-dark: #2563eb;
                --text-primary: #f8fafc;
                --text-secondary: #e2e8f0;
                --text-muted: #94a3b8;
                --border: rgba(255, 255, 255, 0.08);
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
            }

            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            html, body, [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at 20% 30%, #0f1117, #0a0c12);
                color: var(--text-primary);
            }

            /* ===== SIDEBAR ===== */
            [data-testid="stSidebar"] {
                background: rgba(10, 12, 18, 0.8) !important;
                backdrop-filter: blur(20px) !important;
                border-right: 1px solid var(--border) !important;
            }

            /* ===== TARJETAS DE TICKETS ===== */
            .premium-ticket-card {
                background: linear-gradient(145deg, rgba(26, 28, 35, 0.6), rgba(26, 28, 35, 0.4));
                backdrop-filter: blur(16px);
                border: 1.5px solid rgba(59, 130, 246, 0.15);
                border-radius: 20px;
                padding: 1.25rem;
                transition: all 0.3s ease;
                position: relative;
                overflow: visible;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            }

            .premium-ticket-card:hover {
                border-color: rgba(59, 130, 246, 0.4);
                background: linear-gradient(145deg, rgba(26, 28, 35, 0.8), rgba(26, 28, 35, 0.6));
                box-shadow: 0 12px 48px rgba(59, 130, 246, 0.25);
                transform: translateY(-2px);
            }

            .ticket-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 0.75rem;
                position: relative;
            }

            .ticket-header-left {
                flex: 1;
            }

            .ticket-number {
                font-size: 0.75rem;
                font-weight: 700;
                color: var(--text-muted);
                font-family: 'SF Mono', 'Monaco', monospace;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            .ticket-title {
                font-size: 1rem;
                font-weight: 700;
                color: var(--text-primary);
                margin: 0.5rem 0 0 0;
                line-height: 1.35;
            }

            .ticket-person {
                font-size: 0.8rem;
                color: var(--accent-light);
                margin-top: 0.5rem;
                margin-bottom: 0.75rem;
                font-weight: 500;
            }

            .ticket-description {
                font-size: 0.85rem;
                color: var(--text-muted);
                line-height: 1.5;
                margin-bottom: 1rem;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }

            .ticket-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 0.75rem;
                font-size: 0.75rem;
                color: var(--text-muted);
            }

            /* ===== BADGES ===== */
            .badge {
                display: inline-flex;
                align-items: center;
                padding: 0.25rem 0.75rem;
                border-radius: 30px;
                font-size: 0.7rem;
                font-weight: 600;
                border: 1.5px solid;
            }

            .badge-new {
                background: rgba(239, 68, 68, 0.1);
                border-color: rgba(239, 68, 68, 0.3);
                color: #ff8b8e;
            }

            .badge-in-progress {
                background: rgba(245, 158, 11, 0.1);
                border-color: rgba(245, 158, 11, 0.3);
                color: #fbb040;
            }

            .badge-won {
                background: rgba(16, 185, 129, 0.1);
                border-color: rgba(16, 185, 129, 0.3);
                color: #2dd4a4;
            }

            .badge-closed {
                background: rgba(100, 116, 139, 0.1);
                border-color: rgba(100, 116, 139, 0.3);
                color: #cbd5e1;
            }

            .badge-sm {
                display: inline-flex;
                align-items: center;
                padding: 0.35rem 0.85rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                border: 1.2px solid;
                white-space: nowrap;
            }

            /* ===== STAT CARDS ===== */
            .stat-card-premium {
                background: linear-gradient(145deg, rgba(37, 99, 235, 0.1), rgba(37, 99, 235, 0.05));
                backdrop-filter: blur(16px);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 16px;
                padding: 1.25rem;
                transition: all 0.3s ease;
            }

            .stat-card-premium:hover {
                background: linear-gradient(145deg, rgba(37, 99, 235, 0.15), rgba(37, 99, 235, 0.08));
                border-color: rgba(59, 130, 246, 0.3);
                transform: translateY(-2px);
            }

            .stat-label {
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                color: var(--text-muted);
                margin-bottom: 0.5rem;
            }

            .stat-value {
                font-size: 1.75rem;
                font-weight: 800;
                background: linear-gradient(135deg, var(--accent-light), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            /* ===== HEADER HERO ===== */
            .header-hero-premium {
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(37, 99, 235, 0.05) 100%);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 24px;
                padding: 2rem;
                margin-bottom: 2rem;
            }

            .header-hero-premium h1 {
                color: white;
                margin: 0;
                font-size: 2rem;
            }

            .header-hero-premium p {
                color: rgba(255, 255, 255, 0.8);
                margin: 0.5rem 0 0 0;
            }

            /* ===== POPOVER GRANDE - CORREGIDO ===== */
            /* El contenedor principal del popover */
            div[data-testid="stPopover"] {
                background: transparent !important;
            }
            
            /* El contenido del popover */
            div[data-testid="stPopover"] > div:first-child {
                background: rgba(15, 17, 23, 0.98) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(59, 130, 246, 0.3) !important;
                border-radius: 24px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
                min-width: 650px !important;
                width: 650px !important;
                max-width: 650px !important;
                padding: 2rem !important;
                z-index: 999999 !important;
            }

            /* Título dentro del popover */
            div[data-testid="stPopover"] h3 {
                color: var(--text-primary) !important;
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                margin-bottom: 0.25rem !important;
            }

            /* Subtítulo (caption) */
            div[data-testid="stPopover"] .stCaption {
                color: var(--accent-light) !important;
                font-size: 1.2rem !important;
                margin-bottom: 1.5rem !important;
            }

            /* Divisor */
            div[data-testid="stPopover"] .stDivider {
                background: rgba(255, 255, 255, 0.1) !important;
                margin: 1.5rem 0 !important;
            }

            /* Labels */
            div[data-testid="stPopover"] label {
                color: var(--text-muted) !important;
                font-size: 0.9rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                margin-bottom: 0.5rem !important;
            }

            /* Selectboxes */
            div[data-testid="stPopover"] .stSelectbox {
                margin-bottom: 1.5rem !important;
            }

            div[data-testid="stPopover"] .stSelectbox > div {
                background: rgba(10, 12, 18, 0.9) !important;
                border: 1.5px solid var(--border) !important;
                border-radius: 14px !important;
                height: 55px !important;
                font-size: 1.1rem !important;
            }

            div[data-testid="stPopover"] .stSelectbox select {
                color: var(--text-primary) !important;
                font-size: 1.1rem !important;
                padding: 0 1rem !important;
            }

            /* TextArea */
            div[data-testid="stPopover"] .stTextArea {
                margin-bottom: 1.5rem !important;
            }

            div[data-testid="stPopover"] .stTextArea textarea {
                background: rgba(10, 12, 18, 0.9) !important;
                border: 1.5px solid var(--border) !important;
                border-radius: 14px !important;
                color: var(--text-primary) !important;
                font-size: 1.1rem !important;
                min-height: 150px !important;
                padding: 1rem !important;
                line-height: 1.5 !important;
            }

            /* Botón Guardar */
            div[data-testid="stPopover"] .stButton > button {
                background: linear-gradient(135deg, var(--accent), var(--accent-dark)) !important;
                border: none !important;
                color: white !important;
                font-weight: 600 !important;
                font-size: 1.2rem !important;
                border-radius: 14px !important;
                padding: 0.9rem 1.5rem !important;
                width: 100% !important;
                height: auto !important;
                margin-top: 1rem !important;
                transition: all 0.3s !important;
                box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3) !important;
            }

            div[data-testid="stPopover"] .stButton > button:hover {
                background: linear-gradient(135deg, var(--accent-light), var(--accent)) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.5) !important;
            }

            /* Botón de los tres puntos */
            .stPopoverEmoji {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid var(--border) !important;
                border-radius: 10px !important;
                padding: 0.5rem 0.9rem !important;
                color: var(--text-muted) !important;
                font-size: 1.2rem !important;
                cursor: pointer !important;
                transition: all 0.2s !important;
            }

            .stPopoverEmoji:hover {
                background: rgba(59, 130, 246, 0.15) !important;
                color: var(--accent-light) !important;
                border-color: rgba(59, 130, 246, 0.4) !important;
            }

            /* ===== BOTONES GENERALES ===== */
            .stButton > button {
                background: linear-gradient(135deg, var(--accent), var(--accent-dark)) !important;
                border: none !important;
                color: white !important;
                font-weight: 600 !important;
                border-radius: 10px !important;
                transition: all 0.3s !important;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, var(--accent-light), var(--accent)) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
            }

            /* ===== INPUTS GENERALES ===== */
            input, textarea, select {
                background: rgba(10, 12, 18, 0.6) !important;
                border: 1.5px solid var(--border) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
            }

            input:focus, textarea:focus, select:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
            }

            /* Eliminar estilos antiguos que interferían */
            [role="dialog"] {
                all: unset;
            }

            [data-testid="popoverContainer"] {
                all: unset;
            }
        </style>
        """, unsafe_allow_html=True)


class ComponentStyles:
    """Componentes renderizados"""
    
    @staticmethod
    def premium_ticket_card(ticket_number: str, title: str, description: str, status: str, priority: str, date: str, person: str = "") -> str:
        """Tarjeta de ticket minimalista SaaS con bordes sutiles"""
        status_map = {
            "new": "badge-new",
            "in_progress": "badge-in-progress",
            "won": "badge-won",
            "closed": "badge-closed"
        }
        
        status_display = {
            "new": "NUEVO",
            "in_progress": "EN PROGRESO",
            "won": "GANADO",
            "closed": "CERRADO"
        }
        
        badge_class = status_map.get(status, "badge-new")
        status_text = status_display.get(status, "NUEVO")
        
        return f"""
        <div class="premium-ticket-card">
            <div class="ticket-header">
                <div class="ticket-header-left">
                    <span class="ticket-number">#{ticket_number}</span>
                    <div class="ticket-title">{title}</div>
                    {f'<div class="ticket-person">👤 {person}</div>' if person else ''}
                </div>
            </div>
            <div class="ticket-description">"{description}"</div>
            <div class="ticket-footer">
                <span class="badge badge-sm {badge_class}">{status_text}</span>
                <span style="font-size: 0.8rem;">📅 {date}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def stat_card(title: str, value: str, trend: str = "+0%", icon: str = "📊") -> str:
        return f"""
        <div class="stat-card-premium">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span>{icon}</span>
                <span class="stat-label">{title}</span>
            </div>
            <div class="stat-value">{value}</div>
        </div>
        """
    
    @staticmethod
    def header_hero(title: str, subtitle: str = "") -> str:
        return f"""
        <div class="header-hero-premium">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """
    
    @staticmethod
    def alert_success(message: str) -> str:
        return f'<div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); border-radius: 8px; padding: 0.75rem; color: #a7f3d0;">✅ {message}</div>'
    
    @staticmethod
    def alert_error(message: str) -> str:
        return f'<div style="background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 8px; padding: 0.75rem; color: #fecaca;">❌ {message}</div>'