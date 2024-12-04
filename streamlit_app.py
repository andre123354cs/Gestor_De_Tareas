import streamlit as st
import sqlite3
import pandas as pd
import pyrebase
from app import interfaz
import time



firebaseConfig = {
    "apiKey": "AIzaSyBUxKlDXnPSeNLKYXzsp3pUxJ8giAwSkMQ",
    "authDomain": "metadata-c090e.firebaseapp.com",
    "databaseURL": "https://metadata-c090e-default-rtdb.firebaseio.com",
    "projectId": "metadata-c090e",
    "storageBucket": "metadata-c090e.appspot.com",
    "messagingSenderId": "954810311523",
    "appId": "1:954810311523:web:a6b0681e4f164b60cba956"
}

firebase = pyrebase.initialize_app(firebaseConfig)
pb_auth = firebase.auth()
db = firebase.database()  # Referencia a la base de datos

#st.markdown("""
 #   <h1 style='text-align: center; color: #005780; font-size: 50px;'>🌍 MetaData Yes BPO</h1>
#""", unsafe_allow_html=True)

if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def main():
    if st.session_state.user_info:
        user_info = st.session_state.user_info
        if user_info['role'] == 'admin':
            with st.sidebar:
                st.markdown(f"### 🏠 Bienvenido, {user_info['name']}!")
                st.markdown(f"Rol: **{user_info['role']}**")
                #st.button("Cerrar sesión", on_click=lambda: st.session_state.update({"user_info": None}))
                tabs = st.tabs(["Crear usuario", "Gestionar usuarios"])
                with tabs[0]:
                    create_user_form()
                with tabs[1]:
                    manage_users_module()    
        st.markdown(f"""
<h1 style='text-align: center; color: #005780; font-size: 15px;'>🌱 Bienvenido, {user_info['name']} </h1>
""", unsafe_allow_html=True)  
     

# Configuración de la página para modo ancho
st.set_page_config(layout="wide")

st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
  <img src="https://cdn-icons-png.flaticon.com/128/5110/5110088.png" alt="New Left Logo" width="100" height="100">
  <h1 style='color: #0f0a68; font-size: 30px;'> ProductivApp YesBPO</h1>
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

funcionarios_permitidos = ["Alisson Garcia", "Andres Vanegas", "Andres Diaz", "Felipe Rodriguez", "Maicol Yepes"]

# Opciones para el estado de la tarea
estados = ['Activa', 'Terminada']

# Crear la tabla si no existe
create_table()


  
with st.expander("Asignacion de tareas"):
  with st.form("my_form"):
    funcionario = st.selectbox("Funcionario", funcionarios_permitidos)
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

estados_unicos = df['Estado'].unique()
estado_filtro = st.selectbox('Selecciona un estado', estados_unicos, index=list(estados_unicos).index('Terminada'))


# Filtrar el DataFrame basado en el estado seleccionado
df_filtrado = df[df['Estado'] == estado_filtro]

# Mostrar la tabla filtrada
st.subheader("Tareas")
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

def actualizar_estado(tarea_id, nuevo_estado):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET estado = ? WHERE id = ?", (nuevo_estado, tarea_id))
    conn.commit()
    conn.close()
    st.success("Estado actualizado correctamente")

with st.expander("Finalizar Tareas"):
    tarea_id = st.number_input("Ingrese el ID de la tarea", min_value=1)
    nuevo_estado = st.selectbox("Nuevo estado", estados)
    if st.button("Actualizar Estado"):
        actualizar_estado(tarea_id, nuevo_estado)
def mostrar_detalles_tarea(tarea_id):
    # Obtener los detalles de la tarea
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM tareas WHERE id=?", (tarea_id,))
    tarea = cursor.fetchone()
    conn.close()

    # Mostrar los detalles de la tarea
    st.subheader(f"Detalles de la tarea {tarea_id}")
    # ... (mostrar los detalles de la tarea en una tabla o usando st.write)

    with st.expander("Avances de la tarea"):
        # Obtener los avances de la tarea (si existe la tabla de avances)
        try:
            cursor = conn.execute("SELECT * FROM avances WHERE tarea_id=?", (tarea_id,))
            avances = cursor.fetchall()
            df_avances = pd.DataFrame(avances, columns=['ID', 'Tarea ID', 'Fecha', 'Descripción'])
            st.table(df_avances)
        except sqlite3.OperationalError:
            st.write("Aún no hay avances para esta tarea.")

        # Formulario para agregar un nuevo avance
        nuevo_avance = st.text_area("Nuevo avance")
        if st.button("Agregar Avance"):
            # Crear la tabla de avances si no existe
            create_avances_table()
            # Insertar el nuevo avance en la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO avances (tarea_id, fecha_avance, descripcion) VALUES (?, ?, ?)",
                           (tarea_id, datetime.now().strftime("%Y-%m-%d"), nuevo_avance))
            conn.commit()
            conn.close()
            st.success("Avance registrado correctamente")
            st.experimental_rerun()

