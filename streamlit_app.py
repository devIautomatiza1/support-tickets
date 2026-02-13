"""
Dashboard SaaS Pro - Gestión de Tickets
Diseño ultra minimalista tipo Linear
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import random
import base64
from pathlib import Path
import time
import re
from PIL import Image
from io import BytesIO
from datetime import datetime

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
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {}


# ============================================================================
# MODELOS MEJORADOS
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
    def get_badge_class(cls, status: str) -> str:
        badge_map = {
            "new": "badge-new",
            "in_progress": "badge-progress",
            "won": "badge-won",
            "closed": "badge-closed"
        }
        return badge_map.get(status, "badge-new")


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
    def css_class(cls, priority: str) -> str:
        priority_map = {
            "Low": "low",
            "Medium": "medium",
            "High": "high"
        }
        return priority_map.get(priority, "medium")


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
    
    @property
    def display_title(self) -> str:
        """Extrae el título limpio sin el prefijo [IA]"""
        title = self.title
        # Remover [IA] del inicio si existe
        if title.startswith("[IA] "):
            title = title[5:]
        return title.strip()
    
    @property
    def person(self) -> Optional[str]:
        """Extrae la persona mencionada del título si existe"""
        # Buscar patrones como " - Nombre" al final del título
        match = re.search(r'-\s*([^-]+)$', self.title)
        if match:
            return match.group(1).strip()
        
        # Si no hay patrón, buscar en la descripción o notas
        if self.description and "mencionado por:" in self.notes.lower():
            # Intentar extraer de las notas estructuradas
            person_match = re.search(r'👤 Mencionado por:\s*([^\n]+)', self.notes)
            if person_match:
                return person_match.group(1).strip()
        
        return None
    
    @property
    def clean_description(self) -> str:
        """Obtiene una descripción limpia y resumida"""
        # Si es un ticket generado por IA, usar el contexto de las notas
        if self.notes and "🤖 TICKET GENERADO AUTOMÁTICAMENTE" in self.notes:
            context_match = re.search(r'💬 Contexto:\s*"([^"]+)"', self.notes)
            if context_match:
                return context_match.group(1).strip()
        
        # Si no, usar la descripción original pero limpiarla
        if self.description:
            # Remover comillas extras y espacios
            clean = self.description.strip('"').strip()
            # Si es muy larga, acortar inteligentemente
            if len(clean) > 100:
                # Intentar cortar en un punto final
                sentences = re.split(r'[.!?]', clean)
                if len(sentences[0]) < 80:
                    return sentences[0] + "..."
                return clean[:97] + "..."
            return clean
        
        return "Sin descripción"
    
    @property
    def is_ai_generated(self) -> bool:
        """Verifica si el ticket fue generado por IA"""
        return bool(self.notes and "🤖 TICKET GENERADO AUTOMÁTICAMENTE" in self.notes)
    
    @property
    def confidence_score(self) -> Optional[int]:
        """Extrae el score de confianza si existe"""
        if self.notes:
            match = re.search(r'🎯 Confianza:\s*(\d+)%', self.notes)
            if match:
                return int(match.group(1))
        return None
    
    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        """Crea un ticket desde un diccionario con validaciones mejoradas"""
        
        # Validación de status
        status = data.get("status", Status.NEW.value)
        if not status:
            status = Status.NEW.value
        status = str(status).lower().strip()
        if status not in [s.value for s in Status]:
            status = Status.NEW.value
        
        # Validación de priority
        priority = data.get("priority", Priority.MEDIUM.value)
        if not priority:
            priority = Priority.MEDIUM.value
        priority = str(priority).strip()
        if priority not in [p.value for p in Priority]:
            priority = Priority.MEDIUM.value
        
        # Asegurar que ticket_number sea string
        ticket_number = data.get("ticket_number")
        if ticket_number is None:
            ticket_number = f"TKT-{random.randint(1000, 9999)}"
        else:
            ticket_number = str(ticket_number).strip()
        
        return cls(
            id=data.get("id"),
            ticket_number=ticket_number,
            title=str(data.get("title", "Sin título") or "Sin título").strip(),
            description=str(data.get("description", "") or "").strip(),
            status=status,
            priority=priority,
            notes=str(data.get("notes", "") or "").strip(),
            created_at=str(data.get("created_at", datetime.now().strftime("%Y-%m-%d")) or datetime.now().strftime("%Y-%m-%d")).strip()
        )


# ============================================================================
# SERVICIO SUPABASE (MEJORADO)
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
                st.error(f"Error de conexión: {e}")
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
            
            response = query.order("created_at", desc=True).execute()
            
            if response.data:
                df = pd.DataFrame(response.data)
                df.columns = df.columns.str.lower()
                
                if search_query:
                    search_query = search_query.lower()
                    mask = (
                        df['title'].str.lower().str.contains(search_query, na=False) |
                        df['ticket_number'].str.lower().str.contains(search_query, na=False) |
                        df['description'].str.lower().str.contains(search_query, na=False)
                    )
                    df = df[mask]
                
                return df
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching tickets: {e}")
            return pd.DataFrame()
    
    def update_ticket(self, ticket_id: int, status: str, notes: str, 
                     priority: Optional[str] = None) -> bool:
        try:
            client = self._get_client()
            if not client:
                return False
            
            # Validar que notes no sea basura
            if notes and len(notes.strip()) < 2:
                notes = "[Nota actualizada]"
            
            data = {"status": status, "notes": notes}
            if priority:
                data["priority"] = priority
            
            client.table("opportunities").update(data).eq("id", ticket_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating ticket: {e}")
            return False


# ============================================================================
# COMPONENTES UI MEJORADOS
# ============================================================================

def render_metrics(tickets_df: pd.DataFrame):
    """Métricas minimalistas con mejor diseño"""
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
        ("Nuevos", str(new_count), "🆕", f"{round(new_count/total*100) if total > 0 else 0}%"),
        ("En progreso", str(in_progress), "⏳", f"{round(in_progress/total*100) if total > 0 else 0}%"),
        ("Alta prioridad", str(high_priority), "⚡", f"{round(high_priority/total*100) if total > 0 else 0}%")
    ]
    
    for col, (title, value, icon, trend) in zip(cols, metrics):
        with col:
            st.markdown(ComponentStyles.stat_card(title, value, icon, trend), unsafe_allow_html=True)


@st.fragment
def render_ticket_card(ticket: Ticket):
    """Renderiza una tarjeta de ticket minimalista con manejo mejorado"""
    
    # Usar las propiedades mejoradas del modelo
    display_title = ticket.display_title
    person = ticket.person
    clean_description = ticket.clean_description
    is_ai = ticket.is_ai_generated
    confidence = ticket.confidence_score
    
    # Badge y prioridad
    badge_class = Status.get_badge_class(ticket.status)
    status_text = Status.display_names().get(Status(ticket.status), "Nuevo")
    priority_class = Priority.css_class(ticket.priority)
    
    # Determinar el ícono de IA si aplica
    ai_badge = '<span class="ai-badge">🤖 IA</span>' if is_ai else ''
    
    # HTML de la tarjeta mejorado
    card_html = f"""
    <div class="ticket-card {'ticket-ai' if is_ai else ''}">
        <div class="ticket-header">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span class="ticket-id">#{ticket.ticket_number}</span>
                {ai_badge}
                {f'<span class="confidence-badge">{confidence}%</span>' if confidence else ''}
            </div>
            <div class="ticket-menu" id="menu-{ticket.id}">
                <span style="color: var(--text-tertiary);">⋯</span>
            </div>
        </div>
        <div class="ticket-title">{display_title}</div>
        {f'<div class="ticket-person"><i class="far fa-user" style="font-size: 0.7rem;"></i> {person}</div>' if person else ''}
        <div class="ticket-description">"{clean_description}"</div>
        <div class="ticket-footer">
            <span class="badge {badge_class}">{status_text}</span>
            <div class="priority-indicator">
                <span class="priority-dot {priority_class}"></span>
                <span style="color: var(--text-tertiary); font-size: 0.7rem;">{ticket.created_at[:10]}</span>
            </div>
        </div>
    </div>
    """
    
    # Crear un contenedor para la tarjeta
    card_container = st.container()
    
    with card_container:
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Popover para edición (solo visible al hacer clic en el menú)
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            with st.popover("✏️ Editar ticket", use_container_width=True):
                st.markdown(f"### Ticket #{ticket.ticket_number}")
                st.caption(display_title)
                
                if is_ai:
                    st.info("Este ticket fue generado automáticamente por IA")
                
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
                
                # Mostrar notas actuales
                st.markdown("**Notas actuales:**")
                if ticket.notes:
                    st.text(ticket.notes[:200] + ("..." if len(ticket.notes) > 200 else ""))
                
                new_notes = st.text_area(
                    "Actualizar notas",
                    value="",
                    placeholder="Añade una nota...",
                    key=f"notes_{ticket.id}",
                    help="Las notas anteriores se mantendrán, esta es una nueva actualización"
                )
                
                # Botones de acción
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar", type="primary", key=f"save_{ticket.id}", use_container_width=True):
                        if new_notes.strip():
                            # Append a las notas existentes
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                            updated_notes = f"{ticket.notes}\n\n[{timestamp}] {new_notes}"
                        else:
                            updated_notes = ticket.notes
                        
                        supabase = SupabaseService()
                        if supabase.update_ticket(
                            ticket.id,
                            Status.from_display(new_status),
                            updated_notes,
                            Priority.from_display(new_priority)
                        ):
                            st.success("✓ Ticket actualizado")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Error al guardar")
                
                with col_cancel:
                    if st.button("Cancelar", key=f"cancel_{ticket.id}", use_container_width=True):
                        st.rerun()


def render_tickets_grid(tickets_df: pd.DataFrame):
    """Renderiza el grid de tickets con mejor manejo de datos vacíos"""
    if tickets_df.empty:
        st.markdown("""
        <div style="text-align: center; padding: 4rem; background: var(--bg-secondary); border-radius: 24px; border: 1px solid var(--border-medium);">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">✨</div>
            <h3 style="color: var(--text-secondary); margin-bottom: 0.5rem;">No hay tickets</h3>
            <p style="color: var(--text-tertiary);">Los tickets aparecerán aquí cuando estén disponibles</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Grid de 3 columnas con altura consistente
    cols = st.columns(3, gap="small")
    
    # Ordenar por fecha (más recientes primero)
    tickets_df = tickets_df.sort_values("created_at", ascending=False)
    
    tickets_rendered = 0
    for idx, (_, row) in enumerate(tickets_df.iterrows()):
        try:
            ticket = Ticket.from_dict(row.to_dict())
            with cols[idx % 3]:
                render_ticket_card(ticket)
                tickets_rendered += 1
        except Exception as e:
            st.error(f"Error rendering ticket: {e}")
            continue


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
        
        # Búsqueda con debounce
        st.markdown("### Buscar")
        search = st.text_input(
            "Buscar tickets",
            placeholder="ID, título o descripción...",
            label_visibility="collapsed",
            key="search",
            help="Busca por número de ticket, título o contenido"
        )
        
        st.divider()
        
        # Filtros
        st.markdown("### Filtros")
        
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Estado",
                ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"],
                key="status_filter"
            )
        
        with col2:
            priority_filter = st.selectbox(
                "Prioridad",
                ["Todos", "Baja", "Media", "Alta"],
                key="priority_filter"
            )
        
        # Filtro de tipo de ticket
        ticket_type = st.radio(
            "Tipo",
            ["Todos", "Generados por IA", "Manuales"],
            key="ticket_type",
            horizontal=True
        )
        
        # Botón actualizar
        if st.button("↻ Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.divider()
        
        # Estado de conexión con más detalles
        success, message, count = supabase.test_connection()
        st.markdown(ComponentStyles.connection_status(success, message, count or 0), unsafe_allow_html=True)
        
        # Estadísticas rápidas
        if success and count:
            st.caption(f"📊 Total en BD: {count} tickets")
    
    # CONTENIDO PRINCIPAL
    st.markdown(ComponentStyles.page_header(
        "Tickets",
        "Gestiona tus oportunidades de negocio"
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
    
    # Aplicar filtro de tipo si es necesario
    if not tickets.empty and ticket_type != "Todos":
        tickets['is_ai'] = tickets['notes'].str.contains("🤖 TICKET GENERADO AUTOMÁTICAMENTE", na=False)
        if ticket_type == "Generados por IA":
            tickets = tickets[tickets['is_ai'] == True]
        elif ticket_type == "Manuales":
            tickets = tickets[tickets['is_ai'] == False]
        tickets = tickets.drop('is_ai', axis=1)
    
    # MÉTRICAS
    render_metrics(tickets)
    
    st.divider()
    
    # CONTADOR DE RESULTADOS Y ACCIONES
    if not tickets.empty:
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span style="color: var(--text-secondary); font-size: 0.9rem;">Mostrando</span>
                <span style="background: var(--bg-tertiary); color: var(--text-primary); padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{len(tickets)} tickets</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("📥 Exportar CSV", use_container_width=True):
                csv = tickets.to_csv(index=False)
                st.download_button(
                    "Descargar",
                    csv,
                    f"tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    key="download-csv"
                )
    
    # GRID DE TICKETS
    render_tickets_grid(tickets)


if __name__ == "__main__":
    main()