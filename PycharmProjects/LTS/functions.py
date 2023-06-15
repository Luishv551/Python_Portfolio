import os
import pandas as pd


def ler_csvs_pasta_movement(caminho_pasta_movement):
    # Lista todos os arquivos na pasta
    arquivos = os.listdir(caminho_pasta_movement)

    # Filtra apenas os arquivos CSV que correspondem ao padrão de nome (YYYYMMDD_nome)
    arquivos = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]

    # Ordena os arquivos pelo padrão de data no nome
    arquivos.sort(key=lambda x: int(x[:8]))

    # Cria um DataFrame vazio para armazenar as informações
    df = pd.DataFrame()

    # Percorre cada arquivo e adiciona as informações ao DataFrame
    for arquivo in arquivos:
        # Extrai a data do nome do arquivo
        data = arquivo[:8]

        # Carrega o arquivo CSV
        caminho_arquivo = os.path.join(caminho_pasta_movement, arquivo)
        df_arquivo = pd.read_csv(caminho_arquivo, delimiter=',')

        # Adiciona as informações ao DataFrame principal
        df = pd.concat([df, df_arquivo], ignore_index=True)

    return df


def ler_csvs_pasta_balance(caminho_pasta_balance):
    # Lista todos os arquivos na pasta
    arquivos = os.listdir(caminho_pasta_balance)

    # Filtra apenas os arquivos CSV que correspondem ao padrão de nome (YYYYMMDD_nome)
    arquivos = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]

    # Ordena os arquivos pelo padrão de data no nome
    arquivos.sort(key=lambda x: int(x[:8]))

    # Cria um DataFrame vazio para armazenar as informações
    df = pd.DataFrame()

    # Percorre cada arquivo e adiciona as informações ao DataFrame
    for arquivo in arquivos:
        # Extrai a data do nome do arquivo
        data = arquivo[:8]

        # Carrega o arquivo CSV
        caminho_arquivo = os.path.join(caminho_pasta_balance, arquivo)
        df_arquivo = pd.read_csv(caminho_arquivo, delimiter=',')

        # Adiciona as informações ao DataFrame principal
        df = pd.concat([df, df_arquivo], ignore_index=True)

    return df




