import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time

# Configurar la aplicación.
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Soporte de tickets")
st.write(
    """
    Esta aplicación muestra cómo puedes crear una herramienta interna en Streamlit.
    Aquí estamos implementando un flujo de trabajo de tickets de soporte. 
    El usuario puede crear un ticket, editar tickets existentes y ver algunas estadísticas.
    """
)

# Crear un DataFrame de Pandas con tickets existentes.
if "df" not in st.session_state:

    # Establecer la semilla para reproducibilidad.
    np.random.seed(42)

    # Descripciones de problemas ficticias.
    issue_descriptions = [
        "Problemas de conectividad de red en la oficina",
        "Aplicación de software se bloquea al iniciar",
        "La impresora no responde a los comandos de impresión",
        "Tiempo de inactividad del servidor de correo electrónico",
        "Fallo en la copia de seguridad de datos",
        "Problemas de autenticación de inicio de sesión",
        "Degradación del rendimiento del sitio web",
        "Vulnerabilidad de seguridad identificada",
        "Fallo de hardware en la sala de servidores",
        "Empleado no puede acceder a los archivos compartidos",
        "Fallo de conexión a la base de datos",
        "La aplicación móvil no sincroniza datos",
        "Problemas con el sistema de teléfonos VoIP",
        "Problemas de conexión VPN para empleados remotos",
        "Actualizaciones del sistema causan problemas de compatibilidad",
        "El servidor de archivos se está quedando sin espacio de almacenamiento",
        "Alertas del sistema de detección de intrusos",
        "Errores en el sistema de gestión de inventarios",
        "Los datos de clientes no se cargan en el CRM",
        "La herramienta de colaboración no envía notificaciones",
    ]

    # Generar el DataFrame con 100 filas/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Asunto": np.random.choice(issue_descriptions, size=100),
        "Estado": np.random.choice(["Abierto", "En Progreso", "Cerrado"], size=100),
        "Prioridad": np.random.choice(["Alto", "Medio", "Bajo"], size=100),
        "Fecha Enviado": [
            datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Guardar el DataFrame en el estado de sesión.
    st.session_state.df = df


# Mostrar una sección para agregar un nuevo ticket.
st.header("Agregar un ticket")

# Declarar el componente personalizado
custom_component = components.declare_component("custom_text_area", path="public")

# Mostrar el componente en Streamlit
issue = custom_component()

priority = st.selectbox("Prioridad", ["Alto", "Medio", "Bajo"])
submitted = st.button("Enviar")

if submitted:
    # Crear un DataFrame para el nuevo ticket y añadirlo al DataFrame en el estado de sesión.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Asunto": issue,
                "Estado": "Abierto",
                "Prioridad": priority,
                "Fecha Enviado": today,
            }
        ]
    )

    # Mostrar un mensaje de éxito.
    st.write("¡Ticket enviado! Aquí están los detalles del ticket:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Mostrar sección para ver y editar tickets existentes en una tabla.
st.header("Tickets existentes")
st.write(f"Número de tickets: `{len(st.session_state.df)}`")

st.info(
    "Puedes editar los tickets haciendo doble clic en una celda. ¡Observe cómo los gráficos a continuación se actualizan automáticamente! También puede ordenar la tabla haciendo clic en los encabezados de las columnas.",
    icon="✍️",
)

# Mostrar el DataFrame de tickets con `st.data_editor`.
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Estado": st.column_config.SelectboxColumn(
            "Estado",
            help="Estado del Ticket",
            options=["Abierto", "En Progreso", "Cerrado"],
            required=True,
        ),
        "Prioridad": st.column_config.SelectboxColumn(
            "Prioridad",
            help="Prioridad",
            options=["Alto", "Medio", "Bajo"],
            required=True,
        ),
    },
    # Deshabilitar la edición de las columnas ID y Fecha Enviado.
    disabled=["ID", "Fecha Enviado"],
)

# Mostrar algunas métricas y gráficos sobre los tickets.
st.header("Estadísticas")

# Mostrar métricas una al lado de la otra usando `st.columns` y `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Estado == "Abierto"])
col1.metric(label="Número de tickets abiertos", value=num_open_tickets, delta=10)
col2.metric(label="Tiempo de primera respuesta (horas)", value=5.2, delta=-1.5)
col3.metric(label="Tiempo medio de resolución (horas)", value=16, delta=2)

# Mostrar dos gráficos de Altair usando `st.altair_chart`.
st.write("")
st.write("##### Estado del ticket por mes")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Fecha Enviado):O",
        y="count():Q",
        xOffset="Estado:N",
        color="Estado:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Prioridades actuales de tickets")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Prioridad:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
