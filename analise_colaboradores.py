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
st.markdown(page_bg_img, unsafe_allow_html=True)
# st.session_state
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

escolha = st.selectbox('o que deseja ver',['clique para escolher','pular para a análise','ver construção'])
if escolha == 'ver construção':
    if st.session_state.bg_on_off:
        pass
    else:

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
        st.markdown(page_bg_img, unsafe_allow_html=True)
    df_cobranca = pd.read_excel('planilhas/Dados Cobranca - Parte 1.xlsx')
    if st.checkbox('VER DATAFRAME COMPLETO'):
        st.dataframe(df_cobranca)


    # df_cobranca = pd.read_excel('planilhas/Dados Cobranca - Parte 1.xlsx')
    # if st.checkbox('VER DATAFRAME MÉDIAS'):k

    option1 = st.radio('Escolha uma empresa para analisar', list((df_cobranca['Cobrador'].value_counts().index)), horizontal = True)
    df_cobranca.loc[df_cobranca['Cobrador'] == option1]
    st.divider()

    por_cobrador_media = df_cobranca.groupby('Cobrador')[['Valor de Parcela', 'Valor Pago']].mean()

    st.subheader('MÉDIA DOS PAGAMENTOS E AFINS',divider='rainbow')
    por_cobrador_media['PREÇO_CUSTO'] = [10000,9000,3000,7000]
    por_cobrador_media['diferenca_bruta'] = (por_cobrador_media['Valor de Parcela'] - por_cobrador_media['Valor Pago']).round(2).apply(lambda x : f'{x} R$ não recuperados em média' )
    por_cobrador_media['diferenca_relativa'] = (((por_cobrador_media['Valor Pago'] / por_cobrador_media['Valor de Parcela'])) * 100).round(2).apply(lambda x : f'{x} % recuperados em média')
    por_cobrador = por_cobrador_media[['PREÇO_CUSTO', 'Valor de Parcela', 'Valor Pago', 'diferenca_relativa', 'diferenca_bruta']]
    st.dataframe(por_cobrador_media, use_container_width = True)

    st.subheader('AQUI, VEMOS UMA TABELA DA SOMA, PARA VER SE A MEDIA ESTÁ EM HARMONIA COM A SOMA TOTAL',divider='rainbow')

    por_cobrador_soma = df_cobranca.groupby('Cobrador')[['Valor de Parcela', 'Valor Pago']].sum()
    por_cobrador_soma['PREÇO_CUSTO'] = [10000,9000,3000,7000]
    por_cobrador_soma['diferenca_bruta'] = (por_cobrador_soma['Valor de Parcela'] - por_cobrador_soma['Valor Pago']).round(2).apply(lambda x : f'{x} R$ não recuperados no total' )
    por_cobrador_soma['diferenca_relativa'] = (((por_cobrador_soma['Valor Pago'] / por_cobrador_soma['Valor de Parcela'])) * 100).round(2).apply(lambda x : f'{x} % recuperados em média')
    por_cobrador = por_cobrador_soma[['PREÇO_CUSTO', 'Valor de Parcela', 'Valor Pago', 'diferenca_relativa', 'diferenca_bruta']]
    st.dataframe(por_cobrador_soma, use_container_width = True)

    st.header('TERMÔMETRO DE PREÇO DOS SERVIÇOS', divider='rainbow')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('contagem de clientes por cobrador')
        st.dataframe(df_cobranca['Cobrador'].value_counts(), use_container_width = True)#.style.applymap(destaque_max_min)

    with col2:
        st.subheader('preço do serviço de cada cobrador')
        st.dataframe(por_cobrador_soma['PREÇO_CUSTO'].apply(lambda x : f'{x} R$'), use_container_width = True)

    with col3:
        st.subheader('CUSTO POR SERVIÇO(pessoa atendida) MÉDIO')
        # por_cobrador['']
        por_cobrador['PREÇO_CUSTO'] / df_cobranca['Cobrador'].value_counts()
    st.divider()


    df_cobranca
    st.subheader('ZERAMENTO DE PAGAMENTO DE PARCELAS',divider='rainbow')

    # st.dataframe(df_cobranca.groupby('Cobrador')df_cobranca[['Valor Pago'] == 0].count())
    st.dataframe((df_cobranca.loc[df_cobranca['Valor Pago'] == 0])['Cobrador'].value_counts())

    st.subheader('MÉDIA DO VENCIMENTO DAS PARCELAS',divider='rainbow')
    # st.dataframe(df_cobranca.info())

    df_cobranca['tempo_pgto'] = df_cobranca['Data de Cobrança'] - df_cobranca['Data de Vencimento']
    df_cobranca['tempo_pgto'] = df_cobranca['tempo_pgto']
    df_cobranca['tempo_pgto_dias'] = df_cobranca['tempo_pgto'].apply(lambda x: f'{x} dias' if pd.notnull(x) else np.nan)

    df_cobranca

    mes_por_grupo = df_cobranca.groupby('Cobrador')['tempo_pgto'].mean().dt.days.apply(lambda x : f'{x} dias')
    st.dataframe(mes_por_grupo)

