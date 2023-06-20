import pandas as pd
from datetime import datetime

def cotas_mensais_empresas(caminho_pasta):
    df = pd.DataFrame()

    # Carregar o DataFrame original
    df = pd.read_csv(caminho_pasta, delimiter=',')

    # Converter a coluna 'date' para o tipo datetime com o formato DD/MM/YYYY
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # Criar um novo DataFrame para armazenar as cotas repetidas
    df_repeated = pd.DataFrame()

    # Agrupar os dados por ativo
    grouped = df.groupby('name_1')

    # Para cada grupo de ativo
    for name_1, group in grouped:
        # Obter a data de início e fim do grupo
        start_date = group['date'].min()
        end_date = datetime.today().strftime("%d-%m-%y")

        # Gerar as datas de repetição para o grupo
        repeated_dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # Criar um DataFrame temporário para o grupo
        temp_df = pd.DataFrame(repeated_dates, columns=['date'])

        # Copiar as demais colunas do grupo original
        temp_df['name_1'] = name_1
        temp_df['name_2'] = group['name_2'].iloc[0]
        temp_df['asset_class'] = group['asset_class'].iloc[0]
        temp_df['Sector'] = group['Sector'].iloc[0]
        temp_df['currency'] = group['currency'].iloc[0]
        temp_df['shares'] = group['shares'].iloc[0]

        # Adicionar a coluna 'price' repetida para cada mês
        temp_df['price'] = group['price'].reset_index(drop=True)

        # Calcular o valor do 'amount' com base em 'shares' e 'price' para a classe de ativo 'Liquid Funds'
        if group['asset_class'].iloc[0] == 'Liquid Funds':
            temp_df['amount'] = temp_df['shares'] * temp_df['price']
            temp_df['price'].fillna(method='ffill', inplace=True)
            temp_df['amount'].fillna(method='ffill', inplace=True)
        else:
            # Merge para obter os valores corretos de 'amount' para outras classes de ativo
            temp_df = pd.merge(temp_df, group[['date', 'amount']], on='date', how='left')
            temp_df['amount'].fillna(method='ffill', inplace=True)

        # Adicionar o DataFrame temporário ao DataFrame de cotas repetidas
        df_repeated = pd.concat([df_repeated, temp_df])

    # Classificar o DataFrame de cotas repetidas pela data
    df_repeated.sort_values(['name_1', 'date'], inplace=True)

    # Redefinir os índices do DataFrame
    df_repeated.reset_index(drop=True, inplace=True)

    return df_repeated

caminho_pasta = "C:\\Users\\luish\\OneDrive\\Área de Trabalho\\Dados\\consolidado\\dados_completos_balance.csv"

df_cotas_mensais = cotas_mensais_empresas(caminho_pasta)

df_cotas_mensais['date'] = pd.to_datetime(df_cotas_mensais['date'], dayfirst=True)
df_cotas_mensais['date'] = df_cotas_mensais['date'].dt.strftime('%d/%m/%Y')

df_cotas_mensais.to_csv("C:\\Users\\luish\\OneDrive\\Área de Trabalho\\Dados\\cotas_mensais.csv")
