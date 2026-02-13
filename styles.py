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

            /* ===== MODAL PREMIUM - REDISEÑO COMPLETO ===== */
            [data-testid="stPopover"] {
                z-index: 1000 !important;
            }

            /* Overlay de fondo */
            [data-testid="stPopover"]::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                animation: fadeIn 0.2s ease;
                pointer-events: none;
            }
            
            [data-testid="stPopoverBody"] {
                background: var(--glass-bg) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid var(--border-accent) !important;
                border-radius: 32px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05) inset !important;
                padding: 2rem !important;
                min-width: 600px !important;
                max-width: 700px !important;
                animation: modalSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
                transform-origin: center !important;
                position: fixed !important;
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, -50%) !important;
                margin: 0 !important;
                overflow-y: auto !important;
                max-height: 85vh !important;
            }

            @keyframes modalSlideUp {
                from {
                    opacity: 0;
                    transform: translate(-50%, -45%) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translate(-50%, -50%) scale(1);
                }
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            /* ===== HEADER DEL MODAL ===== */
            .modal-header-custom {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 2rem;
                padding-bottom: 1.25rem;
                border-bottom: 1px solid var(--border-medium);
            }

            .modal-title-section {
                display: flex;
                flex-direction: column;
                gap: 0.25rem;
            }

            .modal-title-custom {
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: var(--text-primary) !important;
                letter-spacing: -0.02em !important;
                line-height: 1.2 !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            .modal-subtitle-custom {
                font-size: 0.875rem !important;
                color: var(--text-tertiary) !important;
                font-weight: 400 !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            .modal-close-button {
                width: 36px;
                height: 36px;
                border-radius: 12px;
                background: var(--bg-tertiary);
                border: 1px solid var(--border-medium);
                color: var(--text-secondary);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 1.2rem;
                transition: all 0.2s ease;
            }

            .modal-close-button:hover {
                background: var(--accent);
                border-color: var(--accent);
                color: white;
                transform: rotate(90deg);
            }

            /* ===== CONTENEDOR DE CAMPOS ===== */
            .modal-field-container {
                background: var(--bg-tertiary);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                border: 1px solid var(--border-light);
            }

            .modal-field-group {
                margin-bottom: 1.5rem;
            }

            .modal-field-group:last-child {
                margin-bottom: 0;
            }

            .modal-field-label {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.75rem;
            }

            .modal-field-label i {
                color: var(--accent);
                font-size: 1rem;
                width: 20px;
            }

            .modal-field-label span {
                font-size: 0.85rem;
                font-weight: 600;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 0.02em;
            }

            /* ===== INPUTS MEJORADOS ===== */
            [data-testid="stPopoverBody"] .stTextArea textarea,
            [data-testid="stPopoverBody"] .stSelectbox > div,
            [data-testid="stPopoverBody"] input {
                background: var(--bg-primary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                font-size: 0.95rem !important;
                padding: 0.75rem 1rem !important;
                width: 100% !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stPopoverBody"] .stTextArea textarea:hover,
            [data-testid="stPopoverBody"] .stSelectbox > div:hover,
            [data-testid="stPopoverBody"] input:hover {
                border-color: rgba(255, 255, 255, 0.2) !important;
            }

            [data-testid="stPopoverBody"] .stTextArea textarea:focus,
            [data-testid="stPopoverBody"] .stSelectbox > div:focus,
            [data-testid="stPopoverBody"] input:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
                outline: none !important;
            }

            /* ===== SELECTBOX MEJORADO ===== */
            [data-testid="stPopoverBody"] .stSelectbox [data-testid="baseButton-secondary"] {
                background: var(--bg-primary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                padding: 0.75rem 1rem !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stPopoverBody"] .stSelectbox [data-testid="baseButton-secondary"]:hover {
                border-color: var(--accent) !important;
                background: var(--bg-tertiary) !important;
            }

            /* ===== BOTÓN DE ACCIÓN ===== */
            .modal-actions {
                display: flex;
                gap: 1rem;
                margin-top: 2rem;
                padding-top: 1.5rem;
                border-top: 1px solid var(--border-medium);
            }

            [data-testid="stPopoverBody"] .stButton > button {
                flex: 1;
                background: var(--accent) !important;
                border: none !important;
                border-radius: 12px !important;
                color: white !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                padding: 0.875rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
                margin: 0 !important;
            }

            [data-testid="stPopoverBody"] .stButton > button:hover {
                background: #2563EB !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
            }

            [data-testid="stPopoverBody"] .stButton > button:active {
                transform: translateY(0) !important;
            }

            .modal-button-secondary {
                flex: 1;
                background: transparent !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 12px !important;
                color: var(--text-secondary) !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                padding: 0.875rem !important;
                transition: all 0.2s ease !important;
                cursor: pointer;
                text-align: center;
            }

            .modal-button-secondary:hover {
                background: var(--bg-tertiary) !important;
                border-color: var(--text-tertiary) !important;
                color: var(--text-primary) !important;
            }

            /* ===== DIVISORES Y ESPACIADO ===== */
            .modal-divider {
                height: 1px;
                background: linear-gradient(90deg, 
                    transparent 0%, 
                    var(--border-medium) 20%, 
                    var(--border-medium) 80%, 
                    transparent 100%
                );
                margin: 1.5rem 0;
            }

            /* ===== SCROLLBAR PERSONALIZADO ===== */
            [data-testid="stPopoverBody"]::-webkit-scrollbar {
                width: 6px;
            }

            [data-testid="stPopoverBody"]::-webkit-scrollbar-track {
                background: transparent;
            }

            [data-testid="stPopoverBody"]::-webkit-scrollbar-thumb {
                background: var(--border-medium);
                border-radius: 20px;
            }

            [data-testid="stPopoverBody"]::-webkit-scrollbar-thumb:hover {
                background: var(--text-tertiary);
            }

            /* ===== TÍTULOS Y TEXTOS DENTRO DEL MODAL ===== */
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
                animation: pulse 2s ease-in-out infinite;
            }

            /* ===== ELIMINAR ESTILOS ANTERIORES DEL POPOVER ===== */
            [data-testid="popover"] {
                display: none !important;
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
        return '<div class="connection-status" style="border-color: rgba(239,68,68,0.1); color: #EF4444;">❌ Error de conexión</div>'


class ModalHelper:
    """Helper para crear modales consistentes"""
    
    @staticmethod
    def modal_header(title: str, subtitle: str = ""):
        """Renderiza el header del modal"""
        subtitle_html = f'<p class="modal-subtitle-custom">{subtitle}</p>' if subtitle else ''
        return f"""
        <div class="modal-header-custom">
            <div class="modal-title-section">
                <h3 class="modal-title-custom">{title}</h3>
                {subtitle_html}
            </div>
            <div class="modal-close-button" onclick="document.querySelector(\'[data-testid="stPopover"] button\')?.click()">
                <i class="fas fa-times"></i>
            </div>
        </div>
        """
    
    @staticmethod
    def field_container(content: str, icon: str = "", label: str = ""):
        """Envuelve un campo en un contenedor estilizado"""
        icon_html = f'<i class="fas fa-{icon}"></i>' if icon else ''
        label_html = f'<span>{label}</span>' if label else ''
        
        label_section = f'<div class="modal-field-label">{icon_html}{label_html}</div>' if (icon or label) else ''
        
        return f"""
        <div class="modal-field-group">
            {label_section}
            {content}
        </div>
        """
    
    @staticmethod
    def field_container_start(icon: str = "", label: str = ""):
        """Inicia un contenedor de campo"""
        icon_html = f'<i class="fas fa-{icon}"></i>' if icon else ''
        label_html = f'<span>{label}</span>' if label else ''
        
        label_section = f'<div class="modal-field-label">{icon_html}{label_html}</div>' if (icon or label) else ''
        
        return f"""
        <div class="modal-field-group">
            {label_section}
        """
    
    @staticmethod
    def field_container_end():
        """Cierra un contenedor de campo"""
        return "</div>"
    
    @staticmethod
    def action_buttons(primary_text: str = "Guardar cambios", secondary_text: str = "Cancelar"):
        """Renderiza los botones de acción"""
        return f"""
        <div class="modal-actions">
            <div class="modal-button-secondary" onclick="document.querySelector(\'[data-testid="stPopover"] button\')?.click()">
                {secondary_text}
            </div>
        """
    
    @staticmethod
    def action_buttons_end():
        """Cierra los botones de acción"""
        return "</div>"
    
    @staticmethod
    def divider():
        """Renderiza un divisor"""
        return '<div class="modal-divider"></div>'