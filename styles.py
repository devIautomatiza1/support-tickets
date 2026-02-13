"""
Sistema de estilos HERMOSO - Diseño SaaS Premium tipo Linear/Vercel.
Glassmorphism boutique + Tipografía impecable + Animaciones fluidas.
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
            /* ===== TEMA GLOBAL ===== */
            :root {
                --bg-dark: #0a0e27;
                --bg-secondary: #1a1f3a;
                --bg-tertiary: #252d45;
                --accent: #2563eb;
                --accent-light: #60a5fa;
                --text-primary: #f8fafc;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;
                --border: rgba(203, 213, 225, 0.1);
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
            }

            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            html, body {
                background: var(--bg-dark);
                color: var(--text-primary);
            }

            /* ===== SCROLLBAR CUSTOM ===== */
            ::-webkit-scrollbar {
                width: 10px;
            }
            ::-webkit-scrollbar-track {
                background: transparent;
            }
            ::-webkit-scrollbar-thumb {
                background: var(--accent);
                border-radius: 5px;
                transition: background 0.3s;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: var(--accent-light);
            }

            /* ===== CONTENEDOR PRINCIPAL ===== */
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, var(--bg-dark) 0%, #0f1729 50%, var(--bg-secondary) 100%);
            }

            [data-testid="stSidebar"] {
                background: rgba(10, 14, 39, 0.8) !important;
                backdrop-filter: blur(20px) !important;
                border-right: 1px solid var(--border) !important;
            }

            /* ===== TIPOGRAFÍA ===== */
            h1, h2, h3 {
                font-weight: 700;
                letter-spacing: -0.02em;
                color: var(--text-primary);
            }

            h1 { font-size: 1.875rem; }
            h2 { font-size: 1.5rem; }
            h3 { font-size: 1.125rem; }
            h4 { font-size: 1rem; font-weight: 600; }

            p, span, div {
                line-height: 1.6;
                letter-spacing: 0.3px;
            }

            /* ===== GLASSMORPHISM CORE ===== */
            .glass {
                background: rgba(30, 41, 59, 0.4);
                backdrop-filter: blur(16px);
                border: 1px solid var(--border);
                border-radius: 12px;
            }

            .glass:hover {
                background: rgba(30, 41, 59, 0.5);
                border-color: rgba(203, 213, 225, 0.15);
                box-shadow: 0 0 30px rgba(37, 99, 235, 0.1);
            }

            /* ===== TARJETAS DE TICKETS ===== */
            .ticket-card {
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.3) 0%, rgba(30, 41, 59, 0.1) 100%);
                backdrop-filter: blur(16px);
                border: 1.5px solid rgba(37, 99, 235, 0.2);
                border-radius: 14px;
                padding: 1.25rem;
                transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                cursor: pointer;
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }

            .ticket-card::before {
                content: '';
                position: absolute;
                inset: 0;
                background: linear-gradient(135deg, transparent, rgba(37, 99, 235, 0.05));
                opacity: 0;
                transition: opacity 0.4s;
            }

            .ticket-card:hover {
                border-color: rgba(37, 99, 235, 0.4);
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(30, 41, 59, 0.3) 100%);
                box-shadow: 0 12px 40px rgba(37, 99, 235, 0.25);
                transform: translateY(-6px);
            }

            .ticket-card:hover::before {
                opacity: 1;
            }

            .ticket-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 1rem;
                gap: 0.75rem;
            }

            .ticket-number {
                font-size: 0.8rem;
                color: var(--text-muted);
                font-family: 'Monaco', monospace;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            .ticket-title {
                font-size: 1rem;
                font-weight: 600;
                color: var(--text-primary);
                line-height: 1.5;
                margin: 0.75rem 0;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }

            .ticket-footer {
                display: flex;
                gap: 0.5rem;
                margin-top: 1rem;
            }

            /* ===== BADGES MINIMALISTAS ===== */
            .badge {
                display: inline-flex;
                align-items: center;
                gap: 0.375rem;
                padding: 0.375rem 0.875rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border: 1.5px solid;
                backdrop-filter: blur(8px);
                transition: all 0.3s;
            }

            .badge:hover {
                transform: scale(1.08);
            }

            .badge-new {
                background: rgba(239, 68, 68, 0.15);
                border-color: rgba(239, 68, 68, 0.5);
                color: #fca5a5;
            }

            .badge-in-progress {
                background: rgba(251, 146, 60, 0.15);
                border-color: rgba(251, 146, 60, 0.5);
                color: #fdba74;
            }

            .badge-won {
                background: rgba(34, 197, 94, 0.15);
                border-color: rgba(34, 197, 94, 0.5);
                color: #86efac;
            }

            .badge-closed {
                background: rgba(100, 116, 139, 0.15);
                border-color: rgba(100, 116, 139, 0.5);
                color: #cbd5e1;
            }

            /* ===== INDICADOR DE PRIORIDAD ===== */
            .priority-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                animation: pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
                position: relative;
            }

            .priority-high {
                background: #ff5757;
                box-shadow: 0 0 12px rgba(255, 87, 87, 0.6);
            }

            .priority-medium {
                background: #ffa500;
                box-shadow: 0 0 12px rgba(255, 165, 0, 0.6);
            }

            .priority-low {
                background: #52d383;
                box-shadow: 0 0 12px rgba(82, 211, 131, 0.6);
            }

            @keyframes pulse-glow {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.6; }
            }

            /* ===== STAT CARDS ===== */
            .stat-card {
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, transparent 100%);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(37, 99, 235, 0.2);
                border-radius: 12px;
                padding: 1rem;
                transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                position: relative;
                overflow: hidden;
            }

            .stat-card::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--accent), transparent);
                opacity: 0;
                transition: opacity 0.4s;
            }

            .stat-card:hover {
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(37, 99, 235, 0.05) 100%);
                border-color: rgba(37, 99, 235, 0.3);
                box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
                transform: translateY(-3px);
            }

            .stat-card:hover::after {
                opacity: 1;
            }

            .stat-label {
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                color: var(--text-muted);
                margin-bottom: 0.5rem;
            }

            .stat-value {
                font-size: 2rem;
                font-weight: 800;
                background: linear-gradient(135deg, var(--accent-light), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .stat-trend {
                font-size: 0.75rem;
                font-weight: 700;
                color: var(--success);
            }

            /* ===== ALERTS ===== */
            .alert {
                border-radius: 12px;
                padding: 1rem;
                border: 1.5px solid;
                backdrop-filter: blur(12px);
                animation: slideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                font-size: 0.95rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }

            .alert-success {
                background: rgba(16, 185, 129, 0.1);
                border-color: rgba(16, 185, 129, 0.3);
                color: #6ee7b7;
            }

            .alert-error {
                background: rgba(239, 68, 68, 0.1);
                border-color: rgba(239, 68, 68, 0.3);
                color: #fca5a5;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-12px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* ===== BOTONES ===== */
            button {
                border-radius: 8px !important;
                font-weight: 600 !important;
                font-size: 0.9rem !important;
                transition: all 0.3s !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }

            .stButton > button {
                background: linear-gradient(135deg, var(--accent), #1d4ed8) !important;
                border: none !important;
                color: white !important;
                height: 2.5rem !important;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, var(--accent-light), var(--accent)) !important;
                box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
                transform: translateY(-2px) !important;
            }

            /* ===== HEADER HERO ===== */
            .header-hero {
                background: linear-gradient(135deg, var(--accent) 0%, #1e40af 100%);
                padding: 2.5rem 2rem;
                border-radius: 16px;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(37, 99, 235, 0.3);
            }

            .header-hero::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -20%;
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
                border-radius: 50%;
            }

            .header-hero h1 {
                color: white;
                margin: 0;
                font-size: 2rem;
                position: relative;
                z-index: 1;
            }

            .header-hero p {
                color: rgba(255, 255, 255, 0.9);
                margin: 0.75rem 0 0 0;
                font-size: 0.95rem;
                position: relative;
                z-index: 1;
            }

            /* ===== MODALES ===== */
            [role="dialog"] {
                background: rgba(26, 31, 58, 0.9) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid var(--border) !important;
                border-radius: 16px !important;
                box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5) !important;
            }

            /* ===== INPUT FIELDS ===== */
            input, textarea, select {
                background: rgba(10, 14, 39, 0.5) !important;
                border: 1.5px solid var(--border) !important;
                border-radius: 10px !important;
                color: var(--text-primary) !important;
                padding: 0.875rem 1rem !important;
                font-size: 0.95rem !important;
                transition: all 0.3s !important;
                font-family: 'Inter', sans-serif !important;
            }

            input:focus, textarea:focus, select:focus {
                outline: none !important;
                border-color: var(--accent) !important;
                background: rgba(10, 14, 39, 0.7) !important;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
            }

            /* ===== SELECTBOX & MULTISELECT ===== */
            [data-testid="stSelectbox"] > div > div {
                background: rgba(10, 14, 39, 0.5) !important;
                border: 1.5px solid var(--border) !important;
                border-radius: 10px !important;
            }

            /* ===== DIVIDERS ===== */
            hr {
                border: none !important;
                height: 1px;
                background: var(--border) !important;
                margin: 1.5rem 0 !important;
            }

            /* ===== EXPANDER ===== */
            [data-testid="stExpander"] {
                background: transparent !important;
                border: 1px solid var(--border) !important;
                border-radius: 10px !important;
                padding: 1rem !important;
            }

            /* ===== EFECTO GLOBAL ===== */
            a {
                color: var(--accent-light) !important;
                transition: color 0.3s !important;
            }

            a:hover {
                color: var(--accent) !important;
            }
        </style>
        """, unsafe_allow_html=True)