if escolha == 'pular para a análise':

    if st.session_state.bg_on_off:
        pass
    else:

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
        st.markdown(page_bg_img, unsafe_allow_html=True)

######################################################
    df_cobranca = pd.read_excel('planilhas/Dados Cobranca - Parte 1.xlsx')
    por_cobrador_media = df_cobranca.groupby('Cobrador')[['Valor de Parcela', 'Valor Pago']].mean()

    por_cobrador_media['PREÇO_CUSTO'] = [10000,9000,3000,7000]
    por_cobrador_media['diferenca_bruta'] = (por_cobrador_media['Valor de Parcela'] - por_cobrador_media['Valor Pago']).round(2).apply(lambda x : f'{x} R$ não recuperados em média' )
    por_cobrador_media['diferenca_relativa'] = (((por_cobrador_media['Valor Pago'] / por_cobrador_media['Valor de Parcela'])) * 100).round(2).apply(lambda x : f'{x} % recuperados em média')
    por_cobrador = por_cobrador_media[['PREÇO_CUSTO', 'Valor de Parcela', 'Valor Pago', 'diferenca_relativa', 'diferenca_bruta']]


    por_cobrador_soma = df_cobranca.groupby('Cobrador')[['Valor de Parcela', 'Valor Pago']].sum()
    por_cobrador_soma['PREÇO_CUSTO'] = [10000,9000,3000,7000]
    por_cobrador_soma['diferenca_bruta'] = (por_cobrador_soma['Valor de Parcela'] - por_cobrador_soma['Valor Pago']).round(2).apply(lambda x : f'{x} R$ não recuperados no total' )
    por_cobrador_soma['diferenca_relativa'] = (((por_cobrador_soma['Valor Pago'] / por_cobrador_soma['Valor de Parcela'])) * 100).round(2).apply(lambda x : f'{x} % recuperados em média')
    por_cobrador = por_cobrador_soma[['PREÇO_CUSTO', 'Valor de Parcela', 'Valor Pago', 'diferenca_relativa', 'diferenca_bruta']]

    df_cobranca['tempo_pgto'] = df_cobranca['Data de Cobrança'] - df_cobranca['Data de Vencimento']
    df_cobranca['tempo_pgto'] = df_cobranca['tempo_pgto']
    df_cobranca['tempo_pgto_dias'] = df_cobranca['tempo_pgto'].apply(lambda x: f'{x} dias' if pd.notnull(x) else np.nan)
    mes_por_grupo = df_cobranca.groupby('Cobrador')['tempo_pgto'].mean().dt.days.apply(lambda x : f'{x} dias')




