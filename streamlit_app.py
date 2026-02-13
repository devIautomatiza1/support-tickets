import streamlit as st
import pandas as pd
from datetime import datetime
import traceback
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from functools import lru_cache

# ============================================================================
# CONFIGURACIÓN Y CONSTANTES
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
    def from_display(cls, display_name: str):
        reverse_map = {v: k.value for k, v in cls.display_names().items()}
        return reverse_map.get(display_name, cls.NEW.value)

class Priority(Enum):
    """Prioridades posibles de un ticket"""
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
    def from_display(cls, display_name: str):
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
    def from_dict(cls, data: Dict[str, Any]):
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
        return asdict(self)

# ============================================================================
# ESTILOS CSS
# ============================================================================

class StyleManager:
    """Gestiona la inyección de CSS en la aplicación"""
    
    @staticmethod
    @st.cache_data
    def get_css() -> str:
        return """
        <style>
            /* ===== TOKENS ===== */
            :root {
                --bg-primary: #0A0C10;
                --bg-secondary: #111316;
                --bg-card: #16181C;
                --border: #2A2C30;
                --border-hover: #404448;
                --text-primary: #E8E9EA;
                --text-secondary: #8B8E94;
                --text-tertiary: #5E6269;
                --accent: #3B82F6;
                --accent-soft: rgba(59, 130, 246, 0.1);
                --success: #10B981;
                --warning: #F59E0B;
                --danger: #EF4444;
                --radius-lg: 16px;
                --radius-md: 12px;
                --radius-sm: 8px;
                --shadow: 0 20px 40px -12px rgba(0,0,0,0.4);
                --shadow-hover: 0 25px 50px -12px rgba(59,130,246,0.3);
                --transition: all 0.2s ease;
            }

            [data-testid="stAppViewContainer"] { 
                background: var(--bg-primary); 
            }
            
            [data-testid="stSidebar"] { 
                background: var(--bg-secondary); 
                border-right: 1px solid var(--border); 
            }

            div.row-widget.stHorizontal {
                gap: 0.75rem;
                flex-wrap: wrap;
            }

            .ticket-card {
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 0.85rem;
                transition: var(--transition);
                height: 100%;
                display: flex;
                flex-direction: column;
            }
            
            .ticket-card:hover {
                border-color: var(--border-hover);
                box-shadow: 0 6px 16px rgba(0,0,0,0.4);
                transform: translateY(-2px);
                background: linear-gradient(145deg, var(--bg-card), #1A1E24);
            }

            .ticket-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.4rem;
            }
            
            .ticket-number {
                font-family: 'SF Mono', 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                font-weight: 500;
                color: var(--text-tertiary);
                letter-spacing: 0.02em;
            }

            .badge {
                display: inline-flex;
                align-items: center;
                padding: 0.15rem 0.5rem;
                border-radius: 4px;
                font-size: 0.6rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                border: 1px solid transparent;
                white-space: nowrap;
            }
            
            .badge-new { 
                background: rgba(239,68,68,0.08); 
                color: #F87171; 
                border-color: rgba(239,68,68,0.2); 
            }
            
            .badge-progress { 
                background: rgba(245,158,11,0.08); 
                color: #FBBF24; 
                border-color: rgba(245,158,11,0.2); 
            }
            
            .badge-won { 
                background: rgba(16,185,129,0.08); 
                color: #34D399; 
                border-color: rgba(16,185,129,0.2); 
            }
            
            .badge-closed { 
                background: rgba(107,114,128,0.08); 
                color: #9CA3AF; 
                border-color: rgba(107,114,128,0.2); 
            }

            .ticket-title {
                font-size: 0.8rem;
                font-weight: 450;
                color: var(--text-primary);
                line-height: 1.3;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                min-height: 2rem;
            }

            div[data-testid="stDialog"] {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 1rem 0 !important;
            }
            
            div[data-testid="stDialog"] > div {
                background: var(--bg-card) !important;
                border: 1px solid var(--border) !important;
                border-radius: 20px !important;
                padding: 1.5rem 1.75rem !important;
                box-shadow: var(--shadow) !important;
                max-width: 600px !important;
                width: 100% !important;
                margin: 0 auto !important;
                max-height: 90vh !important;
                overflow-y: auto !important;
            }
            
            div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2 {
                display: none !important;
            }

            .modal-header {
                margin-bottom: 1rem;
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                flex-wrap: wrap;
                border-bottom: 1px solid var(--border);
                padding-bottom: 0.75rem;
            }
            
            .modal-title {
                font-size: 1.2rem;
                font-weight: 600;
                color: var(--text-primary);
                line-height: 1.3;
                letter-spacing: -0.02em;
            }
            
            .modal-date {
                font-size: 0.75rem;
                color: var(--text-tertiary);
                font-family: 'SF Mono', 'JetBrains Mono', monospace;
                background: var(--bg-secondary);
                padding: 0.2rem 0.6rem;
                border-radius: 16px;
                border: 1px solid var(--border);
            }

            .description-section {
                margin-bottom: 1.25rem;
            }
            
            .section-title {
                font-size: 0.7rem;
                font-weight: 600;
                color: var(--text-tertiary);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.5rem;
            }
            
            .description-box {
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 0.9rem 1rem;
                color: var(--text-secondary);
                font-size: 0.85rem;
                line-height: 1.5;
                white-space: pre-wrap;
            }

            .status-priority-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin-bottom: 1.25rem;
            }
            
            .info-card {
                background: var(--bg-secondary);
                border-radius: 12px;
                padding: 0.9rem;
                border: 1px solid var(--border);
            }
            
            .info-label {
                font-size: 0.6rem;
                font-weight: 600;
                color: var(--text-tertiary);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.35rem;
            }
            
            .current-value {
                display: inline-block;
                padding: 0.2rem 0.75rem;
                border-radius: 16px;
                font-size: 0.7rem;
                font-weight: 600;
                margin-bottom: 0.75rem;
            }
            
            .select-label {
                font-size: 0.6rem;
                color: var(--text-tertiary);
                margin-bottom: 0.2rem;
            }

            .stSelectbox {
                margin-bottom: 0.25rem !important;
            }
            
            .stSelectbox [data-baseweb="select"] {
                background: var(--bg-card) !important;
                border: 1px solid var(--border) !important;
                border-radius: 8px !important;
                min-height: 2rem !important;
                transition: var(--transition) !important;
            }
            
            .stSelectbox [data-baseweb="select"]:hover {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
                background: var(--bg-card) !important;
            }
            
            .stTextArea {
                margin-top: 0.25rem;
            }
            
            .stTextArea textarea {
                background: var(--bg-card) !important;
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                font-size: 0.8rem !important;
                line-height: 1.5 !important;
                padding: 0.75rem !important;
                min-height: 120px !important;
                max-height: 150px !important;
                font-family: 'SF Mono', 'JetBrains Mono', monospace !important;
                transition: var(--transition) !important;
            }
            
            .stTextArea textarea:hover {
                border-color: var(--border-hover) !important;
            }
            
            .stTextArea textarea:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
            }

            .stButton > button {
                border-radius: 8px !important;
                font-size: 0.75rem !important;
                padding: 0.35rem 0.75rem !important;
                transition: var(--transition) !important;
                font-weight: 600 !important;
                letter-spacing: 0.02em !important;
                width: 100% !important;
                background: transparent !important;
                color: var(--text-secondary) !important;
                border: 1px solid var(--border) !important;
                position: relative !important;
                overflow: hidden !important;
            }
            
            .stButton > button:hover {
                background: var(--accent-soft) !important;
                border-color: var(--accent) !important;
                color: var(--accent) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(59,130,246,0.2) !important;
            }
            
            .stButton > button:active {
                transform: translateY(0) !important;
            }
            
            .stButton > button[key*="ACTUALIZAR"] {
                background: transparent !important;
                border: 1px solid var(--border) !important;
                padding: 0.5rem 1rem !important;
                font-size: 0.8rem !important;
            }
            
            .stButton > button[key*="ACTUALIZAR"]:hover {
                background: var(--accent) !important;
                border-color: var(--accent) !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
            }
            
            .stButton > button[kind="primary"] {
                background: var(--accent) !important;
                color: white !important;
                border: none !important;
                box-shadow: 0 2px 8px rgba(59,130,246,0.2) !important;
            }
            
            .stButton > button[kind="primary"]:hover {
                background: #2563EB !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(59,130,246,0.4) !important;
            }
            
            .stButton > button[kind="primary"]:active {
                transform: translateY(0) !important;
                box-shadow: 0 2px 8px rgba(59,130,246,0.2) !important;
            }
            
            .stButton > button:not([kind="primary"]) {
                background: transparent !important;
                color: var(--text-secondary) !important;
                border: 1px solid var(--border) !important;
            }
            
            .stButton > button:not([kind="primary"]):hover {
                background: var(--bg-secondary) !important;
                border-color: var(--border-hover) !important;
                color: var(--text-primary) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
            }

            hr {
                border: none;
                height: 1px;
                background: var(--border);
                margin: 1rem 0;
            }
            
            [data-testid="metric-container"] {
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 0.6rem;
                transition: var(--transition) !important;
            }
            
            [data-testid="metric-container"]:hover {
                border-color: var(--border-hover) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
            }
            
            [data-testid="metric-container"] label {
                font-size: 0.6rem !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-value"] {
                font-size: 1.1rem !important;
            }
            
            .streamlit-expanderHeader {
                background: var(--bg-card) !important;
                border: 1px solid var(--border) !important;
                border-radius: 8px !important;
                transition: var(--transition) !important;
            }
            
            .streamlit-expanderHeader:hover {
                border-color: var(--border-hover) !important;
                background: var(--bg-secondary) !important;
            }
        </style>
        """
    
    @staticmethod
    def inject():
        st.markdown(StyleManager.get_css(), unsafe_allow_html=True)


