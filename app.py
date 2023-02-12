import streamlit as st

import pandas as pd
import pandas_datareader.data as pdrd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import yfinance as yf
yf.pdr_override()

# Sidebar - seleção
st.sidebar.title('Menu')

# Lista das empresas - ticket B3
Empresas = ['ITSA4', 'EZTC3', 'ITUB4', 'ENBR3', 'ENAT3', 'ALUP4',
      'RENT3', 'DIRR3', "LREN3", "KLBN11", "WIZS3", "CPLE3", "RADL3"]

Empresas.sort()

Selecao = st.sidebar.selectbox(
  'Selecione a empresa:', Empresas, format_func=lambda x: x + '.SA')

# Range de seleção de meses
slider = st.sidebar.slider('Período de meses', 0, 12, 1, key='Barra_Selecao')
selecao_range = str(slider) + 'mo'

# Colunas
col1, col2 = st.columns([3, 0.2])

# Imagens
col2.image(
  f'https://www.ivalor.com.br/media/emp/logos/{Selecao[0:4]}.png', width=100)

# Titulo
titulo = f'Análise Econômica { str(Selecao) }'
col1.title(titulo)

# Coletar da API do Yahoo Finance
dados = pdrd.get_data_yahoo(Selecao + '.SA', period=selecao_range)

# Filtrando dados sem informação
filtroIndex = dados.loc[(dados['Open'] == 0) & (dados['Low'] == 0)].index
if not filtroIndex.empty:
  dados.drop(filtroIndex, inplace=True)

# Grafico
grafico_candlestick = go.Figure(
  data=[
    go.Candlestick(
      x=dados.index,
      open=dados['Open'],
      high=dados['High'],
      low=dados['Low'],
      close=dados['Close']
    )
  ]
)

grafico_candlestick.update_layout(
  xaxis_rangeslider_visible=False,
  title='Análise das Ações',
  xaxis_title='Período',
  yaxis_title='Preço de Fechamento'
)

# Mostrar o gráfico do plotly no streamlit
st.plotly_chart(grafico_candlestick)


# Mostrar dados do gráfico em tabela
if st.checkbox('Mostrar dados em tabela'):
  st.subheader('Tabela de registro')

  # Ordenação por data mais recente
  dados = dados.sort_index(ascending=False)

  dados.index = dados.index.strftime('%d-%m-%Y')
  dados.index.name = 'Data'
  styler = dados.reset_index().style.hide_index().format(subset=['Open','High','Low','Close','Adj Close'], decimal=',', precision=2)
  st.write(styler.to_html(), unsafe_allow_html=True)

  # Salvando os dados em CSV
  st.markdown('<br />', unsafe_allow_html=True)
  csv = dados.to_csv().encode('utf-8')
  st.download_button('Download CSV file', 
                      data=csv,
                      file_name=f'registro_acao_{Selecao}_em_{selecao_range}m.csv',
                      mime='text/csv')

  # Estilizando a tabela por meio de hack com st.markdown
styler_table = """
      <style>
        .css-1offfwp th, .css-1offfwp td { padding: 0.4rem 1.5rem; border : 0 }
        td, th { text-align: -webkit-center; }
        h1 { padding: 1rem 0px 0.75rem; }
        div.css-ocqkz7 { -webkit-box-align: center; align-items: baseline; }
      </style>
      """

st.markdown(styler_table, unsafe_allow_html=True)
