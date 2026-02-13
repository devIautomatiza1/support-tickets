"""
Dashboard SaaS Pro de gestión de tickets con Glassmorphism.
Diseño profesional tipo Linear, Holded, Vercel - VERSIÓN PREMIUM
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import random

from styles import StyleManager, ComponentStyles


# Configuración
st.set_page_config(
    page_title="FlowTickets | SaaS Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

StyleManager.inject_all()

# Session state init
if "edit_ticket" not in st.session_state:
    st.session_state.edit_ticket = None
if "search_filter" not in st.session_state:
    st.session_state.search_filter = ""
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "grid"


# ============================================================================
# MODELOS
# ============================================================================

class Status(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    CLOSED = "closed"
    
    @classmethod
    def display_names(cls):
        return {
            cls.NEW: "Nuevo",
            cls.IN_PROGRESS: "En progreso",
            cls.WON: "Ganado",
            cls.CLOSED: "Cerrado"
        }
    
    @classmethod
    def from_display(cls, name: str) -> str:
        inverse = {v: k.value for k, v in cls.display_names().items()}
        return inverse.get(name, cls.NEW.value)
    
    @classmethod
    def colors(cls):
        return {
            cls.NEW: "#ef4444",
            cls.IN_PROGRESS: "#f59e0b",
            cls.WON: "#10b981",
            cls.CLOSED: "#64748b"
        }


class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    
    @classmethod
    def display_names(cls):
        return {cls.LOW: "Baja", cls.MEDIUM: "Media", cls.HIGH: "Alta"}
    
    @classmethod
    def from_display(cls, name: str) -> str:
        inverse = {v: k.value for k, v in cls.display_names().items()}
        return inverse.get(name, cls.MEDIUM.value)
    
    @classmethod
    def colors(cls):
        return {
            cls.LOW: "#52d383",
            cls.MEDIUM: "#ffa500",
            cls.HIGH: "#ff5757"
        }


@dataclass
class Ticket:
    id: int
    ticket_number: str
    title: str
    description: str
    status: str
    priority: str
    notes: str
    created_at: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: Optional[list] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        return cls(
            id=data.get("id"),
            ticket_number=data.get("ticket_number", f"TKT-{random.randint(1000, 9999)}"),
            title=data.get("title", "Sin título"),
            description=data.get("description", "").strip(),
            status=data.get("status", Status.NEW.value).lower(),
            priority=data.get("priority", Priority.MEDIUM.value),
            notes=data.get("notes", "") or "",
            created_at=data.get("created_at"),
            assigned_to=data.get("assigned_to", "Sin asignar"),
            tags=data.get("tags", [])
        )


# ============================================================================
# SERVICIO SUPABASE
# ============================================================================

class SupabaseService:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_client(self):
        if self._client is None:
            try:
                from supabase import create_client
                self._client = create_client(
                    st.secrets["SUPABASE_URL"],
                    st.secrets["SUPABASE_KEY"]
                )
            except Exception as e:
                st.error(f"❌ Error al conectar: {e}")
                return None
        return self._client
    
    def test_connection(self) -> Tuple[bool, str, Optional[int]]:
        try:
            client = self._get_client()
            if not client:
                return False, "No se pudo conectar", None
            response = client.table("opportunities").select("count", count="exact").execute()
            count = response.count if hasattr(response, 'count') else len(response.data)
            return True, "Conexión exitosa", count
        except Exception as e:
            return False, str(e), None
    
    def fetch_tickets(self, status_filter: Optional[str] = None, 
                     priority_filter: Optional[str] = None,
                     search_query: Optional[str] = None) -> pd.DataFrame:
        try:
            client = self._get_client()
            if not client:
                return pd.DataFrame()
            
            query = client.table("opportunities").select(
                "id, ticket_number, title, description, status, priority, notes, created_at"
            )
            
            if status_filter and status_filter != "Todos":
                query = query.eq("status", status_filter)
            if priority_filter and priority_filter != "Todos":
                query = query.eq("priority", priority_filter)
            
            response = query.execute()
            
            if response.data:
                df = pd.DataFrame(response.data)
                df.columns = df.columns.str.lower()
                
                if search_query:
                    search_query = search_query.lower()
                    df = df[
                        df['title'].str.lower().str.contains(search_query, na=False) |
                        df['ticket_number'].str.lower().str.contains(search_query, na=False) |
                        df['description'].str.lower().str.contains(search_query, na=False)
                    ]
                
                return df
            return pd.DataFrame()
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return pd.DataFrame()
    
    def update_ticket(self, ticket_id: int, status: str, notes: str, 
                     priority: Optional[str] = None) -> bool:
        try:
            client = self._get_client()
            if not client:
                return False
            data = {"status": status, "notes": notes}
            if priority:
                data["priority"] = priority
            client.table("opportunities").update(data).eq("id", ticket_id).execute()
            return True
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return False
    
    def get_sample_data(self, table: str, limit: int = 5) -> list:
        try:
            client = self._get_client()
            if not client:
                return []
            response = client.table(table).select("*").limit(limit).execute()
            return response.data or []
        except:
            return []


# ============================================================================
# COMPONENTES UI PREMIUM
# ============================================================================

@st.fragment
def render_metrics_dashboard(tickets_df: pd.DataFrame):
    """Dashboard de métricas premium"""
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    
    total = len(tickets_df) if not tickets_df.empty else 0
    
    with col1:
        st.markdown(ComponentStyles.stat_card(
            "Total Tickets", 
            str(total), 
            f"{total} activos",
            "🎫"
        ), unsafe_allow_html=True)
    
    if not tickets_df.empty:
        new_count = len(tickets_df[tickets_df["status"]=="new"])
        in_progress_count = len(tickets_df[tickets_df["status"]=="in_progress"])
        won_count = len(tickets_df[tickets_df["status"]=="won"])
        high_priority = len(tickets_df[tickets_df["priority"]=="High"])
        
        with col2:
            st.markdown(ComponentStyles.stat_card(
                "Nuevos", 
                str(new_count),
                f"{round(new_count/total*100, 1)}%" if total > 0 else "0%",
                "🆕"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(ComponentStyles.stat_card(
                "En Progreso", 
                str(in_progress_count),
                f"{round(in_progress_count/total*100, 1)}%" if total > 0 else "0%",
                "⏳"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(ComponentStyles.stat_card(
                "Ganados", 
                str(won_count),
                f"+{won_count}",
                "✅"
            ), unsafe_allow_html=True)
        
        with col5:
            st.markdown(ComponentStyles.stat_card(
                "Alta Prioridad", 
                str(high_priority),
                f"{round(high_priority/total*100, 1)}%" if total > 0 else "0%",
                "⚡"
            ), unsafe_allow_html=True)
    else:
        for i in range(4):
            with col2 if i == 0 else col3 if i == 1 else col4 if i == 2 else col5:
                st.markdown(ComponentStyles.stat_card(
                    ["Nuevos", "En Progreso", "Ganados", "Alta Prioridad"][i],
                    "0",
                    "0%",
                    ["🆕", "⏳", "✅", "⚡"][i]
                ), unsafe_allow_html=True)


@st.fragment
def render_grid_view(tickets_df: pd.DataFrame):
    """Grid de tickets con glassmorphism premium"""
    if tickets_df.empty:
        st.markdown("""
        <div class="glass" style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem; opacity: 0.5;">✨</div>
            <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">No hay tickets</h3>
            <p style="color: var(--text-muted); font-size: 0.95rem;">Los tickets aparecerán aquí cuando estén disponibles</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    cols = st.columns(3, gap="medium")
    for idx, (_, row) in enumerate(tickets_df.iterrows()):
        with cols[idx % 3]:
            ticket = Ticket.from_dict(row.to_dict())
            
            # Tarjeta premium
            st.markdown(
                ComponentStyles.premium_ticket_card(
                    ticket.ticket_number,
                    ticket.title,
                    ticket.description[:80] + "..." if len(ticket.description) > 80 else ticket.description,
                    ticket.status,
                    ticket.priority,
                    ticket.created_at[:10] if ticket.created_at else None
                ),
                unsafe_allow_html=True
            )
            
            # Botones de acción elegantes
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="small")
            
            with col1:
                if st.button("✎", key=f"edit_{ticket.id}", help="Editar ticket"):
                    st.session_state.edit_ticket = ticket
                    st.rerun()
            
            with col2:
                with st.popover("⚡", help="Cambiar estado"):
                    st.markdown("### Estado rápido")
                    supabase = SupabaseService()
                    
                    for status, display in Status.display_names().items():
                        if st.button(f"{display}", key=f"status_{ticket.id}_{status.value}", use_container_width=True):
                            if supabase.update_ticket(ticket.id, status.value, ticket.notes, ticket.priority):
                                st.success(f"✅ Estado actualizado a {display}")
                                st.rerun()
            
            with col3:
                with st.popover("📋", help="Ver detalles"):
                    st.markdown(f"### #{ticket.ticket_number}")
                    st.markdown(f"**Descripción completa:**")
                    st.markdown(f"<div style='background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px;'>{ticket.description or 'Sin descripción'}</div>", unsafe_allow_html=True)
                    
                    if ticket.notes:
                        st.markdown("**Notas:**")
                        st.markdown(f"<div style='background: rgba(37,99,235,0.1); padding: 0.75rem; border-radius: 8px;'>{ticket.notes}</div>", unsafe_allow_html=True)
            
            with col4:
                if st.button("✓", key=f"complete_{ticket.id}", help="Marcar como completado"):
                    supabase = SupabaseService()
                    if supabase.update_ticket(ticket.id, Status.CLOSED.value, ticket.notes, ticket.priority):
                        st.success("✅ Ticket completado")
                        st.rerun()


