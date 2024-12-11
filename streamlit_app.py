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
    <h1 style='color: #0f0a68; font-size: 29px;'> Proyecto Recursos Humanos</h1>
  </div>
""", unsafe_allow_html=True)
    
st.markdown("""
    <h1 style='text-align: left; color: #0f0a68; font-size: 15px;'>Transparencia y claridad en cada paso. Conoce el estado de tus solicitudes y mantente informado sobre los procesos de RRHH. ¡Tu tranquilidad es nuestra prioridad!</h1>
    """, unsafe_allow_html=True)

#https://docs.google.com/spreadsheets/d/1RbnK8K17h7ttYIDlg9FHtIhkyK8RvrSBqWEeeoMXt68/edit?gid=0#gid=0
gsheetid='1RbnK8K17h7ttYIDlg9FHtIhkyK8RvrSBqWEeeoMXt68'
sheetod='0'
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetod}&format'

dfDatos= pd.read_csv(url)

st.dataframe(dfDatos, use_container_width=True)
    
    
    
    
