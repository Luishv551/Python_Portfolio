# Importa as bibliotecas
import pandas as pd
from datetime import datetime
import numpy as np


# Importa os dados da planilha de movimentações
dados_completos = pd.read_csv('arquivos/dados_completos_movement.csv')

# Escreve 1 nas células em branco da coluna shares
dados_completos['shares'].fillna(1, inplace=True)

# Pega o nome de todas as empresas
ativos = dados_completos['name_1'].unique()
#ativos = ['HD']

# Importa os dados da planilha de preços das ações do Yahoo Finance
dados_yahoo = pd.read_excel('arquivos/dados_yahoo_finance.xlsx')

# Importa os dados da planilha de preços das ações que não são do Yahoo Finance
nao_listados = pd.read_csv('arquivos/precos_mes_1.csv')
nao_listados['Data'] = pd.to_datetime(nao_listados['Data'], dayfirst=True)
nao_listados['Data'] = nao_listados['Data'].dt.strftime('%d/%m/%Y')


# Concatena os dois dataframes de preços
df_precos = pd.concat([dados_yahoo, nao_listados])


# Cria um intervalo de datas
data_inicio = '2021-01-08'
#data_fim = '2021-12-31'
data_fim = datetime.today().strftime("%Y-%m-%d")
intervalo_datas = pd.date_range(start=data_inicio, end=data_fim)