######################################################
    st.header('CONFIGURE SUAS PREFERÊNCIAS')
    tempo_escrita = st.slider('velocidade de escrita do texto',0.00,0.10,0.04)
    tempo_pausa = st.slider('tempo de intervalo entre as análises',0,50,10)

    st.title('VER A ANÁLISE')


    if st.button('conferir analise dos cobradores'):

        _LOREM_IPSUM = """
            De primeiro momento, apenas com a leitura do enunciado,
            notamos que a empresa C é a mais barata disparadamente, e a empresa
            A é a mais cara. Isso nos leva  a alguns pensamentos, do tipo se de fato,
            uma empresa que cobra barato tem um bom serviço, ou até melhor, este
            valor cobrado é pelo serviço inteiro, será que a quantidade de empresas 
            ela atendeu foi menor ou de fato ela tem um preço muito mais abaixo do
            mercado de suas concorrentes? Será que ela por cobrar mais barato tem um serviço
            pior? Será que quanto mais caro, melhor o serviço..?

            Muitas dúvidas surgem ao ver apenas os dados puros, e então, é necessário filtrar 
            os dados para obter alguns insights sobre o que de fato, está acontecendo. 
            Primeiro de tudo, a principal coisa a se fazer é agrupar os dados por empresa 
            cobradora. 
            """


        def stream_data():
            for word in _LOREM_IPSUM.split():
                yield word + " "
                time.sleep(tempo_escrita)


        st.write_stream(stream_data)
        st.header('conferindo média dos pagamentos e afins',divider='rainbow')
        st.dataframe(por_cobrador_media)
        _LOREM_IPSUM = '''
        Aqui, podemos analisar que o valor MÉDIO das parcelas no grupo C é maior, mas
        por outro lado, o valor pago no final pelos alunos também é. Fazendo uma análise simples 
        com seu concorrente D que tem o mesmo valor médio de valor da parcela,
        pode-senotar que a empresa C ja leva uma vantagem sob a empresa D, pois pode-se
        notar um valor muito inferior das parcelas efetivamente pagas pelos alunos na cobradora D 
        comparando com a cobradora C. Fazendo a análise geral, observa-se que a empresa C 
        leva vantagem  disparada em eficiência para fazer com que as pessoas de fato 
        paguem a faculdade. Com uma margem de 75,2 % recuperados, ela lidera o melhor lugar 
        com 15%  de diferença da segunda melhor, que é a B, com 60% em média.
        
        '''
        st.write_stream(stream_data)
        st.divider()
        # time.sleep(10)
########################################
        progress_text = "tempo de espera..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(tempo_pausa/100)
            my_bar.progress(percent_complete + 1, text=progress_text)

########################################
        st.header('Verificando a soma por grupo de cobrador',divider='rainbow')

        _LOREM_IPSUM = '''
        Ao observarmos a soma das parcelas e o valor efetivamente pago, podemos chamar atenção ao grupo B e A principalmente, onde que por uma diferença dde 3%, na
        margem de conversão, a diferença bruta se deu quase que dobrada. Aqui podemos pensar o que pode realmente estar causando isso, e uma das razões é de umm grupo ter atendio mais clientes que
        o outro grupo. Portanto, analisar o preço por completo não é uma maneira boa e analisar o desempenho de cada grupo comparativamente com os outros. Para isso, podemos calcular o custo por serviço 
        e cada empresa, simplesmente pegando o custo total e dividindo pela quantidade de clientes alcançadas. o resultado vemos aqui nas tabelas abaixo. 
        
        '''
        st.write_stream(stream_data)
        st.divider()
        st.header('TERMÔMETRO DE PREÇO DOS SERVIÇOS', divider='rainbow')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('contagem de clientes por cobrador')
            st.dataframe(df_cobranca['Cobrador'].value_counts(), use_container_width = True)#.style.applymap(destaque_max_min)

        with col2:
            st.subheader('preço do serviço de cada cobrador')
            st.dataframe(por_cobrador_soma['PREÇO_CUSTO'].apply(lambda x : f'{x} R$'), use_container_width = True)

        with col3:
            st.subheader('CUSTO POR SERVIÇO(pessoa atendida) MÉDIO')
            # por_cobrador['']
            por_servico = por_cobrador['PREÇO_CUSTO'] / df_cobranca['Cobrador'].value_counts()
            por_servico = por_servico.to_frame('valor médio por serviço')
            st.dataframe(por_servico,use_container_width=True)#.apply(lambda val: 'background-color: green' if val == 187.5 else ('background-color: red' if val == 375 else ''))

        _LOREM_IPSUM = '''
            Vimos aqui na tabela então que o preço cobrado de 3000 reais da cobradora C é mais baixo pois atende menos clientes mas de fato ele é um serviço mais barato que os outros e tambpem mais eficiente,
            visto que a taxa de conversão dos contratos é maior por um preço de custo por serviço médio mais barato , também. Não podemos afirmar que a eficiencia foi oriunda da menor quantiadde de clientes atendidos, pois 
            então poderia dar mais atenção para cada um individualmente, mas o fato é que o serviço apresentado por ela, inicialmente é melhor e mais barato. Por utro lado, o serviço da cobradora A mesmo sendo o mais caro no total,
            vemos que isso se deu a quantidade de clientes que ela atendeu, pois sua média por serviço é de apenas 200 reais,
            bem próximo inclusive da C, porém a efetividade de conversão da A é bem inferior a da C, como ja vimos antes. 
            
            '''

        st.write_stream(stream_data)
        # time.sleep(10)
