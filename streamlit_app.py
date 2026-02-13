import streamlit as st
import pandas as pd
from datetime import datetime
import traceback
from typing import Optional, Dict, Any
from dataclasses import dataclass

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
st.set_page_config(
    page_title="Dashboard de Tickets",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# TAILWIND CSS VÍA CDN - DISEÑO LIMPIO
# ============================================================================
st.markdown("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Ocultar elementos por defecto de Streamlit */
        #MainMenu, footer, header {
            display: none !important;
        }
        
        .stApp {
            background: #0A0C10 !important;
        }
        
        /* Personalización de scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: #111316;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #2A2C30;
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #404448;
        }
        
        /* Ocultar etiquetas de Streamlit que no queremos */
        .st-emotion-cache-16idsys, .st-emotion-cache-1dp5vir {
            display: none !important;
        }
    </style>
</head>
<body>
""", unsafe_allow_html=True)

# ============================================================================
# COMPONENTES REUTILIZABLES CON TAILWIND
# ============================================================================

def tailwind_card(content: str, class_name: str = ""):
    """Wrapper para tarjetas con Tailwind"""
    return f"""
    <div class="bg-[#16181C] border border-[#2A2C30] rounded-xl p-4 hover:border-[#404448] hover:shadow-lg hover:shadow-black/40 transition-all duration-200 {class_name}">
        {content}
    </div>
    """

def tailwind_badge(status: str):
    """Badges con Tailwind"""
    badges = {
        "new": {"bg": "bg-red-500/10", "text": "text-red-400", "border": "border-red-500/20", "label": "NUEVO"},
        "in_progress": {"bg": "bg-yellow-500/10", "text": "text-yellow-400", "border": "border-yellow-500/20", "label": "PROGRESO"},
        "won": {"bg": "bg-green-500/10", "text": "text-green-400", "border": "border-green-500/20", "label": "GANADO"},
        "closed": {"bg": "bg-gray-500/10", "text": "text-gray-400", "border": "border-gray-500/20", "label": "CERRADO"}
    }
    style = badges.get(status.lower(), badges["new"])
    return f"""
    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium {style['bg']} {style['text']} border {style['border']}">
        {style['label']}
    </span>
    """

def tailwind_priority_badge(priority: str):
    """Badge de prioridad con Tailwind"""
    priorities = {
        "High": {"bg": "bg-red-500/10", "text": "text-red-400", "border": "border-red-500/20", "label": "Alta"},
        "Medium": {"bg": "bg-yellow-500/10", "text": "text-yellow-400", "border": "border-yellow-500/20", "label": "Media"},
        "Low": {"bg": "bg-green-500/10", "text": "text-green-400", "border": "border-green-500/20", "label": "Baja"}
    }
    style = priorities.get(priority, priorities["Medium"])
    return f"""
    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium {style['bg']} {style['text']} border {style['border']}">
        {style['label']}
    </span>
    """

def tailwind_metric(label: str, value: str, change: str = None):
    """Métrica con Tailwind"""
    return f"""
    <div class="bg-[#16181C] border border-[#2A2C30] rounded-lg p-4 hover:border-[#404448] transition-all">
        <div class="text-[#8B8E94] text-xs font-medium uppercase tracking-wider">{label}</div>
        <div class="text-[#E8E9EA] text-2xl font-semibold mt-1">{value}</div>
        {f'<div class="text-[#8B8E94] text-xs mt-1">{change}</div>' if change else ''}
    </div>
    """

# ============================================================================
# CREDENCIALES Y FUNCIONES SUPABASE
# ============================================================================

def get_supabase_connection():
    try:
        from supabase import create_client
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        return None

def test_connection():
    try:
        client = get_supabase_connection()
        if not client:
            return False, "No se pudo inicializar", None
        response = client.table("opportunities").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        return True, "Conexión exitosa", count
    except Exception as e:
        return False, f"Error de conexión", None

def fetch_tickets(status_filter=None, priority_filter=None):
    try:
        client = get_supabase_connection()
        if not client:
            return pd.DataFrame()
        
        query = client.table("opportunities").select(
            "id, ticket_number, title, description, status, priority, notes, created_at, recording_id"
        )
        
        if status_filter and status_filter != "Todos":
            query = query.eq("status", status_filter)
        if priority_filter and priority_filter != "Todos":
            query = query.eq("priority", priority_filter)
            
        response = query.execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            df.columns = df.columns.str.lower()
            return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def update_ticket(ticket_id: int, status: str, notes: str, priority: str = None) -> bool:
    try:
        client = get_supabase_connection()
        if not client:
            return False
        
        data = {"status": status, "notes": notes}
        if priority:
            data["priority"] = priority
            
        client.table("opportunities").update(data).eq("id", ticket_id).execute()
        return True
    except Exception as e:
        return False

# ============================================================================
# COMPONENTES DE UI CON TAILWIND
# ============================================================================

def render_ticket_card(ticket: Dict[str, Any]):
    """Renderiza una tarjeta de ticket con Tailwind"""
    ticket_id = ticket.get("id")
    ticket_num = ticket.get("ticket_number", "N/A")
    title = ticket.get("title", "Sin título")
    status = ticket.get("status", "new").lower()
    priority = ticket.get("priority", "Medium")
    
    card_content = f"""
    <div class="flex flex-col h-full">
        <div class="flex justify-between items-start mb-3">
            <span class="text-[#5E6269] text-xs font-mono">#{ticket_num}</span>
            <div class="flex items-center gap-2">
                {tailwind_priority_badge(priority)}
                {tailwind_badge(status)}
            </div>
        </div>
        <div class="text-[#E8E9EA] text-sm font-medium line-clamp-2 mb-4 flex-grow">
            {title}
        </div>
    </div>
    """
    
    return tailwind_card(card_content)

def render_modal_content(ticket: Dict[str, Any]):
    """Renderiza el contenido del modal con Tailwind"""
    ticket_id = ticket.get("id")
    title = ticket.get("title", "Sin título")
    description = ticket.get("description", "").strip()
    current_status = ticket.get("status", "new").lower()
    current_priority = ticket.get("priority", "Medium")
    notes = ticket.get("notes", "") or ""
    created_at = ticket.get("created_at", "")[:10] if ticket.get("created_at") else "N/A"
    
    status_options = {
        "new": "Nuevo",
        "in_progress": "En progreso",
        "closed": "Cerrado",
        "won": "Ganado"
    }
    
    priority_options = ["Low", "Medium", "High"]
    priority_labels = ["Baja", "Media", "Alta"]
    
    # Usar componentes nativos de Streamlit para el formulario
    with st.container():
        # Header con Tailwind
        st.markdown(f"""
        <div class="flex justify-between items-center pb-4 border-b border-[#2A2C30] mb-6">
            <div>
                <h2 class="text-[#E8E9EA] text-xl font-semibold">{title}</h2>
                <p class="text-[#5E6269] text-xs mt-1">Creado: {created_at}</p>
            </div>
            {tailwind_badge(current_status)}
        </div>
        """, unsafe_allow_html=True)
        
        # Descripción
        st.markdown("""
        <div class="mb-6">
            <p class="text-[#8B8E94] text-xs font-semibold uppercase tracking-wider mb-2">Descripción</p>
            <div class="bg-[#111316] border border-[#2A2C30] rounded-lg p-4 text-[#E8E9EA] text-sm whitespace-pre-wrap">
        """, unsafe_allow_html=True)
        
        if description:
            st.markdown(f"{description}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("Sin descripción</div></div>", unsafe_allow_html=True)
        
        # Formulario de edición
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="text-[#8B8E94] text-xs font-semibold uppercase tracking-wider mb-2">Estado</p>', unsafe_allow_html=True)
            status_index = list(status_options.keys()).index(current_status) if current_status in status_options else 0
            new_status_label = st.selectbox(
                "Estado",
                list(status_options.values()),
                index=status_index,
                key=f"modal_status_{ticket_id}",
                label_visibility="collapsed"
            )
            status_map_reverse = {v: k for k, v in status_options.items()}
            new_status = status_map_reverse[new_status_label]
        
        with col2:
            st.markdown('<p class="text-[#8B8E94] text-xs font-semibold uppercase tracking-wider mb-2">Prioridad</p>', unsafe_allow_html=True)
            priority_index = priority_options.index(current_priority) if current_priority in priority_options else 1
            new_priority_label = st.selectbox(
                "Prioridad",
                priority_labels,
                index=priority_index,
                key=f"modal_priority_{ticket_id}",
                label_visibility="collapsed"
            )
            priority_map = {v: k for k, v in zip(priority_labels, priority_options)}
            new_priority = priority_map[new_priority_label]
        
        # Notas
        st.markdown('<p class="text-[#8B8E94] text-xs font-semibold uppercase tracking-wider mb-2 mt-4">Notas</p>', unsafe_allow_html=True)
        new_notes = st.text_area(
            "Notas",
            value=notes,
            placeholder="⭐️ Tema / 📌 Descripción / 👤 Mencionado / 💬 Contexto / 📊 Confianza",
            key=f"modal_notes_{ticket_id}",
            label_visibility="collapsed",
            height=150
        )
        
        # Botones
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Guardar cambios", key=f"modal_save_{ticket_id}", type="primary", use_container_width=True):
                if update_ticket(ticket_id, new_status, new_notes, new_priority):
                    st.success("✅ Ticket actualizado correctamente")
                    st.session_state.modal_ticket = None
                    st.rerun()
        
        with col3:
            if st.button("Cancelar", key=f"modal_cancel_{ticket_id}", use_container_width=True):
                st.session_state.modal_ticket = None
                st.rerun()

@st.dialog("Editar ticket", width="large")
def edit_ticket_modal(ticket_dict: Dict[str, Any]):
    """Modal de edición con Tailwind"""
    render_modal_content(ticket_dict)

def render_ticket_grid(tickets_df: pd.DataFrame):
    """Grid de tickets con Tailwind"""
    if tickets_df.empty:
        st.info("No hay tickets disponibles")
        return
    
    # Crear grid con Tailwind
    st.markdown("""
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    """, unsafe_allow_html=True)
    
    for _, ticket in tickets_df.iterrows():
        ticket_dict = ticket.to_dict()
        ticket_id = ticket_dict.get("id")
        
        # Renderizar tarjeta
        st.markdown(render_ticket_card(ticket_dict), unsafe_allow_html=True)
        
        # Botón de edición con Tailwind
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✏️ Editar", key=f"edit_btn_{ticket_id}", use_container_width=True):
                st.session_state.modal_ticket = ticket_dict
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def main():
    # Header
    st.markdown("""
    <div class="mb-8">
        <h1 class="text-[#E8E9EA] text-3xl font-bold tracking-tight">Dashboard</h1>
        <p class="text-[#8B8E94] text-sm mt-1">Gestión de oportunidades y tickets</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con Tailwind
    with st.sidebar:
        st.markdown("""
        <div class="p-4">
            <h2 class="text-[#E8E9EA] text-lg font-semibold mb-6">Filtros</h2>
        """, unsafe_allow_html=True)
        
        # Obtener todos los tickets para estadísticas
        all_tickets = fetch_tickets()
        
        # Filtros
        status_filter = st.selectbox(
            "Estado",
            ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
            key="sidebar_status"
        )
        
        priority_filter = st.selectbox(
            "Prioridad",
            ["Todos", "Baja", "Media", "Alta"],
            key="sidebar_priority"
        )
        
        # Mapeo de filtros
        status_map = {
            "Todos": "Todos",
            "Nuevo": "new",
            "En progreso": "in_progress",
            "Cerrado": "closed",
            "Ganado": "won"
        }
        priority_map = {
            "Todos": "Todos",
            "Baja": "Low",
            "Media": "Medium",
            "Alta": "High"
        }
        
        selected_status = status_map[status_filter]
        selected_priority = priority_map[priority_filter]
        
        # Botón actualizar con Tailwind
        st.markdown("""
        <style>
            div.stButton > button:first-child {
                background-color: #3B82F6 !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                transition: all 0.2s !important;
            }
            div.stButton > button:first-child:hover {
                background-color: #2563EB !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Actualizar", key="refresh_btn", use_container_width=True):
            st.rerun()
        
        # Estadísticas con Tailwind
        if not all_tickets.empty:
            st.markdown("""
            <div class="mt-8">
                <h3 class="text-[#E8E9EA] text-sm font-semibold uppercase tracking-wider mb-4">Estadísticas</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(tailwind_metric("Total", str(len(all_tickets))), unsafe_allow_html=True)
            with col2:
                nuevos = len(all_tickets[all_tickets["status"] == "new"])
                st.markdown(tailwind_metric("Nuevos", str(nuevos)), unsafe_allow_html=True)
            with col3:
                ganados = len(all_tickets[all_tickets["status"] == "won"])
                st.markdown(tailwind_metric("Ganados", str(ganados)), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Grid de tickets
    tickets = fetch_tickets(
        status_filter=selected_status if selected_status != "Todos" else None,
        priority_filter=selected_priority if selected_priority != "Todos" else None
    )
    
    if tickets.empty:
        st.markdown("""
        <div class="bg-[#16181C] border border-[#2A2C30] rounded-lg p-8 text-center">
            <p class="text-[#8B8E94]">No hay tickets con los filtros seleccionados.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="flex justify-between items-center mb-4">
            <p class="text-[#8B8E94] text-sm">{len(tickets)} tickets encontrados</p>
        </div>
        """, unsafe_allow_html=True)
        
        render_ticket_grid(tickets)
    
    # Modal
    if "modal_ticket" in st.session_state and st.session_state.modal_ticket:
        edit_ticket_modal(st.session_state.modal_ticket)
        st.session_state.modal_ticket = None
    
    # Diagnóstico
    with st.expander("🔧 Diagnóstico del sistema"):
        success, msg, count = test_connection()
        
        if success:
            st.success(f"✅ {msg} — {count} registros")
        else:
            st.error(f"❌ {msg}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Ver opportunities", key="debug_opps"):
                client = get_supabase_connection()
                if client:
                    data = client.table("opportunities").select("*").limit(3).execute().data
                    if data:
                        st.dataframe(pd.DataFrame(data), use_container_width=True)
        with col2:
            if st.button("🎙️ Ver recordings", key="debug_recs"):
                client = get_supabase_connection()
                if client:
                    data = client.table("recordings").select("*").limit(3).execute().data
                    if data:
                        st.dataframe(pd.DataFrame(data), use_container_width=True)

if __name__ == "__main__":
    main()