df_principal = {}
for ativo in ativos:

    # Cria um DataFrame
    df_principal[ativo] = pd.DataFrame({'Data': intervalo_datas, 'Ativo': '', 'Nome Listado': '', 'Classe':'',
                                 'Setor': '', 'Moeda': '', 'Quantidade': '', 'Preço': '', 'Valor': '', 'Variação': '',
                                 'Aporte': '', 'Resgate': ''})

    # Edita o formato da coluna Data
    df_principal[ativo]['Data'] = df_principal[ativo]['Data'].dt.strftime('%d/%m/%Y')

    # Percorre o dataframe
    primeira_linha = True
    ultimo_valor = 0
    for index, row in df_principal[ativo].iterrows():
        
        # Busca vários dados por data e ativo na base de movimentações
        resultado = dados_completos.loc[(dados_completos['date'] == row['Data']) & (dados_completos['name_1'] == ativo)]
        
        # Se o resultado não estiver vazio
        if not resultado.empty:
            indice = int(resultado.index[0])
            
            # Salva os dados no dataframe
            df_principal[ativo].at[index, 'Ativo'] = resultado.at[indice, 'name_1']
            df_principal[ativo].at[index, 'Nome Listado'] = resultado.at[indice, 'name_2']
            df_principal[ativo].at[index, 'Classe'] = resultado.at[indice, 'asset_class']
            df_principal[ativo].at[index, 'Setor'] = resultado.at[indice, 'Sector']
            df_principal[ativo].at[index, 'Moeda'] = resultado.at[indice, 'currency']
            df_principal[ativo].at[index, 'Quantidade'] = resultado.at[indice, 'shares']


        # Busca os preços por data e ativo na base de preços
        resultado2 = df_precos.loc[(df_precos['Data'] == row['Data']) & (df_precos['Sigla'] == ativo)]
        
        # Se o resultado não estiver vazio
        if not resultado2.empty:
            indice2 = int(resultado2.index[0])
            
            # Salva o preço no dataframe
            df_principal[ativo].at[index, 'Preço'] = resultado2.at[indice2, 'Preço']

        # Cálculo das outras coluna
        if primeira_linha:

            # Verifica se a linha está vazia, se estiver passa para a próxima iteração 
            try:
                if df_principal[ativo].at[index, 'Quantidade'] > 0: #Se for Quantidade positiva = Aporte
                    df_principal[ativo].at[index, 'Aporte'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço']
                else:
                    df_principal[ativo].at[index, 'Resgate'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço']
            except:
                continue
                
            df_principal[ativo].at[index, 'Valor'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço']
            df_principal[ativo].at[index, 'Variação'] = float(0)
            ultimo_valor = df_principal[ativo].at[index, 'Valor']
            primeira_linha = False

        # Se não é primeira linha
        else:

            # Se não tem movimentação
            if df_principal[ativo].at[index, 'Quantidade'] == "":
                df_principal[ativo].at[index, 'Quantidade'] = df_principal[ativo].at[index - 1, 'Quantidade']
                df_principal[ativo].at[index, 'Ativo'] = df_principal[ativo].at[index - 1, 'Ativo']
                df_principal[ativo].at[index, 'Nome Listado'] = df_principal[ativo].at[index - 1, 'Nome Listado']
                df_principal[ativo].at[index, 'Classe'] = df_principal[ativo].at[index - 1, 'Classe']
                df_principal[ativo].at[index, 'Setor'] = df_principal[ativo].at[index - 1, 'Setor']
                df_principal[ativo].at[index, 'Moeda'] = df_principal[ativo].at[index - 1, 'Moeda']

                if df_principal[ativo].at[index, 'Preço'] != '':
                    df_principal[ativo].at[index, 'Valor'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço']

                    df_principal[ativo].at[index, 'Variação'] = df_principal[ativo].at[index, 'Valor'] - ultimo_valor
                    ultimo_valor = df_principal[ativo].at[index, 'Valor']

                else: #fim de semana
                    df_principal[ativo].at[index, 'Variação'] = float(0)
            
            # Se tem movimentação
            else:
                if df_principal[ativo].at[index, 'Quantidade'] > 0:
                    df_principal[ativo].at[index, 'Aporte'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço'] # 8 * PRECO

                    # Calcula a nova quantidade de ativos    
                    df_principal[ativo].at[index, 'Quantidade'] = df_principal[ativo].at[index, 'Quantidade'] + df_principal[ativo].at[index - 1, 'Quantidade'] # 8 + 42
                    
                    if df_principal[ativo].at[index, 'Preço'] != '':
                        df_principal[ativo].at[index, 'Valor'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço'] #50 * PRECO

                        df_principal[ativo].at[index, 'Variação'] = df_principal[ativo].at[index, 'Valor'] - ultimo_valor - df_principal[ativo].at[index, 'Aporte'] #VARIACAO DESCONSIDERANDO MOVIMENTAÇÃO
                        ultimo_valor = df_principal[ativo].at[index, 'Valor']

                    else:
                        df_principal[ativo].at[index, 'Variação'] = float(0) #FIM DE SEMANA

                else: #Quantidade < 0
                    df_principal[ativo].at[index, 'Resgate'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço']

                    # Calcula a nova quantidade de ativos    
                    df_principal[ativo].at[index, 'Quantidade'] = df_principal[ativo].at[index, 'Quantidade'] + df_principal[ativo].at[index - 1, 'Quantidade']
                    
                    if df_principal[ativo].at[index, 'Preço'] != '':
                        df_principal[ativo].at[index, 'Valor'] = df_principal[ativo].at[index, 'Quantidade'] * df_principal[ativo].at[index, 'Preço']

                        df_principal[ativo].at[index, 'Variação'] = df_principal[ativo].at[index, 'Valor'] - ultimo_valor + df_principal[ativo].at[index, 'Resgate'] #Resgate é numero negativo
                        ultimo_valor = df_principal[ativo].at[index, 'Valor']

                    else:
                        df_principal[ativo].at[index, 'Variação'] = float(0)


    
    #print(df_principal[ativo])
    df_principal[ativo].to_excel(f'ativos/{ativo}.xlsx', index=False) #gera um df por ativo, depois vamos consolidar
    print(f'{ativo} Salvo')


# Lista de DataFrames
dataframes = [df_principal[ativo] for ativo in ativos]

# Concatena todos os DataFrames da lista
df_concatenado = pd.concat(dataframes)


# Pega os dados do dataframe concatenado 
df_composicao_prov = df_concatenado

# Substitui celulas vazias por 'nan' e pega o valor anteior quando a celula está vazia
df_composicao_prov['Valor'] = df_composicao_prov['Valor'].replace('', np.nan)# Necessario para utilizar o metodo a seguir
df_composicao_prov['Valor'] = df_composicao_prov['Valor'].fillna(method='ffill')#Pega o valor de sexta para sabado e de sabado para domingo

# Apaga as linhas quando coluna Ativo está vazia
df_composicao_prov = df_composicao_prov[df_composicao_prov.Ativo != '']

# Reorganiza o dataframe pelo index
df_composicao_prov = df_composicao_prov.sort_index()
df_composicao_prov = df_composicao_prov.reset_index() #Preciso fazer isso pois sao varios DF concatenados
df_composicao_prov = df_composicao_prov.drop('index', axis=1)

# Convertea coluna Data para o formato datetime
df_composicao_prov['Data'] = pd.to_datetime(df_composicao_prov['Data'], format='%d/%m/%Y')
df_composicao_prov = df_composicao_prov.sort_values(by=['Data', 'Ativo'])
df_composicao_prov['Data'] = df_composicao_prov['Data'].dt.strftime('%d/%m/%Y')

# Calcula a soma da coluna 'Valor' para cada grupo e adiciona na nova coluna
df_composicao_prov['Soma'] = df_composicao_prov.groupby('Data')['Valor'].transform('sum')

# Calcula o valor da coluna carteira
df_composicao_prov['% CARTEIRA'] = df_composicao_prov['Valor'] / df_composicao_prov['Soma']

# Remove as colunas do DataFrame
#df_composicao_prov = df_composicao_prov.drop(['Soma', 'Aporte', 'Resgate', 'Variação'], axis=1)

# Salva o Dataframe em excel
df_composicao_prov.to_excel('resultados/Composicao_Carteira.xlsx', index=False)
print('Composição Salva')



# Apaga as linhas quando coluna Valor  está vazia
df_concatenado = df_concatenado[df_concatenado.Valor != '']
df_concatenado = df_concatenado[df_concatenado.Ativo != '']

# Substitui por zero quando as colunas Aporte e Resgate estiverem vazias
df_concatenado.loc[df_concatenado['Aporte'] == '', 'Aporte'] = float(0)
df_concatenado.loc[df_concatenado['Resgate'] == '', 'Resgate'] = float(0)


# Cria um DataFrame
df_carteira = pd.DataFrame({'Data': intervalo_datas, 'Patrimônio': '', 'Aporte': '', 'Resgate':'', 'Vari Comp': '',
                                'Patrimônio Atualizado': '', 'Novas Cotas': '', 'Cotas': '', 'Valor Cota': '',
                                'Variação': '', 'Rentabilidade Acumulada': ''})

# Edita o formato da coluna Data
df_carteira['Data'] = df_carteira['Data'].dt.strftime('%d/%m/%Y')

primeira_linha = True
for index, row in df_carteira.iterrows():

    resultado3 = df_concatenado.loc[df_concatenado['Data'] == row['Data']]

    if not resultado3.empty:
    
        if primeira_linha == True:
            df_carteira.at[index, 'Patrimônio'] = float(0)
            df_carteira.at[index, 'Aporte'] = resultado3['Aporte'].sum()
            df_carteira.at[index, 'Resgate'] = resultado3['Resgate'].sum()
            df_carteira.at[index, 'Vari Comp'] = resultado3['Variação'].sum()
            df_carteira.at[index, 'Patrimônio Atualizado'] = resultado3['Aporte'].sum()
            df_carteira.at[index, 'Novas Cotas'] = resultado3['Aporte'].sum()
            df_carteira.at[index, 'Cotas'] = resultado3['Aporte'].sum()
            df_carteira.at[index, 'Valor Cota'] = float(1)
            df_carteira.at[index, 'Variação'] = float(0)
            df_carteira.at[index, 'Rentabilidade Acumulada'] = float(0)


            primeira_linha = False

        else:
            df_carteira.at[index, 'Patrimônio'] = df_carteira.at[index - 1, 'Patrimônio Atualizado']
            df_carteira.at[index, 'Aporte'] = resultado3['Aporte'].sum()
            df_carteira.at[index, 'Resgate'] = resultado3['Resgate'].sum()
            df_carteira.at[index, 'Vari Comp'] = resultado3['Variação'].sum()
            df_carteira.at[index, 'Patrimônio Atualizado'] = df_carteira.at[index - 1, 'Patrimônio Atualizado'] + resultado3['Aporte'].sum() + resultado3['Resgate'].sum() + resultado3['Variação'].sum()
            df_carteira.at[index, 'Novas Cotas'] = (df_carteira.at[index, 'Aporte'] + df_carteira.at[index, 'Resgate']) / df_carteira.at[index - 1, 'Valor Cota']
            df_carteira.at[index, 'Cotas'] = df_carteira.at[index, 'Novas Cotas'] + df_carteira.at[index - 1, 'Cotas']
            df_carteira.at[index, 'Valor Cota'] = df_carteira.at[index, 'Patrimônio Atualizado'] / df_carteira.at[index, 'Cotas']
            df_carteira.at[index, 'Variação'] = (df_carteira.at[index, 'Valor Cota'] / df_carteira.at[index - 1, 'Valor Cota']) - 1
            df_carteira.at[index, 'Rentabilidade Acumulada'] = (df_carteira.at[index, 'Valor Cota'] / 1) - 1
            
    else:
        if primeira_linha == True:
            continue

        else:
            df_carteira.at[index, 'Patrimônio'] = df_carteira.at[index - 1, 'Patrimônio Atualizado']
            df_carteira.at[index, 'Aporte'] = float(0)
            df_carteira.at[index, 'Resgate'] = float(0)
            df_carteira.at[index, 'Vari Comp'] = float (0)
            df_carteira.at[index, 'Patrimônio Atualizado'] = df_carteira.at[index - 1, 'Patrimônio Atualizado']
            df_carteira.at[index, 'Novas Cotas'] = (df_carteira.at[index, 'Aporte'] - df_carteira.at[index, 'Resgate']) / df_carteira.at[index - 1, 'Valor Cota'] 
            df_carteira.at[index, 'Cotas'] = df_carteira.at[index, 'Novas Cotas'] + df_carteira.at[index - 1, 'Cotas']
            df_carteira.at[index, 'Valor Cota'] = df_carteira.at[index, 'Patrimônio Atualizado'] / df_carteira.at[index, 'Cotas']
            df_carteira.at[index, 'Variação'] = (df_carteira.at[index, 'Valor Cota'] / df_carteira.at[index - 1, 'Valor Cota']) - 1
            df_carteira.at[index, 'Rentabilidade Acumulada'] = (df_carteira.at[index, 'Valor Cota'] / 1) - 1
            
            
#print(df_carteira)        
df_carteira.to_excel('resultados/Rentabilidade_Carteira.xlsx', index=False)
print('Rentabilidade Salva')