class ComponentStyles:
    """Componentes renderizados hermosamente"""
    
    @staticmethod
    def ticket_card(ticket_number: str, title: str, status: str, priority: str = "Medium") -> str:
        """Tarjeta de ticket - Diseño hermoso"""
        status_map = {
            "new": ("badge-new", "🆕"),
            "in_progress": ("badge-in-progress", "⏳"),
            "won": ("badge-won", "✅"),
            "closed": ("badge-closed", "🔒")
        }
        
        priority_map = {
            "High": "priority-high",
            "Medium": "priority-medium",
            "Low": "priority-low"
        }
        
        badge_class, badge_emoji = status_map.get(status, status_map["new"])
        priority_class = priority_map.get(priority, priority_map["Medium"])
        
        return f"""
        <div class="ticket-card">
            <div class="ticket-header">
                <span class="ticket-number">#{ticket_number}</span>
                <div class="priority-dot {priority_class}"></div>
            </div>
            <h4 class="ticket-title">{title}</h4>
            <div class="ticket-footer">
                <span class="badge {badge_class}">{badge_emoji}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def stat_card(title: str, value: str, trend: str = "+0%", icon: str = "📊") -> str:
        """Tarjeta de estadística - Minimalista bonita"""
        return f"""
        <div class="stat-card">
            <p class="stat-label">{title}</p>
            <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                <span class="stat-value">{value}</span>
                <span class="stat-trend">{trend}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def alert_success(message: str) -> str:
        """Alerta de éxito"""
        return f'<div class="alert alert-success"><i class="fas fa-check-circle" style="flex-shrink: 0;"></i><span>{message}</span></div>'
    
    @staticmethod
    def alert_error(message: str) -> str:
        """Alerta de error"""
        return f'<div class="alert alert-error"><i class="fas fa-exclamation-circle" style="flex-shrink: 0;"></i><span>{message}</span></div>'
    
    @staticmethod
    def header_hero(title: str, subtitle: str = "") -> str:
        """Header hero hermoso"""
        return f"""
        <div class="header-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """
