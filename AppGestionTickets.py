import streamlit as st
import supabase
import requests
import pandas as pd
import datetime
import os

# --- CONFIGURACIÓN DE LA PÁGINA (DEBE SER LO PRIMERO) ---
st.set_page_config(
    page_title="AppGestionTickets", 
    page_icon="📝", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TÍTULO PRINCIPAL ---
st.title("📝 AppGestionTickets - Gestión de Tickets con Supabase")
st.markdown("---")

# --- CONFIGURACIÓN DE CREDENCIALES ---
# Intentar obtener credenciales de diferentes fuentes
SUPABASE_URL = None
SUPABASE_KEY = None
GEMINI_API_KEY = None

# 1. Primero intentar desde secrets de Streamlit
try:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
except:
    pass

# 2. Si no, intentar desde variables de entorno
if not SUPABASE_URL:
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
if not SUPABASE_KEY:
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# --- PANEL DE DIAGNÓSTICO VISUAL ---
with st.expander("🔍 PANEL DE DIAGNÓSTICO - Verificar conexión a Supabase", expanded=True):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 1. Verificación de Credenciales")
        
        # Supabase URL
        if SUPABASE_URL:
            st.success(f"✅ SUPABASE_URL: {SUPABASE_URL[:20]}...")
        else:
            st.error("❌ SUPABASE_URL no configurada")
            st.info("💡 Configura en .streamlit/secrets.toml o variables de entorno")
        
        # Supabase Key
        if SUPABASE_KEY:
            masked_key = f"{SUPABASE_KEY[:8]}...{SUPABASE_KEY[-4:]}" if len(SUPABASE_KEY) > 12 else "***configurada***"
            st.success(f"✅ SUPABASE_KEY: {masked_key}")
        else:
            st.error("❌ SUPABASE_KEY no configurada")
        
        # Gemini Key
        if GEMINI_API_KEY:
            masked_gemini = f"{GEMINI_API_KEY[:8]}...{GEMINI_API_KEY[-4:]}" if len(GEMINI_API_KEY) > 12 else "***configurada***"
            st.success(f"✅ GEMINI_API_KEY: {masked_gemini}")
        else:
            st.warning("⚠️ GEMINI_API_KEY no configurada (solo para análisis con IA)")
    
    with col2:
        st.subheader("🔄 2. Prueba de Conexión a Supabase")
        
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                with st.spinner("Conectando a Supabase..."):
                    client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
                    
                    # Prueba simple de conexión
                    test_query = client.table("opportunities").select("count", count="exact").limit(1).execute()
                    
                    st.success("✅ Conexión a Supabase EXITOSA")
                    
                    # Verificar tabla opportunities
                    try:
                        table_check = client.table("opportunities").select("*").limit(1).execute()
                        if table_check.data:
                            st.success(f"✅ Tabla 'opportunities' encontrada")
                            st.info(f"📊 Columnas disponibles: {list(table_check.data[0].keys())}")
                        else:
                            st.warning("⚠️ Tabla 'opportunities' existe pero está vacía")
                    except Exception as e:
                        st.error(f"❌ Error con tabla 'opportunities': {str(e)}")
                        st.info("💡 Verifica que el nombre de la tabla sea correcto (case-sensitive)")
                        
            except Exception as e:
                st.error(f"❌ Error de conexión a Supabase: {str(e)}")
                client = None
        else:
            st.warning("⏸️ Credenciales incompletas - No se puede probar conexión")
            client = None

st.markdown("---")

# --- FUNCIONES PRINCIPALES ---
@st.cache_data(ttl=30)  # Cache por 30 segundos para datos en tiempo real
def cargar_tickets_supabase():
    """Carga todos los tickets desde Supabase con debugging incluido"""
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.sidebar.error("❌ Credenciales de Supabase no configuradas")
        return pd.DataFrame()
    
    if 'client' not in locals() and 'client' not in globals():
        try:
            client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            st.error(f"Error creando cliente Supabase: {e}")
            return pd.DataFrame()
    
    try:
        # Mostrar estado en sidebar
        with st.sidebar.container():
            st.sidebar.info("🔄 Cargando tickets desde Supabase...")
            
            # Ejecutar consulta
            query = (
                client.table("opportunities")
                .select("id, recording_id, title, description, created_at, status, priority, ticket_number, notes, updated_at, recordings(filename, transcription)")
                .order("created_at", desc=True)
            )
            
            response = query.execute()
            
            if response.data:
                st.sidebar.success(f"✅ {len(response.data)} tickets cargados")
                df = pd.DataFrame(response.data)
                
                # Guardar timestamp en session_state
                st.session_state.ultima_actualizacion = datetime.datetime.now().strftime("%H:%M:%S")
                st.session_state.total_tickets = len(df)
                
                return df
            else:
                st.sidebar.warning("⚠️ No se encontraron tickets")
                return pd.DataFrame()
                
    except Exception as e:
        st.sidebar.error(f"❌ Error cargando tickets: {str(e)}")
        return pd.DataFrame()

def traducir_estado(status_en):
    """Traduce estado de inglés a español"""
    traducciones = {
        "Open": "Abierto", 
        "In Progress": "En progreso", 
        "Closed": "Cerrado",
        "open": "Abierto",
        "in progress": "En progreso", 
        "closed": "Cerrado"
    }
    return traducciones.get(status_en, status_en)

def traducir_prioridad(priority_en):
    """Traduce prioridad de inglés a español"""
    traducciones = {
        "High": "Alta", 
        "Medium": "Media", 
        "Low": "Baja",
        "high": "Alta",
        "medium": "Media", 
        "low": "Baja"
    }
    return traducciones.get(priority_en, priority_en)

def estado_a_ingles(status_es):
    """Traduce estado de español a inglés"""
    traducciones = {
        "Abierto": "Open", 
        "En progreso": "In Progress", 
        "Cerrado": "Closed"
    }
    return traducciones.get(status_es, status_es)

def prioridad_a_ingles(priority_es):
    """Traduce prioridad de español a inglés"""
    traducciones = {
        "Alta": "High", 
        "Media": "Medium", 
        "Baja": "Low"
    }
    return traducciones.get(priority_es, priority_es)

# --- SIDEBAR - FILTROS Y CONTROLES ---
st.sidebar.header("🎛️ Panel de Control")

# Botón para recargar datos manualmente
if st.sidebar.button("🔄 Recargar tickets", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# Mostrar última actualización
if 'ultima_actualizacion' in st.session_state:
    st.sidebar.info(f"📅 Última actualización: {st.session_state.ultima_actualizacion}")
    st.sidebar.info(f"🎫 Total tickets: {st.session_state.total_tickets}")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros")

# --- CARGAR DATOS DESDE SUPABASE ---
df = cargar_tickets_supabase()

# --- APLICACIÓN PRINCIPAL ---
if not df.empty:
    
    # Preparar datos para filtros
    df['estado_es'] = df['status'].apply(traducir_estado)
    df['prioridad_es'] = df['priority'].apply(traducir_prioridad)
    
    # Filtros en sidebar
    status_filter = st.sidebar.selectbox(
        "Estado del ticket",
        ["Todos"] + sorted(df['estado_es'].unique().tolist()),
        key="sidebar_status_filter"
    )
    
    priority_filter = st.sidebar.selectbox(
        "Prioridad",
        ["Todas"] + sorted(df['prioridad_es'].unique().tolist()),
        key="sidebar_priority_filter"
    )
    
    # Búsqueda por texto
    search_term = st.sidebar.text_input("🔎 Buscar en tickets", placeholder="Título, descripción, ticket #...")
    
    # Aplicar filtros
    df_filtered = df.copy()
    
    if status_filter != "Todos":
        df_filtered = df_filtered[df_filtered['estado_es'] == status_filter]
    
    if priority_filter != "Todas":
        df_filtered = df_filtered[df_filtered['prioridad_es'] == priority_filter]
    
    if search_term:
        mask = (
            df_filtered['title'].str.contains(search_term, case=False, na=False) |
            df_filtered['description'].str.contains(search_term, case=False, na=False) |
            df_filtered['ticket_number'].astype(str).str.contains(search_term, case=False, na=False) |
            df_filtered['notes'].str.contains(search_term, case=False, na=False)
        )
        df_filtered = df_filtered[mask]
    
    # --- MÉTRICAS Y ESTADÍSTICAS ---
    st.header("📊 Dashboard de Tickets")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Tickets", len(df_filtered))
    with col2:
        abiertos = len(df_filtered[df_filtered['status'].str.lower() == "open"])
        st.metric("Abiertos", abiertos)
    with col3:
        en_progreso = len(df_filtered[df_filtered['status'].str.lower() == "in progress"])
        st.metric("En Progreso", en_progreso)
    with col4:
        cerrados = len(df_filtered[df_filtered['status'].str.lower() == "closed"])
        st.metric("Cerrados", cerrados)
    with col5:
        alta_prioridad = len(df_filtered[df_filtered['priority'].str.lower() == "high"])
        st.metric("Prioridad Alta", alta_prioridad, delta_color="inverse")
    
    st.markdown("---")
    
    # --- LISTADO DE TICKETS ---
    st.header(f"🎫 Tickets encontrados: {len(df_filtered)}")
    
    if df_filtered.empty:
        st.info("📭 No hay tickets que coincidan con los filtros seleccionados")
    else:
        for idx, row in df_filtered.iterrows():
            
            # Usar columnas para mejor organización
            col_ticket, col_estado, col_prioridad = st.columns([3, 1, 1])
            
            with col_ticket:
                st.subheader(f"🎫 Ticket #{row['ticket_number']}")
                st.write(f"### {row['title']}")
            
            with col_estado:
                estado_color = {
                    "Open": "🔴",
                    "In Progress": "🟡",
                    "Closed": "🟢"
                }
                st.markdown(f"**Estado:** {estado_color.get(row['status'], '⚪')} {traducir_estado(row['status'])}")
            
            with col_prioridad:
                prioridad_color = {
                    "High": "🔴",
                    "Medium": "🟡",
                    "Low": "🟢"
                }
                st.markdown(f"**Prioridad:** {prioridad_color.get(row['priority'], '⚪')} {traducir_prioridad(row['priority'])}")
            
            # Fecha de creación
            if row['created_at']:
                fecha = pd.to_datetime(row['created_at']).strftime("%d/%m/%Y %H:%M")
                st.write(f"📅 **Creado:** {fecha}")
            
            # Descripción
            if row['description']:
                with st.expander("📝 Ver descripción"):
                    st.write(row['description'])
            
            # Grabación y transcripción
            if row['recordings']:
                st.write(f"🎤 **Grabación:** {row['recordings'].get('filename', 'Sin nombre')}")
                
                transcription = row['recordings'].get('transcription', '')
                if transcription:
                    with st.expander("📜 Ver transcripción"):
                        st.text(transcription[:500] + "..." if len(transcription) > 500 else transcription)
                else:
                    st.caption("*Sin transcripción disponible*")
            
            # Notas
            if row['notes']:
                with st.expander("📌 Ver notas"):
                    st.write(row['notes'])
            
            # --- BOTONES DE ACCIÓN ---
            col_edit, col_gemini = st.columns(2)
            
            with col_edit:
                with st.expander("✏️ Editar ticket"):
                    new_title = st.text_input("Título", value=row['title'] or "", key=f"title_{row['id']}")
                    new_desc = st.text_area("Descripción", value=row['description'] or "", key=f"desc_{row['id']}")
                    
                    estados_list = ["Abierto", "En progreso", "Cerrado"]
                    prioridades_list = ["Alta", "Media", "Baja"]
                    
                    new_status = st.selectbox(
                        "Estado", 
                        estados_list, 
                        index=estados_list.index(traducir_estado(row['status'])), 
                        key=f"status_{row['id']}"
                    )
                    
                    new_priority = st.selectbox(
                        "Prioridad", 
                        prioridades_list, 
                        index=prioridades_list.index(traducir_prioridad(row['priority'])), 
                        key=f"priority_{row['id']}"
                    )
                    
                    new_notes = st.text_area("Notas", value=row['notes'] or "", key=f"notes_{row['id']}")
                    
                    if st.button("💾 Guardar cambios", key=f"save_{row['id']}", use_container_width=True):
                        try:
                            client.table("opportunities").update({
                                "title": new_title,
                                "description": new_desc,
                                "status": estado_a_ingles(new_status),
                                "priority": prioridad_a_ingles(new_priority),
                                "notes": new_notes,
                                "updated_at": datetime.datetime.now().isoformat()
                            }).eq("id", row['id']).execute()
                            
                            st.success("✅ Ticket actualizado correctamente")
                            st.cache_data.clear()
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error al actualizar: {str(e)}")
            
            with col_gemini:
                if GEMINI_API_KEY:
                    if st.button("🤖 Analizar con IA", key=f"gemini_{row['id']}", use_container_width=True):
                        transcription = row['recordings'].get('transcription', '') if row['recordings'] else ''
                        
                        if transcription:
                            with st.spinner("Analizando con Gemini..."):
                                try:
                                    prompt = f"""
                                    Analiza este ticket de soporte:
                                    
                                    Número: {row['ticket_number']}
                                    Título: {row['title']}
                                    Descripción: {row['description']}
                                    Transcripción: {transcription[:1500]}
                                    
                                    Por favor, proporciona:
                                    1. Resumen del problema
                                    2. Posible causa raíz
                                    3. Solución recomendada
                                    4. Prioridad sugerida
                                    """
                                    
                                    response = requests.post(
                                        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
                                        json={
                                            "contents": [{
                                                "parts": [{"text": prompt}]
                                            }]
                                        },
                                        timeout=30
                                    )
                                    
                                    if response.status_code == 200:
                                        result = response.json()
                                        analysis = result['candidates'][0]['content']['parts'][0]['text']
                                        st.info(analysis)
                                    else:
                                        st.error(f"Error Gemini: {response.status_code}")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        else:
                            st.warning("⚠️ No hay transcripción")
                else:
                    st.caption("🤖 IA no configurada")
            
            st.markdown("---")
            
else:
    # Mensaje cuando no hay datos o hay error
    st.header("🎫 Tickets de Oportunidad")
    
    if SUPABASE_URL and SUPABASE_KEY:
        st.warning("""
        📭 **No se encontraron tickets en la base de datos**
        
        La conexión a Supabase fue exitosa pero no hay datos en la tabla 'opportunities'.
        
        **Posibles soluciones:**
        1. Verifica que la tabla 'opportunities' tenga datos en Supabase
        2. Revisa que el nombre de la tabla sea exactamente 'opportunities' (case-sensitive)
        3. Inserta algunos tickets de prueba en Supabase
        """)
    else:
        st.error("""
        ❌ **Error de configuración**
        
        No se pueden cargar los tickets porque faltan las credenciales de Supabase.
        
        **Configuración necesaria:**
        
        Crea un archivo `.streamlit/secrets.toml` con:
        ```toml
        SUPABASE_URL = "https://tu-proyecto.supabase.co"
        SUPABASE_KEY = "tu-anon-key"
        GEMINI_API_KEY = "tu-gemini-key"  # opcional
        ```
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 10px;'>
        AppGestionTickets v2.0 - Conexión a Supabase en tiempo real<br>
        Desarrollado con Streamlit y ❤️
    </div>
    """,
    unsafe_allow_html=True
)