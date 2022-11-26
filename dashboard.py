import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import urllib.request
import xlsxwriter
import requests
import io
from io import BytesIO
from google.oauth2.service_account import Credentials
from gspread_pandas import Spread, Client
from pyxlsb import open_workbook as open_xlsb
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
    st.session_state.gastos_es = Spread("Gastos ES", client=client).sheet_to_df().reset_index()
if 'gastos_sl' not in st.session_state:
    st.session_state.gastos_sl = Spread("Gastos SL", client=client).sheet_to_df().reset_index()
if 'gastos_x' not in st.session_state:
    st.session_state.gastos_x = Spread("Gastos X", client=client).sheet_to_df().reset_index()
#======================================================================================
#======================================================================================
def to_excel(df, sheet_name):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine = "xlsxwriter")
    df.to_excel(writer, index = False, sheet_name = sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
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
            if st.checkbox("Mostrar u ocultar descripción y gastos"):
                st.markdown("#### Gastos mantenimiento de local")
                with st.form("my_form"):
                    action = st.radio("Acción", ["Nuevo gasto", "Modificar gasto"])
                    g_1, g_2 = st.columns([1,1])
                    with g_1:
                        if action == "Nuevo gasto":
                            nombre_ng = st.text_input("Categoría")
                    with g_2:
                        if action == "Nuevo gasto":
                            monto_ng = st.number_input("Monto [Q]")
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        if action == "Nuevo gasto":
                            df_new = pd.DataFrame([[nombre_ng,"Q"+str(monto_ng)]], columns = ["Categoría", "Monto [Q]"])
                            df_guardar = pd.concat([df_new, df_gastos_cg], axis = 0)
                            st.session_state.gastos_cg.df_to_sheet(df_guardar, index = false)
                gcg_1, gcg_3, gcg_2 = st.columns([2,0.3,1])
                df_xlsx = to_excel(st.session_state.gastos_cg, "Gastos ubicación - CG")
                with gcg_1:
                    st.dataframe(st.session_state.gastos_cg.style.hide_index().set_precision(2).background_gradient(), use_container_width = True)
                with gcg_2:
                    st.markdown("###### Estrategía ubicación: El local se encuentra ubicado en una zona bastante céntrica y el centro comercial es concurrido, alrededor de la zona hay varias bodegas y zonas residenciales.")
                    st.markdown("#### Total gastos:")
                    #df['Sales'] = df['Sales'].replace({'\$': '', ',': ''}, regex=True).astype(float)
                    st.markdown("##### Q"+str(sum(st.session_state.gastos_cg["Monto [Q]"].str.replace(',','').str.replace('Q','').astype('float'))))
                    st.download_button(label='📥 Descargar tabla', data=df_xlsx,file_name= 'gastos_cg.xlsx')
        elif location == "Xela":
            u_1 = pd.DataFrame([[14.83472, -91.51806]], columns = ["lat","lon"])
            co_2.map(u_1, zoom = 5, use_container_width=True)
            co_1.markdown(":office: C.C. Interplaza Xela Local Free Stand #14")
            co_1.markdown(":iphone: (502) 2328-0093")
            co_1.markdown(":email: xela@kikimarket.com")
            co_1.markdown(":watch: Lunes a sábado 09:00 a 20:00 Hrs. Domingo 10:00 a 19:00 Hrs.")
            co_1.markdown(":car: Cuota parqueo: Q5.00 por 4 horas")
            co_1.markdown(":triangular_ruler: Dimensiones local: 10x10 m")
            st.markdown("***")
            if st.checkbox("Mostrar u ocultar descripción y gastos"):
                st.markdown("#### Gastos mantenimiento de local")
                gcg_1, gcg_3, gcg_2 = st.columns([2,0.3,1])
                df_xlsx = to_excel(gastos_x, "Gastos ubicación - X")
                with gcg_1:
                    st.dataframe(gastos_x.style.hide_index().set_precision(2).background_gradient(), use_container_width = True)
                with gcg_2:
                    st.markdown("###### Estrategía ubicación: El local se encuentra ubicado en una zona bastante céntrica y el centro comercial es concurrido, alrededor de la zona hay varias bodegas y zonas residenciales.")
                    st.markdown("#### Total gastos:")
                    st.markdown("##### Q"+str(sum(gastos_x["Monto [Q]"])))
                    st.download_button(label='📥 Descargar tabla', data=df_xlsx,file_name= 'gastos_x.xlsx')
        elif location == "San Lucas":
            u_1 = pd.DataFrame([[14.61075, -90.65681]], columns = ["lat","lon"])
            co_2.map(u_1, zoom = 5, use_container_width=True)
            co_1.markdown(":office: Km. 29.5 Carretera Interamericana C.C. San Lucas locales 17 y 18, San Lucas Sacatepéquez, Sacatepéquez")
            co_1.markdown(":iphone: (502) 2328-0091")
            co_1.markdown(":email: sanlucas@kikimarket.com")
            co_1.markdown(":watch: Lunes a sábado 09:00 a 20:00 Hrs. Domingo 10:00 a 19:00 Hrs.")
            co_1.markdown(":car: Cuota parqueo: Primeras 2 horas gratis, Q10.00 cada hora adicional")
            co_1.markdown(":triangular_ruler: Dimensiones local: 10x15 m")
            st.markdown("***")
            if st.checkbox("Mostrar u ocultar descripción y gastos"):
                st.markdown("#### Gastos mantenimiento de local")
                gcg_1, gcg_3, gcg_2 = st.columns([2,0.3,1])
                df_xlsx = to_excel(gastos_sl, "Gastos ubicación - SL")
                with gcg_1:
                    st.dataframe(gastos_sl.style.hide_index().set_precision(2).background_gradient(), use_container_width = True)
                with gcg_2:
                    st.markdown("###### Estrategía ubicación: El local se encuentra ubicado en una zona bastante céntrica y el centro comercial es concurrido, alrededor de la zona hay varias bodegas y zonas residenciales.")
                    st.markdown("#### Total gastos:")
                    st.markdown("##### Q"+str(sum(gastos_sl["Monto [Q]"])))
                    st.download_button(label='📥 Descargar tabla', data=df_xlsx,file_name= 'gastos_sl.xlsx')
        elif location == "Escuintla":
            u_1 = pd.DataFrame([[14.3009, -90.78581]], columns = ["lat","lon"])
            co_2.map(u_1, zoom = 5, use_container_width=True)
            co_1.markdown(":office: km 60 autopista de Escuintla a Palin, Local 216, 2do Nivel, Centro Comercial Inter Plaza Escuintla , Escuintla")
            co_1.markdown(":iphone: (502) 2328-0074")
            co_1.markdown(":email: escuintla@kikimarket.com")
            co_1.markdown(":watch: Lunes a sábado 09:00 a 20:00 Hrs. Domingo 10:00 a 19:00 Hrs.")
            co_1.markdown(":car: Cuota parqueo: Gratis con sello de consumo en nuestro establecimiento")
            co_1.markdown(":triangular_ruler: Dimensiones local: 10x10 m")
            st.markdown("***")
            if st.checkbox("Mostrar u ocultar descripción y gastos"):
                st.markdown("#### Gastos mantenimiento de local")
                gcg_1, gcg_3, gcg_2 = st.columns([2,0.3,1])
                #df_xlsx = to_excel(gastos_es, "Gastos ubicación - ES")
                with gcg_1:
                    st.dataframe(gastos_es.style.hide_index().set_precision(2).background_gradient(), use_container_width = True)
                with gcg_2:
                    st.markdown("###### Estrategía ubicación: El local se encuentra ubicado en una zona bastante céntrica y el centro comercial es concurrido, alrededor de la zona hay varias bodegas y zonas residenciales.")
                    st.markdown("#### Total gastos:")
                    
                    st.markdown("##### Q"+str(sum(gastos_es["Monto [Q]"])))
                    st.download_button(label='📥 Descargar tabla', data=df_xlsx,file_name= 'gastos_es.xlsx')
elif control_conoce == "Empleados":
    with mi_vi:
        st.markdown("# :bust_in_silhouette: Nuestros empleados")
        
        
st.sidebar.header("Panel de control")
control = st.sidebar.radio("Acciones", ["Ingreso nuevo cliente",
                                        "Verificación de datos cliente",
                                        ""])
if control == "Ingreso nuevo cliente":
    st.markdown("###### Ingresar información del cliente")
    add_user = st.expander("Formulario", expanded = True)
    with add_user:
        c_1, c_2, c_3 = st.columns(3)
        nombres = c_1.text_input("Nombres")
        apellidos = c_1.text_input("Apellidos")
        genero = c_1.selectbox("Género", ["F", "M"])
        nit = c_2.text_input("NIT (no guiones ni espacios)")
        telefono = c_2.text_input("Número de teléfono")
        direccion = c_2.text_input("Dirección")
        email = c_3.text_input("Correo electrónico")
        if st.button("Guardar Información", key = 1):
            df = st.session_state.spread.sheet_to_df().reset_index()
elif control == "Verificación de datos cliente":
    st.markdown("###### Verificación información del cliente")
    search_user = st.expander("Formulario", expanded = True)
    with search_user:
        c_1, c_2, c_3 = st.columns(3)
        busqueda = st.selectbox("Método de búsqueda", ["Correo electrónico","ID cliente",""])
#        id_cliente st.selectbox()
