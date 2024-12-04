import streamlit as st
import sqlite3
import pandas as pd



# Configuración de la página para modo ancho
st.set_page_config(layout="wide")

st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
  <img src="https://cdn-icons-png.flaticon.com/128/5110/5110088.png" alt="New Left Logo" width="100" height="100">
  <h1 style='color: #0f0a68; font-size: 30px;'> ProductivApp ()</h1>
  <img src="https://cdn-icons-png.flaticon.com/128/8637/8637660.png" alt="New Right Logo" width="100" height="100">
</div>
""", unsafe_allow_html=True)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('tareas.db')
    return conn

# Crear la tabla de tareas si no existe
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario TEXT,
            tarea TEXT,
            prioridad TEXT,
            fecha_entrega TEXT,
            estado TEXT
        )
    ''')
    conn.commit()
    conn.close()



# Opciones para el estado de la tarea
estados = ['Activa', 'Terminada', 'Vencida']

# Crear la tabla si no existe
create_table()

with st.expander("Asignacion de tareas"):
  with st.form("my_form"):
    funcionario = st.text_input("Funcionario")
    tarea = st.text_area("Tarea")
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])
    fecha_entrega = st.date_input("Fecha de entrega")
    estado = st.selectbox("Estado", estados)
    submitted = st.form_submit_button("Agregar Tarea")
    if submitted:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO tareas (funcionario, tarea, prioridad, fecha_entrega, estado) VALUES (?, ?, ?, ?, ?)",
                           (funcionario, tarea, prioridad, fecha_entrega, estado))
            conn.commit()
            st.success("Tarea agregada correctamente")
        except sqlite3.Error as e:
            st.error(f"Error al agregar la tarea: {e}")
        finally:
            conn.close()

# Mostrar todas las tareas
conn = get_db_connection()
cursor = conn.execute("SELECT * FROM tareas")
tareas = cursor.fetchall()
conn.close()

# Convertir los resultados a un DataFrame de pandas para mejor visualización
df = pd.DataFrame(tareas, columns=['ID', 'Funcionario', 'Tarea', 'Prioridad', 'Fecha de Entrega', 'Estado'])

st.subheader("Todas las tareas")
st.table(df)

estado_filtro = st.selectbox('Selecciona un estado', df['Estado'].unique())

# Filtrar el DataFrame basado en el estado seleccionado
df_filtrado = df[df['Estado'] == estado_filtro]

# Mostrar la tabla filtrada
st.subheader("Tareas filtradas por estado")
st.table(df_filtrado)

# Buscar tareas
with st.expander("Buscar tareas"):
    buscar_por = st.selectbox("Buscar por", ["Funcionario", "Tarea"])
    busqueda = st.text_input("Ingrese el término de búsqueda")
    if busqueda:
        conn = get_db_connection()
        cursor = conn.execute(f"SELECT * FROM tareas WHERE {buscar_por} LIKE '%{busqueda}%'")
        resultados = cursor.fetchall()
        conn.close()
        df_resultados = pd.DataFrame(resultados, columns=['ID', 'Funcionario', 'Tarea', 'Prioridad', 'Fecha de Entrega', 'Estado'])
        st.table(df_resultados)

# Eliminar tareas
with st.expander("Eliminar tareas"):
    id_tarea = st.number_input("Ingrese el ID de la tarea a eliminar", min_value=1)
    if st.button("Eliminar"):
        conn = get_db_connection()
        cursor = conn.execute("DELETE FROM tareas WHERE id=?", (id_tarea,))
        conn.commit()
        conn.close()
        st.success("Tarea eliminada correctamente")
