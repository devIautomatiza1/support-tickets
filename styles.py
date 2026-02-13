"""
Sistema de estilos "Beautiful SaaS" - Inspirado en Linear, Vercel y Raycast.
Enfoque: Minimalismo extremo, tipograf�a perfecta y micro-interacciones.
"""

import streamlit as st


class StyleManager:
    """Gestor de estilos - Est�tica Linear"""
    
    @staticmethod
    @st.cache_data
    def inject_all():
        """Inyecta el CSS definitivo"""
        st.markdown("""
        <link href="https://cdn.tailwindcss.com" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --app-bg: #08090a;
                --card-bg: #111214;
                --card-hover: #16171a;
                --border: rgba(255, 255, 255, 0.08);
                --text-main: #eeeeee;
                --text-muted: #888888;
                --accent: #5e6ad2; /* Linear blue */
                --accent-glow: rgba(94, 106, 210, 0.15);
            }

            * {
                font-family: "Inter", -apple-system, sans-serif;
            }

            /* Main App View */
            [data-testid="stAppViewContainer"] {
                background-color: var(--app-bg);
                color: var(--text-main);
            }

            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #0c0d0e !important;
                border-right: 1px solid var(--border) !important;
            }

            /* Clear default padding */
            .main .block-container {
                padding-top: 2rem !important;
                max-width: 1200px !important;
            }

            /* The Perfect Ticket Card */
            .ticket-card {
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1.25rem;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                display: flex;
                flex-direction: column;
                gap: 12px;
                height: 100%;
            }

            .ticket-card:hover {
                background: var(--card-hover);
                border-color: rgba(255, 255, 255, 0.15);
                transform: translateY(-2px);
                box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
            }

            .ticket-top {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .id-label {
                font-family: ui-monospace, SFMono-Regular, monospace;
                font-size: 11px;
                color: var(--text-muted);
                background: rgba(255,255,255,0.03);
                padding: 2px 6px;
                border-radius: 4px;
                border: 1px solid var(--border);
            }

            .ticket-title {
                font-size: 15px;
                font-weight: 500;
                color: var(--text-main);
                margin: 0;
                line-height: 1.4;
                letter-spacing: -0.01em;
            }

            /* Badges */
            .tag-row {
                display: flex;
                gap: 8px;
                align-items: center;
                margin-top: 4px;
            }

            .badge {
                font-size: 11px;
                font-weight: 500;
                padding: 3px 8px;
                border-radius: 6px;
                display: flex;
                align-items: center;
                gap: 6px;
            }

            .badge-status-new { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
            .badge-status-progress { background: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.2); }
            .badge-status-won { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
            .badge-status-closed { background: rgba(107, 114, 128, 0.1); color: #9ca3af; border: 1px solid rgba(107, 114, 128, 0.2); }

            .priority-pill {
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 11px;
                color: var(--text-muted);
                font-weight: 500;
            }

            .dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
            }
            .dot-high { background-color: #ef4444; box-shadow: 0 0 8px rgba(239, 68, 68, 0.5); }
            .dot-medium { background-color: #f59e0b; }
            .dot-low { background-color: #10b981; }

            /* Streamlit overrides */
            .stButton > button {
                border-radius: 8px !important;
                background-color: rgba(255,255,255,0.03) !important;
                border: 1px solid var(--border) !important;
                color: var(--text-main) !important;
                font-size: 13px !important;
                font-weight: 500 !important;
                padding: 0.5rem 1rem !important;
                transition: all 0.2s !important;
            }
            .stButton > button:hover {
                border-color: var(--accent) !important;
                background-color: var(--accent-glow) !important;
                transform: scale(1.02);
            }
            
            /* Metric overrides */
            div[data-testid="stMetricValue"] > div {
                font-size: 28px !important;
                font-weight: 600 !important;
                letter-spacing: -0.03em !important;
            }

            /* Custom Header Hero */
            .hero-section {
                margin-bottom: 40px;
            }
            .hero-section h1 {
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -0.04em;
                margin-bottom: 8px;
            }
            .hero-section p {
                color: var(--text-muted);
                font-size: 16px;
                max-width: 600px;
            }
        </style>
        """, unsafe_allow_html=True)


class ComponentStyles:
    """Componentes refinados"""
    
    @staticmethod
    def ticket_card(ticket_number: str, title: str, status: str, priority: str = "Medium") -> str:
        """La tarjeta definitiva"""
        
        status_classes = {
            "new": "badge-status-new",
            "in_progress": "badge-status-progress",
            "won": "badge-status-won",
            "closed": "badge-status-closed"
        }
        status_labels = {
            "new": "Nuevo",
            "in_progress": "En Curso",
            "won": "Cerrado (Ganado)",
            "closed": "Cerrado"
        }
        
        priority_dots = {
            "High": "dot-high",
            "Medium": "dot-medium",
            "Low": "dot-low"
        }
        
        s_class = status_classes.get(status, "badge-status-new")
        s_label = status_labels.get(status, "Nuevo")
        p_dot = priority_dots.get(priority, "dot-medium")
        
        return f"""
        <div class="ticket-card">
            <div class="ticket-top">
                <span class="id-label">#{ticket_number}</span>
                <div class="priority-pill">
                    <div class="dot {p_dot}"></div>
                    {priority}
                </div>
            </div>
            <h3 class="ticket-title">{title}</h3>
            <div class="tag-row">
                <span class="badge {s_class}">
                    <i class="fa-solid fa-circle" style="font-size: 5px; opacity: 0.8;"></i>
                    {s_label}
                </span>
            </div>
        </div>
        """
    
    @staticmethod
    def header_hero(title: str, subtitle: str) -> str:
        """Hero minimalista"""
        return f"""
        <div class="hero-section">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """
