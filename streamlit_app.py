import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="MetaData",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
  <div style="display: flex; justify-content: Center; align-items: Center;">
    <h1 style='color: #0f0a68; font-size: 29px; flex-grow: 1; text-align: center;'> ProductiApp</h1>
    <img src="https://cdn-icons-png.flaticon.com/128/2118/2118460.png" alt="RRHH YesBpo Logo" width="100" height="100" style="order: 2;">
  </div>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: left; color: #0f0a68; font-size: 15px;'> Bienvenido a ProductiApp, la herramienta definitiva para la supervisión y gestión de tareas. Simplifica tu día a día, mantén el control sobre tus proyectos y colabora eficientemente con tu equipo. Con ProductiApp, monitorear el progreso nunca fue tan fácil. ¡Empieza a transformar tu productividad hoy!</h1>
""", unsafe_allow_html=True)

#https://docs.google.com/spreadsheets/d/1RbnK8K17h7ttYIDlg9FHtIhkyK8RvrSBqWEeeoMXt68/edit?gid=0#gid=0
gsheetid = '1RbnK8K17h7ttYIDlg9FHtIhkyK8RvrSBqWEeeoMXt68'
sheetod = '0'
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

# Primera gráfica ajustada: Tareas activas e inactivas por funcionario
df_agrupado_estado = df_filtrado.groupby(['estado de la tarea', 'funcionario']).size().reset_index(name='conteo')

fig_estado = go.Figure()

for funcionario in df_agrupado_estado['funcionario'].unique():
    df_funcionario = df_agrupado_estado[df_agrupado_estado['funcionario'] == funcionario]
    fig_estado.add_trace(go.Bar(
        x=df_funcionario['estado de la tarea'],
        y=df_funcionario['conteo'],
        name=funcionario,
        text=df_funcionario['conteo'],
        textposition='auto'
    ))

fig_estado.update_layout(
    title='Cantidad de Tareas Activas e Inactivas por Funcionario',
    xaxis_title='Estado de la Tarea',
    yaxis_title='Cantidad de Tareas',
    barmode='stack',
    height=400
)

st.plotly_chart(fig_estado, use_container_width=True)

# Segunda gráfica: Prioridad de tareas por funcionario
df_agrupado_prioridad = df_filtrado.groupby(['prioridad de la tarea', 'funcionario']).size().reset_index(name='conteo')

fig_prioridad = go.Figure()

for funcionario in df_agrupado_prioridad['funcionario'].unique():
    df_funcionario = df_agrupado_prioridad[df_agrupado_prioridad['funcionario'] == funcionario]
    fig_prioridad.add_trace(go.Bar(
        x=df_funcionario['prioridad de la tarea'],
        y=df_funcionario['conteo'],
        name=funcionario,
        text=df_funcionario['conteo'],
        textposition='auto'
    ))

fig_prioridad.update_layout(
    title='Prioridad de Tareas por Funcionario',
    xaxis_title='Prioridad de la Tarea',
    yaxis_title='Cantidad de Tareas',
    barmode='stack',
    height=400
)

st.plotly_chart(fig_prioridad, use_container_width=True)
