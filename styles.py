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
            /* ===== TEMA GLOBAL PREMIUM ===== */
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
                --info: #3b82f6;
            }

            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html, body, [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at 20% 30%, #0f1117, #0a0c12);
                color: var(--text-primary);
            }

            /* ===== SCROLLBAR CUSTOM ===== */
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            ::-webkit-scrollbar-track {
                background: transparent;
            }
            ::-webkit-scrollbar-thumb {
                background: rgba(59, 130, 246, 0.3);
                border-radius: 3px;
                transition: all 0.3s;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(59, 130, 246, 0.6);
            }

            /* ===== SIDEBAR PREMIUM ===== */
            [data-testid="stSidebar"] {
                background: rgba(10, 12, 18, 0.8) !important;
                backdrop-filter: blur(20px) !important;
                border-right: 1px solid var(--border) !important;
            }

            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                gap: 0.5rem !important;
            }

            /* ===== TIPOGRAFÍA PREMIUM ===== */
            h1, h2, h3, h4, h5, h6 {
                font-weight: 600;
                letter-spacing: -0.02em;
                color: var(--text-primary);
            }

            p, span, div, li {
                line-height: 1.6;
                letter-spacing: -0.01em;
            }

            /* ===== GLASSMORPHISM CORE ===== */
            .glass {
                background: rgba(26, 28, 35, 0.6);
                backdrop-filter: blur(16px);
                border: 1px solid var(--border);
                border-radius: 16px;
                transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            }

            .glass:hover {
                background: rgba(26, 28, 35, 0.8);
                border-color: rgba(59, 130, 246, 0.3);
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
            }

            /* ===== TARJETAS DE TICKETS PREMIUM ===== */
            .premium-ticket-card {
                background: linear-gradient(145deg, rgba(26, 28, 35, 0.6), rgba(26, 28, 35, 0.4));
                backdrop-filter: blur(16px);
                border: 1.5px solid rgba(59, 130, 246, 0.15);
                border-radius: 20px;
                padding: 1.5rem;
                transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            }

            .premium-ticket-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, var(--accent), var(--accent-light), transparent);
                opacity: 0;
                transition: opacity 0.4s;
            }

            .premium-ticket-card:hover {
                border-color: rgba(59, 130, 246, 0.4);
                background: linear-gradient(145deg, rgba(26, 28, 35, 0.8), rgba(26, 28, 35, 0.6));
                box-shadow: 0 12px 48px rgba(59, 130, 246, 0.25);
                transform: translateY(-4px);
            }

            .premium-ticket-card:hover::before {
                opacity: 1;
            }

            .ticket-header-premium {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .ticket-number-premium {
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--text-muted);
                font-family: 'SF Mono', 'Monaco', monospace;
                letter-spacing: 0.5px;
                padding: 0.25rem 0.75rem;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 20px;
            }

            .ticket-title-premium {
                font-size: 1.125rem;
                font-weight: 600;
                color: var(--text-primary);
                line-height: 1.5;
                margin: 0.75rem 0;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }

            .ticket-description-premium {
                font-size: 0.85rem;
                color: var(--text-muted);
                line-height: 1.6;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                margin-bottom: 1.25rem;
            }

            .ticket-footer-premium {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 1rem;
            }

            .ticket-date-premium {
                font-size: 0.7rem;
                color: var(--text-muted);
                font-weight: 500;
            }

            /* ===== BADGES PREMIUM ===== */
            .badge-premium {
                display: inline-flex;
                align-items: center;
                gap: 0.375rem;
                padding: 0.375rem 1rem;
                border-radius: 30px;
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border: 1.5px solid;
                backdrop-filter: blur(8px);
                transition: all 0.3s;
            }

            .badge-premium:hover {
                transform: scale(1.05);
                filter: brightness(1.2);
            }

            .badge-premium-new {
                background: rgba(239, 68, 68, 0.15);
                border-color: rgba(239, 68, 68, 0.4);
                color: #fecaca;
            }

            .badge-premium-in-progress {
                background: rgba(245, 158, 11, 0.15);
                border-color: rgba(245, 158, 11, 0.4);
                color: #fed7aa;
            }

            .badge-premium-won {
                background: rgba(16, 185, 129, 0.15);
                border-color: rgba(16, 185, 129, 0.4);
                color: #a7f3d0;
            }

            .badge-premium-closed {
                background: rgba(100, 116, 139, 0.15);
                border-color: rgba(100, 116, 139, 0.4);
                color: #e2e8f0;
            }

            /* ===== INDICADOR DE PRIORIDAD PREMIUM ===== */
            .priority-indicator {
                display: flex;
                align-items: center;
                gap: 0.375rem;
            }

            .priority-dot-premium {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                animation: pulse-glow 2s infinite;
            }

            .priority-high {
                background: #ff5757;
                box-shadow: 0 0 16px rgba(255, 87, 87, 0.4);
            }

            .priority-medium {
                background: #ffa500;
                box-shadow: 0 0 16px rgba(255, 165, 0, 0.4);
            }

            .priority-low {
                background: #52d383;
                box-shadow: 0 0 16px rgba(82, 211, 131, 0.4);
            }

            @keyframes pulse-glow {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }

            /* ===== STAT CARDS PREMIUM ===== */
            .stat-card-premium {
                background: linear-gradient(145deg, rgba(37, 99, 235, 0.1), rgba(37, 99, 235, 0.05));
                backdrop-filter: blur(16px);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 16px;
                padding: 1.25rem;
                transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
                position: relative;
                overflow: hidden;
            }

            .stat-card-premium::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, var(--accent), transparent);
                opacity: 0;
                transition: opacity 0.4s;
            }

            .stat-card-premium:hover {
                background: linear-gradient(145deg, rgba(37, 99, 235, 0.15), rgba(37, 99, 235, 0.08));
                border-color: rgba(59, 130, 246, 0.3);
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
                transform: translateY(-2px);
            }

            .stat-card-premium:hover::after {
                opacity: 1;
            }

            .stat-label-premium {
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: var(--text-muted);
                margin-bottom: 0.5rem;
            }

            .stat-value-premium {
                font-size: 1.75rem;
                font-weight: 800;
                background: linear-gradient(135deg, var(--accent-light), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                line-height: 1.2;
            }

            .stat-trend-premium {
                font-size: 0.7rem;
                font-weight: 600;
                color: var(--success);
                background: rgba(16, 185, 129, 0.1);
                padding: 0.25rem 0.5rem;
                border-radius: 20px;
            }

            /* ===== ALERTS PREMIUM ===== */
            .alert-premium {
                border-radius: 12px;
                padding: 1rem 1.25rem;
                border: 1px solid;
                backdrop-filter: blur(12px);
                animation: slideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }

            .alert-success-premium {
                background: rgba(16, 185, 129, 0.1);
                border-color: rgba(16, 185, 129, 0.3);
                color: #a7f3d0;
            }

            .alert-error-premium {
                background: rgba(239, 68, 68, 0.1);
                border-color: rgba(239, 68, 68, 0.3);
                color: #fecaca;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* ===== BOTONES PREMIUM ===== */
            .stButton > button {
                background: linear-gradient(135deg, var(--accent), var(--accent-dark)) !important;
                border: none !important;
                color: white !important;
                font-weight: 600 !important;
                font-size: 0.85rem !important;
                padding: 0.5rem 1rem !important;
                border-radius: 10px !important;
                transition: all 0.3s !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, var(--accent-light), var(--accent)) !important;
                box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
                transform: translateY(-2px) !important;
            }

            .stButton > button:active {
                transform: translateY(0) !important;
            }

            /* ===== HEADER HERO PREMIUM ===== */
            .header-hero-premium {
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(37, 99, 235, 0.05) 100%);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 24px;
                padding: 2.5rem 2rem;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }

            .header-hero-premium::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -10%;
                width: 400px;
                height: 400px;
                background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
                border-radius: 50%;
                animation: float 20s infinite;
            }

            .header-hero-premium::after {
                content: '';
                position: absolute;
                bottom: -50%;
                left: -10%;
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
                border-radius: 50%;
                animation: float 15s infinite reverse;
            }

            @keyframes float {
                0%, 100% { transform: translate(0, 0); }
                50% { transform: translate(-20px, 20px); }
            }

            .header-hero-premium h1 {
                color: white;
                margin: 0;
                font-size: 2.25rem;
                font-weight: 700;
                position: relative;
                z-index: 1;
            }

            .header-hero-premium p {
                color: rgba(255, 255, 255, 0.8);
                margin: 0.75rem 0 0 0;
                font-size: 1rem;
                position: relative;
                z-index: 1;
            }

            /* ===== MODALES PREMIUM ===== */
            [role="dialog"] {
                background: rgba(15, 17, 23, 0.95) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(59, 130, 246, 0.2) !important;
                border-radius: 24px !important;
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5) !important;
            }

            /* ===== INPUT FIELDS PREMIUM ===== */
            input, textarea, select, [data-testid="stSelectbox"] > div > div {
                background: rgba(10, 12, 18, 0.6) !important;
                border: 1.5px solid var(--border) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                padding: 0.75rem 1rem !important;
                font-size: 0.9rem !important;
                transition: all 0.3s !important;
                font-family: 'Inter', sans-serif !important;
            }

            input:focus, textarea:focus, select:focus, [data-testid="stSelectbox"] > div > div:focus-within {
                outline: none !important;
                border-color: var(--accent) !important;
                background: rgba(10, 12, 18, 0.8) !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
            }

            /* ===== DIVIDERS ===== */
            hr {
                border: none !important;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--border), transparent) !important;
                margin: 2rem 0 !important;
            }

            /* ===== EXPANDER PREMIUM ===== */
            [data-testid="stExpander"] {
                background: rgba(26, 28, 35, 0.4) !important;
                border: 1px solid var(--border) !important;
                border-radius: 16px !important;
                padding: 0.5rem !important;
                backdrop-filter: blur(8px) !important;
            }

            /* ===== TABS PREMIUM ===== */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem;
                background: rgba(10, 12, 18, 0.4);
                padding: 0.25rem;
                border-radius: 40px;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 30px !important;
                padding: 0.5rem 1.25rem !important;
                font-weight: 500 !important;
                color: var(--text-muted) !important;
            }

            .stTabs [aria-selected="true"] {
                background: var(--accent) !important;
                color: white !important;
            }

            /* ===== METRIC CARDS ===== */
            div[data-testid="stMetric"] {
                background: linear-gradient(145deg, rgba(26, 28, 35, 0.6), rgba(26, 28, 35, 0.4));
                backdrop-filter: blur(8px);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 1rem;
            }

            div[data-testid="stMetric"] label {
                color: var(--text-muted) !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }

            div[data-testid="stMetric"] [data-testid="stMetricValue"] {
                color: var(--text-primary) !important;
                font-size: 1.75rem !important;
                font-weight: 700 !important;
            }

            /* ===== RADIO BUTTONS PREMIUM ===== */
            div[role="radiogroup"] {
                background: rgba(10, 12, 18, 0.4);
                padding: 0.25rem;
                border-radius: 40px;
                display: flex;
                gap: 0.25rem;
            }

            div[role="radiogroup"] label {
                border-radius: 30px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                color: var(--text-muted) !important;
                background: transparent !important;
                transition: all 0.3s !important;
            }

            div[role="radiogroup"] label[data-checked="true"] {
                background: var(--accent) !important;
                color: white !important;
            }

            /* ===== POPOVER PREMIUM ===== */
            div[data-testid="stPopover"] {
                background: rgba(15, 17, 23, 0.95) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(59, 130, 246, 0.2) !important;
                border-radius: 16px !important;
                padding: 1rem !important;
            }

            /* ===== ANIMACIONES GLOBALES ===== */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .fade-in {
                animation: fadeIn 0.5s ease;
            }

            .slide-up {
                animation: slideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            }
        </style>
        """, unsafe_allow_html=True)



class ComponentStyles:
    """Componentes renderizados hermosamente"""
    
    @staticmethod
    def premium_ticket_card(ticket_number: str, title: str, description: str, status: str, priority: str = "Medium", date: str = None) -> str:
        """Tarjeta de ticket premium"""
        status_map = {
            "new": ("badge-premium-new", "🆕"),
            "in_progress": ("badge-premium-in-progress", "⏳"),
            "won": ("badge-premium-won", "✅"),
            "closed": ("badge-premium-closed", "🔒")
        }
        
        priority_map = {
            "High": "priority-high",
            "Medium": "priority-medium",
            "Low": "priority-low"
        }
        
        badge_class, badge_emoji = status_map.get(status, status_map["new"])
        priority_class = priority_map.get(priority, priority_map["Medium"])
        
        date_str = f"📅 {date}" if date else ""
        
        return f"""
        <div class="premium-ticket-card slide-up">
            <div class="ticket-header-premium">
                <span class="ticket-number-premium">#{ticket_number}</span>
                <div class="priority-indicator">
                    <span class="priority-dot-premium {priority_class}"></span>
                </div>
            </div>
            <h4 class="ticket-title-premium">{title}</h4>
            <p class="ticket-description-premium">{description}</p>
            <div class="ticket-footer-premium">
                <span class="badge-premium {badge_class}">{badge_emoji}</span>
                <span class="ticket-date-premium">{date_str}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def stat_card(title: str, value: str, trend: str = "+0%", icon: str = "📊") -> str:
        """Tarjeta de estadística premium"""
        return f"""
        <div class="stat-card-premium">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.25rem;">{icon}</span>
                <p class="stat-label-premium">{title}</p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                <span class="stat-value-premium">{value}</span>
                <span class="stat-trend-premium">{trend}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def alert_success(message: str) -> str:
        """Alerta de éxito premium"""
        return f"""
        <div class="alert-premium alert-success-premium">
            <i class="fas fa-check-circle" style="flex-shrink: 0; font-size: 1.25rem;"></i>
            <span>{message}</span>
        </div>
        """
    
    @staticmethod
    def alert_error(message: str) -> str:
        """Alerta de error premium"""
        return f"""
        <div class="alert-premium alert-error-premium">
            <i class="fas fa-exclamation-circle" style="flex-shrink: 0; font-size: 1.25rem;"></i>
            <span>{message}</span>
        </div>
        """
    
    @staticmethod
    def header_hero(title: str, subtitle: str = "") -> str:
        """Header hero premium"""
        return f"""
        <div class="header-hero-premium">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """