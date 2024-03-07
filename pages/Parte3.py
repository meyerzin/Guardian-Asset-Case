import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from functions import *
import base64
st.set_page_config(
    layout = 'wide',
    page_title = 'Case GUARDIAN ASSET'
    )

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")
if not st.sidebar.checkbox('desabilitar imagens de fundo'):

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://media.licdn.com/dms/image/C4D1BAQFph9x17nqZJw/company-background_10000/0/1610146397383/guardian_capital_gestora_de_recursos_s_a_cover?e=1710435600&v=beta&t=nNnbQS1gM2cmj07OC9lOL9QOhSTvjwZCUeappY1SYpo");
    background-size: 180%;
    background-position: top left;

    background-attachment: local;
    }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 

    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """
else:
    page_bg_img = f"""
    <style>


    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

st.markdown(page_bg_img, unsafe_allow_html=True)
########################################################################################################################
try: 
    ms = st.session_state
    if "themes" not in ms: 
        ms.themes = {"current_theme": "dark",
                        "refreshed": True,
                        
                        "light": {"theme.base": "dark", 
                                "theme.primaryColor": "#FF4B4B", # c98bdb  
                                "theme.backgroundColor": "#FFFFFF", # black
                                "theme.textColor": "#31333F", # white
                                "theme.secondaryBackgroundColor": "#F0F2F6", # 5591f5
                                "button_face": "🌜"},

                        "dark":  {"theme.base": "light",
                                "theme.primaryColor": "#FF4B4B", # 5591f5 
                                "theme.backgroundColor": "#0E1117", # white
                                "theme.textColor": "#FAFAFA", # 0a1464
                                "theme.secondaryBackgroundColor": "#262730", # 82E1D7
                                "button_face": "🌞"},
                        }
    
    def ChangeTheme():
        previous_theme = ms.themes["current_theme"]
        tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
        for vkey, vval in tdict.items(): 
            if vkey.startswith("theme"): st._config.set_option(vkey, vval)

        ms.themes["refreshed"] = False
        if previous_theme == "dark": ms.themes["current_theme"] = "light"
        elif previous_theme == "light": ms.themes["current_theme"] = "dark"


    btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
    st.sidebar.button(btn_face, on_click=ChangeTheme)

    if ms.themes["refreshed"] == False:
        ms.themes["refreshed"] = True
        st.rerun()
except:
    pass

################################
col1,col2 = st.columns([0.2,0.8])
with col2:
    st.title('RESOLUÇÃO DO CASE - GUARDIAN-ASSET')
with col1:
    st.image('https://media.licdn.com/dms/image/C560BAQFoFX4_O4YFjA/company-logo_200_200/0/1630650151370/guardian_capital_gestora_de_recursos_s_a_logo?e=1717632000&v=beta&t=IH8eSlq68yL83p_2Bm1rDeaKEFjjiO10qn-Sw7IhpDo')

st.title('Banco de dados - SQL')
with st.expander('objetivos'):
    st.text('''Utilizando a planilha "Dados Contratos" fornecida para a resolução da Parte 2, quais comando você
utilizaria em SQL para chegar aos seguintes resultados:
a. Número total de contratos.
b. Contratos com um Valor de Parcela maior do que R$ 100.
c. Selecionar todos os campos da tabela, ordenado pela data de vencimento.
Utilize o seguinte nome para as colunas:
Código do Contrato = codigo_contrato
Número de Parcelas = numero_parcelas
Valor da Parcela = valor_parcela
Data de Vencimento = data_vencimento
Data de Aquisição = data_aquisicao
ID do Cliente = id_cliente''')
    
st.header('A) Número total de contratos')
st.code('''
SELECT COUNT(*) AS total_contratos
FROM DadosContratos;        
''')

st.header('B) Contratos que valor de parcela maior do que 100 reais')

st.code('''
SELECT codigo_contrato
FROM DadosContratos
WHERE valor_parcela > 100;
''')

st.header('C) Selecionar todos os campos da tabela por data de vencimento')
st.code('''
SELECT *
FROM DadosContratos
ORDER BY data_vencimento ASC;
''')