# ============================================================================
# SERVICIO DE SUPABASE
# ============================================================================

class SupabaseService:
    """Servicio para interactuar con Supabase"""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_client(self):
        """Obtiene o crea el cliente de Supabase"""
        if self._client is None:
            try:
                from supabase import create_client
                SUPABASE_URL = st.secrets["SUPABASE_URL"]
                SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
                self._client = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as e:
                st.error(f"Error al inicializar Supabase: {e}")
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
            st.error(f"Error al obtener tickets: {e}")
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
            st.error(f"Error al actualizar ticket: {e}")
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
# COMPONENTES UI
# ============================================================================

class TicketCard:
    """Componente para renderizar una tarjeta de ticket"""
    
    BADGE_STYLES = {
        Status.NEW.value: {"class": "badge-new", "label": "NUEVO"},
        Status.IN_PROGRESS.value: {"class": "badge-progress", "label": "PROGRESO"},
        Status.WON.value: {"class": "badge-won", "label": "GANADO"},
        Status.CLOSED.value: {"class": "badge-closed", "label": "CERRADO"}
    }
    
    @classmethod
    def render(cls, ticket: Ticket):
        """Renderiza una tarjeta de ticket"""
        
        badge = cls.BADGE_STYLES.get(
            ticket.status, 
            cls.BADGE_STYLES[Status.NEW.value]
        )
        
        card_html = f"""
        <div class="ticket-card">
            <div class="ticket-header">
                <span class="ticket-number">#{ticket.ticket_number}</span>
                <span class="badge {badge['class']}">{badge['label']}</span>
            </div>
            <div class="ticket-title">{ticket.title[:60]}</div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        if st.button("EDITAR", key=f"edit_{ticket.id}", use_container_width=True):
            st.session_state.edit_ticket = ticket.to_dict()
            st.rerun()


class TicketGrid:
    """Grid de tickets en columnas"""
    
    def __init__(self, num_columns: int = 3):
        self.num_columns = num_columns
    
    @st.fragment
    def render(self, tickets_df: pd.DataFrame):
        """Renderiza el grid de tickets"""
        
        if tickets_df.empty:
            st.info("No hay tickets disponibles")
            return
        
        columns = st.columns(self.num_columns, gap="small")
        
        for idx, (_, row) in enumerate(tickets_df.iterrows()):
            with columns[idx % self.num_columns]:
                ticket = Ticket.from_dict(row.to_dict())
                TicketCard.render(ticket)


class EditTicketModal:
    """Modal para editar tickets"""
    
    STATUS_COLORS = {
        Status.NEW.value: {"bg": "rgba(239,68,68,0.1)", "color": "#F87171"},
        Status.IN_PROGRESS.value: {"bg": "rgba(245,158,11,0.1)", "color": "#FBBF24"},
        Status.CLOSED.value: {"bg": "rgba(107,114,128,0.1)", "color": "#9CA3AF"},
        Status.WON.value: {"bg": "rgba(16,185,129,0.1)", "color": "#34D399"}
    }
    
    PRIORITY_COLORS = {
        Priority.LOW.value: {"bg": "rgba(16,185,129,0.1)", "color": "#34D399"},
        Priority.MEDIUM.value: {"bg": "rgba(245,158,11,0.1)", "color": "#FBBF24"},
        Priority.HIGH.value: {"bg": "rgba(239,68,68,0.1)", "color": "#F87171"}
    }
    
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
    
    def _clean_description(self, description: str) -> str:
        """Limpia la descripción eliminando líneas vacías"""
        if description:
            return "\n".join([line for line in description.split("\n") if line.strip()])
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
        """Renderiza la sección de estado y retorna el nuevo estado"""
        
        status_style = self.STATUS_COLORS.get(
            ticket.status, 
            self.STATUS_COLORS[Status.NEW.value]
        )
        status_label = Status.display_names().get(
            Status(ticket.status), 
            "Nuevo"
        )
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">ESTADO ACTUAL</div>
            <span class="current-value" style="background: {status_style['bg']}; color: {status_style['color']};">
                {status_label}
            </span>
            <div class="select-label">CAMBIAR A</div>
        </div>
        """, unsafe_allow_html=True)
        
        status_options = list(Status.display_names().values())
        current_idx = list(Status.display_names().keys()).index(
            Status(ticket.status)
        ) if Status(ticket.status) in Status.display_names().keys() else 0
        
        new_status_display = st.selectbox(
            "", 
            status_options, 
            index=current_idx, 
            key=f"status_{ticket.id}", 
            label_visibility="collapsed"
        )
        
        return Status.from_display(new_status_display)
    
    def _render_priority_section(self, ticket: Ticket) -> str:
        """Renderiza la sección de prioridad y retorna la nueva prioridad"""
        
        priority_style = self.PRIORITY_COLORS.get(
            ticket.priority,
            self.PRIORITY_COLORS[Priority.MEDIUM.value]
        )
        priority_label = Priority.display_names().get(
            Priority(ticket.priority),
            "Media"
        )
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">PRIORIDAD ACTUAL</div>
            <span class="current-value" style="background: {priority_style['bg']}; color: {priority_style['color']};">
                {priority_label}
            </span>
            <div class="select-label">CAMBIAR A</div>
        </div>
        """, unsafe_allow_html=True)
        
        priority_options = list(Priority.display_names().values())
        current_idx = list(Priority.display_names().keys()).index(
            Priority(ticket.priority)
        ) if Priority(ticket.priority) in Priority.display_names().keys() else 1
        
        new_priority_display = st.selectbox(
            "", 
            priority_options, 
            index=current_idx, 
            key=f"priority_{ticket.id}", 
            label_visibility="collapsed"
        )
        
        return Priority.from_display(new_priority_display)
    
    def _render_notes_form(self, ticket: Ticket, new_status: str, new_priority: str):
        """Renderiza el formulario de notas"""
        
        st.markdown("""
        <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
            <span class="section-title">NOTAS</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key=f"edit_modal_form_{ticket.id}"):
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
                    "Guardar cambios", 
                    use_container_width=True,
                    type="primary"
                )
            
            with col3:
                cancelled = st.form_submit_button(
                    "Cancelar", 
                    use_container_width=True
                )
            
            if saved:
                if self.supabase.update_ticket(
                    ticket.id,
                    new_status,
                    new_notes,
                    new_priority
                ):
                    st.success("✓ Actualizado")
                    st.rerun()
                else:
                    st.error("Error al actualizar")
            
            if cancelled:
                st.rerun()


