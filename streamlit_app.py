import datetime
import random
import unicodedata

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Parametros de título y descripción de la aplicación.
st.set_page_config(page_title="TicketEase - TFG Maestria en Ciencia de Datos UAGRM)", page_icon="🎫")

# Renderizar el menú en la barra lateral izquierda
st.sidebar.subheader("Menú de Navegación")

# Generar enlaces en la barra lateral para navegar a cada sección
st.sidebar.markdown("""
<style>
.sidebar-menu, .sidebar-menu li {
    list-style-type: none;
    margin: 0;
    padding: 0;
    font-size: 18px;
}

.sidebar-menu li {
    margin-bottom: 5px;
    border-radius: 10px;
    background-color: #d6d6d6;
    transition: all 0.3s ease;
}

.sidebar-menu li a {
    color: #333;
    text-decoration: none;
    display: block;
    padding: 10px;
    border-radius: 5px;
    position: relative;
    transition: all 0.3s ease;
}

.sidebar-menu li:hover {
    background-color: #d6f7fc;
    transform: scale(1.05);
}

.sidebar-menu li a::before {
    content: '';
    position: absolute;
    left: 0;
    bottom: 0;
    height: 3px;
    width: 0;
    background-color: #333;
    transition: width 0.3s ease;
}

.sidebar-menu li a:hover::before {
    width: 100%;
}
</style>
<div >
    <ul class='sidebar-menu'>
        <li><a href='#home'><span>HOME</span></a></li>
        <li><a href='#create'><span>Crear Tickets</span></a></li>
        <li><a href='#view'><span>Ver Tickets</span></a></li>
        <li><a href='#stats'><span>Estadisticas</span></a></li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.markdown(
    """
    <hr style="margin:0;" id="home"/>
    <h1 style="padding-top: 0;">🎫 <em>TicketEase</em></h1>
    <h4>Descripción de la Aplicación de <strong>TicketEase</strong> <em>(Gestión de Tickets)</em></h4>
    <p>En esta aplicación estamos implementando un flujo de trabajo de tickets de soporte. El usuario puede crear un ticket, editar tickets existentes y ver algunas estadísticas.</p>

    <h5>Características principales</h5>
    <ol>
        <li><strong>Crear Tickets:</strong> Los usuarios pueden describir el problema y asignar una prioridad al ticket antes de enviarlo.</li>
        <li><strong>Editar Tickets:</strong> Los tickets existentes pueden ser modificados para actualizar la información relevante o cambiar el estado.</li>
        <li><strong>Ver Estadísticas:</strong> La aplicación proporciona gráficos que muestran estadísticas sobre el estado y la prioridad de los tickets, permitiendo una visión rápida y eficiente del flujo de trabajo de soporte.</li>
    </ol>
    """,
    unsafe_allow_html=True
)

# Creando con pandas un Dataframe con datos aleatorio con tickets existentes 
if "df" not in st.session_state:

    # Estableciendo semillas reproducible para los datos aleatorios.
    np.random.seed(42)

    # Realizando algunas descripciones de problemas ficticios.
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

    # Genere el dataframe de datos con 100 filas o tickets.
    data = {
        "ID": [f"TKT-{i}" for i in range(1100, 1000, -1)],
        "Asunto": np.random.choice(issue_descriptions, size=100),
        "Estado": np.random.choice(["Abierto", "En Progreso", "Cerrado"], size=100),
        "Prioridad": np.random.choice(["Alto", "Medio", "Bajo"], size=100),
        "Fecha Enviado": [
            datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Guardando el dataframe de datos en la session_state (un objeto similar a un diccionario que persiste a lo largo
    # de las ejecuciones de la página). Esto garantiza que nuestros datos persistan cuando se actualiza la aplicación.
    st.session_state.df = df

# Inicializa los valores en session_state si no existen
if 'issue' not in st.session_state:
    st.session_state.issue = ""
if 'priority' not in st.session_state:
    st.session_state.priority = "Medio"

def remove_accents(text):
    """Elimina acentos y otras marcas diacríticas de un texto determinado."""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

# Definir la función de callback para actualizar la prioridad
def on_text_change():
    issue_text = remove_accents(st.session_state.issue.lower())
    
    # Define las listas de palabras clave
    priority_high = [
        "urgente", "critico", "inmediato", 
        "rapido", "alta prioridad", "prioridad alta", 
        "emergencia", "inaplazable", "vital"
    ]

    priority_medium = [
        "importante", "moderado", "media prioridad", 
        "prioridad media", "significativo", "necesario", 
        "esencial", "considerable", "atención media", "atencion media", "relevante"
    ]

    priority_low = [
        "bajo", "menos importante", "baja prioridad", 
        "prioridad baja", "minimo", "postergable", 
        "retrasable", "deferible", "poco urgente", "secundario"
    ]
    
    # Define una función auxiliar para verificar si alguna palabra clave está en el texto
    def contains_keyword(text, keywords):
        return any(keyword in text for keyword in keywords)
    
    # Determina la prioridad basada en las palabras clave
    if contains_keyword(issue_text, priority_high):
        st.session_state.priority = "Alto"
    elif contains_keyword(issue_text, priority_medium):
        st.session_state.priority = "Medio"
    else:
        st.session_state.priority = "Bajo"

st.markdown("""<br/><a name="create"></a><hr/>""", unsafe_allow_html=True)
# Mostrar un contenendor con un formulario para agregar un nuevo ticket.
with st.container(border=True): 
    st.subheader("Agregar un ticket :sunglasses:", divider='blue')
    st.text_area("Describa el problema", key="issue", on_change=on_text_change)
    st.selectbox("Prioridad", ["Alto", "Medio", "Bajo"], key="priority")
    with st.form("add_ticket_form", border=False):
        submitted = st.form_submit_button("Enviar")

if submitted:
    # Creando un dataframe de datos para el nuevo ticket para luego agregarlo 
    # al dataframe en session_state.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TKT-{recent_ticket_number+1}",
                "Asunto": st.session_state.issue,
                "Estado": "Abierto",
                "Prioridad": st.session_state.priority,
                "Fecha Enviado": today,
            }
        ]
    )

    # Mostrando un pequeño mensaje de éxito.
    st.write("Ticket guardado! Aquí están los detalles del ticket.:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

st.markdown("""<br/><a name="view"></a><hr/>""", unsafe_allow_html=True)
# Mostrar sección para ver y editar tickets existentes en una tabla.
st.subheader("Tickets existentes", divider='blue')
st.write(f"Numero de tickets: `{len(st.session_state.df)}`")

st.info(
    "Puedes editar los tickets haciendo doble clic en una celda. ¡Observe cómo los gráficos a continuación se actualizan"
    "automáticamente! También puede ordenar la tabla haciendo clic en los encabezados de las columnas.",
    icon="✍️",
)

# Mostrando el dataframe de los tickets con `st.data_editor`. Esto permite al usuario editar 
# las celdas de la tabla. Los datos editados se devuelven como un nuevo dataframe.
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
            help="Prioridad del Ticket",
            options=["Alto", "Medio", "Bajo"],
            required=True,
        ),
    },
    # Deshabilitando la edición de las columnas ID y Fecha Enviado.
    disabled=["ID", "Fecha Enviado"],
)

st.markdown("""<br/><a name="stats"></a><hr/>""", unsafe_allow_html=True)
# Muestra algunas métricas y gráficos de los tickets.
st.subheader("Estadisticas", divider='blue')

# Mostrando métricas una al lado de la otra usando `st.columns` y `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Estado == "Abierto"])
col1.metric(label="Número de tickets abiertos", value=num_open_tickets, delta=10)
col2.metric(label="Tiempo de primera respuesta (horas)", value=5.2, delta=-1.5)
col3.metric(label="Tiempo medio de resolución (horas)", value=16, delta=2)

# Mostrar dos gráficos usando `st.altair_chart`.
st.write("")
st.write("##### Estado del ticket por mes")
# creando un gráfico de barras apiladas, con la cantidad de tickets por estado para cada mes
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
# Calcular el conteo de cada prioridad y el porcentaje correspondiente
priority_counts = edited_df['Prioridad'].value_counts().reset_index()
priority_counts.columns = ['Prioridad', 'count']
priority_counts['percentage'] = (priority_counts['count'] / priority_counts['count'].sum()) * 100

# Creando un gráfico de pastel con las etiquetas de porcentaje de tickets por estado
priority_plot = (
    alt.Chart(priority_counts)
    .mark_arc()
    .encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="Prioridad", type="nominal"),
        tooltip=[alt.Tooltip(field="Prioridad", type="nominal"),
                 alt.Tooltip(field="percentage", type="quantitative", format=".2f")]
    )
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
