"""
Dashboard SaaS Pro de gestión de tickets con Glassmorphism.
Diseño profesional tipo Linear, Holded, Vercel.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from styles import StyleManager, ComponentStyles


# Configuración
st.set_page_config(
    page_title="Dashboard de Tickets | SaaS Pro",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

StyleManager.inject_all()

# Session state init
if "edit_ticket" not in st.session_state:
    st.session_state.edit_ticket = None
if "search_filter" not in st.session_state:
    st.session_state.search_filter = ""


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
    
    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        return cls(
            id=data.get("id"),
            ticket_number=data.get("ticket_number", "N/A"),
            title=data.get("title", "Sin título"),
            description=data.get("description", "").strip(),
            status=data.get("status", Status.NEW.value).lower(),
            priority=data.get("priority", Priority.MEDIUM.value),
            notes=data.get("notes", "") or "",
            created_at=data.get("created_at")
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
                     priority_filter: Optional[str] = None) -> pd.DataFrame:
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
# COMPONENTES UI
# ============================================================================

@st.fragment
def render_grid(tickets_df: pd.DataFrame, on_edit_callback=None):
    """Grid de tickets con glassmorphism y acciones rápidas"""
    if tickets_df.empty:
        st.markdown("""
        <div class="glass-container" style="text-align: center; padding: 3rem 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
            <p style="color: #94A3B8; font-size: 0.95rem;">No hay tickets con los filtros seleccionados</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    cols = st.columns(3, gap="medium")
    for idx, (_, row) in enumerate(tickets_df.iterrows()):
        with cols[idx % 3]:
            ticket = Ticket.from_dict(row.to_dict())
            
            # Tarjeta principal
            st.markdown(
                ComponentStyles.ticket_card(
                    ticket.ticket_number,
                    ticket.title,
                    ticket.status,
                    ticket.priority
                ),
                unsafe_allow_html=True
            )
            
            # Botones de acción
            col1, col2, col3 = st.columns(3, gap="small")
            
            with col1:
                if st.button("✏️", key=f"edit_{ticket.id}", help="Editar", use_container_width=True):
                    st.session_state.edit_ticket = ticket
                    st.rerun()
            
            with col2:
                with st.popover("⚡", help="Acciones rápidas"):
                    st.markdown("### Acciones rápidas")
                    supabase = SupabaseService()
                    
                    if st.button("🟢 Completar", key=f"complete_{ticket.id}", use_container_width=True):
                        if supabase.update_ticket(ticket.id, Status.CLOSED.value, ticket.notes):
                            st.success("✅ Ticket completado")
                            st.rerun()
                    
                    if st.button("⏳ En progreso", key=f"progress_{ticket.id}", use_container_width=True):
                        if supabase.update_ticket(ticket.id, Status.IN_PROGRESS.value, ticket.notes):
                            st.success("✅ Estado actualizado")
                            st.rerun()
                    
                    st.divider()
                    st.caption("Descripción")
                    st.text(ticket.description[:100] + "..." if len(ticket.description) > 100 else ticket.description)
            
            with col3:
                if st.button("📋", key=f"view_{ticket.id}", help="Ver detalles", use_container_width=True):
                    st.session_state.show_details = ticket.id


