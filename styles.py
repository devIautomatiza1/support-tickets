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

            /* ===== TARJETAS DE TICKETS ===== */
            .ticket-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-medium);
                border-radius: 16px;
                padding: 1.25rem;
                transition: all 0.2s ease;
                position: relative;
                margin-bottom: 1rem;
            }

            .ticket-card:hover {
                background: var(--bg-tertiary);
                border-color: var(--border-accent);
                transform: translateY(-1px);
            }

            .ticket-header {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                margin-bottom: 1rem;
            }

            .ticket-id {
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--text-tertiary);
                letter-spacing: 0.02em;
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
                font-size: 1rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 0.5rem;
                line-height: 1.4;
            }

            .ticket-person {
                font-size: 0.85rem;
                color: var(--text-secondary);
                margin-bottom: 0.75rem;
                display: flex;
                align-items: center;
                gap: 0.25rem;
            }

            .ticket-description {
                font-size: 0.85rem;
                color: var(--text-tertiary);
                line-height: 1.5;
                margin-bottom: 1rem;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }

            .ticket-footer {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-top: 0.75rem;
            }

            /* ===== BADGES ===== */
            .badge {
                display: inline-flex;
                align-items: center;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.7rem;
                font-weight: 600;
                letter-spacing: 0.02em;
                border: 1px solid;
            }

            .badge-new {
                background: rgba(239, 68, 68, 0.1);
                border-color: rgba(239, 68, 68, 0.2);
                color: #FCA5A5;
            }

            .badge-progress {
                background: rgba(245, 158, 11, 0.1);
                border-color: rgba(245, 158, 11, 0.2);
                color: #FCD34D;
            }

            .badge-won {
                background: rgba(16, 185, 129, 0.1);
                border-color: rgba(16, 185, 129, 0.2);
                color: #6EE7B7;
            }

            .badge-closed {
                background: rgba(107, 114, 128, 0.1);
                border-color: rgba(107, 114, 128, 0.2);
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

            /* ===== STAT CARDS ===== */
            .stat-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-medium);
                border-radius: 16px;
                padding: 1.25rem;
            }

            .stat-card-header {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.75rem;
            }

            .stat-icon {
                color: var(--text-tertiary);
                font-size: 1rem;
            }

            .stat-label {
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--text-tertiary);
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .stat-value {
                font-size: 2rem;
                font-weight: 700;
                color: var(--text-primary);
                line-height: 1;
            }

            /* ===== MODAL/POPOVER MEJORADO ===== */
            [data-testid="stPopoverBody"] {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border-accent) !important;
                border-radius: 24px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
                padding: 1.5rem !important;
                min-width: 400px !important;
                animation: modalFadeIn 0.2s ease !important;
            }

            @keyframes modalFadeIn {
                from {
                    opacity: 0;
                    transform: scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
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

            /* ===== POPOVER CENTRADO ===== */
            [data-testid="stPopover"] {
                position: fixed !important;
                left: 50% !important;
                top: 50% !important;
                transform: translate(-50%, -50%) !important;
                z-index: 9999 !important;
            }

            [data-testid="stPopoverBody"] {
                max-width: 500px;
                margin: 0 auto;
            }
        </style>
        
        <script>
        function centerPopovers() {
            const popovers = document.querySelectorAll('[data-testid="stPopover"]');
            popovers.forEach(popover => {
                popover.style.position = 'fixed';
                popover.style.left = '50%';
                popover.style.top = '50%';
                popover.style.transform = 'translate(-50%, -50%)';
                popover.style.zIndex = '9999';
            });
        }
        
        // Ejecutar cuando se abra un popover
        const observer = new MutationObserver(centerPopovers);
        observer.observe(document.body, { childList: true, subtree: true });
        
        // Ejecutar inmediatamente
        centerPopovers();
        </script>
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