########################################
        progress_text = "tempo de espera..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(tempo_pausa/100)
            my_bar.progress(percent_complete + 1, text=progress_text)

########################################
        st.divider()
        st.header('ainda há outras possiveis analises a se fazer',divider='rainbow')

        _LOREM_IPSUM = '''
        Podemos analisar tambem o quanto cada cobradora foi eficaz no sentido de pelo menos fazer com que o cliente pagasse uma parte do valor da parcela. No caso, como podemos ver no dataframe ao lado, a C foi 
        a  que tambem, mais conseguiu ter sucesso converter pelo menos uma parte do valor da parcela em caixa para a faculadde, com apenas 6,25% não pagando nada, enquanto a A, foi a segunda melhor, com 24%.
        
        '''
        col1,col2,col3 = st.columns([0.4,0.25,0.35])
        with col1:
            st.write_stream(stream_data)
        with col2:
            st.subheader('qtde de zeramentos')
            st.dataframe((df_cobranca.loc[df_cobranca['Valor Pago'] == 0])['Cobrador'].value_counts(),use_container_width=True)
        with col3:
            st.subheader('qtde de zeramentos relativo')
            st.dataframe(((df_cobranca.loc[df_cobranca['Valor Pago'] == 0])['Cobrador'].value_counts() / df_cobranca['Cobrador'].value_counts() * 100),use_container_width=True)

        st.divider()
########################################
        progress_text = "tempo de espera..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(tempo_pausa/100)
            my_bar.progress(percent_complete + 1, text=progress_text)

########################################
        st.header('Eficiência vs Prazo de tempo',divider='rainbow')

        _LOREM_IPSUM = '''
        Antes de tirar quaisquer conclusões finais, precisamos analisar o tempo médio de cobrança que cada grupo cobrador teve. Quanto menor o tempo para o cliente pagar as parcelas, mais chance do próprio não pagar. 
        Então não adianta nada comparar a eficiencia em receber as parcelas sem ao menos olhar o prazo em que essas foram cobradas para cada grupo cobrador. Analisando aqui a tabela ao lado, vimis que o grupo C também leva uma
        vantagem sob esse aspecto, onde com menos tempo para conseguir cobrar, ou melhor, mais rapido os clientes da faculdade terem que pagara  faculdade, ele conseguiu atingir mmelhores resultados em termos de eficiencia 
        na conversão das parcelas em caixa para a faculdade. As outras tiveram um tempo relativamente igual, muita relevância. 
        
        '''
        col1,col2 = st.columns([0.8,0.2])
        with col1:
            st.write_stream(stream_data)
        with col2:
            df_cobranca['tempo_pgto'] = df_cobranca['Data de Cobrança'] - df_cobranca['Data de Vencimento']
            df_cobranca['tempo_pgto'] = df_cobranca['tempo_pgto']
            df_cobranca['tempo_pgto_dias'] = df_cobranca['tempo_pgto'].apply(lambda x: f'{x} dias' if pd.notnull(x) else np.nan)

            # df_cobranca

            mes_por_grupo = df_cobranca.groupby('Cobrador')['tempo_pgto'].mean().dt.days.apply(lambda x : f'{x} dias')
            st.dataframe(mes_por_grupo)
        # time.sleep(10)
