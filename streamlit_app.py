import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import traceback
from typing import Optional, List

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    page_title="Dashboard - Tickets de Soporte",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar tema glassmorphism
st.markdown("""
<style>
    /* Fondo y tema oscuro */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Cards glassmorphism */
    .ticket-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .ticket-card:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
    }
    
    .debug-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }
    
    /* Estilos de texto */
    h1, h2, h3 {
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stMarkdown {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: bold;
    }
    
    .status-open {
        background: rgba(255, 107, 107, 0.3);
        color: #ff6b6b;
        border: 1px solid rgba(255, 107, 107, 0.5);
    }
    
    .status-progress {
        background: rgba(255, 193, 7, 0.3);
        color: #ffc107;
        border: 1px solid rgba(255, 193, 7, 0.5);
    }
    
    .status-closed {
        background: rgba(76, 175, 80, 0.3);
        color: #4caf50;
        border: 1px solid rgba(76, 175, 80, 0.5);
    }
    
    .priority-high {
        color: #ff6b6b;
        font-weight: bold;
    }
    
    .priority-medium {
        color: #ffc107;
        font-weight: bold;
    }
    
    .priority-low {
        color: #4caf50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CREDENCIALES DE SUPABASE
# ============================================================================

SUPABASE_URL = "https://euqtlsheickstdtcfhfi.supabase.co"
SUPABASE_KEY = "sb_publishable_cVoObJObqnsKxRIXgcft4g_ejb6VJnC"
GEMINI_API_KEY = "AIzaSyBBD6CoJl2n2--7DWRTrdLxZMYcr_Mzk0I"

# ============================================================================
# FUNCIONES DE CONEXIÓN A SUPABASE
# ============================================================================

def get_supabase_connection():
    """Obtiene la conexión a Supabase"""
    try:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return client
    except Exception as e:
        return None

def test_connection() -> tuple[bool, str, Optional[int]]:
    """Prueba la conexión a Supabase y retorna (éxito, mensaje, count)"""
    try:
        client = get_supabase_connection()
        if not client:
            return False, "❌ No se pudo inicializar el cliente de Supabase", None
        
        # Intentar obtener conteo de registros
        response = client.table("opportunities").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        
        return True, "✅ Conexión exitosa a Supabase", count
    except Exception as e:
        return False, f"❌ Error de conexión: {str(e)}", None

def fetch_tickets(status_filter: Optional[str] = None, priority_filter: Optional[str] = None) -> pd.DataFrame:
    """Obtiene los tickets de Supabase con filtros opcionales"""
    try:
        client = get_supabase_connection()
        if not client:
            return pd.DataFrame()
        
        # Query base
        query = client.table("opportunities").select(
            "id, ticket_number, title, description, status, priority, notes, created_at, recording_id"
        )
        
        # Aplicar filtros
        if status_filter and status_filter != "Todos":
            query = query.eq("status", status_filter)
        
        if priority_filter and priority_filter != "Todos":
            query = query.eq("priority", priority_filter)
        
        response = query.execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            # Normalizar nombres de columnas y datos
            df.columns = df.columns.str.lower()
            return df
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error al obtener tickets: {str(e)}")
        return pd.DataFrame()

def fetch_recording_name(recording_id: Optional[str]) -> str:
    """Obtiene el nombre de la grabación por ID"""
    if not recording_id:
        return "N/A"
    
    try:
        client = get_supabase_connection()
        if not client:
            return "N/A"
        
        response = client.table("recordings").select("name").eq("id", recording_id).execute()
        if response.data:
            return response.data[0].get("name", "N/A")
        return "N/A"
    except:
        return "N/A"

def update_ticket(ticket_id: int, status: str, notes: str) -> bool:
    """Actualiza un ticket en Supabase"""
    try:
        client = get_supabase_connection()
        if not client:
            return False
        
        response = client.table("opportunities").update({
            "status": status,
            "notes": notes
        }).eq("id", ticket_id).execute()
        
        return True
    except Exception as e:
        st.error(f"Error al actualizar ticket: {str(e)}")
        return False

# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================

# Título principal
st.title("🎫 Dashboard de Tickets de Soporte")
st.markdown("*Sistema integrado con Supabase para gestión de tickets*")
st.markdown("---")

# ============================================================================
# BARRA LATERAL - FILTROS
# ============================================================================

st.sidebar.title("🎛️ Filtros")
st.sidebar.markdown("---")

# Obtener valores únicos para filtros
all_tickets = fetch_tickets()

if not all_tickets.empty:
    status_options = ["Todos"] + sorted(all_tickets["status"].unique().tolist())
    priority_options = ["Todos"] + sorted(all_tickets["priority"].unique().tolist())
else:
    status_options = ["Todos"]
    priority_options = ["Todos"]

selected_status = st.sidebar.selectbox(
    "📊 Filtrar por Estado",
    status_options,
    key="status_filter"
)

selected_priority = st.sidebar.selectbox(
    "🎯 Filtrar por Prioridad",
    priority_options,
    key="priority_filter"
)

# Botón de actualizar
if st.sidebar.button("🔄 Actualizar", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")

# Mostrar estadísticas
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.metric("Total", len(all_tickets) if not all_tickets.empty else 0)

if not all_tickets.empty:
    nuevos = len(all_tickets[all_tickets["status"] == "new"])
    en_progreso = len(all_tickets[all_tickets["status"] == "in_progress"])
    ganados = len(all_tickets[all_tickets["status"] == "won"])
    
    with col2:
        st.metric("🆕 Nuevos", nuevos)
    with col3:
        st.metric("🎉 Ganados", ganados)

# ============================================================================
# CONTENIDO PRINCIPAL - VISTA DE TARJETAS
# ============================================================================

# Obtener tickets con filtros
tickets = fetch_tickets(
    status_filter=selected_status if selected_status != "Todos" else None,
    priority_filter=selected_priority if selected_priority != "Todos" else None
)

if tickets.empty:
    st.info("📭 No hay tickets disponibles con los filtros seleccionados.")
else:
    st.subheader(f"📋 Tickets ({len(tickets)})")
    st.markdown("---")
    
    # Crear contenedor para tarjetas
    for idx, ticket in tickets.iterrows():
        with st.container():
            # Determinar color de estado
            status_value = str(ticket.get("status", "")).lower()
            if status_value == "new":
                status_class = "status-open"
                status_icon = "🆕"
                status_label = "Nuevo"
            elif status_value == "in_progress":
                status_class = "status-progress"
                status_icon = "⏳"
                status_label = "En progreso"
            elif status_value == "closed":
                status_class = "status-closed"
                status_icon = "✅"
                status_label = "Cerrado"
            elif status_value == "won":
                status_class = "status-closed"
                status_icon = "🎉"
                status_label = "Ganado"
            else:
                status_class = "status-open"
                status_icon = "❓"
                status_label = status_value
            
            # Determinar color de prioridad
            priority_value = str(ticket.get("priority", "")).lower()
            if priority_value == "high":
                priority_class = "priority-high"
                priority_icon = "⚠️"
                priority_label = "Alta"
            elif priority_value == "medium":
                priority_class = "priority-medium"
                priority_icon = "📌"
                priority_label = "Media"
            elif priority_value == "low":
                priority_class = "priority-low"
                priority_icon = "📍"
                priority_label = "Baja"
            else:
                priority_class = "priority-medium"
                priority_icon = "❓"
                priority_label = priority_value
            
            # Crear columnas para la tarjeta
            col1, col2 = st.columns([0.1, 0.9])
            
            with col1:
                st.markdown(f"<div style='font-size: 2em; margin-top: 10px;'>{priority_icon}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="ticket-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                        <div style="flex: 1;">
                            <h3 style="margin: 0; color: #ffffff;">{ticket.get('ticket_number', 'N/A')} - {ticket.get('title', 'Sin título')}</h3>
                            <p style="margin: 5px 0; color: rgba(255,255,255,0.7); font-size: 0.9em;">{ticket.get('description', '')}</p>
                        </div>
                        <div style="text-align: right;">
                            <span class="status-badge {status_class}">{status_icon} {status_label}</span>
                        </div>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 10px 0;">
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.85em; margin-bottom: 10px;">
                        <div>
                            <span style="color: rgba(255,255,255,0.5);">📅 Creado:</span><br>
                            <span style="color: rgba(255,255,255,0.9);">{ticket.get('created_at', 'N/A')[:10]}</span>
                        </div>
                        <div>
                            <span style="color: rgba(255,255,255,0.5);">🎙️ Grabación:</span><br>
                            <span style="color: rgba(255,255,255,0.9);">{ticket.get('recording_id', 'N/A')}</span>
                        </div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                        <p style="margin: 0; color: rgba(255,255,255,0.7); font-size: 0.85em;"><strong>Notas:</strong></p>
                        <p style="margin: 5px 0; color: rgba(255,255,255,0.9); font-size: 0.85em;">{ticket.get('notes', 'Sin notas') or 'Sin notas'}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Botón para expandir y editar
            with st.expander(f"✏️ Editar Ticket {ticket.get('ticket_number', 'N/A')}", expanded=False):
                edit_col1, edit_col2 = st.columns(2)
                
                with edit_col1:
                    status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
                    current_status_label = {"new": "Nuevo", "in_progress": "En progreso", "closed": "Cerrado", "won": "Ganado"}.get(ticket.get('status', 'new'), "Nuevo")
                    status_display = st.selectbox(
                        "Cambiar Estado",
                        list(status_map.keys()),
                        index=list(status_map.keys()).index(current_status_label) if current_status_label in status_map.keys() else 0,
                        key=f"status_{ticket.get('id')}"
                    )
                    new_status = status_map[status_display]
                
                with edit_col2:
                    priority_map = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
                    current_priority_label = {"Low": "Baja", "Medium": "Media", "High": "Alta"}.get(ticket.get('priority', 'Medium'), "Media")
                    priority_display = st.selectbox(
                        "Prioridad",
                        list(priority_map.keys()),
                        index=list(priority_map.keys()).index(current_priority_label) if current_priority_label in priority_map.keys() else 0,
                        key=f"priority_{ticket.get('id')}"
                    )
                    new_priority = priority_map[priority_display]
                
                new_notes = st.text_area(
                    "Agregar Notas",
                    value=ticket.get('notes', '') or '',
                    key=f"notes_{ticket.get('id')}"
                )
                
                if st.button("💾 Guardar Cambios", key=f"save_{ticket.get('id')}"):
                    if update_ticket(ticket.get('id'), new_status, new_notes):
                        st.success("✅ Ticket actualizado correctamente")
                        st.rerun()
                    else:
                        st.error("❌ Error al actualizar el ticket")

# ============================================================================
# PANEL DE DIAGNÓSTICO - DEBUG
# ============================================================================

st.markdown("---")

with st.expander("🛠️ Debug & Estado de Conexión", expanded=False):
    st.markdown("""
    <div class="debug-container">
    """, unsafe_allow_html=True)
    
    debug_col1, debug_col2 = st.columns(2)
    
    with debug_col1:
        st.subheader("📡 Verificación de Conexión")
        
        # Intentar conectar
        success, message, count = test_connection()
        
        if success:
            st.success(message)
            st.info(f"📊 Total de registros en 'opportunities': **{count}**")
        else:
            st.error(message)
    
    with debug_col2:
        st.subheader("🔑 Credenciales Configuradas")
        st.info(f"""
        **URL Supabase:** `{SUPABASE_URL[:30]}...`
        
        **API Key:** `{SUPABASE_KEY[:20]}...`
        
        **Gemini API:** `{GEMINI_API_KEY[:20]}...`
        """)
    
    st.markdown("---")
    
    st.subheader("🧪 Pruebas de Diagnóstico")
    
    if st.button("🔍 Verificar Tabla 'opportunities'"):
        try:
            client = get_supabase_connection()
            if client:
                response = client.table("opportunities").select("*").limit(3).execute()
                if response.data:
                    st.success("✅ Tabla 'opportunities' accesible")
                    st.dataframe(pd.DataFrame(response.data), use_container_width=True)
                else:
                    st.warning("⚠️ La tabla está vacía o no contiene datos")
            else:
                st.error("❌ No se pudo inicializar cliente Supabase")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.code(traceback.format_exc(), language="python")
    
    if st.button("🔍 Verificar Tabla 'recordings'"):
        try:
            client = get_supabase_connection()
            if client:
                response = client.table("recordings").select("*").limit(3).execute()
                if response.data:
                    st.success("✅ Tabla 'recordings' accesible")
                    st.dataframe(pd.DataFrame(response.data), use_container_width=True)
                else:
                    st.warning("⚠️ La tabla está vacía o no contiene datos")
            else:
                st.error("❌ No se pudo inicializar cliente Supabase")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.code(traceback.format_exc(), language="python")
    
    if st.button("📋 Listar Todas las Tablas"):
        try:
            client = get_supabase_connection()
            if client:
                # Intentar obtener información del esquema
                response = client.table("information_schema.tables").select("table_name").eq("table_schema", "public").execute()
                if response.data:
                    tables = [row["table_name"] for row in response.data]
                    st.success("✅ Tablas disponibles:")
                    for table in tables:
                        st.write(f"  • {table}")
                else:
                    st.info("No se pudo obtener listado de tablas del esquema")
            else:
                st.error("❌ No se pudo inicializar cliente Supabase")
        except Exception as e:
            st.warning("⚠️ Esquema information_schema puede requerir permisos especiales")
            st.code(str(e), language="text")
    
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📝 Información de Triaje")
    st.write("""
    - **Conexión exitosa (✅)**: El dashboard puede acceder a Supabase
    - **Conexión fallida (❌)**: Verifica las credenciales en el código
    - **Tablas no encontradas**: Verifica que existan 'opportunities' y 'recordings'
    """)