"""
Dashboard profesional de gestión de tickets.
Arquitectura refactorizada con separación de responsabilidades.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Importar módulo de estilos centralizado
from styles import (
    StyleManager, 
    StatusColors, 
    PriorityColors, 
    ComponentStyles
)


# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
st.set_page_config(
    page_title="Dashboard de Tickets",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar todos los estilos desde el módulo centralizado
StyleManager.inject_all()


# ============================================================================
# MODELOS DE DATOS
# ============================================================================

class Status(Enum):
    """Estados posibles de un ticket"""
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
    def from_display(cls, display_name: str) -> str:
        reverse_map = {v: k.value for k, v in cls.display_names().items()}
        return reverse_map.get(display_name, cls.NEW.value)


class Priority(Enum):
    """Prioridades posibles"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    
    @classmethod
    def display_names(cls):
        return {
            cls.LOW: "Baja",
            cls.MEDIUM: "Media",
            cls.HIGH: "Alta"
        }
    
    @classmethod
    def from_display(cls, display_name: str) -> str:
        reverse_map = {v: k.value for k, v in cls.display_names().items()}
        return reverse_map.get(display_name, cls.MEDIUM.value)


@dataclass
class Ticket:
    """Modelo de datos para un ticket"""
    id: int
    ticket_number: str
    title: str
    description: str
    status: str
    priority: str
    notes: str
    created_at: Optional[str] = None
    recording_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ticket":
        """Crea un Ticket desde un diccionario"""
        return cls(
            id=data.get("id"),
            ticket_number=data.get("ticket_number", "N/A"),
            title=data.get("title", "Sin título"),
            description=data.get("description", "").strip(),
            status=data.get("status", Status.NEW.value).lower(),
            priority=data.get("priority", Priority.MEDIUM.value),
            notes=data.get("notes", "") or "",
            created_at=data.get("created_at"),
            recording_id=data.get("recording_id")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el Ticket a diccionario"""
        return asdict(self)


# ============================================================================
# SERVICIO DE SUPABASE
# ============================================================================

class SupabaseService:
    """Servicio centralizado para operaciones con Supabase"""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_client(self):
        """Obtiene o inicializa el cliente de Supabase"""
        if self._client is None:
            try:
                from supabase import create_client
                SUPABASE_URL = st.secrets["SUPABASE_URL"]
                SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
                self._client = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as e:
                st.error(f"❌ Error al inicializar Supabase: {e}")
                return None
        return self._client
    
    def test_connection(self) -> Tuple[bool, str, Optional[int]]:
        """Prueba la conexión a Supabase"""
        try:
            client = self._get_client()
            if not client:
                return False, "No se pudo inicializar el cliente", None
            
            response = client.table("opportunities").select("count", count="exact").execute()
            count = response.count if hasattr(response, 'count') else len(response.data)
            return True, "Conexión exitosa", count
        except Exception as e:
            return False, f"Error de conexión: {str(e)}", None
    
    def fetch_tickets(self, 
                      status_filter: Optional[str] = None, 
                      priority_filter: Optional[str] = None) -> pd.DataFrame:
        """Obtiene tickets con filtros opcionales"""
        try:
            client = self._get_client()
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
            st.error(f"❌ Error al obtener tickets: {e}")
            return pd.DataFrame()
    
    def update_ticket(self, 
                     ticket_id: int, 
                     status: str, 
                     notes: str, 
                     priority: Optional[str] = None) -> bool:
        """Actualiza un ticket existente"""
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
            st.error(f"❌ Error al actualizar ticket: {e}")
            return False
    
    def get_sample_data(self, table: str, limit: int = 3) -> List[Dict]:
        """Obtiene datos de muestra de una tabla"""
        try:
            client = self._get_client()
            if not client:
                return []
            response = client.table(table).select("*").limit(limit).execute()
            return response.data or []
        except Exception:
            return []


# ============================================================================
# COMPONENTES DE UI
# ============================================================================

class TicketCard:
    """Componente para renderizar una tarjeta de ticket"""
    
    BADGE_STYLES = {
        Status.NEW.value: ("badge-new", "NUEVO"),
        Status.IN_PROGRESS.value: ("badge-progress", "PROGRESO"),
        Status.WON.value: ("badge-won", "GANADO"),
        Status.CLOSED.value: ("badge-closed", "CERRADO")
    }
    
    @staticmethod
    def render(ticket: Ticket):
        """Renderiza una tarjeta de ticket profesional"""
        badge_class, badge_label = TicketCard.BADGE_STYLES.get(
            ticket.status, 
            TicketCard.BADGE_STYLES[Status.NEW.value]
        )
        
        card_html = f"""
        <div class="ticket-card">
            <div class="ticket-header">
                <span class="ticket-number">#{ticket.ticket_number}</span>
                <span class="badge {badge_class}">{badge_label}</span>
            </div>
            <div class="ticket-title">{ticket.title[:60]}</div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        if st.button("EDITAR", key=f"edit_{ticket.id}", use_container_width=True):
            st.session_state.edit_ticket = ticket.to_dict()
            st.rerun()


class TicketGrid:
    """Grid responsiva de tickets"""
    
    def __init__(self, num_columns: int = 3):
        self.num_columns = num_columns
    
    @st.fragment
    def render(self, tickets_df: pd.DataFrame):
        """Renderiza el grid de tickets"""
        if tickets_df.empty:
            st.info("📭 No hay tickets disponibles")
            return
        
        columns = st.columns(self.num_columns, gap="small")
        
        for idx, (_, row) in enumerate(tickets_df.iterrows()):
            with columns[idx % self.num_columns]:
                ticket = Ticket.from_dict(row.to_dict())
                TicketCard.render(ticket)


class EditTicketModal:
    """Modal profesional para editar tickets"""
    
    def __init__(self, supabase_service: SupabaseService):
        self.supabase = supabase_service
    
    @st.dialog("Editar ticket", width="large")
    def render(self, ticket_dict: Dict[str, Any]):
        """Renderiza el modal de edición"""
        ticket = Ticket.from_dict(ticket_dict)
        
        # Limpiar descripción
        description = self._clean_description(ticket.description)
        created_at = ticket.created_at[:10] if ticket.created_at else "N/A"
        
        # Renderizar componentes
        self._render_header(ticket.title, created_at)
        self._render_description(description)
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_status = self._render_status_section(ticket)
        
        with col2:
            new_priority = self._render_priority_section(ticket)
        
        self._render_notes_form(ticket, new_status, new_priority)
    
    @staticmethod
    def _clean_description(description: str) -> str:
        """Limpia la descripción eliminando líneas vacías"""
        if description:
            desc_clean = "\n".join([l for l in description.split("\n") if l.strip()])
            return desc_clean or "Sin descripción"
        return "Sin descripción"
    
    def _render_header(self, title: str, created_at: str):
        """Renderiza el header del modal"""
        st.markdown(f"""
        <div class="modal-header">
            <div>
                <span class="modal-title">{title}</span>
            </div>
            <span class="modal-date">{created_at}</span>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_description(self, description: str):
        """Renderiza la sección de descripción"""
        st.markdown('<div class="section-title">DESCRIPCIÓN</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="description-box">
            {description}
        </div>
        """, unsafe_allow_html=True)
    
    def _render_status_section(self, ticket: Ticket) -> str:
        """Renderiza la sección de estado"""
        status_obj = Status(ticket.status)
        status_colors = {
            Status.NEW: StatusColors.NEW,
            Status.IN_PROGRESS: StatusColors.IN_PROGRESS,
            Status.WON: StatusColors.WON,
            Status.CLOSED: StatusColors.CLOSED
        }
        
        color = status_colors.get(status_obj, StatusColors.NEW)
        status_label = Status.display_names()[status_obj]
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">ESTADO ACTUAL</div>
            <span class="current-value" style="background: {color.bg}; color: {color.color};">
                {status_label}
            </span>
            <div class="select-label">CAMBIAR A</div>
        </div>
        """, unsafe_allow_html=True)
        
        status_options = list(Status.display_names().values())
        current_idx = list(Status.display_names().values()).index(status_label)
        
        new_status_display = st.selectbox(
            "", 
            status_options, 
            index=current_idx, 
            key=f"status_{ticket.id}", 
            label_visibility="collapsed"
        )
        
        return Status.from_display(new_status_display)
    
    def _render_priority_section(self, ticket: Ticket) -> str:
        """Renderiza la sección de prioridad"""
        priority_obj = Priority(ticket.priority)
        priority_colors = {
            Priority.LOW: PriorityColors.LOW,
            Priority.MEDIUM: PriorityColors.MEDIUM,
            Priority.HIGH: PriorityColors.HIGH
        }
        
        color = priority_colors.get(priority_obj, PriorityColors.MEDIUM)
        priority_label = Priority.display_names()[priority_obj]
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">PRIORIDAD ACTUAL</div>
            <span class="current-value" style="background: {color.bg}; color: {color.color};">
                {priority_label}
            </span>
            <div class="select-label">CAMBIAR A</div>
        </div>
        """, unsafe_allow_html=True)
        
        priority_options = list(Priority.display_names().values())
        current_idx = list(Priority.display_names().values()).index(priority_label)
        
        new_priority_display = st.selectbox(
            "", 
            priority_options, 
            index=current_idx, 
            key=f"priority_{ticket.id}", 
            label_visibility="collapsed"
        )
        
        return Priority.from_display(new_priority_display)
    
    def _render_notes_form(self, ticket: Ticket, new_status: str, new_priority: str):
        """Renderiza el formulario de notas y botones de acción"""
        st.markdown("""
        <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
            <span class="section-title">NOTAS</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key=f"edit_form_{ticket.id}"):
            new_notes = st.text_area(
                "",
                value=ticket.notes,
                height=120,
                placeholder="⭐️ Tema / 📌 Descripción / 👤 Mencionado / 💬 Contexto / 📊 Confianza",
                key=f"notes_{ticket.id}",
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                saved = st.form_submit_button(
                    "✓ Guardar cambios", 
                    use_container_width=True,
                    type="primary"
                )
            
            with col3:
                cancelled = st.form_submit_button(
                    "✕ Cancelar", 
                    use_container_width=True
                )
            
            if saved:
                if self.supabase.update_ticket(ticket.id, new_status, new_notes, new_priority):
                    st.success("✅ Ticket actualizado correctamente")
                    st.rerun()
                else:
                    st.error("❌ Error al actualizar el ticket")
            
            if cancelled:
                st.rerun()


# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def render_sidebar(supabase: SupabaseService) -> Tuple[str, str]:
    """Renderiza la barra lateral con filtros"""
    with st.sidebar:
        st.markdown("## 🔍 Filtros")
        
        status_filter = st.selectbox(
            "Estado",
            ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
            key="status_filter"
        )
        
        priority_filter = st.selectbox(
            "Prioridad",
            ["Todos", "Baja", "Media", "Alta"],
            key="priority_filter"
        )
        
        if st.button("🔄 ACTUALIZAR", key="ACTUALIZAR", use_container_width=True):
            st.rerun()
        
        st.divider()
        
        # Estadísticas
        st.markdown("## 📊 Estadísticas")
        all_tickets = supabase.fetch_tickets()
        
        if not all_tickets.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", len(all_tickets))
            with col2:
                st.metric("Nuevos", len(all_tickets[all_tickets["status"] == "new"]))
            with col3:
                st.metric("Ganados", len(all_tickets[all_tickets["status"] == "won"]))
        else:
            st.info("📭 Sin datos")
        
        return status_filter, priority_filter


def render_diagnostics(supabase: SupabaseService):
    """Renderiza la sección de diagnóstico"""
    with st.expander("🔧 Diagnóstico del sistema", expanded=False):
        success, msg, count = supabase.test_connection()
        
        if success:
            st.success(f"✅ {msg} — {count} registros")
        else:
            st.error(f"❌ {msg}")
        
        st.caption("Configuración: Secrets de Streamlit")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Ver opportunities", key="ver_opp"):
                data = supabase.get_sample_data("opportunities")
                if data:
                    st.dataframe(pd.DataFrame(data))
        with col2:
            if st.button("🎙️ Ver recordings", key="ver_rec"):
                data = supabase.get_sample_data("recordings")
                if data:
                    st.dataframe(pd.DataFrame(data))


def main():
    """Función principal"""
    
    # Inicializar servicios
    supabase = SupabaseService()
    modal_editor = EditTicketModal(supabase)
    grid = TicketGrid(num_columns=3)
    
    # Header
    st.title("🎫 Dashboard de Tickets")
    st.markdown(
        "<h3 style='color: var(--text-secondary); font-weight: 400; margin-top: -0.5rem;'>"
        "Gestión de oportunidades profesional</h3>",
        unsafe_allow_html=True
    )
    st.divider()
    
    # Sidebar
    status_filter, priority_filter = render_sidebar(supabase)
    
    # Mapeos para filtros
    status_map = {
        "Todos": "Todos", "Nuevo": "new", "En progreso": "in_progress", 
        "Cerrado": "closed", "Ganado": "won"
    }
    priority_map = {
        "Todos": "Todos", "Baja": "Low", "Media": "Medium", "Alta": "High"
    }
    
    selected_status = status_map[status_filter]
    selected_priority = priority_map[priority_filter]
    
    # Obtener tickets
    tickets = supabase.fetch_tickets(
        status_filter=selected_status if selected_status != "Todos" else None,
        priority_filter=selected_priority if selected_priority != "Todos" else None
    )
    
    # Mostrar grid
    if tickets.empty:
        st.info("📭 No hay tickets con los filtros seleccionados.")
    else:
        st.markdown(f"#### 📌 {len(tickets)} tickets encontrados")
        grid.render(tickets)
    
    # Modal de edición
    if "edit_ticket" in st.session_state and st.session_state.edit_ticket:
        modal_editor.render(st.session_state.edit_ticket)
        st.session_state.edit_ticket = None
    
    # Diagnóstico
    render_diagnostics(supabase)


if __name__ == "__main__":
    main()