@st.fragment
def render_list_view(tickets_df: pd.DataFrame):
    """Vista de lista compacta"""
    if tickets_df.empty:
        return
    
    st.markdown('<div class="glass" style="padding: 0.5rem;">', unsafe_allow_html=True)
    
    for idx, (_, row) in enumerate(tickets_df.iterrows()):
        ticket = Ticket.from_dict(row.to_dict())
        
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 1.5, 1.5, 1.5])
        
        with col1:
            priority_color = Priority.colors().get(Priority(ticket.priority), "#94a3b8")
            st.markdown(f'<div style="width: 10px; height: 10px; background: {priority_color}; border-radius: 50%; box-shadow: 0 0 12px {priority_color}80;"></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<span style="font-family: monospace; color: var(--text-muted);">#{ticket.ticket_number}</span>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<span style="font-weight: 500;">{ticket.title[:50]}{"..." if len(ticket.title) > 50 else ""}</span>', unsafe_allow_html=True)
        
        with col4:
            status_color = Status.colors().get(Status(ticket.status), "#64748b")
            status_name = Status.display_names().get(Status(ticket.status), "Nuevo")
            st.markdown(f'<span style="background: {status_color}20; color: {status_color}; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{status_name}</span>', unsafe_allow_html=True)
        
        with col5:
            if st.button("✎ Editar", key=f"list_edit_{ticket.id}", use_container_width=True):
                st.session_state.edit_ticket = ticket
                st.rerun()
        
        with col6:
            if st.button("✓", key=f"list_complete_{ticket.id}", use_container_width=True):
                supabase = SupabaseService()
                if supabase.update_ticket(ticket.id, Status.CLOSED.value, ticket.notes, ticket.priority):
                    st.success("✅ Completado")
                    st.rerun()
        
        if idx < len(tickets_df) - 1:
            st.divider()
    
    st.markdown('</div>', unsafe_allow_html=True)


