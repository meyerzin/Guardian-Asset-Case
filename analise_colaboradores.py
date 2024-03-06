import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    layout = 'wide',
    page_title = 'Una INVESTMENT - Data Science'
    )


df_cobranca = pd.read_excel('planilhas/Dados Cobranca - Parte 1.xlsx')
