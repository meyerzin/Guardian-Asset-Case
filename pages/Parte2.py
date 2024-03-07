import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from functions import *

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
    background-size: 100%;
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
        ms.themes = {"current_theme": "light",
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
st.header('PARTE 2 - MANIPULAÇÃO DE DADOS',divider='rainbow')

if st.checkbox('ver codigo    '):
    st.code('''
df_contratos = pd.read_csv('planilhas/Dados Contratos - Parte 2.csv', sep=';', index_col='ID do Cliente')
df_nascimento = pd.read_csv('planilhas/Data Nascimento - Parte 2.csv', sep=';', index_col='Cliente')
st.subheader('tabela de nascimento')
df_nascimento
st.divider()
st.subheader('tabela de contratos')
df_contratos
''')
df_contratos = pd.read_csv('planilhas/Dados Contratos - Parte 2.csv', sep=';', index_col='ID do Cliente')
df_nascimento = pd.read_csv('planilhas/Data Nascimento - Parte 2.csv', sep=';', index_col='Cliente')
st.subheader('tabela de nascimento')
df_nascimento
st.divider()
st.subheader('tabela de contratos',divider='rainbow')
df_contratos

st.subheader('Juntando os dois dataframes',divider='rainbow')
if st.checkbox('ver codigo  '):
    st.code('''
col1,col2 = st.columns(2)
with col1:
    st.dataframe(df_contratos.merge(df_nascimento, left_index=True, right_index=True)['Data de Nascimento'])
with col2:
    st.dataframe(df_nascimento.dropna())

df_junto = df_contratos.merge(df_nascimento, left_index=True, right_index=True)

''')
col1,col2 = st.columns(2)
with col1:
    st.dataframe(df_contratos.merge(df_nascimento, left_index=True, right_index=True)['Data de Nascimento'])
with col2:
    st.dataframe(df_nascimento.dropna())

df_junto = df_contratos.merge(df_nascimento, left_index=True, right_index=True)

st.subheader('tratando os dados',divider='rainbow')
if st.checkbox('ver o codigo'):
    st.code('''
df_junto.dropna(axis=1,inplace = True)
print(df_junto.info())
df_junto.columns = ['codigo_do_contrato', 'numero_parcelas', 'valor_parcela', 'data_vencimento', 'data_aquisicao', 'data_nascimento' ]
df_junto = df_junto.astype({
    'numero_parcelas': np.int64,
    'valor_parcela': float,
})
print(df_junto.info())

df_junto.data_vencimento = pd.to_datetime(df_junto.data_vencimento, format='%d/%m/%Y')
df_junto.data_aquisicao = pd.to_datetime(df_junto.data_aquisicao, format='%d/%m/%Y')
df_junto.data_nascimento = pd.to_datetime(df_junto.data_nascimento, format='%d/%m/%Y')
df_junto.info()
''')

df_junto.dropna(axis=1,inplace = True)
print(df_junto.info())
df_junto.columns = ['codigo_do_contrato', 'numero_parcelas', 'valor_parcela', 'data_vencimento', 'data_aquisicao', 'data_nascimento' ]
df_junto = df_junto.astype({
    'numero_parcelas': np.int64,
    'valor_parcela': float,
})
print(df_junto.info())

df_junto.data_vencimento = pd.to_datetime(df_junto.data_vencimento, format='%d/%m/%Y')
df_junto.data_aquisicao = pd.to_datetime(df_junto.data_aquisicao, format='%d/%m/%Y')
df_junto.data_nascimento = pd.to_datetime(df_junto.data_nascimento, format='%d/%m/%Y')
df_junto.info()

df_junto
st.subheader('criando a coluna do valor de contrato',divider='rainbow')
if st.checkbox('ver codigo'):
    st.code('''
df_junto['valor_de_contrato'] = df_junto.numero_parcelas * df_junto.valor_parcela
df_junto = df_junto[['codigo_do_contrato', 'numero_parcelas', 'valor_parcela','valor_de_contrato', 'data_vencimento', 'data_aquisicao', 'data_nascimento' ]]
df_junto.info()
df_junto['tempo_contrato'] = df_junto.data_vencimento - df_junto.data_aquisicao
col1,col2 = st.columns([0.7,0.3])
with col1:
    st.dataframe(df_junto, use_container_width=True)
with col2:
    st.dataframe((df_junto.tempo_contrato.dt.days / 30).round(0).apply(lambda x : f'{int(x)} meses'),use_container_width=True)

df_junto.tempo_contrato = (df_junto.tempo_contrato.dt.days / 30).round(0)
st.dataframe(df_junto)
df_junto.tempo_contrato = df_junto.tempo_contrato.astype(int)
df_junto.info()

df_junto['VP'] = df_junto.valor_de_contrato / (1 + 0.018) ** df_junto.tempo_contrato
df_junto.info()
''')

df_junto['valor_de_contrato'] = df_junto.numero_parcelas * df_junto.valor_parcela
df_junto = df_junto[['codigo_do_contrato', 'numero_parcelas', 'valor_parcela','valor_de_contrato', 'data_vencimento', 'data_aquisicao', 'data_nascimento' ]]
df_junto.info()
df_junto['tempo_contrato'] = df_junto.data_vencimento - df_junto.data_aquisicao
col1,col2 = st.columns([0.7,0.3])
with col1:
    st.dataframe(df_junto, use_container_width=True)
with col2:
    st.dataframe((df_junto.tempo_contrato.dt.days / 30).round(0).apply(lambda x : f'{int(x)} meses'),use_container_width=True)

df_junto.tempo_contrato = (df_junto.tempo_contrato.dt.days / 30).round(0)
st.dataframe(df_junto)
df_junto.tempo_contrato = df_junto.tempo_contrato.astype(int)
df_junto.info()

df_junto['VP'] = df_junto.valor_de_contrato / (1 + 0.018) ** df_junto.tempo_contrato
df_junto.info()
df_junto
st.subheader('dataframe com o valor presente e colunas ordenadas',divider='rainbow')
st.code('''df_junto = df_junto[['data_nascimento','codigo_do_contrato','numero_parcelas','valor_parcela','valor_de_contrato','tempo_contrato','VP','data_vencimento','data_aquisicao']]
''')
df_junto = df_junto[['data_nascimento','codigo_do_contrato','numero_parcelas','valor_parcela','valor_de_contrato','tempo_contrato','VP','data_vencimento','data_aquisicao']]
st.dataframe(df_junto)

st.subheader('concatenando as duas colunas',divider='rainbow')
st.text('ADCIONEI |||| para identificar o contrato das parcelas')
st.code('''df_junto['cod_cont_num_par'] = df_junto.codigo_do_contrato + '|||' + df_junto.numero_parcelas.astype(str)
''')
df_junto['cod_cont_num_par'] = df_junto.codigo_do_contrato + '|||' + df_junto.numero_parcelas.astype(str)
df_junto


st.header('AGRUPANDO O DATAFRAME POR ID DO CLIENTE',divider='rainbow')
col1,col2 = st.columns(2)
with col1:
    df_agrupado = df_junto.groupby(df_junto.index).agg({
        'valor_de_contrato': ['sum', 'count'],
        'data_aquisicao': 'min',  # 'min' para a data mais antiga, presumindo que é a data do primeiro contrato
        'numero_parcelas': 'mean',
        'valor_parcela': 'sum'
    })
    st.dataframe(df_agrupado)
with col2:
    st.code('''df_junto.groupby(df_junto.index).agg({
        'valor_de_contrato': ['sum', 'count'],
        'data_aquisicao': 'min',  
        'numero_parcelas': 'mean',
        'valor_parcela': 'sum'
    })''')

st.dataframe(df_junto.index.value_counts())