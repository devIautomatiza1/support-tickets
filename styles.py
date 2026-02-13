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
            .ticket-grid {
                display: grid;
                gap: 1rem;
            }

            .ticket-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-medium);
                border-radius: 16px;
                padding: 1.25rem;
                transition: all 0.2s ease;
                position: relative;
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
                position: relative;
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
                backdrop-filter: blur(8px);
            }

            .edit-button:hover {
                background: rgba(59, 130, 246, 0.1);
                border-color: var(--accent);
                color: var(--accent);
                transform: scale(1.05);
            }

            .edit-button i {
                font-size: 0.9rem;
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

            .ticket-person i {
                color: var(--text-tertiary);
                font-size: 0.7rem;
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
                font-style: italic;
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

            .priority-dot.high { background: var(--danger); box-shadow: 0 0 8px var(--danger); }
            .priority-dot.medium { background: var(--warning); }
            .priority-dot.low { background: var(--success); }

            /* ===== STAT CARDS MINIMAL ===== */
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

            .stat-trend {
                font-size: 0.75rem;
                color: var(--text-tertiary);
                margin-top: 0.5rem;
            }

            /* ===== HEADER MINIMAL ===== */
            .page-header {
                margin-bottom: 2rem;
            }

            .page-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 0.25rem;
            }

            .page-subtitle {
                font-size: 0.9rem;
                color: var(--text-tertiary);
            }

            /* ===== MODAL/POPOVER MEJORADO ===== */
            [data-testid="stPopoverBody"] {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border-accent) !important;
                border-radius: 24px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(59, 130, 246, 0.1) !important;
                padding: 2rem !important;
                min-width: 480px !important;
                max-width: 520px !important;
                backdrop-filter: blur(20px) !important;
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

            /* Encabezado del modal */
            [data-testid="stPopoverBody"] .modal-header {
                margin-bottom: 2rem;
                padding-right: 2rem;
            }

            [data-testid="stPopoverBody"] h3 {
                font-size: 1.25rem !important;
                font-weight: 600 !important;
                color: var(--text-primary) !important;
                margin: 0 0 0.25rem 0 !important;
                letter-spacing: -0.01em !important;
            }

            [data-testid="stPopoverBody"] .stCaption {
                color: var(--text-tertiary) !important;
                font-size: 0.85rem !important;
                margin: 0 !important;
            }

            /* Campos del formulario */
            [data-testid="stPopoverBody"] .field-group {
                margin-bottom: 1.5rem;
            }

            [data-testid="stPopoverBody"] label {
                font-size: 0.75rem !important;
                font-weight: 600 !important;
                color: var(--text-tertiary) !important;
                text-transform: uppercase !important;
                letter-spacing: 0.03em !important;
                margin-bottom: 0.5rem !important;
                display: block !important;
            }

            [data-testid="stPopoverBody"] .stSelectbox > div,
            [data-testid="stPopoverBody"] .stTextArea textarea {
                background: var(--bg-primary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 14px !important;
                color: var(--text-primary) !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stPopoverBody"] .stSelectbox > div:hover,
            [data-testid="stPopoverBody"] .stTextArea textarea:hover {
                border-color: var(--border-accent) !important;
            }

            [data-testid="stPopoverBody"] .stSelectbox > div:focus-within,
            [data-testid="stPopoverBody"] .stTextArea textarea:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            }

            [data-testid="stPopoverBody"] .stTextArea textarea {
                min-height: 120px !important;
                resize: vertical !important;
                line-height: 1.6 !important;
            }

            /* Separador */
            [data-testid="stPopoverBody"] .modal-divider {
                height: 1px;
                background: var(--border-medium);
                margin: 1.5rem 0;
            }

            /* Botón de guardar mejorado */
            [data-testid="stPopoverBody"] .stButton > button {
                background: var(--accent) !important;
                border: none !important;
                color: white !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                border-radius: 14px !important;
                padding: 0.75rem 1.5rem !important;
                width: 100% !important;
                height: auto !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 0.5rem !important;
            }

            [data-testid="stPopoverBody"] .stButton > button:hover {
                background: #2563EB !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
            }

            [data-testid="stPopoverBody"] .stButton > button:active {
                transform: translateY(0) !important;
            }

            [data-testid="stPopoverBody"] .stButton > button i {
                font-size: 1rem;
            }

            /* Badge de información en el modal */
            .info-badge {
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid var(--border-accent);
                border-radius: 10px;
                padding: 0.75rem 1rem;
                margin-bottom: 1.5rem;
                font-size: 0.85rem;
                color: var(--text-secondary);
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }

            .info-badge i {
                color: var(--accent);
                font-size: 1rem;
            }

            /* ===== BOTONES GENERALES ===== */
            .stButton > button {
                background: transparent !important;
                border: 1px solid var(--border-medium) !important;
                color: var(--text-secondary) !important;
                font-weight: 500 !important;
                font-size: 0.85rem !important;
                border-radius: 12px !important;
                padding: 0.5rem 1rem !important;
                transition: all 0.2s ease !important;
            }

            .stButton > button:hover {
                border-color: var(--accent) !important;
                color: var(--text-primary) !important;
                background: rgba(59, 130, 246, 0.1) !important;
            }

            button[type="primary"] {
                background: var(--accent) !important;
                border-color: var(--accent) !important;
                color: white !important;
            }

            button[type="primary"]:hover {
                background: #2563EB !important;
                border-color: #2563EB !important;
            }

            /* ===== INPUTS ===== */
            input, select, textarea {
                background: var(--bg-primary) !important;
                border: 1px solid var(--border-medium) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                font-size: 0.9rem !important;
                padding: 0.75rem 1rem !important;
            }

            input:focus, select:focus, textarea:focus {
                border-color: var(--accent) !important;
                outline: none !important;
                box-shadow: 0 0 0 2px var(--border-accent) !important;
            }

            /* ===== DIVIDER ===== */
            hr {
                border: none !important;
                border-top: 1px solid var(--border-medium) !important;
                margin: 1.5rem 0 !important;
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
                box-shadow: 0 0 8px var(--success);
            }
        </style>
        """, unsafe_allow_html=True)