@st.dialog("✏️ Editar Ticket", width="large")
def edit_modal(ticket: Ticket):
    """Modal de edición con diseño profesional"""
    st.markdown(f"### 📋 {ticket.title}")
    st.caption(f"🆔 Ticket: #{ticket.ticket_number} | 📅 {ticket.created_at[:10] if ticket.created_at else 'N/A'}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📝 Descripción**")
        st.text(ticket.description or "Sin descripción")
    
    with col2:
        st.markdown("**📊 Información**")
        info_text = f"""
        **Estado:** {Status.display_names().get(Status(ticket.status), 'Nuevo')}
        
        **Prioridad:** {Priority.display_names().get(Priority(ticket.priority), 'Media')}
        """
        st.markdown(info_text)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Estado**")
        status_label = Status.display_names().get(Status(ticket.status), "Nuevo")
        new_status_label = st.selectbox(
            "Cambiar a:", 
            list(Status.display_names().values()),
            index=list(Status.display_names().values()).index(status_label),
            key="status_select"
        )
        new_status = Status.from_display(new_status_label)
    
    with col2:
        st.markdown("**Prioridad**")
        priority_label = Priority.display_names().get(Priority(ticket.priority), "Media")
        new_priority_label = st.selectbox(
            "Cambiar a:",
            list(Priority.display_names().values()),
            index=list(Priority.display_names().values()).index(priority_label),
            key="priority_select"
        )
        new_priority = Priority.from_display(new_priority_label)
    
    st.markdown("**Notas**")
    new_notes = st.text_area("", value=ticket.notes, height=100, placeholder="Añade notas sobre este ticket...")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Guardar", use_container_width=True, type="primary"):
            supabase = SupabaseService()
            if supabase.update_ticket(ticket.id, new_status, new_notes, new_priority):
                st.markdown(ComponentStyles.alert_success("Cambios guardados exitosamente"), unsafe_allow_html=True)
                st.rerun()
    
    with col2:
        if st.button("🔄 Resetear", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("❌ Cerrar", use_container_width=True):
            st.session_state.edit_ticket = None
            st.rerun()


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    supabase = SupabaseService()
    
    # HEADER PROFESIONAL
    st.markdown(ComponentStyles.header_hero(
        "Dashboard de Tickets",
        "Gestiona tus oportunidades y tickets de soporte con eficiencia"
    ), unsafe_allow_html=True)
    
    # LAYOUT PRINCIPAL
    col_sidebar, col_main = st.columns([1, 4], gap="large")
    
    with col_sidebar:
        st.markdown("### 🔍 Filtros")
        
        status = st.selectbox(
            "Estado", 
            ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
            key="status_filter"
        )
        
        priority = st.selectbox(
            "Prioridad", 
            ["Todos", "Baja", "Media", "Alta"],
            key="priority_filter"
        )
        
        if st.button("🔄 Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.divider()
        
        # ESTADÍSTICAS
        st.markdown("### 📊 Estadísticas")
        all_tickets = supabase.fetch_tickets()
        
        if not all_tickets.empty:
            st.markdown(ComponentStyles.stat_card(
                "Total", 
                str(len(all_tickets)), 
                f"+{len(all_tickets)}",
                "🎫"
            ), unsafe_allow_html=True)
            
            new_count = len(all_tickets[all_tickets["status"]=="new"])
            st.markdown(ComponentStyles.stat_card(
                "Nuevos", 
                str(new_count),
                f"+{new_count}" if new_count > 0 else "-",
                "🆕"
            ), unsafe_allow_html=True)
            
            won_count = len(all_tickets[all_tickets["status"]=="won"])
            st.markdown(ComponentStyles.stat_card(
                "Ganados", 
                str(won_count),
                f"+{won_count}" if won_count > 0 else "-",
                "✅"
            ), unsafe_allow_html=True)
        
        st.divider()
        
        # DIAGNÓSTICO
        with st.expander("🔧 Diagnóstico"):
            success, msg, count = supabase.test_connection()
            if success:
                st.markdown(ComponentStyles.alert_success(f"{msg} — {count} registros"), unsafe_allow_html=True)
            else:
                st.markdown(ComponentStyles.alert_error(msg), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2, gap="small")
            with col1:
                if st.button("👁️ Opportunities", use_container_width=True):
                    data = supabase.get_sample_data("opportunities")
                    if data:
                        st.dataframe(pd.DataFrame(data), use_container_width=True)
            
            with col2:
                if st.button("📹 Recordings", use_container_width=True):
                    data = supabase.get_sample_data("recordings")
                    if data:
                        st.dataframe(pd.DataFrame(data), use_container_width=True)
    
    with col_main:
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
            status_map[status] if status_map[status] != "Todos" else None,
            priority_map[priority] if priority_map[priority] != "Todos" else None
        )
        
        # HEADER DE RESULTADOS
        if not tickets.empty:
            st.markdown(f"""
            <div style="margin-bottom: 1.5rem;">
                <h3 style="margin: 0; color: #F1F5F9; font-size: 1.125rem;">
                    📌 {len(tickets)} ticket{'s' if len(tickets) != 1 else ''} encontrado{'s' if len(tickets) != 1 else ''}
                </h3>
                <p style="margin: 0.25rem 0 0 0; color: #94A3B8; font-size: 0.85rem;">
                    {status} • {priority}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # GRID DE TICKETS
        render_grid(tickets)
    
    # MODAL DE EDICIÓN
    if st.session_state.edit_ticket:
        edit_modal(st.session_state.edit_ticket)


if __name__ == "__main__":
    main()