########################################
        progress_text = "tempo de espera..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(tempo_pausa/100)
            my_bar.progress(percent_complete + 1, text=progress_text)

########################################
        st.divider()

        st.header('O ULTIMO PONTO DE VISTA: analisando sem considerar os zeramentos',divider='rainbow')

        _LOREM_IPSUM = '''
            Aqui vamos verificar de maneira rápida a perfoemance dos cobradores, excluindo aqueles clientes que não pagaram nada. O intuito aqui é ver se ou pela quantidade muito alta de clientes
            que uma empresa teve ou por qualquer outro motivo que posasa ter, a empresa não cosneguiou lidar com tamanha demanda e então, deixou de lado, abriu mao de alguns clientes para cuidar dos outros. Então, 
            para fins de simplificar a análise e não entrar em algo tão arbitrário, verificaremos apenas a eficiencia dos grupos excluindo os zeramentos.
            '''
        col1,col2 = st.columns([0.5,0.5])
        st.write_stream(stream_data)


        st.subheader('comparando sem zeramentos VS com zeramento')
        c1,c2 = st.columns(2)
        with c1:
            st.subheader('SEM ZERAMENTOS')
            df_nulos = df_cobranca.dropna()
            por_cobrador_media = df_nulos.groupby('Cobrador')[['Valor de Parcela', 'Valor Pago']].mean()
            por_cobrador_media['PREÇO_CUSTO'] = [10000,9000,3000,7000]
            por_cobrador_media['diferenca_bruta'] = (por_cobrador_media['Valor de Parcela'] - por_cobrador_media['Valor Pago']).round(2).apply(lambda x : f'{x} R$ perdidos' )
            por_cobrador_media['diferenca_relativa'] = (((por_cobrador_media['Valor Pago'] / por_cobrador_media['Valor de Parcela'])) * 100).round(2).apply(lambda x : f'{x} % convertidos')
            por_cobrador = por_cobrador_media[['PREÇO_CUSTO', 'Valor de Parcela', 'Valor Pago', 'diferenca_relativa', 'diferenca_bruta']]
            st.dataframe(por_cobrador_media, use_container_width = True)
        with c2:
            st.subheader('COM ZERAMENTOS')
            por_cobrador_media = df_cobranca.groupby('Cobrador')[['Valor de Parcela', 'Valor Pago']].mean()
            por_cobrador_media['PREÇO_CUSTO'] = [10000,9000,3000,7000]
            por_cobrador_media['diferenca_bruta'] = (por_cobrador_media['Valor de Parcela'] - por_cobrador_media['Valor Pago']).round(2).apply(lambda x : f'{x} R$ perdidos' )
            por_cobrador_media['diferenca_relativa'] = (((por_cobrador_media['Valor Pago'] / por_cobrador_media['Valor de Parcela'])) * 100).round(2).apply(lambda x : f'{x} % convertidos')
            por_cobrador = por_cobrador_media[['PREÇO_CUSTO', 'Valor de Parcela', 'Valor Pago', 'diferenca_relativa', 'diferenca_bruta']]
            st.dataframe(por_cobrador_media, use_container_width = True)

        _LOREM_IPSUM = '''
        Dá para perceber aqui que o que puxou de fato a empresa A para baixo foi os clientes que não apgaram nada para ela. isso pode se dar ao fato tanto dos clientes que foram escolhidos para a cobradora A cuidar serem
        mais chatos de lidar até o fato de que a empresa cobradora não conseguiu lidar com a grande quantidade de clientes (a maior quantidade) e teve que abdicar de cobrar alguns e preferiram focar em outros. A empresa C
        mal mudou alguma coisa pois tinha apenas 1 zeramento e olhando para as empresas B e C, detalhe para a TOP 2 em questão de custo total( cobradora B), pois seu rating de conversão das parcelas aumentou bastante tambem,
        mesmo ela tendo metade dos clientes que a A tem e sendo a segunda mais cara.
        A que mais melhorou, obviamente foi a D, que faz juz com a proporção entre quantidade de zeramentos e quantidade de clientes atendidos, tendo ai quase 1/3 dos clientes sem pagar absolutamente nada. 
            
            '''

        st.write_stream(stream_data)
        # time.sleep(10)
