"""
Sistema de estilos SaaS Pro - Glassmorphism + Minimalismo profesional.
Inspirado en Linear, Holded, Vercel.
"""

import streamlit as st


class StyleManager:
    """Gestor de estilos SaaS Pro - Glassmorphism y animaciones"""
    
    @staticmethod
    @st.cache_data
    def inject_all():
        """Inyecta estilos profesionales SaaS Pro"""
        st.markdown("""
        <link href="https://cdn.tailwindcss.com" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
        
        <style>
            /* ===== DARK MODE PROFUNDO ===== */
            :root {
                --bg-primary: #0F172A;
                --bg-secondary: #1E293B;
                --bg-tertiary: #334155;
                --border-color: rgba(148, 163, 184, 0.1);
                --text-primary: #F1F5F9;
                --text-secondary: #CBD5E1;
                --text-tertiary: #94A3B8;
                --accent-primary: #3B82F6;
                --accent-secondary: #1E40AF;
                --glass-blur: blur(12px);
                --glass-bg: rgba(30, 41, 59, 0.5);
                --glass-border: rgba(148, 163, 184, 0.1);
            }

            /* ===== SCROLLBAR MINIMALISTA ===== */
            * {
                scrollbar-width: thin;
                scrollbar-color: var(--accent-primary) var(--bg-secondary);
            }
            
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: transparent;
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--accent-primary);
                border-radius: 4px;
                transition: background 0.3s ease;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #60A5FA;
            }

            /* ===== APLICACIÓN ===== */
            html, body {
                background: var(--bg-primary);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Helvetica Neue", sans-serif;
                letter-spacing: -0.01em;
            }
            
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, var(--bg-primary) 0%, #1A1F3A 50%, var(--bg-secondary) 100%);
                color: var(--text-primary);
            }
            
            [data-testid="stSidebar"] {
                background: var(--glass-bg) !important;
                backdrop-filter: var(--glass-blur) !important;
                border-right: 1px solid var(--glass-border) !important;
            }

            /* ===== TIPOGRAFÍA ===== */
            h1, h2, h3, h4, h5, h6 {
                font-weight: 600;
                letter-spacing: -0.02em;
            }

            h1 { font-size: 2rem; }
            h2 { font-size: 1.5rem; }
            h3 { font-size: 1.125rem; }

            p {
                font-size: 0.9rem;
                line-height: 1.6;
                color: var(--text-secondary);
            }

            /* ===== BOTONES ===== */
            .btn-primary {
                background: var(--accent-primary) !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.1) !important;
            }

            .btn-primary:hover {
                background: #2563EB !important;
                box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3) !important;
                transform: translateY(-2px) !important;
            }

            /* ===== CONTENEDORES CON GLASS EFFECT ===== */
            .glass-container {
                background: var(--glass-bg);
                backdrop-filter: var(--glass-blur);
                border: 1px solid var(--glass-border);
                border-radius: 12px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .glass-container:hover {
                border-color: rgba(59, 130, 246, 0.3);
                background: rgba(30, 41, 59, 0.7);
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
            }

            /* ===== TARJETAS DE TICKETS ===== */
            .ticket-card {
                background: var(--glass-bg);
                backdrop-filter: var(--glass-blur);
                border: 1px solid var(--glass-border);
                border-radius: 12px;
                padding: 1rem;
                transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
                position: relative;
                overflow: hidden;
            }

            .ticket-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .ticket-card:hover {
                border-color: rgba(59, 130, 246, 0.4);
                box-shadow: 0 12px 32px rgba(59, 130, 246, 0.2), 0 0 1px rgba(59, 130, 246, 0.1);
                transform: translateY(-4px);
            }

            .ticket-card:hover::before {
                opacity: 1;
            }

            /* ===== BADGES & STATUS ===== */
            .badge-status {
                display: inline-flex;
                align-items: center;
                gap: 0.375rem;
                padding: 0.375rem 0.75rem;
                border-radius: 999px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border: 1.5px solid;
                backdrop-filter: blur(8px);
                transition: all 0.2s ease;
            }

            .badge-status:hover {
                transform: scale(1.05);
            }

            .badge-new {
                background: rgba(239, 68, 68, 0.1);
                border-color: rgba(239, 68, 68, 0.3);
                color: #FCA5A5;
            }

            .badge-in-progress {
                background: rgba(251, 146, 60, 0.1);
                border-color: rgba(251, 146, 60, 0.3);
                color: #FDBA74;
            }

            .badge-won {
                background: rgba(34, 197, 94, 0.1);
                border-color: rgba(34, 197, 94, 0.3);
                color: #86EFAC;
            }

            .badge-closed {
                background: rgba(100, 116, 139, 0.1);
                border-color: rgba(100, 116, 139, 0.3);
                color: #CBD5E1;
            }

            /* ===== INDICADORES DE PRIORIDAD ===== */
            .priority-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }

            .priority-high {
                background: #FF6B6B;
                box-shadow: 0 0 8px rgba(255, 107, 107, 0.5);
            }

            .priority-medium {
                background: #FFB800;
                box-shadow: 0 0 8px rgba(255, 184, 0, 0.5);
            }

            .priority-low {
                background: #51CF66;
                box-shadow: 0 0 8px rgba(81, 207, 102, 0.5);
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }

            /* ===== STAT CARD ===== */
            .stat-card {
                background: var(--glass-bg);
                backdrop-filter: var(--glass-blur);
                border: 1px solid var(--glass-border);
                border-radius: 12px;
                padding: 1rem;
                transition: all 0.3s ease;
                position: relative;
            }

            .stat-card::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .stat-card:hover {
                border-color: rgba(59, 130, 246, 0.3);
                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.1);
            }

            .stat-card:hover::after {
                opacity: 1;
            }

            .stat-value {
                font-size: 1.875rem;
                font-weight: 700;
                color: var(--accent-primary);
                letter-spacing: -0.02em;
            }

            .stat-label {
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: var(--text-tertiary);
                margin-bottom: 0.5rem;
            }

            /* ===== ALERTS ===== */
            .alert-base {
                border-radius: 12px;
                padding: 1rem;
                font-size: 0.9rem;
                border: 1px solid;
                backdrop-filter: blur(8px);
                animation: slideIn 0.3s ease;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-8px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .alert-success {
                background: rgba(34, 197, 94, 0.1);
                border-color: rgba(34, 197, 94, 0.3);
                color: #86EFAC;
            }

            .alert-error {
                background: rgba(239, 68, 68, 0.1);
                border-color: rgba(239, 68, 68, 0.3);
                color: #FCA5A5;
            }

            .alert-info {
                background: rgba(59, 130, 246, 0.1);
                border-color: rgba(59, 130, 246, 0.3);
                color: #93C5FD;
            }

            /* ===== DIVIDERS ===== */
            hr {
                border: none;
                height: 1px;
                background: var(--glass-border);
                margin: 1.5rem 0;
            }

            /* ===== HEADER ===== */
            .header-hero {
                background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
                padding: 1.5rem 2rem;
                border-radius: 12px;
                margin-bottom: 1.5rem;
                box-shadow: 0 20px 40px rgba(59, 130, 246, 0.2);
                position: relative;
                overflow: hidden;
            }

            .header-hero::before {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 200px;
                height: 200px;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                border-radius: 50%;
                opacity: 0.5;
            }

            .header-hero h1 {
                color: white;
                margin: 0;
                font-size: 1.75rem;
                position: relative;
            }

            .header-hero p {
                color: rgba(255, 255, 255, 0.9);
                margin: 0.5rem 0 0 0;
                font-size: 0.95rem;
                position: relative;
            }

            /* ===== POPOVER CUSTOMIZADO ===== */
            [role="dialog"] {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--glass-border) !important;
                border-radius: 16px !important;
                backdrop-filter: var(--glass-blur) !important;
            }

            /* ===== MODAL DIALOG ===== */
            [role="alertdialog"] {
                background: var(--glass-bg) !important;
                border: 1px solid var(--glass-border) !important;
                border-radius: 16px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
            }

            /* ===== INPUT FIELDS ===== */
            input, textarea, select {
                background: rgba(15, 23, 42, 0.5) !important;
                border: 1px solid var(--glass-border) !important;
                border-radius: 8px !important;
                color: var(--text-primary) !important;
                padding: 0.75rem 1rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
            }

            input:focus, textarea:focus, select:focus {
                outline: none !important;
                border-color: var(--accent-primary) !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            }

            /* ===== Z-INDEX ===== */
            [data-testid="widgetLabelHelpIcon"] {
                color: var(--text-tertiary);
            }
        </style>
        """, unsafe_allow_html=True)