class SidebarComponent:
    """Componente de barra lateral"""
    
    def __init__(self, supabase_service: SupabaseService):
        self.supabase = supabase_service
    
    def render(self) -> Tuple[Optional[str], Optional[str]]:
        """Renderiza la barra lateral y retorna los filtros seleccionados"""
        
        with st.sidebar:
            st.markdown("## Filtros")
            
            all_tickets = self.supabase.fetch_tickets()
            
            status_filter = st.selectbox(
                "Estado",
                ["Todos"] + list(Status.display_names().values()),
                key="status_filter"
            )
            
            priority_filter = st.selectbox(
                "Prioridad",
                ["Todos"] + list(Priority.display_names().values()),
                key="priority_filter"
            )
            
            # Mapear valores de display a valores de DB
            status_map = {"Todos": "Todos"}
            status_map.update({v: k.value for k, v in Status.display_names().items()})
            
            priority_map = {"Todos": "Todos"}
            priority_map.update({v: k.value for k, v in Priority.display_names().items()})
            
            selected_status = status_map[status_filter]
            selected_priority = priority_map[priority_filter]
            
            if st.button("ACTUALIZAR", key="ACTUALIZAR", use_container_width=True):
                st.rerun()
            
            st.divider()
            
            self._render_stats(all_tickets)
            
            return selected_status, selected_priority
    
    def _render_stats(self, tickets_df: pd.DataFrame):
        """Renderiza las estadísticas en la barra lateral"""
        
        st.markdown("## Estadísticas")
        
        if tickets_df.empty:
            st.info("Sin datos")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total", len(tickets_df))
        with col2:
            nuevos = len(tickets_df[tickets_df["status"] == Status.NEW.value])
            st.metric("Nuevos", nuevos)
        with col3:
            ganados = len(tickets_df[tickets_df["status"] == Status.WON.value])
            st.metric("Ganados", ganados)


