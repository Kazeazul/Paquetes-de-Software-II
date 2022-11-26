import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import urllib.request
import xlsxwriter
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

st.title("Bienvenido")
st.write(pd.read_csv("Gastos CG.csv", , encoding="utf8"))
