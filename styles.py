"""
Sistema de estilos minimalista basado en Tailwind CSS.
"""

import streamlit as st


class StyleManager:
    """Gestor de estilos Tailwind CSS - Minimalista y profesional"""
    
    @staticmethod
    @st.cache_data
    def inject_all():
        """Inyecta Tailwind CSS y estilos minimalistas"""
        st.markdown("""
        <link href="https://cdn.tailwindcss.com" rel="stylesheet">
        <style>
            * {
                scrollbar-width: thin;
                scrollbar-color: #3B82F6 #1E293B;
            }
            ::-webkit-scrollbar {
                width: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #1E293B;
            }
            ::-webkit-scrollbar-thumb {
                background: #3B82F6;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #60A5FA;
            }
            
            html {
                background: #0F172A;
            }
            
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0F172A 0%, #1A1F3A 100%);
            }
            
            [data-testid="stSidebar"] {
                background: #1E293B;
                border-right: 1px solid #334155;
            }
        </style>
        """, unsafe_allow_html=True)


class ComponentStyles:
    """Componentes minimalistas con Tailwind"""
    
    @staticmethod
    def ticket_card(ticket_number: str, title: str, status: str) -> str:
        """Tarjeta de ticket"""
        status_map = {
            "new": ("bg-red-500/10 text-red-400 border-red-500/20", "🆕"),
            "in_progress": ("bg-amber-500/10 text-amber-400 border-amber-500/20", "⏳"),
            "won": ("bg-emerald-500/10 text-emerald-400 border-emerald-500/20", "✅"),
            "closed": ("bg-slate-500/10 text-slate-400 border-slate-500/20", "🔒")
        }
        color, icon = status_map.get(status, status_map["new"])
        
        return f"""
        <div class="bg-slate-950 border border-slate-700 rounded-lg p-4 hover:border-blue-500/50 hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300">
            <div class="flex justify-between items-center mb-3">
                <span class="text-xs font-mono text-slate-500">#{ticket_number}</span>
                <span class="px-2 py-1 rounded text-xs font-bold border {color}">
                    {icon}
                </span>
            </div>
            <p class="text-sm text-slate-200 line-clamp-2">{title}</p>
        </div>
        """
    
    @staticmethod
    def stat_card(title: str, value: str, icon: str = "📊") -> str:
        """Tarjeta de estadística"""
        return f"""
        <div class="bg-slate-950 border border-slate-700 rounded-lg p-4 hover:border-blue-500/50 transition-all duration-300">
            <div class="flex justify-between">
                <div>
                    <p class="text-xs text-slate-500 uppercase tracking-wider font-semibold">{title}</p>
                    <p class="text-2xl font-bold text-slate-100 mt-1">{value}</p>
                </div>
                <span class="text-3xl opacity-20">{icon}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def alert_success(message: str) -> str:
        """Alerta de éxito"""
        return f'<div class="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-3 text-emerald-400 text-sm">✅ {message}</div>'
    
    @staticmethod
    def alert_error(message: str) -> str:
        """Alerta de error"""
        return f'<div class="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">❌ {message}</div>'
