'''
pip install yfinance
pip install pandas
pip install openpyxl
'''

# Importa as bibliotecas
import yfinance as yf
import pandas as pd
from datetime import datetime


# Cria uma dataframe com os nomes das colunas
df = pd.DataFrame(columns=['Data', 'Preço', 'Sigla'])

# Lista com os ativos a serem pesquisados
ativos = ['HD', 'QSR', 'GOOGL', 'ABI.BR', 'TSLA', 'PETR3.SA', 'IBM', 'INTC', 'SONY', 'VALE3.SA']

# Percorre a lista
for ativo in ativos:

    # Símbolo da ação
    dados = yf.Ticker(ativo)

    # Intervalo da pesquisa
    data_inicial = "2021-01-08"
    #data_final = "2021-12-31"
    data_final = datetime.today().strftime("%Y-%m-%d")
    historico_dados = dados.history(start=data_inicial, end=data_final)

    # Obtém a cotação
    cotacao = historico_dados["Close"]

    # Edita o dataframe
    df_provisorio = cotacao.reset_index()
    df_provisorio.columns = ['Data', 'Preço']
    df_provisorio['Sigla'] = ativo

    # Adiciona o dataframe provisório ao principal
    df = pd.concat([df, df_provisorio])

# Organiza o dataframe por data, reseta o indice e apaga a coluna index
df = df.sort_values('Data')
df = df.reset_index()
df = df.drop('index', axis=1)


# Edita a data para o formato padrão
df['Data'] = df['Data'].astype(str)
df['Data'] = df['Data'].str.slice(stop=-15)
df['Data'] = pd.to_datetime(df['Data'])
df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')

# Exporta o dataframe para excel
df.to_excel('arquivos/dados_yahoo_finance.xlsx', index=False)