class DiagnosticsComponent:
    """Componente de diagnóstico del sistema"""
    
    def __init__(self, supabase_service: SupabaseService):
        self.supabase = supabase_service
    
    def render(self):
        """Renderiza el panel de diagnóstico"""
        
        with st.expander("Diagnóstico del sistema", expanded=False):
            success, msg, count = self.supabase.test_connection()
            
            if success:
                st.success(f"{msg} — {count} registros")
            else:
                st.error(msg)
            
            st.caption(f"URL: Configurada en secrets")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Ver opportunities", key="ver_opp"):
                    data = self.supabase.get_sample_data("opportunities")
                    if data:
                        st.dataframe(pd.DataFrame(data))
            with col2:
                if st.button("🎙️ Ver recordings", key="ver_rec"):
                    data = self.supabase.get_sample_data("recordings")
                    if data:
                        st.dataframe(pd.DataFrame(data))


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

class TicketDashboardApp:
    """Aplicación principal del dashboard de tickets"""
    
    def __init__(self):
        self.supabase = SupabaseService()
        self.sidebar = SidebarComponent(self.supabase)
        self.ticket_grid = TicketGrid(num_columns=3)
        self.edit_modal = EditTicketModal(self.supabase)
        self.diagnostics = DiagnosticsComponent(self.supabase)
    
    def setup_page(self):
        """Configuración inicial de la página"""
        st.set_page_config(
            page_title="Dashboard de Tickets",
            page_icon="🎫",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Inyectar CSS
        StyleManager.inject()
    
    def render_header(self):
        """Renderiza el header de la aplicación"""
        st.title("Dashboard")
        st.markdown(
            "<h3 style='color: var(--text-secondary); font-weight: 400; margin-top: -0.5rem;'>"
            "Gestión de oportunidades"
            "</h3>", 
            unsafe_allow_html=True
        )
        st.divider()
    
    def render_main_content(self, status_filter: Optional[str], priority_filter: Optional[str]):
        """Renderiza el contenido principal"""
        
        tickets = self.supabase.fetch_tickets(
            status_filter=status_filter if status_filter != "Todos" else None,
            priority_filter=priority_filter if priority_filter != "Todos" else None
        )
        
        if tickets.empty:
            st.info("No hay tickets con los filtros seleccionados.")
        else:
            st.markdown(f"#### {len(tickets)} tickets encontrados")
            self.ticket_grid.render(tickets)
    
    def render_edit_modal(self):
        """Renderiza el modal de edición si está activo"""
        if "edit_ticket" in st.session_state and st.session_state.edit_ticket:
            self.edit_modal.render(st.session_state.edit_ticket)
            st.session_state.edit_ticket = None
    
    def run(self):
        """Ejecuta la aplicación"""
        
        # Configuración inicial
        self.setup_page()
        
        # Header
        self.render_header()
        
        # Sidebar con filtros
        status_filter, priority_filter = self.sidebar.render()
        
        # Contenido principal
        self.render_main_content(status_filter, priority_filter)
        
        # Modal de edición
        self.render_edit_modal()
        
        # Diagnóstico
        self.diagnostics.render()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

def main():
    app = TicketDashboardApp()
    app.run()


if __name__ == "__main__":
    main()