class ComponentStyles:
    """Componentes SaaS Pro con Glassmorphism"""
    
    @staticmethod
    def ticket_card(ticket_number: str, title: str, status: str, priority: str = "Medium") -> str:
        """Tarjeta de ticket con efecto glass y indicador de prioridad"""
        status_map = {
            "new": ("badge-new", "🆕 Nuevo"),
            "in_progress": ("badge-in-progress", "⏳ En progreso"),
            "won": ("badge-won", "✅ Ganado"),
            "closed": ("badge-closed", "🔒 Cerrado")
        }
        
        priority_map = {
            "High": ("priority-high", "🔴 Alta"),
            "Medium": ("priority-medium", "🟠 Media"),
            "Low": ("priority-low", "🟢 Baja")
        }
        
        badge_class, badge_text = status_map.get(status, status_map["new"])
        priority_class, priority_text = priority_map.get(priority, priority_map["Medium"])
        
        return f"""
        <div class="ticket-card" style="cursor: pointer;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                <div>
                    <span style="font-size: 0.75rem; color: #94A3B8; font-family: 'Monaco', monospace; font-weight: 500;">#{ticket_number}</span>
                </div>
                <div style="display: flex; gap: 0.25rem; align-items: center;">
                    <span class="priority-indicator {priority_class}" title="{priority_text}"></span>
                </div>
            </div>
            
            <h4 style="margin: 0.75rem 0; font-size: 0.95rem; font-weight: 600; color: #F1F5F9; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                {title}
            </h4>
            
            <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem;">
                <span class="badge-status {badge_class}">{badge_text}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def stat_card(title: str, value: str, trend: str = "+0%", icon: str = "📊") -> str:
        """Tarjeta de estadística minimalista con tendencia"""
        trend_color = "#51CF66" if trend.startswith("+") else "#FF6B6B"
        
        return f"""
        <div class="stat-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <p class="stat-label">{title}</p>
                    <div style="display: flex; align-items: baseline; gap: 0.75rem;">
                        <span class="stat-value">{value}</span>
                        <span style="font-size: 0.75rem; color: {trend_color}; font-weight: 600;">{trend}</span>
                    </div>
                </div>
                <span style="font-size: 1.75rem; opacity: 0.4;">{icon}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def alert_success(message: str) -> str:
        """Alerta de éxito con animación"""
        return f'<div class="alert-base alert-success"><i class="fas fa-check-circle"></i> {message}</div>'
    
    @staticmethod
    def alert_error(message: str) -> str:
        """Alerta de error con animación"""
        return f'<div class="alert-base alert-error"><i class="fas fa-exclamation-circle"></i> {message}</div>'
    
    @staticmethod
    def alert_info(message: str) -> str:
        """Alerta informativa"""
        return f'<div class="alert-base alert-info"><i class="fas fa-info-circle"></i> {message}</div>'
    
    @staticmethod
    def action_button(label: str, emoji: str = "✨", full_width: bool = False) -> str:
        """Botón minimalista SaaS"""
        width = "width: 100%;" if full_width else ""
        return f'<button class="btn-primary" style="{width}"><i class="fas fa-{emoji}"></i> {label}</button>'
    
    @staticmethod
    def header_hero(title: str, subtitle: str = "", emoji: str = "🎫") -> str:
        """Header hero con gradiente"""
        return f"""
        <div class="header-hero">
            <h1>{emoji} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """
    
    @staticmethod
    def container_glass(content: str) -> str:
        """Contenedor con efecto glass"""
        return f'<div class="glass-container">{content}</div>'
