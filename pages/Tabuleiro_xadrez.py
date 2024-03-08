import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
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

# st.session_state
img = get_img_as_base64("image.jpg")
if st.sidebar.checkbox('desabilitar imagens de fundo',key='bg_on_off'):

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
else:
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
st.header('PARTE 4 - TABULEIRO DE XADREZ',divider='rainbow')

def criar_e_posicionar_rainhas(n, posicoes_rainhas):
    '''
    Args:
    - n: Tamanho do lado do tabuleiro de xadrez.
    - posicoes_rainhas: Lista de tuplas, onde cada tupla contém as coordenadas (linha, coluna) para posicionar cada rainha.'''

    tabuleiro = [[' ' for _ in range(n)] for _ in range(n)]
    
    def marcar_movimentos(linha, coluna):

        for i in range(n):
            # horizontal e vertical
            tabuleiro[linha][i] = 'X'
            tabuleiro[i][coluna] = 'X'
            
            # diagonais
            if linha+i < n and coluna+i < n:
                tabuleiro[linha+i][coluna+i] = 'X'
            if linha-i >= 0 and coluna+i < n:
                tabuleiro[linha-i][coluna+i] = 'X'
            if linha+i < n and coluna-i >= 0:
                tabuleiro[linha+i][coluna-i] = 'X'
            if linha-i >= 0 and coluna-i >= 0:
                tabuleiro[linha-i][coluna-i] = 'X'
    
    # Posiciona as rainhas e marca os movimentos
    for linha, coluna in posicoes_rainhas:
        marcar_movimentos(linha, coluna)
        tabuleiro[linha][coluna] = 'Q'  # Marca a posição da rainha
    
    return tabuleiro

# Exemplo de uso: criar um tabuleiro 8x8 com duas rainhas
posicoes_rainhas = []
n = st.selectbox('selcione a quantidade e lados que o tabuleiro terá:',[i for i in range(16)],0 )
qtde_rainhas = st.selectbox('selcione a quantidade de rainhas a posicionar:',[i for i in range(16)],0 )

for i in range(qtde_rainhas):
    linha = st.radio(f'POSIÇÃO DA RAINHA {i} (linha)',[i for i in range(n)], horizontal=True)
    coluna = st.radio(f'POSIÇÃO DA RAINHA {i} (coluna)', [i for i in range(n)],horizontal=True)
    posicoes_rainhas.append((linha,coluna))
    st.divider()

if st.checkbox('mostrar tabuleiro'):
    st.table(criar_e_posicionar_rainhas(n,posicoes_rainhas))
    tabuleiro_exemplo = criar_e_posicionar_rainhas(n,posicoes_rainhas)

    # if st.button('OPCIONAL: TABULEIRO E XADREZ ESTILIZADO'):   
        

    #     import matplotlib.pyplot as plt
    #     import numpy as np

    #     def desenhar_tabuleiro(tabuleiro):
    #         n = len(tabuleiro)
    #         tabuleiro_imagem = np.zeros((n, n, 3), dtype=np.uint8)

    #         # Cores
    #         cor_branca = [255, 255, 255]
    #         cor_preta = [0, 0, 0]
    #         cor_rainha = [255, 0, 0]  # Vermelho para a rainha
    #         cor_acesso = [0, 255, 0]  # Verde para casas acessíveis

    #         # Desenha o tabuleiro
    #         for i in range(n):
    #             for j in range(n):
    #                 if tabuleiro[i][j] == ' ':
    #                     # Alternar cores das casas
    #                     if (i + j) % 2 == 0:
    #                         tabuleiro_imagem[i, j] = cor_branca
    #                     else:
    #                         tabuleiro_imagem[i, j] = cor_preta
    #                 elif tabuleiro[i][j] == 'X':
    #                     tabuleiro_imagem[i, j] = cor_acesso
    #                 elif tabuleiro[i][j] == 'Q':
    #                     tabuleiro_imagem[i, j] = cor_rainha

    #         plt.figure(figsize=(8, 8))
    #         plt.imshow(tabuleiro_imagem)
    #         plt.xticks([]), plt.yticks([])  # Esconder os eixos
    #         # plt.show()

    #     # Usar o tabuleiro de exemplo do passo anterior
    #     st.pyplot(desenhar_tabuleiro(tabuleiro_exemplo))
