"""
Dashboard SaaS Pro de gestión de tickets con Glassmorphism.
Diseño profesional tipo Linear, Holded, Vercel - VERSIÓN SIMPLIFICADA
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random
import base64
from pathlib import Path

from styles import StyleManager, ComponentStyles


# Función para cargar imagen y convertir a base64
@st.cache_data
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None


# Configuración
st.set_page_config(
    page_title="FlowTickets | SaaS Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

StyleManager.inject_all()

# Session state init
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
def render_tickets(tickets_df: pd.DataFrame):
    """Renderiza los tickets en grid 3D minimalista con edición integrada en popover"""
    if tickets_df.empty:
        st.markdown("""
        <div class="glass" style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem; opacity: 0.5;">✨</div>
            <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">No hay tickets</h3>
            <p style="color: var(--text-muted); font-size: 0.95rem;">Los tickets aparecerán aquí cuando estén disponibles</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    cols = st.columns(3, gap="large")
    for idx, (_, row) in enumerate(tickets_df.iterrows()):
        with cols[idx % 3]:
            ticket = Ticket.from_dict(row.to_dict())
            
            # Extraer persona del título si existe
            title_parts = ticket.title.split(" - ")
            display_title = ticket.title
            person = ""
            if len(title_parts) > 1:
                display_title = title_parts[0]
                person = title_parts[1]
            
            # Descripción truncada
            description = ticket.description[:80] + "..." if len(ticket.description) > 80 else ticket.description
            date_str = ticket.created_at[:10] if ticket.created_at else "2026-02-13"
            
            # Mapeo de estados y colores
            status_map = {
                "new": ("badge-new", "NUEVO"),
                "in_progress": ("badge-in-progress", "EN PROGRESO"),
                "won": ("badge-won", "GANADO"),
                "closed": ("badge-closed", "CERRADO")
            }
            badge_class, status_text = status_map.get(ticket.status, ("badge-new", "NUEVO"))
            
            # Renderizar tarjeta premium
            st.markdown(f"""
            <div class="premium-ticket-card">
                <div class="ticket-header">
                    <div class="ticket-header-left">
                        <div class="ticket-number">#{ticket.ticket_number}</div>
                        <div class="ticket-title">{display_title}</div>
                        {'<div class="ticket-person">👤 ' + person + '</div>' if person else ''}
                    </div>
                </div>
                <div class="ticket-description">"{description}"</div>
                <div class="ticket-footer">
                    <span class="badge badge-sm {badge_class}">{status_text}</span>
                    <span>📅 {date_str}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Popover discreto - integrado DENTRO de la tarjeta (arriba a la derecha)
            st.markdown(f"""
            <div style="position: relative; margin-top: -4.1rem;">
                <div style="position: absolute; top: 0.75rem; right: 0.75rem; z-index: 20;">
                    <div id="popover-anchor-{ticket.id}"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Contenedor del popover dentro de la tarjeta
            with st.container():
                col_empty, col_popover = st.columns([0.85, 0.15], gap="small")
                with col_popover:
                    with st.popover("⋯", use_container_width=True):
                        st.markdown(f"### #{ticket.ticket_number}")
                        st.caption(display_title)
                        st.divider()
                        
                        # Mini-formulario dentro del popover
                        status_label = Status.display_names().get(Status(ticket.status), "Nuevo")
                        priority_label = Priority.display_names().get(Priority(ticket.priority), "Media")
                        
                        new_status_label = st.selectbox(
                            "Estado",
                            list(Status.display_names().values()),
                            index=list(Status.display_names().values()).index(status_label),
                            key=f"pop_status_{ticket.id}"
                        )
                        new_status = Status.from_display(new_status_label)
                        
                        new_priority_label = st.selectbox(
                            "Prioridad",
                            list(Priority.display_names().values()),
                            index=list(Priority.display_names().values()).index(priority_label),
                            key=f"pop_priority_{ticket.id}"
                        )
                        new_priority = Priority.from_display(new_priority_label)
                        
                        new_notes = st.text_area(
                            "Notas",
                            value=ticket.notes,
                            height=100,
                            key=f"pop_notes_{ticket.id}",
                            placeholder="Añade notas internas..."
                        )
                        
                        st.divider()
                        
                        # Botón guardar en popover
                        if st.button("💾 Guardar", key=f"pop_save_{ticket.id}", use_container_width=True, type="primary"):
                            supabase = SupabaseService()
                            if supabase.update_ticket(ticket.id, new_status, new_notes, new_priority):
                                st.success("✅ Actualizado")
                                st.rerun()
                            else:
                                st.error("❌ Error al guardar")




# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    supabase = SupabaseService()
    
    # Cargar el icono
    icon_base64 = get_image_base64("icon.jpeg")
    
    # SIDEBAR PREMIUM
    with st.sidebar:
        # Icono personalizado con texto "Control Tickets" y "IAutomatiza"
        if icon_base64:
            st.markdown(f"""
            <div style="padding: 1.5rem 0.5rem; text-align: center;">
                <div style="background: linear-gradient(135deg, var(--accent), #1e40af); width: 60px; height: 60px; border-radius: 16px; margin: 0 auto 0.5rem auto; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                    <img src="data:image/jpeg;base64,{icon_base64}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h2 style="margin: 0; color: var(--text-primary); font-size: 1.5rem;">Control Tickets</h2>
                <p style="margin: 0.25rem 0 0 0; color: var(--text-muted); font-size: 0.8rem;">IAutomatiza</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback si no se encuentra el icono
            st.markdown("""
            <div style="padding: 1.5rem 0.5rem; text-align: center;">
                <div style="background: linear-gradient(135deg, var(--accent), #1e40af); width: 60px; height: 60px; border-radius: 16px; margin: 0 auto 0.5rem auto; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 2rem;">🎫</span>
                </div>
                <h2 style="margin: 0; color: var(--text-primary); font-size: 1.5rem;">Control Tickets</h2>
                <p style="margin: 0.25rem 0 0 0; color: var(--text-muted); font-size: 0.8rem;">IAutomatiza</p>
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
    
    # RENDERIZAR TICKETS
    render_tickets(tickets)


if __name__ == "__main__":
    main()