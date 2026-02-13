"""
Dashboard SaaS Pro - Gestión de Tickets
Diseño ultra minimalista tipo Linear
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random
import base64
from pathlib import Path
import time
from PIL import Image
from io import BytesIO

from styles import StyleManager, ComponentStyles


# Configuración
icon_image = Image.open("icon.jpeg")
st.set_page_config(
    page_title="Soporte Oportunidades",
    page_icon=icon_image,
    layout="wide",
    initial_sidebar_state="expanded"
)

StyleManager.inject_all()

# Convertir imagen a base64
def get_image_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    return img_base64

icon_base64 = get_image_base64("icon.jpeg")

# Session state
if "search_filter" not in st.session_state:
    st.session_state.search_filter = ""
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()


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
    
    @classmethod
    def css_class(cls):
        return {
            cls.LOW: "low",
            cls.MEDIUM: "medium",
            cls.HIGH: "high"
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
    
    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        # Validaciones defensivas para campos que pueden estar vacíos
        status = data.get("status", Status.NEW.value)
        if not status or status is None:
            status = Status.NEW.value
        status = str(status).lower().strip()
        if status not in [s.value for s in Status]:
            status = Status.NEW.value
            
        priority = data.get("priority", Priority.MEDIUM.value)
        if not priority or priority is None:
            priority = Priority.MEDIUM.value
        priority = str(priority).strip()
        if priority not in [p.value for p in Priority]:
            priority = Priority.MEDIUM.value
        
        return cls(
            id=data.get("id"),
            ticket_number=str(data.get("ticket_number") or f"TKT-{random.randint(1000, 9999)}").strip(),
            title=str(data.get("title", "Sin título") or "Sin título").strip(),
            description=str(data.get("description", "") or "").strip(),
            status=status,
            priority=priority,
            notes=str(data.get("notes", "") or "").strip(),
            created_at=str(data.get("created_at", "2026-02-13") or "2026-02-13").strip()
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
                        df['ticket_number'].str.lower().str.contains(search_query, na=False)
                    ]
                
                return df
            return pd.DataFrame()
        except Exception as e:
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
            return False


# ============================================================================
# COMPONENTES UI
# ============================================================================

def render_metrics(tickets_df: pd.DataFrame):
    """Métricas minimalistas"""
    if tickets_df.empty:
        cols = st.columns(4)
        metrics = [
            ("Total", "0", "🎫"),
            ("Nuevos", "0", "🆕"),
            ("En progreso", "0", "⏳"),
            ("Alta prioridad", "0", "⚡")
        ]
        for col, (title, value, icon) in zip(cols, metrics):
            with col:
                st.markdown(ComponentStyles.stat_card(title, value, icon), unsafe_allow_html=True)
        return
    
    total = len(tickets_df)
    new_count = len(tickets_df[tickets_df["status"]=="new"])
    in_progress = len(tickets_df[tickets_df["status"]=="in_progress"])
    high_priority = len(tickets_df[tickets_df["priority"]=="High"])
    
    cols = st.columns(4)
    metrics = [
        ("Total", str(total), "🎫", f"{total} tickets"),
        ("Nuevos", str(new_count), "🆕", f"{round(new_count/total*100)}%"),
        ("En progreso", str(in_progress), "⏳", f"{round(in_progress/total*100)}%"),
        ("Alta prioridad", str(high_priority), "⚡", f"{round(high_priority/total*100)}%")
    ]
    
    for col, (title, value, icon, trend) in zip(cols, metrics):
        with col:
            st.markdown(ComponentStyles.stat_card(title, value, icon, trend), unsafe_allow_html=True)


def escape_html(text: str) -> str:
    """Escapa caracteres especiales HTML"""
    if not text:
        return ""
    text = str(text)
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def sanitize_text(text: str) -> str:
    """Limpia texto malformado"""
    if not text:
        return ""
    text = str(text).strip()
    # Remover comillas al inicio/final
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        text = text[1:-1]
    # Remover HTML tags
    import re
    text = re.sub(r'<[^>]+>', '', text)
    # Remover caracteres repetidos erráticos (aaaaaaa)
    text = re.sub(r'([a-z])\1{4,}', r'\1', text)
    return text.strip()


def detect_malformed_ticket(ticket: Ticket) -> bool:
    """Detecta si un ticket está malformado"""
    # Título sin [IA] o muy corto
    if not ticket.title.startswith("[IA]") or len(ticket.title) < 10:
        return True
    # Description muy corta o vacía
    if len(ticket.description) < 5:
        return True
    # Notes vacías o solo un placeholder
    if not ticket.notes or len(ticket.notes) < 5 or ticket.notes.lower() in ["sad", "n/a", "none"]:
        return True
    return False


@st.fragment
def render_ticket_card(ticket: Ticket):
    """Renderiza una tarjeta de ticket minimalista - maneja tickets bien formados y defectuosos"""
    
    is_malformed = detect_malformed_ticket(ticket)
    
    # Extraer persona del título
    title_parts = ticket.title.split(" - ")
    display_title = escape_html(sanitize_text(title_parts[0]))
    person = escape_html(sanitize_text(title_parts[1])) if len(title_parts) > 1 else ""
    
    # Limpiar descripción - NO escapar aquí, solo sanitizar
    desc = sanitize_text(ticket.description)
    desc_preview = escape_html(desc[:100])
    
    # Mapeo de estados
    badge_map = {
        "new": "badge-new",
        "in_progress": "badge-progress",
        "won": "badge-won",
        "closed": "badge-closed"
    }
    status_text = Status.display_names().get(Status(ticket.status), "Nuevo")
    
    # Prioridad
    priority_class = Priority.css_class().get(Priority(ticket.priority), "medium")
    
    # Clase adicional si está malformado
    malformed_class = " ticket-card-warning" if is_malformed else ""
    
    # HTML de la tarjeta
    card_html = f"""
    <div class="ticket-card{malformed_class}">
        <div class="ticket-header">
            <span class="ticket-id">#{ticket.ticket_number}</span>
            {'<span class="ticket-warning" title="Datos incompletos">⚠️</span>' if is_malformed else ''}
            <div class="ticket-menu" id="menu-{ticket.id}">
                <span style="color: var(--text-tertiary);">⋯</span>
            </div>
        </div>
        <div class="ticket-title">{display_title}</div>
        {'<div class="ticket-person"><i class="far fa-user" style="font-size: 0.7rem;"></i> ' + person + '</div>' if person else ''}
        <div class="ticket-description">\"{desc_preview}{'...' if len(desc) > 100 else ''}\"</div>
        <div class="ticket-footer">
            <span class="badge {badge_map.get(ticket.status, 'badge-new')}">{status_text}</span>
            <div class="priority-indicator">
                <span class="priority-dot {priority_class}"></span>
                <span style="color: var(--text-tertiary); font-size: 0.7rem;">{ticket.created_at[:10]}</span>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Popover para edición
    with st.popover("Editar"):
        st.markdown(f"### {ticket.ticket_number}")
        st.caption(display_title)
        
        # Formulario de edición
        status_label = Status.display_names().get(Status(ticket.status), "Nuevo")
        priority_label = Priority.display_names().get(Priority(ticket.priority), "Media")
        
        new_status = st.selectbox(
            "Estado",
            list(Status.display_names().values()),
            index=list(Status.display_names().values()).index(status_label),
            key=f"status_{ticket.id}"
        )
        
        new_priority = st.selectbox(
            "Prioridad",
            list(Priority.display_names().values()),
            index=list(Priority.display_names().values()).index(priority_label),
            key=f"priority_{ticket.id}"
        )
        
        new_notes = st.text_area(
            "Notas",
            value=ticket.notes,
            placeholder="Añade notas internas...",
            key=f"notes_{ticket.id}"
        )
        
        if st.button("Guardar cambios", type="primary", key=f"save_{ticket.id}", use_container_width=True):
            supabase = SupabaseService()
            if supabase.update_ticket(
                ticket.id,
                Status.from_display(new_status),
                new_notes,
                Priority.from_display(new_priority)
            ):
                st.success("✓ Actualizado")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Error al guardar")


