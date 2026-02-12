import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Mostrar título y descripción de la aplicación.
st.set_page_config(page_title="Tickets de soporte", page_icon="🎫")
st.title("🎫 Tickets de soporte")
st.write(
    """
    Esta aplicación muestra cómo puedes construir una herramienta interna en Streamlit. 
    Aquí, implementamos un flujo de trabajo para tickets de soporte. El usuario puede 
    crear un ticket, editar tickets existentes y ver algunas estadísticas.
    """
)

# Crear un DataFrame aleatorio de Pandas con tickets existentes.
if "df" not in st.session_state:

    # Establecer semilla para reproducibilidad.
    np.random.seed(42)

    # Crear algunas descripciones de problemas ficticias.
    descripciones_problemas = [
        "Problemas de conectividad de red en la oficina",
        "La aplicación de software falla al iniciar",
        "La impresora no responde a los comandos de impresión",
        "Servidor de correo electrónico fuera de servicio",
        "Fallo en la copia de seguridad de datos",
        "Problemas de autenticación al iniciar sesión",
        "Degradación del rendimiento del sitio web",
        "Vulnerabilidad de seguridad identificada",
        "Fallo de hardware en la sala de servidores",
        "Empleado no puede acceder a archivos compartidos",
        "Fallo en la conexión a la base de datos",
        "La aplicación móvil no sincroniza datos",
        "Problemas con el sistema de telefonía VoIP",
        "Problemas de conexión VPN para empleados remotos",
        "Actualizaciones del sistema causan problemas de compatibilidad",
        "Servidor de archivos sin espacio de almacenamiento",
        "Alertas del sistema de detección de intrusiones",
        "Errores en el sistema de gestión de inventario",
        "Los datos de clientes no cargan en el CRM",
        "La herramienta de colaboración no envía notificaciones",
    ]

    # Generar el dataframe con 100 filas/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Problema": np.random.choice(descripciones_problemas, size=100),
        "Estado": np.random.choice(["Abierto", "En progreso", "Cerrado"], size=100),
        "Prioridad": np.random.choice(["Alta", "Media", "Baja"], size=100),
        "Fecha de envío": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Guardar el dataframe en el estado de sesión
    st.session_state.df = df

# Mostrar una sección para añadir un nuevo ticket.
st.header("Añadir un ticket")

with st.form("add_ticket_form"):
    problema = st.text_area("Describe el problema")
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])
    enviado = st.form_submit_button("Enviar")

if enviado:
    numero_ticket_reciente = int(max(st.session_state.df.ID).split("-")[1])
    hoy = datetime.datetime.now().strftime("%d-%m-%Y")
    df_nuevo = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{numero_ticket_reciente+1}",
                "Problema": problema,
                "Estado": "Abierto",
                "Prioridad": prioridad,
                "Fecha de envío": hoy,
            }
        ]
    )

    st.write("¡Ticket enviado! Aquí están los detalles del ticket:")
    st.dataframe(df_nuevo, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_nuevo, st.session_state.df], axis=0)

# Mostrar sección para ver y editar tickets existentes en una tabla.
st.header("Tickets existentes")
st.write(f"Número de tickets: `{len(st.session_state.df)}`")

st.info(
    "Puedes editar los tickets haciendo doble clic en una celda. ¡Observa cómo los gráficos "
    "se actualizan automáticamente! También puedes ordenar la tabla haciendo clic en los encabezados de las columnas.",
    icon="✍️",
)

# Mostrar el dataframe de tickets con `st.data_editor`
df_editado = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Estado": st.column_config.SelectboxColumn(
            "Estado",
            help="Estado del ticket",
            options=["Abierto", "En progreso", "Cerrado"],
            required=True,
        ),
        "Prioridad": st.column_config.SelectboxColumn(
            "Prioridad",
            help="Prioridad",
            options=["Alta", "Media", "Baja"],
            required=True,
        ),
    },
    # Deshabilitar la edición de las columnas ID y Fecha de envío.
    disabled=["ID", "Fecha de envío"],
)

# Mostrar algunas métricas y gráficos sobre los tickets.
st.header("Estadísticas")

# Mostrar métricas lado a lado usando `st.columns` y `st.metric`
col1, col2, col3 = st.columns(3)
# CORREGIDO: Usar "Estado" en lugar de "status"
num_tickets_abiertos = len(st.session_state.df[st.session_state.df["Estado"] == "Abierto"])
col1.metric(label="Número de tickets abiertos", value=num_tickets_abiertos, delta=10)
col2.metric(label="Tiempo de primera respuesta (horas)", value=5.2, delta=-1.5)
col3.metric(label="Tiempo promedio de resolución (horas)", value=16, delta=2)

# Mostrar dos gráficos de Altair
st.write("")
st.write("##### Estado de tickets por mes")
grafico_estado = (
    alt.Chart(df_editado)
    .mark_bar()
    .encode(
        x="month(Fecha de envío):O",
        y="count():Q",
        xOffset="Estado:N",
        color="Estado:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(grafico_estado, use_container_width=True, theme="streamlit")

st.write("##### Prioridades actuales de tickets")
grafico_prioridad = (
    alt.Chart(df_editado)
    .mark_arc()
    .encode(theta="count():Q", color="Prioridad:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(grafico_prioridad, use_container_width=True, theme="streamlit")