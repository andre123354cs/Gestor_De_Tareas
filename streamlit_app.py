import streamlit as st
import pandas as pd
import plotly.express as px

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

df = pd.read_csv(url)

# Obtener los valores únicos de la columna 'estado de la tarea'
estados_unicos = df['estado de la tarea'].unique()

# Filtrar por funcionario y obtener los valores únicos
funcionarios_unicos = df['funcionario'].unique()

novedad_seleccionada = st.multiselect('Selecciona Estados', estados_unicos)
funcionario_seleccionada = st.multiselect('Selecciona Funcionario', funcionarios_unicos)

# Filtrar el DataFrame según las selecciones
df_filtrado = df.copy()

if novedad_seleccionada:
    df_filtrado = df_filtrado[df_filtrado['estado de la tarea'].isin(novedad_seleccionada)]

if funcionario_seleccionada:
    df_filtrado = df_filtrado[df_filtrado['funcionario'].isin(funcionario_seleccionada)]

# Mostrar el DataFrame filtrado
st.dataframe(df_filtrado, use_container_width=True)

# Crear gráfico de barras para visualizar las tareas por funcionario
fig = px.bar(df_filtrado, x='funcionario', y='tarea', color='estado de la tarea', 
             title='Tareas por Funcionario', labels={'tarea':'Cantidad de Tareas'}, 
             barmode='group', height=400)

st.plotly_chart(fig, use_container_width=True)
