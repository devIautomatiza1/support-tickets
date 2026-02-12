import streamlit as st
import supabase
import requests
import pandas as pd
import datetime
import os

# --- CONFIGURACIÓN ---
# Configuración de la página PRIMERO
st.set_page_config(page_title="AppGestionTickets", page_icon="📝", layout="wide")

# Título principal
st.title("📝 AppGestionTickets - Debug Visual")
st.markdown("---")

# --- SECCIÓN DE DEBUG VISUAL ---
st.header("🔍 Panel de Diagnóstico")

# Crear columnas para el diagnóstico
col_debug1, col_debug2, col_debug3 = st.columns(3)

with col_debug1:
    st.subheader("📡 Configuración Supabase")
    # Usar secrets de Streamlit Cloud o variables de entorno
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL"))
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY"))
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    
    # Mostrar estado de las variables
    st.write("**Estado de credenciales:**")
    if SUPABASE_URL:
        st.success(f"✅ SUPABASE_URL: {SUPABASE_URL[:20]}...")
    else:
        st.error("❌ SUPABASE_URL no configurada")
    
    if SUPABASE_KEY:
        # Mostrar solo primeros y últimos caracteres por seguridad
        masked_key = f"{SUPABASE_KEY[:10]}...{SUPABASE_KEY[-5:]}"
        st.success(f"✅ SUPABASE_KEY: {masked_key}")
    else:
        st.error("❌ SUPABASE_KEY no configurada")
    
    if GEMINI_API_KEY:
        masked_gemini = f"{GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-5:]}"
        st.success(f"✅ GEMINI_API_KEY: {masked_gemini}")
    else:
        st.warning("⚠️ GEMINI_API_KEY no configurada (opcional)")

with col_debug2:
    st.subheader("🔄 Conexión Supabase")
    
    # Probar conexión a Supabase
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            st.write("**Intentando conectar a Supabase...**")
            client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
            
            # Prueba simple de conexión
            test_query = client.table("opportunities").select("count", count="exact").limit(1).execute()
            
            st.success("✅ Conexión exitosa a Supabase")
            
            # Obtener información de la tabla
            try:
                table_info = client.table("opportunities").select("*").limit(1).execute()
                if table_info.data:
                    st.info(f"📊 Tabla 'opportunities' encontrada")
                    st.write(f"Estructura de columnas: {list(table_info.data[0].keys()) if table_info.data else 'No data'}")
                else:
                    st.warning("⚠️ Tabla 'opportunities' existe pero está vacía")
            except Exception as e:
                st.error(f"❌ Error accediendo a tabla 'opportunities': {str(e)}")
                
        except Exception as e:
            st.error(f"❌ Error de conexión a Supabase: {str(e)}")
            client = None
    else:
        st.warning("⚠️ Credenciales incompletas para probar conexión")
        client = None

with col_debug3:
    st.subheader("📋 Estado de la aplicación")
    
    # Contadores y estado
    st.write("**Session State:**")
    st.write(f"Keys en session_state: {list(st.session_state.keys()) if st.session_state else 'Vacío'}")
    
    # Cache info
    st.write("**Cache:**")
    if 'df_cache' in st.session_state:
        st.write(f"DataFrame en cache: {len(st.session_state.df_cache)} registros")
        st.write(f"Timestamp: {st.session_state.get('cache_timestamp', 'N/A')}")
    else:
        st.write("No hay datos en cache")

st.markdown("---")