def create_avances_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarea_id INTEGER,
            fecha_avance TEXT,
            descripcion TEXT,
            FOREIGN KEY(tarea_id) REFERENCES tareas(id)
        )
    ''')
    conn.commit()
    conn.close()

    else:
        st.markdown("")
        form = st.form("login_form")
        form.markdown("<h2 style='text-align: center'>Autenticación</h2>", unsafe_allow_html=True)
        email = form.text_input("Correo")
        password = form.text_input("Contraseña", type="password")
        col1, col2 = form.columns([8, 2])
        
        if col2.form_submit_button("Iniciar Sesión"):
            with st.spinner("Procesando..."):
                try:
                    # Autenticar usuario
                    user = pb_auth.sign_in_with_email_and_password(email, password)
                    user_id = user['localId']
                    
                    # Obtener información adicional de la base de datos
                    user_info = db.child("users").child(user_id).get().val()
                    if user_info:
                        if user_info["habilitado"]:
                            st.session_state.user_info = user_info
                            st.toast(f"✅ ¡Inicio de sesión exitoso, {user_info['name']}! 🎉")
                            st.rerun()  # Recargar para mostrar la información
                        else:
                            st.error("❌ El usuario se encuentra inhabilitado.")
                    else:
                        st.error("No se encontró información del usuario.")
                except Exception as e:
                    error_message = str(e)
                    if "INVALID_PASSWORD" in error_message:
                        st.toast("❌ Contraseña incorrecta. 🔒")
                    elif "EMAIL_NOT_FOUND" in error_message:
                        st.toast("❌ Correo no registrado. 📧")
                    else:
                        st.toast("⚠️ Error inesperado. Intenta nuevamente. ❓")
                        st.write(e)


def register_user(email, password, name, role):
    try:
        user = pb_auth.create_user_with_email_and_password(email, password)
        user_id = user['localId']
        # Guardar información adicional en la base de datos
        db.child("users").child(user_id).set({"name": name, "role": role, "email": email, "habilitado": True})
        st.success(f"✅ Usuario {name} creado exitosamente con rol {role}!")
    except Exception as e:
        st.error(f"❌ Error al crear el usuario: {e}")


def create_user_form():
    """Función para mostrar el formulario de creación de usuario."""
    st.markdown("## Crear usuario")
    with st.form("create_user_form"):
        new_email = st.text_input("Correo del nuevo usuario")
        new_password = st.text_input("Contraseña", type="password")
        new_name = st.text_input("Nombre")
        new_role = st.selectbox("Rol", ["admin", "Director", "Coordinador", "Analista"])
        submitted = st.form_submit_button("Crear Usuario")

        if submitted:
            if new_email and new_password and new_name and new_role:
                register_user(new_email, new_password, new_name, new_role)
            else:
                st.error("❌ Todos los campos son obligatorios.")

def manage_users_module():
    """Módulo para gestionar usuarios (cambiar rol y contraseña)."""
    st.markdown("## Gestión de usuarios")
    users = db.child("users").get().val()

    if not users:
        st.warning("No hay usuarios registrados.")
        return

    user_list = [{"id": user_id, **info} for user_id, info in users.items()]
    selected_user = st.selectbox(
        "Selecciona un usuario",
        options=user_list,
        format_func=lambda user: f"{user['name']} ({user['email']})"
    )

    if selected_user:
        st.markdown(f"### Editar usuario: **{selected_user['name']}**")
        formulario_mod_usuario = st.form("form_editar_usuario")
        habilitado = formulario_mod_usuario.checkbox("Habilitado", value=selected_user['habilitado'])
        new_role = formulario_mod_usuario.selectbox(
            "Nuevo rol",
            options=["admin", "Director", "Coordinador", "Analista"],
            index=["admin", "Director", "Coordinador", "Analista"].index(selected_user['role'])
        )
        new_password = formulario_mod_usuario.text_input("Nueva contraseña (opcional)", type="password")

        if formulario_mod_usuario.form_submit_button("Guardar cambios"):
            try:
                # Actualizar rol en la base de datos
                db.child("users").child(selected_user["id"]).update({"role": new_role, 'habilitado': habilitado})

                # Actualizar contraseña si se proporciona una nueva
                if new_password:
                    pb_auth.update_user(selected_user["id"], password=new_password)

                st.success(f"✅ Usuario {selected_user['name']} actualizado correctamente.")
            except Exception as e:
                st.error(f"❌ Error al actualizar el usuario: {e}")


if __name__ == "__main__":
    main()