########################################
        progress_text = "tempo de espera..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(tempo_pausa/100)
            my_bar.progress(percent_complete + 1, text=progress_text)

########################################
        st.divider()

        st.title('CONCLUSÕES FINAIS')
        
        _LOREM_IPSUM = '''
        Portanto, com base nas análises feitas anteriormente, podemos tirar algumas conclusões, mas claramente ja podemos verificar que a empresa C leva vantagem absoluta em tudo.         
            '''
        st.write_stream(stream_data)

        _LOREM_IPSUM = '''
        Em relação ao custo e benefício e eficiência, a cobradora C, apesar de cobrar o menor preço total pelo serviço (R$3.000), possui a maior eficiência em termos de conversão de pagamento. 
        Isso indica que a cobradora C não só oferece um serviço mais acessível em termos de custo mas também consegue manter uma alta eficácia 
        na recuperação de valores, com 75,2% das parcelas sendo efetivamente pagas.     
            '''
        st.write_stream(stream_data)
        
        _LOREM_IPSUM = '''
        A análise comparativa entre as cobradoras C e D, que têm o mesmo valor médio de parcela, destaca a vantagem da C sobre a D, especialmente no que tange à recuperação efetiva dos pagamentos. 
        Ainda que a D apresente um valor de parcela similar, sua eficiência na recuperação dos pagamentos é significativamente menor. Olhando um pouco agora para a cobradora A, apesar de atender 
        o maior número de clientes e ter o maior custo total de serviço, apresenta uma eficiência de conversão inferior à da cobradora C. Isso sugere que a quantidade de 
        clientes atendidos e a gestão de casos de não pagamento (zeramentos) são fatores críticos na eficiência global da recuperação de pagamentos. A cobradora C, com apenas 
        1 caso de não pagamento, destaca-se pela eficácia na gestão de sua carteira de clientes.
            '''
        st.write_stream(stream_data)

        _LOREM_IPSUM = '''
        No que tange ao tempo médi de pagamento, ele é um indicador relevante da pressão sobre os clientes para a quitação das parcelas. A cobradora C, com o menor tempo médio (39 dias), 
        não apenas conseguiu manter uma alta taxa de recuperação como também demonstrou eficácia na rápida conversão de pagamentos. Quando excluimos os casos de não pagamento, observamos melhorias 
        na eficiência de conversão das cobradoras A e D, o que ressalta o impacto negativo significativo dos zeramentos sobre a eficiência geral.
        Ainda assim, a cobradora C mantém sua posição de liderança, evidenciando uma estratégia de cobrança robusta e eficaz.
            '''
        st.write_stream(stream_data)

        _LOREM_IPSUM = '''
    Sendo assim, a análise dos dados sugere que a cobradora C não só oferece o serviço mais acessível mas também demonstra ser a mais eficaz na recuperação de pagamentos, 
    evidenciando uma combinação ótima de estratégia de precificação e eficiência de cobrança. Embora a cobradora A atenda a mais clientes, a gestão eficaz dos casos de 
    pagamento e a minimização de zeramentos são essenciais para a maximização da eficiência. As cobradoras precisam equilibrar o volume de clientes, a estratégia de precificação e as 
    práticas de cobrança para otimizar sua eficiência e eficácia. 
    A estratégia adotada pela cobradora C serve como um modelo eficaz nesse contexto, oferecendo lições valiosas sobre a gestão de serviços de cobrança.
            '''
        st.write_stream(stream_data)



    st.divider()