def render_tickets_grid(tickets_df: pd.DataFrame):
    """Renderiza el grid de tickets"""
    if tickets_df.empty:
        st.markdown("""
        <div style="text-align: center; padding: 4rem; background: var(--bg-secondary); border-radius: 24px; border: 1px solid var(--border-medium);">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">✨</div>
            <h3 style="color: var(--text-secondary); margin-bottom: 0.5rem;">No hay tickets</h3>
            <p style="color: var(--text-tertiary);">Los tickets aparecerán aquí cuando estén disponibles</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Grid de 3 columnas
    cols = st.columns(3, gap="small")
    
    for idx, (_, row) in enumerate(tickets_df.iterrows()):
        ticket = Ticket.from_dict(row.to_dict())
        with cols[idx % 3]:
            render_ticket_card(ticket)


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    supabase = SupabaseService()
    
    # SIDEBAR
    with st.sidebar:
        # Logo y título
        st.markdown(f"""
        <div style="padding: 0.5rem 0 1.5rem 0;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <img src="data:image/jpeg;base64,{icon_base64}" style="width: 32px; height: 32px; border-radius: 10px;" />
                <div>
                    <div style="font-weight: 700; color: var(--text-primary);">Soporte Oportunidades</div>
                    <div style="font-size: 0.7rem; color: var(--text-tertiary);">Automatiza</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Búsqueda
        st.markdown("### Buscar")
        search = st.text_input(
            "Buscar tickets",
            placeholder="ID o título...",
            label_visibility="collapsed",
            key="search"
        )
        
        st.divider()
        
        # Filtros
        st.markdown("### Filtros")
        
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
        
        # Botón actualizar
        if st.button("↻ Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.divider()
        
        # Estado de conexión
        success, _, count = supabase.test_connection()
        st.markdown(ComponentStyles.connection_status(success, count or 0), unsafe_allow_html=True)
    
    # CONTENIDO PRINCIPAL
    st.markdown(ComponentStyles.page_header(
        "Tickets",
        "Gestiona tus oportunidades"
    ), unsafe_allow_html=True)
    
    # MAPEO DE FILTROS
    status_map = {
        "Todos": None,
        "Nuevo": "new",
        "En progreso": "in_progress",
        "Cerrado": "closed",
        "Ganado": "won"
    }
    priority_map = {
        "Todos": None,
        "Baja": "Low",
        "Media": "Medium",
        "Alta": "High"
    }
    
    # OBTENER TICKETS
    with st.spinner("Cargando tickets..."):
        tickets = supabase.fetch_tickets(
            status_map[status_filter],
            priority_map[priority_filter],
            search if search else None
        )
    
    # MÉTRICAS
    render_metrics(tickets)
    
    st.divider()
    
    # CONTADOR DE RESULTADOS
    if not tickets.empty:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span style="color: var(--text-secondary); font-size: 0.9rem;">Mostrando</span>
                <span style="background: var(--bg-tertiary); color: var(--text-primary); padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{len(tickets)} tickets</span>
            </div>
            """, unsafe_allow_html=True)
    
    # GRID DE TICKETS
    render_tickets_grid(tickets)


if __name__ == "__main__":
    main()