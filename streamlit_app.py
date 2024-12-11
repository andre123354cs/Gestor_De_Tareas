import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="MetaData",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

st.markdown("""
  <div style="display: flex; justify-content: Center; align-items: Center;">
    <img src="https://cdn-icons-png.flaticon.com/128/2118/2118460.png" alt="RRHH YesBpo Logo" width="100" height="100">
    <h1 style='color: #0f0a68; font-size: 29px;'> ProductiApp</h1>
  </div>
""", unsafe_allow_html=True)
    
st.markdown("""
    <h1 style='text-align: left; color: #0f0a68; font-size: 15px;'> Bienvenido a ProductiApp, la herramienta definitiva para la supervisión y gestión de tareas. Simplifica tu día a día, mantén el control sobre tus proyectos y colabora eficientemente con tu equipo. Con ProductiApp, monitorear el progreso nunca fue tan fácil. ¡Empieza a transformar tu productividad hoy!</h1>
    """, unsafe_allow_html=True)

#https://docs.google.com/spreadsheets/d/1RbnK8K17h7ttYIDlg9FHtIhkyK8RvrSBqWEeeoMXt68/edit?gid=0#gid=0
gsheetid='1RbnK8K17h7ttYIDlg9FHtIhkyK8RvrSBqWEeeoMXt68'
sheetod='0'
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetod}&format'

df= pd.read_csv(url)

st.dataframe(df, use_container_width=True)
    
    
    
    
# Obtener los valores únicos de la columna 'estado de la tarea'
estados_unicos = df['estado de la tarea'].unique()

# Filtrar por funcionario y obtener los valores únicos
funcionarios_unicos = df['funcionario'].unique()

estado_selector = widgets.Dropdown(
    options=estados_unicos,
    description='Estado de la Tarea:',
    disabled=False,
)

funcionario_selector = widgets.Dropdown(
    options=funcionarios_unicos,
    description='Funcionario:',
    disabled=False,
)

# Función para filtrar los datos según las selecciones
def filtrar_datos(estado, funcionario):
    filtro = df[(df['estado_tarea'] == estado) & (df['funcionario'] == funcionario)]
    return filtro

# Mostrar widgets
display(estado_selector, funcionario_selector)

# Filtrar datos cuando se cambia una selección
def actualizar_filtro(change):
    estado = estado_selector.value
    funcionario = funcionario_selector.value
    datos_filtrados = filtrar_datos(estado, funcionario)
    print(datos_filtrados)
