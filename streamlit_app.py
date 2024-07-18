import datetime
import random
import unicodedata

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Parametros de tÃ­tulo y descripciÃ³n de la aplicaciÃ³n.
st.set_page_config(page_title="TicketEase - TFG Maestria en Ciencia de Datos UAGRM)", page_icon="ð«")

# Renderizar el menÃº en la barra lateral izquierda
st.sidebar.subheader("ð« Contenido", divider='blue')

# Generar enlaces en la barra lateral para navegar a cada secciÃ³n
st.sidebar.markdown("""
<style>
.sidebar-menu, .sidebar-menu li {
    list-style-type: none;
    margin: 0;
    padding: 0;
    font-size: 15px;
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
        <li><a href='#home'><span>ð  Inicio</span></a></li>
        <li><a href='#create'><span>ð Crear un Ticket</span></a></li>
        <li><a href='#view'><span>ð Ver Tickets</span></a></li>
        <li><a href='#stats'><span>ð EstadÃ­sticas</span></a></li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.markdown(
"""<br id="home"/><hr style="margin:0;"/>
<h1 style="padding-top: 0;">ð« <em>TicketEase</em></h1>
<h4>DescripciÃ³n de la AplicaciÃ³n de <strong>TicketEase</strong> <em>(GestiÃ³n de Tickets)</em></h4>
<p>En esta aplicaciÃ³n estamos implementando un flujo de trabajo de tickets de soporte. El usuario puede crear un ticket, editar tickets existentes y ver algunas estadÃ­sticas.</p>

<h5>CaracterÃ­sticas principales</h5>
<ol>
    <li><strong>Crear Tickets:</strong> Los usuarios pueden describir el problema y asignar una prioridad al ticket antes de enviarlo.</li>
    <li><strong>Editar Tickets:</strong> Los tickets existentes pueden ser modificados para actualizar la informaciÃ³n relevante o cambiar el estado.</li>
    <li><strong>Ver EstadÃ­sticas:</strong> La aplicaciÃ³n proporciona grÃ¡ficos que muestran estadÃ­sticas sobre el estado y la prioridad de los tickets, permitiendo una visiÃ³n rÃ¡pida y eficiente del flujo de trabajo de soporte.</li>
</ol>
""", unsafe_allow_html=True
)

# Creando con pandas un Dataframe con datos aleatorio con tickets existentes 
if "df" not in st.session_state:

    # Estableciendo semillas reproducible para los datos aleatorios.
    np.random.seed(42)

    # Realizando algunas descripciones de problemas ficticios.
    issue_descriptions = [
        "Problemas de conectividad de red en la oficina",
        "AplicaciÃ³n de software se bloquea al iniciar",
        "La impresora no responde a los comandos de impresiÃ³n",
        "Tiempo de inactividad del servidor de correo electrÃ³nico",
        "Fallo en la copia de seguridad de datos",
        "Problemas de autenticaciÃ³n de inicio de sesiÃ³n",
        "DegradaciÃ³n del rendimiento del sitio web",
        "Vulnerabilidad de seguridad identificada",
        "Fallo de hardware en la sala de servidores",
        "Empleado no puede acceder a los archivos compartidos",
        "Fallo de conexiÃ³n a la base de datos",
        "La aplicaciÃ³n mÃ³vil no sincroniza datos",
        "Problemas con el sistema de telÃ©fonos VoIP",
        "Problemas de conexiÃ³n VPN para empleados remotos",
        "Actualizaciones del sistema causan problemas de compatibilidad",
        "El servidor de archivos se estÃ¡ quedando sin espacio de almacenamiento",
        "Alertas del sistema de detecciÃ³n de intrusos",
        "Errores en el sistema de gestiÃ³n de inventarios",
        "Los datos de clientes no se cargan en el CRM",
        "La herramienta de colaboraciÃ³n no envÃ­a notificaciones",
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
    # de las ejecuciones de la pÃ¡gina). Esto garantiza que nuestros datos persistan cuando se actualiza la aplicaciÃ³n.
    st.session_state.df = df

# Inicializa los valores en session_state si no existen
if 'issue' not in st.session_state:
    st.session_state.issue = ""
if 'priority' not in st.session_state:
    st.session_state.priority = "Medio"

def remove_accents(text):
    """Elimina acentos y otras marcas diacrÃ­ticas de un texto determinado."""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

# Definir la funciÃ³n de callback para actualizar la prioridad
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
        "esencial", "considerable", "atenciÃ³n media", "atencion media", "relevante"
    ]

    priority_low = [
        "bajo", "menos importante", "baja prioridad", 
        "prioridad baja", "minimo", "postergable", 
        "retrasable", "deferible", "poco urgente", "secundario"
    ]
    
    # Define una funciÃ³n auxiliar para verificar si alguna palabra clave estÃ¡ en el texto
    def contains_keyword(text, keywords):
        return any(keyword in text for keyword in keywords)
    
    # Determina la prioridad basada en las palabras clave
    if contains_keyword(issue_text, priority_high):
        st.session_state.priority = "Alto"
    elif contains_keyword(issue_text, priority_medium):
        st.session_state.priority = "Medio"
    else:
        st.session_state.priority = "Bajo"

st.markdown("""<br id="create"/><hr/>""", unsafe_allow_html=True)
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

    # Mostrando un pequeÃ±o mensaje de Ã©xito.
    st.write("Ticket guardado! AquÃ­ estÃ¡n los detalles del ticket.:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

st.markdown("""<br id="view"/><hr/>""", unsafe_allow_html=True)
# Mostrar secciÃ³n para ver y editar tickets existentes en una tabla.
st.subheader("Tickets existentes", divider='blue')
st.write(f"Numero de tickets: `{len(st.session_state.df)}`")

st.info(
    "Puedes editar los tickets haciendo doble clic en una celda. Â¡Observe cÃ³mo los grÃ¡ficos a continuaciÃ³n se actualizan"
    "automÃ¡ticamente! TambiÃ©n puede ordenar la tabla haciendo clic en los encabezados de las columnas.",
    icon="âïž",
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
    # Deshabilitando la ediciÃ³n de las columnas ID y Fecha Enviado.
    disabled=["ID", "Fecha Enviado"],
)

st.markdown("""<br id="stats"/><hr/>""", unsafe_allow_html=True)
# Muestra algunas mÃ©tricas y grÃ¡ficos de los tickets.
st.subheader("Estadisticas", divider='blue')

# Mostrando mÃ©tricas una al lado de la otra usando `st.columns` y `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Estado == "Abierto"])
col1.metric(label="NÃºmero de tickets abiertos", value=num_open_tickets, delta=10)
col2.metric(label="Tiempo de primera respuesta (horas)", value=5.2, delta=-1.5)
col3.metric(label="Tiempo medio de resoluciÃ³n (horas)", value=16, delta=2)

# Mostrar dos grÃ¡ficos usando `st.altair_chart`.
st.write("")
st.write("##### Estado del ticket por mes")
# creando un grÃ¡fico de barras apiladas, con la cantidad de tickets por estado para cada mes
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

# Creando un grÃ¡fico de pastel con las etiquetas de porcentaje de tickets por estado
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

# Cargar el cÃ³digo JavaScript para smooth scrolling
st.components.v1.html("""
 <script src="https://cdn.jsdelivr.net/npm/smoothscroll-polyfill@0.4.3/dist/smoothscroll.min.js"></script>
<script>
    document.addEventListener("DOMContentLoaded", function() {
        smoothscroll.polyfill();
    });
</script>
""", height=0)