@st.dialog("✏️ Editar Ticket", width="large")
def edit_modal(ticket: Ticket):
    """Modal de edición premium"""
    
    # Header con gradiente
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(37,99,235,0.2) 0%, transparent 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="background: var(--accent); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 1.25rem;">🎫</span>
            </div>
            <div>
                <h3 style="margin: 0; color: var(--text-primary);">{ticket.title}</h3>
                <p style="margin: 0.25rem 0 0 0; color: var(--text-muted); font-size: 0.85rem;">#{ticket.ticket_number} • {ticket.created_at[:10] if ticket.created_at else 'Fecha no disponible'}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout en pestañas
    tab1, tab2 = st.tabs(["📋 Información", "📝 Notas y descripción"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Estado actual**")
            status_label = Status.display_names().get(Status(ticket.status), "Nuevo")
            new_status_label = st.selectbox(
                "Cambiar estado:", 
                list(Status.display_names().values()),
                index=list(Status.display_names().values()).index(status_label),
                key="status_select",
                label_visibility="collapsed"
            )
            new_status = Status.from_display(new_status_label)
        
        with col2:
            st.markdown("**Prioridad actual**")
            priority_label = Priority.display_names().get(Priority(ticket.priority), "Media")
            new_priority_label = st.selectbox(
                "Cambiar prioridad:",
                list(Priority.display_names().values()),
                index=list(Priority.display_names().values()).index(priority_label),
                key="priority_select",
                label_visibility="collapsed"
            )
            new_priority = Priority.from_display(new_priority_label)
    
    with tab2:
        st.markdown("**Descripción**")
        st.text_area(
            "",
            value=ticket.description,
            height=120,
            key="desc_edit",
            placeholder="Descripción del ticket...",
            label_visibility="collapsed"
        )
        
        st.markdown("**Notas internas**")
        new_notes = st.text_area(
            "",
            value=ticket.notes,
            height=100,
            key="notes_edit",
            placeholder="Añade notas o comentarios internos...",
            label_visibility="collapsed"
        )
    
    # Botones de acción premium
    st.divider()
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("💾 Guardar cambios", use_container_width=True, type="primary"):
            supabase = SupabaseService()
            if supabase.update_ticket(ticket.id, new_status, new_notes, new_priority):
                st.markdown(ComponentStyles.alert_success("✓ Cambios guardados exitosamente"), unsafe_allow_html=True)
                st.session_state.edit_ticket = None
                st.rerun()
    
    with col4:
        if st.button("❌ Cancelar", use_container_width=True):
            st.session_state.edit_ticket = None
            st.rerun()


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    supabase = SupabaseService()
    
    # SIDEBAR PREMIUM
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1.5rem 0.5rem; text-align: center;">
            <div style="background: linear-gradient(135deg, var(--accent), #1e40af); width: 60px; height: 60px; border-radius: 16px; margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 2rem;">⚡</span>
            </div>
            <h2 style="margin: 0; color: var(--text-primary); font-size: 1.5rem;">FlowTickets</h2>
            <p style="margin: 0.25rem 0 0 0; color: var(--text-muted); font-size: 0.8rem;">SaaS Pro Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Búsqueda
        st.markdown("### 🔍 Búsqueda")
        search_query = st.text_input(
            "Buscar tickets",
            placeholder="ID, título o descripción...",
            label_visibility="collapsed",
            key="global_search"
        )
        
        st.divider()
        
        # Filtros premium
        st.markdown("### 🎯 Filtros")
        
        status_filter = st.selectbox(
            "Estado",
            ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
            key="sidebar_status_filter"
        )
        
        priority_filter = st.selectbox(
            "Prioridad",
            ["Todos", "Baja", "Media", "Alta"],
            key="sidebar_priority_filter"
        )
        
        # Vista selector
        st.divider()
        st.markdown("### 🎨 Vista")
        
        view_mode = st.radio(
            "Modo de visualización",
            ["grid", "list"],
            format_func=lambda x: "📱 Grid" if x == "grid" else "📋 Lista",
            horizontal=True,
            key="view_mode_radio"
        )
        st.session_state.view_mode = view_mode
        
        # Botón de actualización
        if st.button("🔄 Actualizar datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.divider()
        
        # Estado de conexión
        success, msg, count = supabase.test_connection()
        if success:
            st.markdown(f"""
            <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); border-radius: 8px; padding: 0.75rem;">
                <p style="margin: 0; color: #6ee7b7; font-size: 0.8rem;">
                    <span style="display: inline-block; width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-right: 0.5rem;"></span>
                    Conectado • {count} registros
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(ComponentStyles.alert_error("Error de conexión"), unsafe_allow_html=True)
    
    # CONTENIDO PRINCIPAL
    # Header hero
    st.markdown(ComponentStyles.header_hero(
        "Dashboard de Tickets",
        "Gestiona tus oportunidades con eficiencia y estilo"
    ), unsafe_allow_html=True)
    
    # MAPEOS
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
    
    # OBTENER TICKETS
    tickets = supabase.fetch_tickets(
        status_map[status_filter] if status_filter != "Todos" else None,
        priority_map[priority_filter] if priority_filter != "Todos" else None,
        search_query if search_query else None
    )
    
    # MÉTRICAS
    render_metrics_dashboard(tickets)
    
    st.divider()
    
    # HEADER DE RESULTADOS
    if not tickets.empty:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: var(--text-primary); font-size: 1.125rem;">📌 Tickets encontrados</h3>
                <span style="background: rgba(37,99,235,0.2); color: var(--accent-light); padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{len(tickets)}</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if not tickets.empty:
                st.markdown(f'<p style="text-align: right; color: var(--text-muted); font-size: 0.85rem;">{status_filter} • {priority_filter}</p>', unsafe_allow_html=True)
    
    # VISTA DE TICKETS
    if st.session_state.view_mode == "grid":
        render_grid_view(tickets)
    else:
        render_list_view(tickets)
    
    # MODAL DE EDICIÓN
    if st.session_state.edit_ticket:
        edit_modal(st.session_state.edit_ticket)


if __name__ == "__main__":
    main()