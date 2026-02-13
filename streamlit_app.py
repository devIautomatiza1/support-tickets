"""
Dashboard minimalista de gestión de tickets con Tailwind CSS.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from styles import StyleManager, ComponentStyles


# Configuración
st.set_page_config(
    page_title="Dashboard de Tickets",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

StyleManager.inject_all()


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
                st.error(f"Error al conectar: {e}")
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
            st.error(f"Error: {e}")
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
            st.error(f"Error: {e}")
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
def render_grid(tickets_df: pd.DataFrame):
    """Grid de tickets"""
    if tickets_df.empty:
        st.info("📭 No hay tickets")
        return
    
    cols = st.columns(3, gap="medium")
    for idx, (_, row) in enumerate(tickets_df.iterrows()):
        with cols[idx % 3]:
            ticket = Ticket.from_dict(row.to_dict())
            st.markdown(
                ComponentStyles.ticket_card(
                    ticket.ticket_number,
                    ticket.title,
                    ticket.status
                ),
                unsafe_allow_html=True
            )
            if st.button("✏️ Editar", key=f"edit_{ticket.id}", use_container_width=True):
                st.session_state.edit_ticket = ticket
                st.rerun()


@st.dialog("Editar Ticket", width="large")
def edit_modal(ticket: Ticket):
    """Modal de edición"""
    st.markdown(f"### 📋 {ticket.title}")
    st.caption(f"Creado: {ticket.created_at[:10] if ticket.created_at else 'N/A'}")
    
    st.markdown("**Descripción:**")
    st.text(ticket.description or "Sin descripción")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Estado actual:**")
        status_label = Status.display_names().get(Status(ticket.status), "Nuevo")
        st.markdown(f"🔹 {status_label}")
        new_status_label = st.selectbox(
            "Cambiar a:", 
            list(Status.display_names().values()),
            index=list(Status.display_names().values()).index(status_label)
        )
        new_status = Status.from_display(new_status_label)
    
    with col2:
        st.markdown("**Prioridad actual:**")
        priority_label = Priority.display_names().get(Priority(ticket.priority), "Media")
        st.markdown(f"⚡ {priority_label}")
        new_priority_label = st.selectbox(
            "Cambiar a:",
            list(Priority.display_names().values()),
            index=list(Priority.display_names().values()).index(priority_label)
        )
        new_priority = Priority.from_display(new_priority_label)
    
    st.markdown("**Notas:**")
    new_notes = st.text_area("", value=ticket.notes, height=120)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Guardar", use_container_width=True, type="primary"):
            supabase = SupabaseService()
            if supabase.update_ticket(ticket.id, new_status, new_notes, new_priority):
                st.success("✅ Guardado")
                st.rerun()
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    supabase = SupabaseService()
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%); padding: 2rem; border-radius: 0.5rem; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2rem;">🎫 Dashboard de Tickets</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">Gestión minimalista de oportunidades</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔍 Filtros")
        status = st.selectbox("Estado", ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"])
        priority = st.selectbox("Prioridad", ["Todos", "Baja", "Media", "Alta"])
        
        if st.button("🔄 Actualizar", use_container_width=True):
            st.rerun()
        
        st.divider()
        
        st.markdown("### 📊 Estadísticas")
        all_tickets = supabase.fetch_tickets()
        if not all_tickets.empty:
            st.markdown(ComponentStyles.stat_card("Total", str(len(all_tickets))), unsafe_allow_html=True)
            st.markdown(ComponentStyles.stat_card("Nuevos", str(len(all_tickets[all_tickets["status"]=="new"]))), unsafe_allow_html=True)
            st.markdown(ComponentStyles.stat_card("Ganados", str(len(all_tickets[all_tickets["status"]=="won"]))), unsafe_allow_html=True)
    
    # Mapeos
    status_map = {"Todos": "Todos", "Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
    priority_map = {"Todos": "Todos", "Baja": "Low", "Media": "Medium", "Alta": "High"}
    
    # Obtener y mostrar tickets
    tickets = supabase.fetch_tickets(
        status_map[status] if status_map[status] != "Todos" else None,
        priority_map[priority] if priority_map[priority] != "Todos" else None
    )
    
    if not tickets.empty:
        st.markdown(f"#### 📌 {len(tickets)} tickets encontrados")
        render_grid(tickets)
    else:
        st.info("📭 No hay tickets con esos filtros")
    
    # Modal
    if "edit_ticket" in st.session_state and st.session_state.edit_ticket:
        edit_modal(st.session_state.edit_ticket)
        st.session_state.edit_ticket = None
    
    # Diagnóstico
    with st.expander("🔧 Diagnóstico"):
        success, msg, count = supabase.test_connection()
        if success:
            st.markdown(ComponentStyles.alert_success(f"{msg} — {count} registros"), unsafe_allow_html=True)
        else:
            st.markdown(ComponentStyles.alert_error(msg), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ver opportunities"):
                data = supabase.get_sample_data("opportunities")
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True)
        with col2:
            if st.button("Ver recordings"):
                data = supabase.get_sample_data("recordings")
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True)


if __name__ == "__main__":
    main()