# --- FUNCIONES PRINCIPALES ---
@st.cache_data(ttl=60)  # Cache por 60 segundos para debugging
def get_all_opportunities():
    """Carga todos los tickets de oportunidades con debugging visual"""
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("❌ Credenciales de Supabase no configuradas")
        return pd.DataFrame()
    
    try:
        with st.spinner("🔄 Cargando tickets desde Supabase..."):
            st.write("**Ejecutando query a Supabase...**")
            
            # Log de la consulta
            st.code(f"""
            Query:
            - Tabla: opportunities
            - Select: id, recording_id, title, description, created_at, status, priority, ticket_number, notes, updated_at
            - Join: recordings(filename, transcription)
            - Order: created_at DESC
            """)
            
            # Ejecutar consulta
            query = (
                client.table("opportunities")
                .select("id, recording_id, title, description, created_at, status, priority, ticket_number, notes, updated_at, recordings(filename, transcription)")
                .order("created_at", desc=True)
            )
            
            response = query.execute()
            
            # Debug de la respuesta
            st.write(f"**Respuesta recibida:**")
            st.write(f"- Status: {response}")
            st.write(f"- Tipo de datos: {type(response.data)}")
            st.write(f"- Longitud de datos: {len(response.data) if response.data else 0}")
            
            if response.data:
                st.success(f"✅ {len(response.data)} tickets encontrados")
                
                # Mostrar primer registro como ejemplo
                st.write("**Ejemplo del primer ticket:**")
                primer_ticket = response.data[0]
                
                # Formatear para mostrar de forma legible
                ticket_info = {
                    "ID": primer_ticket.get('id'),
                    "Ticket #": primer_ticket.get('ticket_number'),
                    "Título": primer_ticket.get('title')[:50] + "..." if primer_ticket.get('title') and len(primer_ticket.get('title')) > 50 else primer_ticket.get('title'),
                    "Estado": primer_ticket.get('status'),
                    "Prioridad": primer_ticket.get('priority'),
                    "Fecha": primer_ticket.get('created_at'),
                    "Tiene grabación": "✅" if primer_ticket.get('recordings') else "❌"
                }
                st.json(ticket_info)
                
                # Convertir a DataFrame
                df = pd.DataFrame(response.data)
                
                # Debug del DataFrame
                st.write(f"**DataFrame creado:**")
                st.write(f"- Shape: {df.shape}")
                st.write(f"- Columnas: {list(df.columns)}")
                st.write(f"- Tipos de datos:\n{df.dtypes}")
                
                # Guardar en session_state para debug
                st.session_state.df_cache = df
                st.session_state.cache_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                return df
            else:
                st.warning("⚠️ No se encontraron tickets en la base de datos")
                
                # Verificar si la tabla existe y tiene datos
                try:
                    count_query = client.table("opportunities").select("*", count="exact").execute()
                    st.write(f"Total de registros en tabla: {count_query.count if hasattr(count_query, 'count') else 'desconocido'}")
                except Exception as e:
                    st.error(f"Error verificando tabla: {e}")
                
                return pd.DataFrame()
                
    except Exception as e:
        st.error(f"❌ Error cargando tickets: {str(e)}")
        st.exception(e)  # Esto muestra el traceback completo
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

# --- FILTROS EN SIDEBAR ---
st.sidebar.header("🔍 Filtros avanzados")

# Solo mostrar filtros si hay datos
df_original = None
if 'client' in locals() and client:
    df_original = get_all_opportunities()
else:
    if SUPABASE_URL and SUPABASE_KEY:
        st.sidebar.warning("⚠️ Error de conexión. Revisa el panel de diagnóstico.")
    else:
        st.sidebar.error("❌ Configura las credenciales de Supabase en secrets.toml")

# --- APLICACIÓN PRINCIPAL ---
st.header("📋 Tickets de Oportunidad - Datos en Tiempo Real")

