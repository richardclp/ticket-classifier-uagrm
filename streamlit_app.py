import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Tickets final (UAGRM)", page_icon="🎫")
st.title("🎫 Soporte de tickets")
st.write(
    """
    Esta aplicación muestra cómo puedes crear una herramienta interna en Streamlit.
    Aquí estamos implementando un flujo de trabajo de tickets de soporte. 
    El usuario puede crear un ticket, editar tickets existentes y ver algunas estadísticas.
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
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

    # Generate the dataframe with 100 rows/tickets.
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

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df

# Inicializa los valores en session_state si no existen
if 'issue' not in st.session_state:
    st.session_state.issue = ""
if 'priority' not in st.session_state:
    st.session_state.priority = "Medio"

# Definir la función de callback para actualizar la prioridad
def on_text_change():
    issue_text = st.session_state.issue
    # Aquí puedes definir la lógica para cambiar la prioridad basada en el texto
    if "urgente" in issue_text.lower():
        st.session_state.priority = "Alto"
    elif "importante" in issue_text.lower():
        st.session_state.priority = "Medio"
    else:
        st.session_state.priority = "Bajo"

with st.container(border=True): 
    # Show a section to add a new ticket.
    st.header("Agregar un ticket")
    issue = st.text_area("Describa el problema", key="issue", on_change=on_text_change)
    priority = st.selectbox("Prioridad", ["Alto", "Medio", "Bajo"], key="priority")
    with st.form("add_ticket_form", border=False):
        submitted = st.form_submit_button("Enviar")

if submitted:
    # Make a dataframe for the new ticket and append it to the dataframe in session
    # state.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Asunto": st.session_state.issue,
                "Estado": "Abierto",
                "Prioridad": st.session_state.priority,
                "Fecha Enviado": today,
            }
        ]
    )

    # Show a little success message.
    st.write("Ticket enviado! Aquí están los detalles del ticket.:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("Tickets existentes")
st.write(f"Numero de tickets: `{len(st.session_state.df)}`")

st.info(
    "Puedes editar los tickets haciendo doble clic en una celda. ¡Observe cómo los gráficos a continuación se actualizan"
    "automáticamente! También puede ordenar la tabla haciendo clic en los encabezados de las columnas.",
    icon="✍️",
)

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
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
    # Disable editing the ID and Date Submitted columns.
    disabled=["ID", "Fecha Enviado"],
)

# Show some metrics and charts about the ticket.
st.header("Estadisticas")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Estado == "Abierto"])
col1.metric(label="Número de tickets abiertos", value=num_open_tickets, delta=10)
col2.metric(label="Tiempo de primera respuesta (horas)", value=5.2, delta=-1.5)
col3.metric(label="Tiempo medio de resolución (horas)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
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

st.write("##### Prioridades actuales de los tickets")
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
