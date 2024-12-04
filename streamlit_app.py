import streamlit as st
import sqlite3
import pandas as pd

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('tareas.db')
    return conn

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
    
# Título de la aplicación
st.title("Gestor de Tareas Personalizado")

# Opciones para el estado de la tarea
estados = ['Activa', 'Terminada', 'Vencida']

# Formulario para agregar una nueva tarea
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
        cursor.execute("INSERT INTO tareas (funcionario, tarea, prioridad, fecha_entrega, estado) VALUES (?, ?, ?, ?, ?)",
                       (funcionario, tarea, prioridad, fecha_entrega, estado))
        conn.commit()
        conn.close()
        st.success("Tarea agregada correctamente")

# Mostrar todas las tareas
conn = get_db_connection()
cursor = conn.execute("SELECT * FROM tareas")
tareas = cursor.fetchall()
conn.close()

# Convertir los resultados a un DataFrame de pandas para mejor visualización
df = pd.DataFrame(tareas, columns=['ID', 'Funcionario', 'Tarea', 'Prioridad', 'Fecha de Entrega', 'Estado'])

# Mostrar el DataFrame en Streamlit
st.subheader("Todas las tareas")
st.table(df)

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
