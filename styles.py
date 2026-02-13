"""
Sistema de estilos premium - Diseño ultra minimalista tipo Linear/Vercel
"""

import streamlit as st


class StyleManager:
    """Gestor maestro de estilos - Diseño ultra premium"""
    
    @staticmethod
    @st.cache_data
    def inject_all():
        """Inyecta CSS ultra minimalista y profesional"""
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
        
        <style>
            /* ===== VARIABLES ===== */
            :root {
                --bg-primary: #0B0D12;
                --bg-secondary: #12141A;
                --bg-tertiary: #1A1D26;
                --accent: #3B82F6;
                --accent-glow: rgba(59, 130, 246, 0.5);
                --text-primary: #F0F2F5;
                --text-secondary: #B0B7C4;
                --text-tertiary: #6B7280;
                --border-light: rgba(255, 255, 255, 0.03);
                --border-medium: rgba(255, 255, 255, 0.06);
                --border-accent: rgba(59, 130, 246, 0.2);
                --success: #10B981;
                --warning: #F59E0B;
                --danger: #EF4444;
                --glass-bg: rgba(18, 20, 26, 0.7);
            }

            /* ===== RESET Y BASE ===== */
            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html, body, [data-testid="stAppViewContainer"] {
                background: var(--bg-primary);
                color: var(--text-primary);
                font-feature-settings: "ss01", "ss02", "cv01", "cv02";
            }

            /* ===== SIDEBAR MINIMAL ===== */
            [data-testid="stSidebar"] {
                background: var(--bg-secondary) !important;
                border-right: 1px solid var(--border-medium) !important;
                box-shadow: none !important;
            }

            [data-testid="stSidebar"] > div {
                background: transparent !important;
                padding: 1.5rem 1rem !important;
            }

            /* ===== TARJETAS DE TICKETS (PREMIUM) ===== */
            .ticket-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-medium);
                border-radius: 12px;
                padding: 1.5rem;
                transition: all 0.2s ease;
                position: relative;
                margin-bottom: 1.25rem;
            }

            .ticket-card:hover {
                background: var(--bg-tertiary);
                border-color: rgba(255, 255, 255, 0.12);
                transform: translateY(-2px);
                box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.3);
            }

            /* ===== TARJETAS INTERACTIVAS CON HOVER EDITAR ===== */
            .ticket-card-interactive {
                position: relative;
                cursor: pointer;
                overflow: hidden;
            }

            .ticket-overlay {
                position: absolute;
                top: 0;0
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(59, 130, 246, 0.15);
                opacity: 0;
                z-index: 1;
                transition: opacity 0.2s ease;
                pointer-events: none;
                border-radius: 12px;
            }

            .ticket-card-interactive:hover .ticket-overlay {
                opacity: 1;
            }

            .ticket-edit-hint {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: var(--accent);
                font-weight: 600;
                font-size: 0.95rem;
                opacity: 0;
                z-index: 2;
                pointer-events: none;
                transition: opacity 0.2s ease;
            }

            .ticket-card-interactive:hover .ticket-edit-hint {
                opacity: 1;
            }

            /* ===== TICKETS MALFORMADOS ===== */
            .ticket-card-warning {
                border-color: rgba(245, 158, 11, 0.4);
                background: rgba(245, 158, 11, 0.05);
            }

            .ticket-card-warning:hover {
                border-color: rgba(245, 158, 11, 0.6);
                background: rgba(245, 158, 11, 0.1);
                box-shadow: 0 8px 20px -4px rgba(245, 158, 11, 0.2);
            }

            .ticket-warning {
                color: #F59E0B;
                font-size: 0.9rem;
                margin-right: 0.5rem;
                animation: blink 2s ease-in-out infinite;
            }

            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.6; }
            }

            /* ===== TICKET CARD CLICKEABLE ===== */
            .ticket-card-clickable {
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }

            .ticket-hover-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(59, 130, 246, 0.1);
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.2s ease;
                border-radius: 16px;
                backdrop-filter: blur(2px);
                pointer-events: none;
            }

            .ticket-card-clickable:hover .ticket-hover-overlay {
                opacity: 1;
            }

            .ticket-hover-text {
                color: var(--accent);
                font-weight: 600;
                font-size: 0.95rem;
                text-align: center;
                animation: pulse 1.5s ease-in-out infinite;
            }

            @keyframes pulse {
                0%, 100% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.05);
                }
            }

            .ticket-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 0.75rem;
            }

            .ticket-id {
                font-size: 0.72rem;
                font-weight: 500;
                color: var(--text-tertiary);
                letter-spacing: 0.01em;
            }
            
            .ticket-menu {
                opacity: 0;
                transition: opacity 0.2s ease;
                cursor: pointer;
                color: var(--text-tertiary);
                font-size: 1.2rem;
                transition: all 0.2s ease;
            }
            
            .ticket-card:hover .ticket-menu {
                opacity: 1;
                color: var(--text-secondary);
            }

            /* ===== BOTÓN DE EDICIÓN MEJORADO ===== */
            .edit-button-container {
                opacity: 0;
                transition: opacity 0.2s ease;
            }

            .ticket-card:hover .edit-button-container {
                opacity: 1;
            }

            .edit-button {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid var(--border-medium);
                border-radius: 8px;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                color: var(--text-tertiary);
                font-size: 1rem;
                transition: all 0.2s ease;
            }

            .edit-button:hover {
                background: rgba(59, 130, 246, 0.1);
                border-color: var(--accent);
                color: var(--accent);
                transform: scale(1.05);
            }

            .ticket-title {
                font-size: 0.95rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 0.4rem;
                line-height: 1.3;
            }

            .ticket-person {
                font-size: 0.8rem;
                color: var(--text-secondary);
                margin-bottom: 0.75rem;
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }

            .ticket-description {
                font-size: 0.8rem;
                color: var(--text-tertiary);
                line-height: 1.4;
                margin-bottom: 1rem;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                word-break: break-word;
            }

            .ticket-footer {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-top: 1rem;
                padding-top: 0.75rem;
                border-top: 1px solid var(--border-light);
            }

            /* ===== BADGES (PILL STYLE MINIMALISTA) ===== */
            .badge {
                display: inline-flex;
                align-items: center;
                padding: 0.3rem 0.65rem;
                border-radius: 12px;
                font-size: 0.68rem;
                font-weight: 500;
                letter-spacing: 0.01em;
                border: 1px solid;
                text-transform: uppercase;
                backdrop-filter: blur(1px);
            }

            .badge-new {
                background: rgba(239, 68, 68, 0.08);
                border-color: rgba(239, 68, 68, 0.15);
                color: #EC8787;
            }

            .badge-progress {
                background: rgba(245, 158, 11, 0.08);
                border-color: rgba(245, 158, 11, 0.15);
                color: #F5D547;
            }

            .badge-won {
                background: rgba(16, 185, 129, 0.08);
                border-color: rgba(16, 185, 129, 0.15);
                color: #5EE8B7;
            }

            .badge-closed {
                background: rgba(107, 114, 128, 0.08);
                border-color: rgba(107, 114, 128, 0.15);
                color: #9CA3AF;
            }

            /* ===== PRIORITY INDICATORS ===== */
            .priority-indicator {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .priority-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
            }

            .priority-dot.high { background: var(--danger); }
            .priority-dot.medium { background: var(--warning); }
            .priority-dot.low { background: var(--success); }

            /* ===== STAT CARDS (HORIZONTAL PREMIUM) ===== */
            .stat-card {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 1rem 1.25rem;
                display: flex;
                align-items: center;
                gap: 1rem;
                backdrop-filter: blur(3px);
                transition: all 0.2s ease;
            }
            
            .stat-card:hover {
                border-color: rgba(255, 255, 255, 0.15);
                background: rgba(255, 255, 255, 0.02);
            }

            .stat-card-header {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                flex-shrink: 0;
            }

            .stat-icon {
                color: var(--accent);
                font-size: 1.2rem;
            }

            .stat-label {
                font-size: 0.7rem;
                font-weight: 500;
                color: var(--text-tertiary);
                text-transform: uppercase;
                letter-spacing: 0.04em;
                line-height: 1;
            }

            .stat-value {
                font-size: 1.75rem;
                font-weight: 700;
                color: var(--text-primary);
                line-height: 1;
            }
            
            .stat-card-content {
                flex: 1;
            }

            /* ===== MODAL/POPOVER MEJORADO ===== */
            [data-testid="stPopover"] {
                z-index: 1000 !important;
            }
            
            [data-testid="stPopoverBody"] {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border-accent) !important;
                border-radius: 24px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
                padding: 2rem !important;
                min-width: 600px !important;
                max-width: 700px !important;
                animation: modalFadeIn 0.2s ease !important;
                transform-origin: center !important;
                position: fixed !important;
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, -50%) !important;
                margin: 0 !important;
                overflow-y: auto !important;
                max-height: 80vh !important;
            }

            @keyframes modalFadeIn {
                from {
                    opacity: 0;
                    transform: translate(-50%, -50%) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translate(-50%, -50%) scale(1);
                }
            }
            
            [data-testid="stPopoverBody"] > h3 {
                margin: 0 0 0.5rem 0 !important;
                padding: 0 !important;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: var(--text-primary) !important;
            }
            
            [data-testid="stPopoverBody"] > .stCaption {
                margin-bottom: 1.5rem !important;
                padding-bottom: 1.5rem !important;
                border-bottom: 1px solid var(--border-medium) !important;
            }

            [data-testid="stPopoverBody"] h3 {
                font-size: 1.25rem !important;
                font-weight: 600 !important;
                color: var(--text-primary) !important;
                margin-bottom: 0.25rem !important;
            }

            [data-testid="stPopoverBody"] .stCaption {
                color: var(--text-tertiary) !important;
                font-size: 0.85rem !important;
                margin-bottom: 1.5rem !important;
            }

            [data-testid="stPopoverBody"] label {
                font-size: 0.75rem !important;
                font-weight: 600 !important;
                color: var(--text-tertiary) !important;
                text-transform: uppercase !important;
                letter-spacing: 0.03em !important;
                margin-bottom: 0.5rem !important;
            }

            [data-testid="stPopoverBody"] .stSelectbox > div,
            [data-testid="stPopoverBody"] .stTextArea textarea {
                background: var(--bg-primary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                margin-bottom: 1rem !important;
            }

            [data-testid="stPopoverBody"] .stButton > button {
                background: var(--accent) !important;
                border: none !important;
                color: white !important;
                font-weight: 600 !important;
                border-radius: 12px !important;
                padding: 0.75rem !important;
                width: 100% !important;
                margin-top: 1rem !important;
            }

            [data-testid="stPopoverBody"] .stButton > button:hover {
                background: #2563EB !important;
            }

            /* ===== BOTÓN INVISIBLE PARA CLICK DETECTION ===== */
            .stContainer > .stButton > button {
                background: transparent !important;
                border: none !important;
                color: transparent !important;
                padding: 0 !important;
                height: 0 !important;
                min-height: 0 !important;
                box-shadow: none !important;
            }

            .stContainer > .stButton > button:hover {
                background: transparent !important;
            }

            /* ===== CONNECTION STATUS ===== */
            .connection-status {
                background: rgba(16, 185, 129, 0.05);
                border: 1px solid rgba(16, 185, 129, 0.1);
                border-radius: 10px;
                padding: 0.75rem;
                font-size: 0.8rem;
                color: var(--text-secondary);
            }

            .connection-dot {
                display: inline-block;
                width: 8px;
                height: 8px;
                background: var(--success);
                border-radius: 50%;
                margin-right: 0.5rem;
            }

            /* ===== POPOVER / MODAL MINIMALISTA ===== */
            [data-testid="popover"] {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 16px !important;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4) !important;
            }

            /* Stylear inputs y textareas dentro del popover */
            [data-testid="popover"] input,
            [data-testid="popover"] textarea,
            [data-testid="popover"] select {
                background: var(--bg-tertiary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 10px !important;
                color: var(--text-primary) !important;
                padding: 0.75rem !important;
                font-family: 'Inter', sans-serif !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="popover"] input:focus,
            [data-testid="popover"] textarea:focus,
            [data-testid="popover"] select:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1) !important;
                background: var(--bg-tertiary) !important;
            }

            /* Labels dentro del popover */
            [data-testid="popover"] label {
                color: var(--text-primary) !important;
                font-weight: 500 !important;
                font-size: 0.85rem !important;
                margin-bottom: 0.5rem !important;
            }

            /* Separadores entre campos */
            [data-testid="popover"] [data-testid="element-container"]:not(:last-child) {
                margin-bottom: 1.25rem !important;
                padding-bottom: 1.25rem !important;
                border-bottom: 1px solid var(--border-light) !important;
            }

            /* Botones dentro del popover */
            [data-testid="popover"] button[kind="primary"] {
                background: var(--accent) !important;
                border: none !important;
                border-radius: 10px !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 0.75rem 1.25rem !important;
                transition: all 0.2s ease !important;
                width: 100% !important;
                margin-top: 1rem !important;
            }

            [data-testid="popover"] button[kind="primary"]:hover {
                background: #2563eb !important;
                box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3) !important;
                transform: translateY(-1px) !important;
            }

            [data-testid="popover"] button[kind="primary"]:active {
                transform: translateY(0) !important;
            }

            /* Selectbox (dropdown) dentro del popover */
            [data-testid="popover"] [data-testid="selectbox"] {
                margin-bottom: 1rem !important;
            }

            [data-testid="popover"] [role="combobox"] {
                background: var(--bg-tertiary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 10px !important;
                color: var(--text-primary) !important;
            }

            /* Heading dentro del popover */
            [data-testid="popover"] h3 {
                color: var(--text-primary) !important;
                font-size: 1.1rem !important;
                font-weight: 700 !important;
                margin-bottom: 0.75rem !important;
            }

            [data-testid="popover"] p {
                color: var(--text-secondary) !important;
                font-size: 0.85rem !important;
                margin-bottom: 1.5rem !important;
            }
        </style>
        """, unsafe_allow_html=True)


class ComponentStyles:
    """Componentes renderizados minimalistas"""
    
    @staticmethod
    def stat_card(title: str, value: str, icon: str = "📊", trend: str = "") -> str:
        return f"""
        <div class="stat-card">
            <div class="stat-card-header">
                <span class="stat-icon">{icon}</span>
                <span class="stat-label">{title}</span>
            </div>
            <div class="stat-value">{value}</div>
        </div>
        """
    
    @staticmethod
    def page_header(title: str, subtitle: str = "") -> str:
        return f"""
        <div class="page-header">
            <h1 class="page-title">{title}</h1>
            {f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
        """
    
    @staticmethod
    def connection_status(connected: bool, count: int = 0) -> str:
        if connected:
            return f"""
            <div class="connection-status">
                <span class="connection-dot"></span>
                Conectado • {count} registros
            </div>
            """
        return '<div class="connection-status" style="border-color: rgba(239,68,68,0.1);">❌ Error de conexión</div>'