if df_original is not None and not df_original.empty:
    
    # Filtros en sidebar
    status_filter = st.sidebar.selectbox(
        "Estado", 
        ["Todos"] + list(set(df_original["status"].apply(traducir_estado))),
        key="status_filter"
    )
    
    priority_filter = st.sidebar.selectbox(
        "Prioridad", 
        ["Todas"] + list(set(df_original["priority"].apply(traducir_prioridad))),
        key="priority_filter"
    )
    
    # Botón para recargar datos
    if st.sidebar.button("🔄 Recargar datos"):
        st.cache_data.clear()
        st.rerun()
    
    # Aplicar filtros
    df_filtered = df_original.copy()
    
    if status_filter != "Todos":
        status_en = estado_a_ingles(status_filter)
        df_filtered = df_filtered[df_filtered["status"] == status_en]
    
    if priority_filter != "Todas":
        priority_en = prioridad_a_ingles(priority_filter)
        df_filtered = df_filtered[df_filtered["priority"] == priority_en]
    
    # Métricas
    st.subheader("📊 Resumen")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tickets", len(df_filtered))
    with col2:
        abiertos = len(df_filtered[df_filtered["status"].str.lower() == "open"])
        st.metric("Abiertos", abiertos)
    with col3:
        en_progreso = len(df_filtered[df_filtered["status"].str.lower() == "in progress"])
        st.metric("En Progreso", en_progreso)
    with col4:
        cerrados = len(df_filtered[df_filtered["status"].str.lower() == "closed"])
        st.metric("Cerrados", cerrados)
    
    # Mostrar tickets
    st.subheader(f"🎫 Tickets encontrados: {len(df_filtered)}")
    
    if df_filtered.empty:
        st.info("No hay tickets que coincidan con los filtros seleccionados")
    else:
        for idx, row in df_filtered.iterrows():
            with st.container():
                st.markdown("---")
                
                # Cabecera del ticket
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"### 🎫 Ticket #{row['ticket_number']}")
                    st.write(f"**{row['title']}**")
                with col2:
                    st.write(f"**Estado:** {traducir_estado(row['status'])}")
                with col3:
                    st.write(f"**Prioridad:** {traducir_prioridad(row['priority'])}")
                
                # Fecha
                if row['created_at']:
                    fecha = pd.to_datetime(row['created_at']).strftime("%d/%m/%Y %H:%M")
                    st.write(f"📅 **Creado:** {fecha}")
                
                # Descripción
                if row['description']:
                    st.write(f"📝 **Descripción:**")
                    st.write(row['description'])
                
                # Grabación y transcripción
                if row['recordings']:
                    st.write(f"🎤 **Grabación:** {row['recordings'].get('filename', 'N/D')}")
                    
                    transcription = row['recordings'].get('transcription', '')
                    if transcription:
                        with st.expander("📜 Ver transcripción completa"):
                            st.write(transcription)
                    else:
                        st.write("*Sin transcripción disponible*")
                else:
                    st.write("*Sin grabación asociada*")
                
                # Notas
                if row['notes']:
                    with st.expander("📌 Notas"):
                        st.write(row['notes'])
                
                # Botones de acción
                col1, col2 = st.columns(2)
                with col1:
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
                        
                        if st.button("💾 Guardar cambios", key=f"save_{row['id']}"):
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
                                st.error(f"❌ Error: {str(e)}")
                
                with col2:
                    if st.button("🤖 Analizar con Gemini", key=f"gemini_{row['id']}"):
                        transcription = row['recordings'].get('transcription', '') if row['recordings'] else ''
                        if transcription and GEMINI_API_KEY:
                            with st.spinner("Analizando..."):
                                try:
                                    response = requests.post(
                                        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
                                        json={
                                            "contents": [{
                                                "parts": [{
                                                    "text": f"Analiza este ticket de soporte:\n\nTítulo: {row['title']}\nDescripción: {row['description']}\nTranscripción: {transcription[:1000]}"
                                                }]
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
                            st.warning("No hay transcripción o API key")
                
                st.markdown("---")
                
else:
    if df_original is not None and df_original.empty:
        st.warning("""
        📭 **No se encontraron tickets en la base de datos**
        
        La conexión a Supabase fue exitosa pero la tabla 'opportunities' está vacía.
        
        Posibles soluciones:
        1. Verifica que la tabla tenga datos en Supabase
        2. Revisa el nombre de la tabla (case-sensitive)
        3. Crea algunos tickets de prueba en Supabase
        """)
    else:
        st.error("""
        ❌ **No se pudieron cargar los datos**
        
        Revisa el panel de diagnóstico en la parte superior para identificar el problema.
        
        Causas comunes:
        1. Credenciales incorrectas
        2. Tabla 'opportunities' no existe
        3. Problemas de red/permissions
        """)

# --- FOOTER CON INFORMACIÓN ---
st.markdown("---")
st.markdown("**ℹ️ Información de debugging:**")
st.write(f"Última actualización: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
if 'cache_timestamp' in st.session_state:
    st.write(f"Datos en caché desde: {st.session_state.cache_timestamp}")