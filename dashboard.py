import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import urllib.request
import xlsxwriter
import requests
import io
from google.oauth2.service_account import Credentials
from gspread_pandas import Spread, Client
#======================================================================================
#======================================================================================
URL = 'https://scontent.fgua1-3.fna.fbcdn.net/v/t1.18169-9/1660963_606924706060130_284056617_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=wnFMucwa0_kAX-Ph1TL&_nc_ht=scontent.fgua1-3.fna&oh=00_AfA8xCmc1P5H30p1a5oBEmHua_2wlhmU_ZU70HojSbDdBg&oe=63976B39'
img = Image.open(urllib.request.urlopen(URL))
st.set_page_config(page_title='Control - Kiki Supermarket', page_icon = img, layout="wide")
#======================================================================================
#======================================================================================
#Configuración para ocultar menu de hamburguesa y pie de página
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
#======================================================================================
#======================================================================================
st.markdown(hide_st_style, unsafe_allow_html = True)
st.image("https://i.imgur.com/HZDOve8.jpg")
#======================================================================================
#======================================================================================
url = "https://raw.githubusercontent.com/Kazeazul/Paquetes-de-Software-II/main/Gastos%20CG.csv"
download = requests.get(url).content
#======================================================================================
#======================================================================================
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_info(st.secrets["s_g"], scopes=scope)
client = Client(scope=scope, creds=credentials)
#======================================================================================
#======================================================================================
#Cargando datos
if 'gastos_cg' not in st.session_state:
    st.session_state.gastos_cg = Spread("Gastos CG", client=client).sheet_to_df().reset_index()
if 'gastos_es' not in st.session_state:
    st.session_state.gastos_cg = Spread("Gastos ES", client=client).sheet_to_df().reset_index()
if 'gastos_sl' not in st.session_state:
    st.session_state.gastos_cg = Spread("Gastos SL", client=client).sheet_to_df().reset_index()
if 'gastos_x' not in st.session_state:
    st.session_state.gastos_cg = Spread("Gastos X", client=client).sheet_to_df().reset_index()
    
st.dataframe(st.session_state.gastos_cg)

#======================================================================================
#======================================================================================
st.sidebar.header("Conoce nuestra empresa")
control_conoce = st.sidebar.selectbox("¿Qué deseas conocer?", ["Misión y visión","Ubicaciones y más...", "Empleados","Proveedores"])
mi_vi = st.expander("Conocenos...", expanded = True)
if control_conoce == "Misión y visión":
    with mi_vi:
        st.markdown("# :smirk_cat: Misión")
        st.markdown("""###### 1. Crear nuevas oportunidades económicas para los agricultores y fabricantes de productos locales mediante el establecimiento de una salida sostenible durante todo el año para los alimentos y productos locales donde no existe.
###### 2. Crear un espacio virtual para generar empleos por medio de nuestra cadena de Supermercados.""")
        st.markdown("# :smile_cat: Visión")
        st.markdown("""###### Construir una cadena de supermercados en línea para proveer productos de forma local y expandirnos a nivel regional donde los productos guatemaltecos puedan prosperar y ser reconocidos por su calidad.""")
elif control_conoce == "Ubicaciones y más...":
    with mi_vi:
        st.markdown("# :earth_americas: Ubicaciones, contacto y horarios de atención")
        co_1, co_2 = st.columns([1,2])
        co_1.markdown("###### Conoce nuestras bodegas la ubicación de nuestros puntos de distribución.")
        location = co_1.selectbox("Escoge una ubicación", ["Ciudad de Guatemala","Xela","San Lucas","Escuintla"])
        if location == "Ciudad de Guatemala":
            u_1 = pd.DataFrame([[14.6349, -90.5069]], columns = ["lat","lon"])
            co_2.map(u_1, zoom = 5, use_container_width=True)
            co_1.markdown(":office: Plaza Kalú LOCAL 9, Nivel 1 Guatemala, Guatemala")
            co_1.markdown(":iphone: (502) 2328-0085")
            co_1.markdown(":email: ciudadguatemala@kikimarket.com")
            co_1.markdown(":watch: Lunes a sábado 09:00 a 20:00 Hrs. Domingo 10:00 a 19:00 Hrs.")
            co_1.markdown(":car: Cuota parqueo: Q10.00 por 4 horas")
            co_1.markdown(":triangular_ruler: Dimensiones local: 10x20 m")
            st.markdown("***")
